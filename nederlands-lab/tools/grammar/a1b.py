"""A1, deel 2 — bezit, modale werkwoorden, scheidbaar, tijd en beleefdheid."""

from _kit import (concept, lesson, module, ex, wrong, pattern, discover, rule,
                  mc, dehet, nietgeen, pickorder, pick2, dialogue, scenario,
                  blank, conjugate, transform, fa2nl, fix, type_all,
                  order, question, subclause)

# ---------------------------------------------------------------- concepts

C_POSS = concept(
    "poss-pronoun", "Bezittelijke voornaamwoorden", "ضمیر ملکی", "A1",
    keywords=["mijn", "jouw", "zijn", "haar", "ons", "onze", "hun", "bezit", "ملکی"],
    summary_fa="mijn، jouw، zijn، haar، ons/onze، jullie، hun — «مالِ کی».")

C_DEM = concept(
    "demonstrative", "Deze, dit, die, dat", "اشاره: این و آن", "A1",
    keywords=["deze", "dit", "die", "dat", "aanwijzend", "اشاره"],
    summary_fa="نزدیک: deze (de) / dit (het). دور: die (de) / dat (het).")

C_OBJ = concept(
    "pron-object", "Objectvormen", "ضمیر مفعولی", "A1",
    keywords=["mij", "me", "jou", "hem", "haar", "ons", "hen", "object", "مفعول"],
    summary_fa="mij، jou، hem، haar، ons، jullie، hen — کسی که کار روی او انجام می‌شود.")

C_MODAL = concept(
    "modal-verbs", "Modale werkwoorden", "افعال کمکی وجهی", "A1",
    keywords=["kunnen", "willen", "moeten", "mogen", "modaal", "kan", "wil", "moet", "mag"],
    summary_fa="kunnen (توانستن)، willen (خواستن)، moeten (باید)، mogen (اجازه داشتن).")

C_INF_END = concept(
    "verb-second-end", "Tweede werkwoord achteraan", "فعل دوم در انتهای جمله", "A1",
    keywords=["infinitief achteraan", "tweede werkwoord", "werkwoord einde", "مصدر آخر"],
    summary_fa="فعل صرف‌شده جای دوم، فعل دومِ مصدری آخرِ جمله.")

C_SEP = concept(
    "verb-separable", "Scheidbare werkwoorden", "افعال جداشدنی", "A1",
    keywords=["scheidbaar", "opstaan", "meenemen", "aankomen", "opbellen", "جداشدنی"],
    summary_fa="پیشوند از فعل جدا می‌شود و می‌رود آخر جمله: opstaan → ik sta op.")

C_TIME = concept(
    "time-expressions", "Tijd zeggen", "بیان زمان", "A1",
    keywords=["om acht uur", "'s ochtends", "op maandag", "in juni", "tijd", "ساعت"],
    summary_fa="om + ساعت، op + روز، in + ماه، 's ochtends/'s avonds برای بخش‌های روز.")

C_PREP = concept(
    "prepositions-place", "Voorzetsels van plaats", "حروف اضافه‌ی مکان", "A1",
    keywords=["in", "op", "aan", "naar", "bij", "voorzetsel", "حرف اضافه"],
    summary_fa="naar = حرکت به سمت، in/op/bij = جای ثابت، aan = کنارِ چیزی.")

C_IMP = concept(
    "imperative", "Gebiedende wijs", "وجه امری", "A1",
    keywords=["imperatief", "gebiedende wijs", "kom", "ga", "kijk", "امری"],
    summary_fa="فقط ریشه‌ی فعل: Kom! Kijk! برای مؤدبانه‌تر شدن even یا eens اضافه کن.")

# ----------------------------------------------------------------- lessons

lesson(
    "a1-l11", "a1-bezit", "A1",
    "Mijn, jouw, zijn, haar", "ضمیرهای ملکی",
    [C_POSS],
    discover(
        ["mijn boek", "jouw fiets", "zijn auto", "haar tas", "ons huis", "onze buren"],
        "به دو مورد آخر نگاه کن. چرا یکی ons است و دیگری onze؟",
        "فقط ons دو شکل دارد: با کلمات het می‌شود ons، با بقیه (de و همه‌ی جمع‌ها) onze."),
    rule("mijn · jouw/je · zijn · haar · ons/onze · jullie · hun",
         "همه ثابت‌اند؛ فقط ons استثناست: ons huis (het) ولی onze auto (de) و onze kinderen (جمع).",
         "my / your / his / her / our / their"),
    pattern([("ons", "poss"), ("huis", "het-noun"), ("|", "sep"),
             ("onze", "poss"), ("auto", "de-noun")],
            "زبان محاوره: jouw معمولاً je می‌شود، مگر وقتی تأکید باشد."),
    [
        ex("Dit is mijn collega.", "این همکار من است."),
        ex("Waar is je telefoon?", "گوشی‌ات کجاست؟", "je = jouw بدون تأکید"),
        ex("Zijn vrouw werkt in het ziekenhuis.", "همسرش در بیمارستان کار می‌کند."),
        ex("Haar dochter zit op school.", "دخترش مدرسه می‌رود."),
        ex("Ons huis is klein, maar onze tuin is groot.", "خانه‌مان کوچک است، ولی باغمان بزرگ است."),
        ex("Hun kinderen spelen buiten.", "بچه‌هایشان بیرون بازی می‌کنند."),
    ],
    [
        wrong("onze huis", "ons huis",
              "huis کلمه‌ی het است، پس ons می‌گیرد."),
        wrong("Dit is de mijn boek.", "Dit is mijn boek.",
              "ضمیر ملکی خودش جای حرف تعریف را می‌گیرد؛ de/het بعدش نمی‌آید."),
    ],
    "در معرفی خانواده، نشان دادن وسایل و صحبت کاری («mijn manager»، «onze afdeling»). هر روز لازمش داری.",
    [
        mc("Dit is ___ huis.", ["ons", "onze", "onzes"], "ons",
           "huis کلمه‌ی het است → ons.", concept=C_POSS),
        mc("___ kinderen gaan naar school.", ["Onze", "Ons", "Onzen"], "Onze",
           "جمع همیشه onze می‌گیرد.", concept=C_POSS),
        mc("Waar is ___ jas? (van jou)", ["je", "jij", "jouw's"], "je",
           "jouw در گفتار روزمره je می‌شود.", concept=C_POSS),
        blank("Zij komt met ___ man. (van haar)", "haar",
              "برای یک زن haar.", concept=C_POSS),
        blank("Hij belt ___ moeder. (van hem)", "zijn",
              "برای یک مرد zijn.", concept=C_POSS),
        fix("Dit is onze appartement.", "Dit is ons appartement.",
            "appartement کلمه‌ی het است → ons.", concept=C_POSS),
        fix("De mijn auto staat daar.", "Mijn auto staat daar.",
            "بعد از ضمیر ملکی حرف تعریف نمی‌آید.", concept=C_POSS),
        fa2nl("«بچه‌هایشان اینجا زندگی می‌کنند.»", "Hun kinderen wonen hier.",
              "hun برای «آن‌ها».", concept=C_POSS),
        pick2("___ fiets staat buiten. (van ons)", ["Onze", "Ons"], "Onze",
              "fiets کلمه‌ی de است → onze.", concept=C_POSS),
    ])

lesson(
    "a1-l12", "a1-bezit", "A1",
    "Deze, dit, die, dat", "این و آن",
    [C_DEM],
    discover(
        ["deze stoel — dit boek", "die stoel — dat boek"],
        "چرا گاهی deze و گاهی dit؟ به حرف تعریف کلمه‌ها فکر کن.",
        "deze/die برای کلمات de هستند و dit/dat برای کلمات het. نزدیک: deze/dit. دور: die/dat."),
    rule("de-woord → deze (dichtbij) / die (ver) · het-woord → dit / dat",
         "چهار کلمه که همه با de/het گره خورده‌اند. جمع همیشه deze/die.",
         "this / that"),
    pattern([("dichtbij", "label"), ("deze stoel · dit boek", "near"), ("|", "sep"),
             ("ver", "label"), ("die stoel · dat boek", "far")],
            "برای همین de/het انقدر مهم است: نیمی از دستور زبان به آن وصل است."),
    [
        ex("Deze stoel is vrij.", "این صندلی خالی است."),
        ex("Dit boek is heel goed.", "این کتاب خیلی خوب است."),
        ex("Die man daar is mijn buurman.", "آن مرد آنجا همسایه‌ام است."),
        ex("Dat is een goed idee.", "فکر خوبی است."),
        ex("Deze schoenen zijn te klein.", "این کفش‌ها خیلی کوچک‌اند.", "جمع → deze"),
    ],
    [
        wrong("dit stoel", "deze stoel",
              "stoel کلمه‌ی de است → deze."),
        wrong("deze boek", "dit boek",
              "boek کلمه‌ی het است → dit."),
    ],
    "در مغازه، در رستوران، وقتی چیزی را نشان می‌دهی. «Dat is…» هم برای اظهار نظر خیلی پرکاربرد است: Dat is mooi. Dat klopt.",
    [
        mc("___ boek is interessant.", ["Dit", "Deze", "Die"], "Dit",
           "boek کلمه‌ی het است → dit.", concept=C_DEM),
        mc("___ tafel is te klein.", ["Deze", "Dit", "Dat"], "Deze",
           "tafel کلمه‌ی de است → deze.", concept=C_DEM),
        mc("___ kinderen zijn van mijn zus.", ["Deze", "Dit", "Dat"], "Deze",
           "جمع همیشه deze/die.", concept=C_DEM),
        mc("Zie je ___ huis daar?", ["dat", "die", "deze"], "dat",
           "huis کلمه‌ی het است و دور است → dat.", concept=C_DEM),
        blank("___ is een goed idee!", "Dat", 
              "برای اظهار نظر کلی «Dat is…» رایج‌ترین شکل است.", alt=["Dit"], concept=C_DEM),
        fix("Deze huis is groot.", "Dit huis is groot.",
            "huis کلمه‌ی het است.", concept=C_DEM),
        fa2nl("«این کتاب مالِ من است.»", "Dit boek is van mij.",
              "boek با het می‌آید → dit. مالکیت با «van mij».", concept=C_DEM),
        scenario("Je wijst in de winkel naar een jas die vlakbij hangt.",
                 "Wat zeg je?", ["Deze jas is mooi.", "Dit jas is mooi.", "Dat jas is mooi."],
                 "Deze jas is mooi.",
                 "jas کلمه‌ی de است و نزدیک است → deze.", concept=C_DEM),
    ])

lesson(
    "a1-l13", "a1-bezit", "A1",
    "Mij, jou, hem, haar", "ضمیر مفعولی",
    [C_OBJ],
    discover(
        ["Ik zie hem.", "Hij ziet mij.", "Wij helpen jullie.", "Zij belt ons."],
        "شکل ضمیرها وقتی فاعل نیستند چه تغییری می‌کند؟",
        "ik → mij/me، hij → hem، wij → ons، zij (جمع) → hen/ze. یعنی هر ضمیر دو شکل دارد."),
    rule("mij/me · jou/je · hem · haar · ons · jullie · hen/ze",
         "وقتی ضمیر مفعول جمله است یا بعد از حرف اضافه می‌آید، شکل مفعولی می‌گیرد.",
         "me / you / him / her / us / them"),
    pattern([("Ik", "subject"), ("bel", "verb"), ("hem", "object"), ("|", "sep"),
             ("Hij", "subject"), ("belt", "verb"), ("mij", "object")],
            "همان دو نفر، جای عوض‌شده — شکل ضمیر هم عوض می‌شود."),
    [
        ex("Ik bel je vanavond.", "امشب بهت زنگ می‌زنم."),
        ex("Kun je mij helpen?", "می‌توانی کمکم کنی؟"),
        ex("Wij kennen hem goed.", "ما او را خوب می‌شناسیم."),
        ex("Dit is voor haar.", "این برای اوست.", "بعد از حرف اضافه هم شکل مفعولی"),
        ex("Ik heb hen gisteren gezien.", "دیروز آن‌ها را دیدم."),
    ],
    [
        wrong("Kun je ik helpen?", "Kun je mij helpen?",
              "ik فقط فاعل است؛ برای مفعول باید mij/me بگویی."),
        wrong("Dit is voor zij.", "Dit is voor haar.",
              "بعد از حرف اضافه همیشه شکل مفعولی می‌آید."),
    ],
    "در هر جمله‌ای که کسی کاری برای کسی می‌کند: کمک خواستن، زنگ زدن، قرار گذاشتن. «Kun je mij helpen?» را در هلند خیلی لازم داری.",
    [
        mc("Kun je ___ helpen?", ["mij", "ik", "mijn"], "mij",
           "مفعول جمله است → mij.", concept=C_OBJ),
        mc("Ik ken ___ niet.", ["hem", "hij", "zijn"], "hem",
           "hij در جایگاه مفعول می‌شود hem.", concept=C_OBJ),
        mc("Dit cadeau is voor ___.", ["haar", "zij", "ze"], "haar",
           "بعد از voor شکل مفعولی می‌آید.", concept=C_OBJ),
        blank("Zij belt ___ elke week. (wij)", "ons",
              "wij در جایگاه مفعول می‌شود ons.", concept=C_OBJ),
        transform("Ik zie hij. → (درست کن)", "Ik zie hem.",
                  "بعد از فعل، شکل مفعولی لازم است.", concept=C_OBJ),
        fix("Hij helpt wij vaak.", "Hij helpt ons vaak.",
            "wij → ons در جایگاه مفعول.", concept=C_OBJ),
        fa2nl("«می‌توانی کمکم کنی؟»", "Kun je mij helpen?", 
              "mij/me مفعول است و فعل دوم آخر می‌آید.", alt=["Kun je me helpen?", "Kunt u mij helpen?"], concept=C_OBJ),
        order("Ik bel hem morgen.",
              why="فاعل، فعل، مفعول، بعد زمان.", concept=C_OBJ),
    ])

lesson(
    "a1-l14", "a1-modaal", "A1",
    "Kunnen, willen, moeten, mogen", "می‌توانم، می‌خواهم، باید، اجازه دارم",
    [C_MODAL, C_INF_END],
    discover(
        ["Ik kan zwemmen.", "Ik wil koffie drinken.", "Ik moet werken.", "Mag ik iets vragen?"],
        "در هر جمله دو فعل هست. فعل دوم کجا ایستاده؟",
        "همیشه آخرِ جمله و همیشه به شکل مصدر. فعل اول (modaal) صرف می‌شود."),
    rule("kan / wil / moet / mag + … + infinitief",
         "فعل وجهی صرف می‌شود و جای دوم می‌ایستد؛ فعل اصلی مصدر می‌ماند و می‌رود آخر.",
         "can / want / must / may + verb at the end"),
    pattern([("Ik", "subject"), ("moet", "modal"), ("morgen", "time"),
             ("naar de dokter", "place"), ("gaan", "infinitive")],
            "ik kan/wil/moet/mag — سوم‌شخص مفرد هم t نمی‌گیرد: hij kan، hij moet."),
    [
        ex("Ik kan een beetje Nederlands spreken.", "کمی هلندی می‌توانم حرف بزنم."),
        ex("Wil je iets drinken?", "چیزی می‌خواهی بنوشی؟"),
        ex("Ik moet morgen vroeg opstaan.", "فردا باید زود بیدار شوم."),
        ex("Mag ik hier zitten?", "اجازه هست اینجا بنشینم؟"),
        ex("Hij kan niet komen.", "او نمی‌تواند بیاید."),
        ex("We moeten dit vandaag afmaken.", "باید امروز این را تمام کنیم."),
    ],
    [
        wrong("Ik kan spreek Nederlands.", "Ik kan Nederlands spreken.",
              "فعل دوم باید مصدر باشد و آخر جمله برود."),
        wrong("Hij kant komen.", "Hij kan komen.",
              "فعل‌های وجهی در سوم‌شخص مفرد t نمی‌گیرند: hij kan، hij wil، hij moet، hij mag."),
    ],
    "این چهار فعل ستون فقرات مکالمه‌ی روزمره‌اند: درخواست، اجازه، اجبار و توانایی. در محل کار و مصاحبه مدام لازم می‌شوند.",
    [
        mc("Ik ___ morgen niet komen.", ["kan", "kant", "kunnen"], "kan",
           "با ik شکل kan.", concept=C_MODAL),
        mc("Hij ___ vandaag overwerken.", ["moet", "moett", "moeten"], "moet",
           "سوم‌شخص مفرد در فعل وجهی t نمی‌گیرد.", concept=C_MODAL),
        pickorder("کدام درست است؟",
                  ["Ik wil een kopje koffie drinken.", "Ik wil drinken een kopje koffie.",
                   "Ik wil drink een kopje koffie."],
                  "Ik wil een kopje koffie drinken.",
                  "مصدر آخر جمله می‌رود.", concept=C_INF_END),
        order("Ik moet morgen vroeg opstaan.",
              why="فعل وجهی جای دوم، مصدر آخر.", concept=C_INF_END),
        order("We kunnen vanavond samen eten.",
              why="kunnen صرف‌شده جای دوم، eten مصدر در انتها.", concept=C_INF_END),
        fix("Ik wil ga naar huis.", "Ik wil naar huis gaan.",
            "بعد از فعل وجهی، فعل دوم مصدر است و آخر می‌آید.", concept=C_INF_END),
        fa2nl("«باید فردا زود بیدار شوم.»", "Ik moet morgen vroeg opstaan.",
              "moet جای دوم، opstaan آخر.", concept=C_INF_END),
        dialogue("— ___ ik je iets vragen?", "— Ja, natuurlijk.",
                 ["Mag", "Moet", "Wil"], "Mag",
                 "برای اجازه گرفتن mogen: «Mag ik…?» مؤدبانه‌ترین شکل است.", concept=C_MODAL),
        scenario("Je hebt morgen een afspraak bij de dokter en moet dat op je werk zeggen.",
                 "Wat zeg je?",
                 ["Ik moet morgen naar de dokter.", "Ik moet morgen naar de dokter gaan niet.",
                  "Ik moet gaan morgen naar de dokter."],
                 "Ik moet morgen naar de dokter.",
                 "با naar + مکان، فعل gaan اغلب حذف می‌شود — کاملاً طبیعی است.",
                 concept=C_MODAL),
    ])

lesson(
    "a1-l15", "a1-modaal", "A1",
    "Twee werkwoorden in één zin", "دو فعل در یک جمله",
    [C_INF_END],
    discover(
        ["Ik ga vanavond koken.", "Ik probeer Nederlands te spreken.",
         "Hij komt morgen helpen."],
        "در هر سه جمله فعل دوم کجاست؟",
        "آخر جمله. این قانون فقط مالِ فعل‌های وجهی نیست — تقریباً همیشه صادق است."),
    rule("vervoegd werkwoord op plaats 2 · infinitief helemaal achteraan",
         "هر چیزی که بین این دو بیاید (زمان، مکان، مفعول) وسط قرار می‌گیرد.",
         "conjugated verb second, infinitive last"),
    pattern([("Ik", "subject"), ("ga", "verb"), ("vanavond", "time"),
             ("bij mijn zus", "place"), ("eten", "infinitive")],
            "به این ساختار می‌گویند «قاب فعلی» (werkwoordelijke tang)."),
    [
        ex("Ik ga vanavond koken.", "امشب آشپزی می‌کنم."),
        ex("Zij blijft thuis werken.", "او خانه می‌ماند و کار می‌کند."),
        ex("We komen je zondag ophalen.", "یکشنبه می‌آییم دنبالت."),
        ex("Hij laat zijn auto repareren.", "ماشینش را می‌دهد تعمیر کنند."),
        ex("Ik hoor de kinderen buiten spelen.", "صدای بچه‌ها را می‌شنوم که بیرون بازی می‌کنند."),
    ],
    [
        wrong("Ik ga koken vanavond.", "Ik ga vanavond koken.",
              "زمان وسط می‌آید؛ مصدر باید آخرین کلمه باشد."),
        wrong("Ik ga vanavond kook.", "Ik ga vanavond koken.",
              "فعل دوم صرف نمی‌شود — مصدر می‌ماند."),
    ],
    "به محض اینکه جمله‌هایت از سه کلمه بلندتر شوند، این ساختار همه‌جا پیدا می‌شود. عادت کردن به «فعل آخر» بزرگ‌ترین جهش در روان شدن هلندی است.",
    [
        pickorder("کدام درست است؟",
                  ["Ik ga morgen boodschappen doen.", "Ik ga doen morgen boodschappen.",
                   "Ik ga morgen doen boodschappen."],
                  "Ik ga morgen boodschappen doen.",
                  "مصدر آخرین کلمه است.", concept=C_INF_END),
        order("We komen je zondag ophalen.",
              why="فعل صرف‌شده دوم، مصدر آخر.", concept=C_INF_END),
        order("Zij blijft vandaag thuis werken.",
              why="زمان و مکان وسط، مصدر آخر.", concept=C_INF_END),
        fix("Ik wil leren Nederlands.", "Ik wil Nederlands leren.",
            "مفعول وسط می‌آید و مصدر آخر.", concept=C_INF_END),
        fix("Hij gaat zwemt vanavond.", "Hij gaat vanavond zwemmen.",
            "فعل دوم مصدر است، و زمان وسط قرار می‌گیرد.", concept=C_INF_END),
        transform("Ik kook vanavond. → (met «gaan»)", "Ik ga vanavond koken.",
                  "gaan صرف می‌شود و koken مصدر آخر می‌شود.", concept=C_INF_END),
        fa2nl("«فردا می‌روم خرید کنم.»", "Ik ga morgen boodschappen doen.",
              "ga جای دوم، doen آخر جمله.", concept=C_INF_END),
        blank("Ik kan je morgen ___. (helpen)", "helpen",
              "فعل دوم به شکل مصدر و در انتها.", concept=C_INF_END),
    ])

lesson(
    "a1-l16", "a1-scheidbaar", "A1",
    "Scheidbare werkwoorden", "افعال جداشدنی",
    [C_SEP],
    discover(
        ["opstaan → Ik sta om zeven uur op.", "meenemen → Neem je je paspoort mee?",
         "aankomen → De trein komt om acht uur aan."],
        "با پیشوند (op، mee، aan) چه اتفاقی افتاد؟",
        "از فعل جدا شد و رفت آخر جمله. به این‌ها فعل جداشدنی می‌گویند."),
    rule("prefix gaat naar het einde van de zin",
         "در جمله‌ی ساده پیشوند جدا می‌شود و آخر می‌رود. ولی بعد از فعل وجهی، فعل کامل و سرِهم می‌ماند: Ik moet vroeg opstaan.",
         "separable verbs split"),
    pattern([("Ik", "subject"), ("sta", "verb"), ("om zeven uur", "time"), ("op", "prefix")],
            "پیشوند مثل یک آهنربا به انتهای جمله کشیده می‌شود."),
    [
        ex("Ik sta elke dag om zes uur op.", "هر روز ساعت شش بیدار می‌شوم."),
        ex("Neem je je paspoort mee?", "پاسپورتت را با خودت می‌آوری؟"),
        ex("De trein komt om tien uur aan.", "قطار ساعت ده می‌رسد."),
        ex("Ik bel je morgen op.", "فردا بهت زنگ می‌زنم."),
        ex("Ik moet morgen vroeg opstaan.", "فردا باید زود بیدار شوم.", "بعد از فعل وجهی سرِهم می‌ماند"),
        ex("Doe de deur even dicht.", "لطفاً در را ببند."),
    ],
    [
        wrong("Ik opsta om zeven uur.", "Ik sta om zeven uur op.",
              "در جمله‌ی ساده پیشوند باید جدا شود و آخر برود."),
        wrong("Ik moet vroeg sta op.", "Ik moet vroeg opstaan.",
              "بعد از فعل وجهی، فعل جداشدنی مصدر و سرِهم می‌ماند."),
    ],
    "بخش بزرگی از فعل‌های روزمره جداشدنی‌اند: opstaan، meenemen، aankomen، opbellen، meegaan، uitgaan، schoonmaken. بدون این قاعده جمله‌هایت نامفهوم می‌شوند.",
    [
        order("Ik sta om zeven uur op.",
              why="پیشوند op آخر جمله می‌رود.", concept=C_SEP),
        order("De trein komt om acht uur aan.",
              why="aan جدا می‌شود و انتها می‌ایستد.", concept=C_SEP),
        pickorder("کدام درست است؟",
                  ["Ik bel je morgen op.", "Ik opbel je morgen.", "Ik bel op je morgen."],
                  "Ik bel je morgen op.",
                  "پیشوند op آخرین کلمه است.", concept=C_SEP),
        pickorder("کدام درست است؟",
                  ["Ik moet morgen vroeg opstaan.", "Ik moet morgen vroeg sta op.",
                   "Ik moet op morgen vroeg staan."],
                  "Ik moet morgen vroeg opstaan.",
                  "بعد از moeten، فعل کامل و مصدر می‌ماند.", concept=C_SEP),
        transform("opstaan (ik, om 6 uur) → ", "Ik sta om 6 uur op.",
                  "فعل صرف می‌شود و پیشوند آخر می‌رود.", concept=C_SEP),
        fix("Ik meeneem mijn paspoort.", "Ik neem mijn paspoort mee.",
            "پیشوند mee باید جدا شود و آخر بیاید.", concept=C_SEP),
        fa2nl("«فردا بهت زنگ می‌زنم.»", "Ik bel je morgen op.",
              "opbellen جداشدنی است: bel … op.", concept=C_SEP),
        blank("Hoe laat komt de trein ___? (aankomen)", "aan",
              "پیشوند aan آخر جمله می‌آید.", concept=C_SEP),
        dialogue("— Ga je mee naar de markt?",
                 "— Ja, ik ga ___.", ["mee", "meegaan", "gaan mee"], "mee",
                 "meegaan جداشدنی است: ik ga mee.", concept=C_SEP),
    ])

lesson(
    "a1-l17", "a1-tijd", "A1",
    "Hoe laat? Wanneer?", "ساعت و زمان",
    [C_TIME],
    discover(
        ["om acht uur", "op maandag", "in juni", "'s ochtends", "half negen"],
        "به «half negen» دقت کن — یعنی ساعت چند؟",
        "یعنی ۸:۳۰، نه ۹:۳۰. هلندی‌ها به ساعتِ بعدی اشاره می‌کنند: half negen = نیم‌ساعت مانده به نُه."),
    rule("om + uur · op + dag · in + maand · 's ochtends/'s middags/'s avonds",
         "و مهم‌تر از همه: half negen = ۸:۳۰. «نیم‌ساعت به سمت نُه».",
         "at / on / in"),
    pattern([("om", "prep"), ("half negen", "time"), ("=", "eq"), ("8:30", "clock")],
            "kwart over acht = ۸:۱۵ · kwart voor negen = ۸:۴۵"),
    [
        ex("De les begint om negen uur.", "کلاس ساعت نه شروع می‌شود."),
        ex("Ik werk op maandag en dinsdag.", "دوشنبه و سه‌شنبه کار می‌کنم."),
        ex("In juli gaan we op vakantie.", "در ژوئیه به تعطیلات می‌رویم."),
        ex("'s Ochtends drink ik altijd koffie.", "صبح‌ها همیشه قهوه می‌خورم."),
        ex("We spreken af om half acht.", "ساعت هفت‌و‌نیم قرار می‌گذاریم.", "half acht = ۷:۳۰"),
        ex("Het is kwart over drie.", "ساعت سه‌و‌ربع است."),
    ],
    [
        wrong("half negen = 9:30", "half negen = 8:30",
              "این پرتکرارترین سوءتفاهم است و می‌تواند باعث شود یک ساعت دیر برسی."),
        wrong("Ik werk in maandag.", "Ik werk op maandag.",
              "برای روزهای هفته op می‌آید، نه in."),
    ],
    "برای قرار گذاشتن، وقت دکتر، ساعت کاری و قطار. اشتباه در half یعنی یک ساعت دیر یا زود رسیدن — این را حتماً درست یاد بگیر.",
    [
        mc("«half negen» betekent:", ["8:30", "9:30", "9:00"], "8:30",
           "half + عدد یعنی نیم ساعت مانده به آن عدد.", concept=C_TIME),
        mc("De les begint ___ negen uur.", ["om", "op", "in"], "om",
           "برای ساعت om.", concept=C_TIME),
        mc("Ik werk ___ maandag.", ["op", "in", "om"], "op",
           "برای روزهای هفته op.", concept=C_TIME),
        mc("___ juni ga ik naar Iran.", ["In", "Op", "Om"], "In",
           "برای ماه‌ها in.", concept=C_TIME),
        blank("Het is ___ over drie. (3:15)", "kwart",
              "kwart over = ربع گذشته.", concept=C_TIME),
        blank("We spreken af ___ half acht. (7:30)", "om",
              "برای ساعت‌ها om می‌آید، حتی با half.", concept=C_TIME),
        fix("Ik sta 's ochtend vroeg op.", "Ik sta 's ochtends vroeg op.",
            "شکل درست 's ochtends است (با s پایانی).", concept=C_TIME),
        fa2nl("«ساعت هشت‌و‌نیم قرار داریم.»", "We spreken af om half negen.",
              "۸:۳۰ در هلندی می‌شود half negen.", concept=C_TIME),
        dialogue("— Hoe laat begint de vergadering?",
                 "— ___ tien uur.", ["Om", "Op", "In"], "Om",
                 "برای ساعت همیشه om.", concept=C_TIME),
    ])

lesson(
    "a1-l18", "a1-tijd", "A1",
    "In, op, naar, bij", "حروف اضافه‌ی مکان",
    [C_PREP],
    discover(
        ["Ik ben in de winkel.", "Ik ga naar de winkel.",
         "Het boek ligt op tafel.", "Ik ben bij de dokter."],
        "فرق in و naar در این جمله‌ها چیست؟",
        "naar یعنی حرکت به سمتِ جایی؛ in/op/bij یعنی همان‌جا بودن."),
    rule("naar = beweging · in / op / bij / aan = plaats",
         "اگر داری می‌روی: naar. اگر آنجایی: in، op، bij یا aan.",
         "to vs. in/at"),
    pattern([("Ik ga", "verb"), ("naar", "prep-move"), ("het station", "place"), ("|", "sep"),
             ("Ik ben", "verb"), ("op", "prep-static"), ("het station", "place")],
            "op برای سطح‌ها و بعضی مکان‌های ثابت: op school، op kantoor، op het station."),
    [
        ex("Ik ga naar mijn werk.", "می‌روم سر کار."),
        ex("Ik ben op mijn werk.", "سر کارم."),
        ex("De kinderen zitten op school.", "بچه‌ها مدرسه‌اند."),
        ex("Ik woon in Delft.", "در دلفت زندگی می‌کنم."),
        ex("We eten vanavond bij mijn ouders.", "امشب خانه‌ی پدر و مادرم شام می‌خوریم."),
        ex("Hij zit aan tafel.", "او سر میز نشسته است."),
    ],
    [
        wrong("Ik ga in de winkel.", "Ik ga naar de winkel.",
              "با فعل‌های حرکتی naar لازم است."),
        wrong("Ik ben naar huis.", "Ik ben thuis.",
              "«خانه بودن» عبارت ثابت خودش را دارد: thuis. و «رفتن به خانه» می‌شود naar huis."),
    ],
    "برای آدرس دادن، قرار گذاشتن و گفتن اینکه کجایی. اشتباه گرفتن in و naar یکی از چیزهایی است که فوراً شنیده می‌شود.",
    [
        mc("Ik ga ___ het station.", ["naar", "in", "op"], "naar",
           "gaan فعل حرکتی است → naar.", concept=C_PREP),
        mc("Ik werk ___ kantoor.", ["op", "in", "naar"], "op",
           "با kantoor و school هلندی op می‌گوید.", concept=C_PREP),
        mc("Wij wonen ___ Rotterdam.", ["in", "op", "naar"], "in",
           "برای شهرها in.", concept=C_PREP),
        mc("Vanavond eten we ___ mijn zus.", ["bij", "in", "naar"], "bij",
           "«خانه‌ی کسی بودن» با bij.", concept=C_PREP),
        blank("Het boek ligt ___ tafel.", "op",
              "روی سطح → op. (اینجا حرف تعریف هم نمی‌آید: op tafel.)", concept=C_PREP),
        fix("Ik ga in mijn werk.", "Ik ga naar mijn werk.",
            "حرکت به سمت جایی → naar.", concept=C_PREP),
        fix("Ik ben naar huis, kom maar langs.", "Ik ben thuis, kom maar langs.",
            "«در خانه بودن» می‌شود thuis.", concept=C_PREP),
        fa2nl("«فردا می‌روم دکتر.»", "Ik ga morgen naar de dokter.",
              "حرکت → naar.", concept=C_PREP),
        pick2("De kinderen zitten ___ school.", ["op", "in"], "op",
              "با school هلندی op به کار می‌برد.", concept=C_PREP),
    ])

lesson(
    "a1-l19", "a1-beleefd", "A1",
    "Kom binnen! Vriendelijk vragen", "امری و درخواست مؤدبانه",
    [C_IMP],
    discover(
        ["Kom binnen!", "Kijk eens!", "Doe de deur even dicht.",
         "Zou je de deur even dicht willen doen?"],
        "چه چیزی جمله‌ی سوم را نرم‌تر از دومی می‌کند؟",
        "کلمه‌های کوچک even و eens. هلندی‌ها با همین کلمه‌های ریز دستور را به خواهش تبدیل می‌کنند."),
    rule("stam = bevel · + even/eens = vriendelijk · Kun je…? = nog beleefder",
         "شکل امری فقط ریشه‌ی فعل است. برای مؤدبانه شدن even یا eens اضافه کن، یا کلاً سؤالی بپرس.",
         "imperative = stem"),
    pattern([("Doe", "verb"), ("de deur", "object"), ("even", "softener"), ("dicht", "prefix")],
            "even = «یک لحظه/یک زحمتی» — تقریباً همیشه لحن را نرم می‌کند."),
    [
        ex("Kom binnen!", "بیا تو!"),
        ex("Wacht even.", "یک لحظه صبر کن."),
        ex("Doe de deur even dicht.", "لطفاً در را ببند."),
        ex("Kun je me even helpen?", "می‌شود یک لحظه کمکم کنی؟"),
        ex("Zegt u het maar.", "بفرمایید.", "در مغازه و اداره خیلی می‌شنوی"),
        ex("Let op!", "حواست باشد!"),
    ],
    [
        wrong("Jij komt hier!", "Kom hier!",
              "برای دستور دادن فاعل نمی‌آید؛ فقط ریشه‌ی فعل."),
        wrong("Geef mij het zout!", "Kun je me het zout even geven?",
              "شکل امری تنها در هلندی خشن به نظر می‌رسد. با سؤال یا even خیلی مؤدبانه‌تر می‌شود."),
    ],
    "در مغازه، سر کار و بین دوستان. هلندی‌ها مستقیم حرف می‌زنند، ولی «even» و «kun je…?» همان چیزی است که مستقیم بودن را بی‌ادبی نمی‌کند.",
    [
        mc("___ binnen!", ["Kom", "Komt", "Komen"], "Kom",
           "شکل امری فقط ریشه است: kom.", concept=C_IMP),
        mc("___ even!", ["Wacht", "Wachten", "Wachtte"], "Wacht",
           "ریشه‌ی wachten می‌شود wacht.", concept=C_IMP),
        pickorder("کدام مؤدبانه‌ترین است؟",
                  ["Kun je me even helpen?", "Help mij!", "Jij helpt mij."],
                  "Kun je me even helpen?",
                  "سؤال + even نرم‌ترین شکل درخواست است.", concept=C_IMP),
        transform("de deur dichtdoen (bevel, vriendelijk) →", "Doe de deur even dicht.",
                  "ریشه + مفعول + even + پیشوند جداشده.", concept=C_IMP),
        fix("Jij komt hier!", "Kom hier!",
            "در امری فاعل نمی‌آید.", concept=C_IMP),
        fa2nl("«یک لحظه صبر کن.»", "Wacht even.",
              "ریشه‌ی فعل + even.", concept=C_IMP),
        scenario("Je zit in de trein en iemands tas ligt op jouw stoel.",
                 "Wat zeg je?",
                 ["Kunt u uw tas even weghalen?", "Haal je tas weg!", "Uw tas weg!"],
                 "Kunt u uw tas even weghalen?",
                 "با u و even، درخواست مؤدبانه و طبیعی می‌شود.", concept=C_IMP),
        dialogue("— Mag ik iets vragen?", "— Ja hoor, ___ het maar.",
                 ["zeg", "zegt", "zeggen"], "zeg",
                 "«Zeg het maar» شکل امری ریشه است.", concept=C_IMP),
    ])

# ----------------------------------------------------------------- modules

module("a1-bezit", "A1", "Bezit en aanwijzen", "مالکیت و اشاره",
       "بگویی چیزی مالِ کیست، به چیزها اشاره کنی و ضمیر مفعولی درست به کار ببری.",
       ["a1-l11", "a1-l12", "a1-l13"], icon="user")

module("a1-modaal", "A1", "Modale werkwoorden", "افعال وجهی",
       "kunnen، willen، moeten و mogen، و قانون «فعل دوم آخر جمله».",
       ["a1-l14", "a1-l15"], icon="target")

module("a1-scheidbaar", "A1", "Scheidbare werkwoorden", "افعال جداشدنی",
       "پیشوندی که آخر جمله می‌رود — یکی از عجیب‌ترین و پرکاربردترین چیزهای هلندی.",
       ["a1-l16"], icon="gap")

module("a1-tijd", "A1", "Tijd en plaats", "زمان و مکان",
       "ساعت بگویی، قرار بگذاری و حروف اضافه‌ی مکان را درست به کار ببری.",
       ["a1-l17", "a1-l18"], icon="clock")

module("a1-beleefd", "A1", "Vragen en verzoeken", "درخواست و ادب",
       "دستور، خواهش و درخواست مؤدبانه — همان کلمه‌های ریزی که لحن را می‌سازند.",
       ["a1-l19"], icon="volume")
