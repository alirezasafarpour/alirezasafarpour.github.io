from __future__ import annotations

import json
import math
import urllib.request
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.io import loadmat
from sklearn.covariance import LedoitWolf
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.metrics import (accuracy_score, balanced_accuracy_score,
                             cohen_kappa_score, confusion_matrix, f1_score)
from sklearn.model_selection import GroupShuffleSplit
from sklearn.preprocessing import StandardScaler

SEEDS = [11, 23, 37, 51, 73]
DATA_URL = (
    "https://raw.githubusercontent.com/GatorSense/MUUFLGulfport/master/"
    "MUUFLGulfportSceneLabels/muufl_gulfport_campus_1_hsi_220_label.mat"
)


def download(url: str, path: Path) -> None:
    if path.exists() and path.stat().st_size > 100_000:
        return
    print(f"Downloading {url}")
    urllib.request.urlretrieve(url, path)


def extract_dataset(path: Path):
    obj = loadmat(path, simplify_cells=True)
    hsi = obj["hsi"]
    cube = np.asarray(hsi["Data"], dtype=np.float64)
    lidar = hsi["Lidar"]
    if isinstance(lidar, dict):
        z = np.asarray(lidar.get("z"), dtype=np.float64)
    else:
        z = np.asarray(lidar, dtype=np.float64)
    labels = np.asarray(hsi["sceneLabels"]["labels"]).squeeze().astype(int)
    material_names = hsi["sceneLabels"].get("Materials_Type", None)
    if cube.shape[:2] != labels.shape:
        raise RuntimeError(f"HSI/label mismatch: {cube.shape}, {labels.shape}")
    if z.shape != labels.shape:
        z = np.squeeze(z)
        if z.shape != labels.shape:
            raise RuntimeError(f"LiDAR/label mismatch: {z.shape}, {labels.shape}")
    return cube, z, labels, material_names


def build_lidar_features(z: np.ndarray) -> np.ndarray:
    zf = z.astype(np.float64)
    zf = np.where(np.isfinite(zf), zf, np.nanmedian(zf))
    gy, gx = np.gradient(zf)
    slope = np.hypot(gx, gy)
    lap = np.gradient(gx, axis=1) + np.gradient(gy, axis=0)
    feats = np.stack([zf, gx, gy, slope, lap], axis=-1)
    return feats


def spatial_groups(shape, block=20):
    rr, cc = np.indices(shape)
    nbc = math.ceil(shape[1] / block)
    return (rr // block) * nbc + (cc // block)


def make_split(y, groups, seed):
    idx = np.arange(len(y))
    classes = np.unique(y)
    for attempt in range(100):
        gss1 = GroupShuffleSplit(n_splits=1, train_size=0.35, random_state=seed + attempt)
        train, rest = next(gss1.split(idx, y, groups))
        gss2 = GroupShuffleSplit(n_splits=1, train_size=0.30, random_state=seed + 1000 + attempt)
        val_rel, test_rel = next(gss2.split(rest, y[rest], groups[rest]))
        val, test = rest[val_rel], rest[test_rel]
        if all(np.isin(classes, np.unique(y[s])).all() for s in (train, val, test)):
            return train, val, test
    raise RuntimeError("Could not create class-complete spatial split")


def entropy_reliability(p):
    p = np.clip(p, 1e-8, 1.0)
    ent = -np.sum(p * np.log(p), axis=1) / np.log(p.shape[1])
    return np.clip(1.0 - ent, 0.05, 1.0)


def align_probs(model, p, classes):
    out = np.full((len(p), len(classes)), 1e-8)
    for j, c in enumerate(model.classes_):
        out[:, np.where(classes == c)[0][0]] = p[:, j]
    out /= out.sum(axis=1, keepdims=True)
    return out


def fit_score_stats(scores, y, classes):
    target = np.eye(len(classes))[np.searchsorted(classes, y)]
    residual = scores - target
    mean = residual.mean(axis=0)
    cov = LedoitWolf().fit(residual).covariance_ + 1e-5 * np.eye(len(classes))
    return mean, cov


def fuse_scores(ph, pl, qh, ql, muh, mul, rh, rl, mode="proposed"):
    c = ph.shape[1]
    prior_mean = np.full(c, 1.0 / c)
    prior_cov = np.eye(c) * 0.50
    ip = np.linalg.inv(prior_cov)
    ih = np.linalg.inv(rh)
    il = np.linalg.inv(rl)
    out = np.empty_like(ph)
    for i in range(len(ph)):
        if mode == "proposed":
            j = ip + qh[i] * ih + ql[i] * il
            rhs = ip @ prior_mean + qh[i] * ih @ (ph[i] - muh) + ql[i] * il @ (pl[i] - mul)
            out[i] = np.linalg.solve(j, rhs)
        elif mode == "colored_only":
            j = ip + ih + il
            rhs = ip @ prior_mean + ih @ (ph[i] - muh) + il @ (pl[i] - mul)
            out[i] = np.linalg.solve(j, rhs)
        elif mode == "reliability_diagonal":
            out[i] = (qh[i] * ph[i] + ql[i] * pl[i]) / (qh[i] + ql[i])
        elif mode == "classical":
            out[i] = 0.5 * (ph[i] + pl[i])
        else:
            raise ValueError(mode)
    return out


def metrics(y, pred):
    return {
        "OA": accuracy_score(y, pred),
        "AA": balanced_accuracy_score(y, pred),
        "Kappa": cohen_kappa_score(y, pred),
        "MacroF1": f1_score(y, pred, average="macro"),
    }


def run_seed(cube, lidar_feats, labels, seed, outdir):
    mask = labels > 0
    rows, cols = np.where(mask)
    y = labels[mask]
    classes = np.unique(y)
    xh = cube[mask]
    xl = lidar_feats[mask]
    groups = spatial_groups(labels.shape)[mask]
    train, val, test = make_split(y, groups, seed)

    # Remove nonfinite values and standardize from training only.
    xh = np.nan_to_num(xh, nan=np.nanmedian(xh[train], axis=0), posinf=0, neginf=0)
    xl = np.nan_to_num(xl, nan=np.nanmedian(xl[train], axis=0), posinf=0, neginf=0)
    sh, sl = StandardScaler(), StandardScaler()
    xh_s = sh.fit(xh[train]).transform(xh)
    xl_s = sl.fit(xl[train]).transform(xl)

    # Shrinkage LDA is stable in small spatially separated training sets.
    hsi = LinearDiscriminantAnalysis(solver="lsqr", shrinkage="auto").fit(xh_s[train], y[train])
    lid = LinearDiscriminantAnalysis(solver="lsqr", shrinkage="auto").fit(xl_s[train], y[train])
    early = LinearDiscriminantAnalysis(solver="lsqr", shrinkage="auto").fit(
        np.hstack([xh_s[train], xl_s[train]]), y[train]
    )

    ph_val = align_probs(hsi, hsi.predict_proba(xh_s[val]), classes)
    pl_val = align_probs(lid, lid.predict_proba(xl_s[val]), classes)
    muh, rh = fit_score_stats(ph_val, y[val], classes)
    mul, rl = fit_score_stats(pl_val, y[val], classes)

    ph = align_probs(hsi, hsi.predict_proba(xh_s[test]), classes)
    pl = align_probs(lid, lid.predict_proba(xl_s[test]), classes)
    qh, ql = entropy_reliability(ph), entropy_reliability(pl)

    predictions = {
        "HSI-only": hsi.predict(xh_s[test]),
        "LiDAR-only": lid.predict(xl_s[test]),
        "Early-fusion LDA": early.predict(np.hstack([xh_s[test], xl_s[test]])),
    }
    for mode, name in [
        ("classical", "Classical score fusion"),
        ("reliability_diagonal", "Reliability-diagonal"),
        ("colored_only", "Colored-only"),
        ("proposed", "Proposed reliability-precision"),
    ]:
        fused = fuse_scores(ph, pl, qh, ql, muh, mul, rh, rl, mode)
        predictions[name] = classes[np.argmax(fused, axis=1)]

    rows_out = []
    for method, pred in predictions.items():
        row = {"seed": seed, "method": method, **metrics(y[test], pred)}
        rows_out.append(row)
        cm = confusion_matrix(y[test], pred, labels=classes)
        pd.DataFrame(cm, index=classes, columns=classes).to_csv(
            outdir / f"confusion_seed{seed}_{method.replace(' ', '_').replace('/', '_')}.csv"
        )

    # Native missing-modality stress test: remove HSI or LiDAR score information.
    proposed_full = classes[np.argmax(fuse_scores(ph, pl, qh, ql, muh, mul, rh, rl, "proposed"), axis=1)]
    missing_h = classes[np.argmax(fuse_scores(ph, pl, np.full_like(qh, 0.05), ql, muh, mul, rh, rl, "proposed"), axis=1)]
    missing_l = classes[np.argmax(fuse_scores(ph, pl, qh, np.full_like(ql, 0.05), muh, mul, rh, rl, "proposed"), axis=1)]
    stress = []
    for scenario, pred in [("Both modalities", proposed_full), ("HSI low reliability", missing_h), ("LiDAR low reliability", missing_l)]:
        stress.append({"seed": seed, "scenario": scenario, **metrics(y[test], pred)})

    # Save split map for first seed.
    if seed == SEEDS[0]:
        split_map = np.full(labels.shape, -1)
        split_map[rows[train], cols[train]] = 1
        split_map[rows[val], cols[val]] = 2
        split_map[rows[test], cols[test]] = 3
        np.save(outdir / "spatial_split_map.npy", split_map)

    return rows_out, stress, classes


def main():
    outdir = Path("muufl_results")
    outdir.mkdir(exist_ok=True)
    mat_path = outdir / "muufl_gulfport_campus_1_hsi_220_label.mat"
    download(DATA_URL, mat_path)
    cube, lidar, labels, material_names = extract_dataset(mat_path)
    lidar_feats = build_lidar_features(lidar)

    all_rows, all_stress = [], []
    classes = None
    for seed in SEEDS:
        rows, stress, classes = run_seed(cube, lidar_feats, labels, seed, outdir)
        all_rows.extend(rows)
        all_stress.extend(stress)

    df = pd.DataFrame(all_rows)
    stress_df = pd.DataFrame(all_stress)
    df.to_csv(outdir / "muufl_metrics_all_seeds.csv", index=False)
    stress_df.to_csv(outdir / "muufl_missing_modality.csv", index=False)

    summary = df.groupby("method")[["OA", "AA", "Kappa", "MacroF1"]].agg(["mean", "std"])
    summary.to_csv(outdir / "muufl_metrics_summary.csv")

    # Publication-ready OA/Macro-F1 chart.
    plot_df = df.groupby("method")[["OA", "MacroF1"]].agg(["mean", "std"])
    methods = plot_df.index.tolist()
    x = np.arange(len(methods))
    fig, ax = plt.subplots(figsize=(10, 4.6))
    width = 0.36
    ax.bar(x - width/2, plot_df[("OA", "mean")], width,
           yerr=plot_df[("OA", "std")], capsize=3, label="OA")
    ax.bar(x + width/2, plot_df[("MacroF1", "mean")], width,
           yerr=plot_df[("MacroF1", "std")], capsize=3, label="Macro-F1")
    ax.set_ylim(0, 1)
    ax.set_ylabel("Score")
    ax.set_xticks(x)
    ax.set_xticklabels(methods, rotation=25, ha="right")
    ax.legend(frameon=False)
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(outdir / "muufl_native_results.png", dpi=300)
    plt.close(fig)

    # RGB, LiDAR, labels, split overview.
    rgb = cube[:, :, [45, 25, 10]]
    lo, hi = np.nanpercentile(rgb, [2, 98])
    rgb = np.clip((rgb - lo) / max(hi - lo, 1e-9), 0, 1)
    split_map = np.load(outdir / "spatial_split_map.npy")
    fig, axes = plt.subplots(1, 4, figsize=(12, 3.2))
    axes[0].imshow(rgb); axes[0].set_title("MUUFL HSI composite")
    axes[1].imshow(lidar); axes[1].set_title("Co-registered LiDAR")
    axes[2].imshow(labels); axes[2].set_title("11-class ground truth")
    axes[3].imshow(split_map); axes[3].set_title("Spatial train/val/test")
    for ax in axes: ax.axis("off")
    fig.tight_layout()
    fig.savefig(outdir / "muufl_dataset_overview.png", dpi=300)
    plt.close(fig)

    best = summary[("OA", "mean")].idxmax()
    report = {
        "dataset_shape": list(cube.shape),
        "number_of_labeled_pixels": int(np.sum(labels > 0)),
        "classes": [int(x) for x in classes],
        "seeds": SEEDS,
        "best_method_by_OA": best,
        "summary": {
            method: {
                metric: {
                    "mean": float(summary.loc[method, (metric, "mean")]),
                    "std": float(summary.loc[method, (metric, "std")]),
                } for metric in ["OA", "AA", "Kappa", "MacroF1"]
            } for method in summary.index
        },
    }
    (outdir / "summary.json").write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
