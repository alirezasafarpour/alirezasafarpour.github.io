import os, json, math, zipfile, warnings
warnings.filterwarnings('ignore')
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.model_selection import GroupKFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import average_precision_score, roc_auc_score, f1_score, precision_score, recall_score, balanced_accuracy_score, brier_score_loss
from sklearn.inspection import permutation_importance
from xgboost import XGBClassifier

OUT=Path('fire_experiment/results'); OUT.mkdir(parents=True, exist_ok=True)
BASE='https://raw.githubusercontent.com/Obuda-University-Space-Lab/NASA_SpaceApps_challenge_2025/main/data/'
files=['greece_fire_dates.csv','greece_fire_places.csv','greece_fire_weather.csv']
for f in files:
    p=Path('fire_experiment')/f
    if not p.exists():
        import urllib.request; urllib.request.urlretrieve(BASE+f,p)

fires=pd.read_csv('fire_experiment/greece_fire_dates.csv', low_memory=False)
places=pd.read_csv('fire_experiment/greece_fire_places.csv')
weather=pd.read_csv('fire_experiment/greece_fire_weather.csv', low_memory=False)

fires['acq_date']=pd.to_datetime(fires['acq_date'], errors='coerce')
weather['time']=pd.to_datetime(weather['time'], errors='coerce')
fires=fires.dropna(subset=['acq_date','latitude','longitude'])
weather=weather.dropna(subset=['time','location_id'])
weather['location_id']=pd.to_numeric(weather['location_id'],errors='coerce')
places['location_id']=pd.to_numeric(places['location_id'],errors='coerce')
weather=weather.dropna(subset=['location_id']).copy(); places=places.dropna(subset=['location_id']).copy()
weather['location_id']=weather['location_id'].astype(int); places['location_id']=places['location_id'].astype(int)
fires=fires[pd.to_numeric(fires['confidence'],errors='coerce').fillna(0)>=80].copy()

latp=np.radians(places['latitude'].to_numpy()); lonp=np.radians(places['longitude'].to_numpy())
flats=np.radians(fires['latitude'].to_numpy()); flons=np.radians(fires['longitude'].to_numpy())
nearest=[]; distkm=[]
for a,b in zip(flats,flons):
    x=(lonp-b)*np.cos((latp+a)/2); y=latp-a
    d=np.sqrt(x*x+y*y)*6371.0
    j=int(np.argmin(d)); nearest.append(int(places.iloc[j]['location_id'])); distkm.append(float(d[j]))
fires['location_id']=nearest; fires['nearest_km']=distkm
fires=fires[fires['nearest_km']<=35].copy()
fire_days=fires[['location_id','acq_date']].drop_duplicates().copy(); fire_days['fire_next_day']=1

df=weather.merge(places[['location_id','latitude','longitude','elevation']],on='location_id',how='left')
df['target_date']=df['time']+pd.Timedelta(days=1)
df=df.merge(fire_days,left_on=['location_id','target_date'],right_on=['location_id','acq_date'],how='left')
df['fire_next_day']=df['fire_next_day'].fillna(0).astype(int)
df['year']=df['time'].dt.year; df['month']=df['time'].dt.month; df['doy']=df['time'].dt.dayofyear
df=df[df['month'].between(5,10) & df['year'].between(2012,2021)].copy()
df['sin_doy']=np.sin(2*np.pi*df['doy']/365.25); df['cos_doy']=np.cos(2*np.pi*df['doy']/365.25)

exclude={'location_id','time','target_date','acq_date','fire_next_day','year','month','doy','latitude','longitude','sunrise (iso8601)','sunset (iso8601)','timezone','timezone_abbreviation'}
features=[]
for c in df.columns:
    if c in exclude: continue
    if pd.api.types.is_numeric_dtype(df[c]): features.append(c)
features=[c for c in features if c not in {'utc_offset_seconds'}]
for c in features: df[c]=pd.to_numeric(df[c],errors='coerce')
df=df.dropna(subset=features+['latitude','longitude'])

train=df[df.year<=2020].copy(); test=df[df.year==2021].copy()
X=train[features]; y=train.fire_next_day; Xt=test[features]; yt=test.fire_next_day
train['spatial_group']=(np.floor(train.latitude).astype(int)*100+np.floor(train.longitude).astype(int)).astype(str)
n_groups=int(train['spatial_group'].nunique())
if n_groups < 3:
    raise RuntimeError(f'Insufficient independent spatial groups for validation: {n_groups}')
n_splits=min(5,n_groups)

def metrics(y_true,p):
    pred=(p>=0.5).astype(int)
    return {'pr_auc':float(average_precision_score(y_true,p)),'roc_auc':float(roc_auc_score(y_true,p)),'f1':float(f1_score(y_true,pred,zero_division=0)),'precision':float(precision_score(y_true,pred,zero_division=0)),'recall':float(recall_score(y_true,pred,zero_division=0)),'balanced_accuracy':float(balanced_accuracy_score(y_true,pred)),'brier':float(brier_score_loss(y_true,p))}

pos=max(1,int(y.sum())); neg=max(1,int((1-y).sum())); spw=neg/pos
models={
 'Logistic Regression':make_pipeline(StandardScaler(),LogisticRegression(max_iter=2000,class_weight='balanced',solver='liblinear')),
 'Random Forest':RandomForestClassifier(n_estimators=180,min_samples_leaf=3,class_weight='balanced_subsample',n_jobs=-1,random_state=42),
 'XGBoost':XGBClassifier(n_estimators=300,max_depth=5,learning_rate=.05,subsample=.85,colsample_bytree=.85,scale_pos_weight=spw,eval_metric='logloss',n_jobs=4,random_state=42)
}

gkf=GroupKFold(n_splits=n_splits); rows=[]
for name,model in models.items():
    for fold,(tr,va) in enumerate(gkf.split(X,y,groups=train.spatial_group),1):
        model.fit(X.iloc[tr],y.iloc[tr]); p=model.predict_proba(X.iloc[va])[:,1]
        r={'model':name,'fold':fold}; r.update(metrics(y.iloc[va],p)); rows.append(r)
cv=pd.DataFrame(rows); cv.to_csv(OUT/'spatial_cv_metrics.csv',index=False)
summary=cv.groupby('model').agg(['mean','std']); summary.to_csv(OUT/'spatial_cv_summary.csv')
best=cv.groupby('model')['pr_auc'].mean().idxmax()

final=models[best]; final.fit(X,y); ptest=final.predict_proba(Xt)[:,1]
test_metrics=metrics(yt,ptest); test_metrics.update({'model':best,'n_test':int(len(test)),'positives_test':int(yt.sum()),'prevalence_test':float(yt.mean())})
pd.DataFrame([test_metrics]).to_csv(OUT/'temporal_holdout_2021.csv',index=False)

att=test[(test.latitude.between(37.6,38.5)) & (test.longitude.between(22.7,24.3))].copy()
att_out={'n':int(len(att)),'positives':int(att.fire_next_day.sum()),'prevalence':float(att.fire_next_day.mean()) if len(att) else None}
if len(att)>0 and att.fire_next_day.nunique()>1:
    pa=final.predict_proba(att[features])[:,1]; att_out.update(metrics(att.fire_next_day,pa))
pd.DataFrame([att_out]).to_csv(OUT/'attica_window_2021.csv',index=False)

sample=test.sample(min(12000,len(test)),random_state=42)
try:
    pi=permutation_importance(final,sample[features],sample.fire_next_day,n_repeats=5,scoring='average_precision',random_state=42,n_jobs=-1)
    pd.DataFrame({'feature':features,'importance_mean':pi.importances_mean,'importance_std':pi.importances_std}).sort_values('importance_mean',ascending=False).to_csv(OUT/'permutation_importance.csv',index=False)
except Exception as e:
    (OUT/'importance_error.txt').write_text(str(e))

cal=pd.DataFrame({'y':yt.to_numpy(),'p':ptest}); cal['bin']=pd.qcut(cal.p.rank(method='first'),10,labels=False,duplicates='drop')
cal.groupby('bin').agg(mean_pred=('p','mean'),observed=('y','mean'),n=('y','size')).reset_index().to_csv(OUT/'calibration_2021.csv',index=False)

prov={'source_fire':'NASA FIRMS active-fire CSV via public NASA Space Apps repository','source_weather':'Open-Meteo daily historical weather via public NASA Space Apps repository','study_period_train':'2012-2020 May-Oct','locked_test':'2021 May-Oct','forecast_horizon':'1 day','fire_confidence_threshold':80,'max_fire_to_weather_location_km':35,'n_train':int(len(train)),'positive_train':int(y.sum()),'prevalence_train':float(y.mean()),'features':features,'spatial_group_definition':'1-degree latitude-longitude blocks','n_spatial_groups':n_groups,'spatial_cv_folds':n_splits,'selected_model_by_spatial_cv_pr_auc':best}
(OUT/'provenance.json').write_text(json.dumps(prov,indent=2))
registry={'cv':cv.groupby('model')[['pr_auc','roc_auc','f1','precision','recall','balanced_accuracy','brier']].mean().round(6).to_dict(orient='index'),'test_2021':test_metrics,'attica_window_2021':att_out,'provenance':prov}
(OUT/'results_registry.json').write_text(json.dumps(registry,indent=2))
with zipfile.ZipFile('fire_experiment/fire_geoai_results.zip','w',zipfile.ZIP_DEFLATED) as z:
    for p in OUT.rglob('*'):
        if p.is_file(): z.write(p,arcname=p.name)
print(json.dumps(registry,indent=2))
