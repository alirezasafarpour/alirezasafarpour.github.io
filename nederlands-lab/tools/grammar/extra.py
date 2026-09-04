"""Aanvullingen na de audit van het curriculum.

Twee onderwerpen die in de eerste opzet ontbraken en die Perzischtalige
leerders juist heel vaak fout doen: het verschil tussen toen, als en wanneer,
en de volgorde van twee objecten in één zin.
"""

from _kit import (concept, lesson, module, ex, wrong, pattern, discover, rule,
                  mc, pickorder, pick2, dialogue, scenario,
                  blank, transform, fa2nl, fix, order, subclause)

# ---------------------------------------------------------------- concepts

C_TOEN_ALS = concept(
    "toen-als-wanneer", "Toen, als of wanneer?", "toen، als یا wanneer؟", "A2",
    keywords=["toen", "als", "wanneer", "tijd bijzin", "verleden", "چه وقت"],
    summary_fa="گذشته‌ی یک‌بار → toen. تکرارشونده یا آینده → als. سؤال → wanneer.")

C_TWO_OBJ = concept(
    "object-order", "Twee objecten in één zin", "ترتیب دو مفعول", "B1",
    keywords=["twee objecten", "meewerkend voorwerp", "geef hem het boek", "aan hem"],
    summary_fa="اسم: غیرمستقیم اول. ضمیرِ مستقیم: اول می‌آید و بقیه با aan.")

# ----------------------------------------------------------------- lessons

lesson(
    "a2-l21", "a2-tijdzinnen", "A2",
    "Toen, als of wanneer?", "toen، als یا wanneer؟",
    [C_TOEN_ALS],
    discover(
        ["Toen ik klein was, woonde ik in Iran.",
         "Als ik klaar ben, bel ik je.",
         "Als ik moe ben, ga ik vroeg naar bed.",
         "Wanneer begint de les?"],
        "هر سه در فارسی «وقتی» ترجمه می‌شوند. چه چیزی آن‌ها را از هم جدا می‌کند؟",
        "toen فقط برای گذشته‌ی یک‌بار. als برای آینده یا کاری که تکرار می‌شود. wanneer فقط در سؤال."),
    rule("toen = eenmalig verleden · als = herhaling of toekomst · wanneer = vraag",
         "این سه را در فارسی یک کلمه می‌گوییم، برای همین راحت قاطی می‌شوند. اشتباه‌شان بلافاصله شنیده می‌شود.",
         "when (past) / when(ever) / when?"),
    pattern([("Toen", "past-once"), ("ik klein was", "clause"), ("|", "sep"),
             ("Als", "future-repeat"), ("ik klaar ben", "clause"), ("|", "sep"),
             ("Wanneer", "question"), ("begint de les?", "clause")],
            "هر سه جمله‌واره می‌سازند، پس در هر سه فعل آخر می‌رود."),
    [
        ex("Toen ik in Iran woonde, werkte ik als ingenieur.", "وقتی در ایران زندگی می‌کردم، مهندس بودم."),
        ex("Toen ik gisteren thuiskwam, was het al donker.", "دیروز که رسیدم خانه، هوا تاریک شده بود."),
        ex("Als ik klaar ben met werken, bel ik je.", "وقتی کارم تمام شد، بهت زنگ می‌زنم."),
        ex("Als het regent, neem ik de bus.", "وقتی باران می‌بارد، اتوبوس سوار می‌شوم.", "کار تکرارشونده"),
        ex("Wanneer heb je tijd?", "کِی وقت داری؟"),
        ex("Ik weet niet wanneer hij komt.", "نمی‌دانم کِی می‌آید.", "در سؤال غیرمستقیم هم wanneer"),
    ],
    [
        wrong("Als ik klein was, woonde ik in Iran.", "Toen ik klein was, woonde ik in Iran.",
              "برای گذشته‌ی یک‌بار حتماً toen. این پرتکرارترین اشتباه در این موضوع است."),
        wrong("Toen ik klaar ben, bel ik je.", "Als ik klaar ben, bel ik je.",
              "برای آینده als می‌آید، نه toen."),
    ],
    "در تعریف کردن گذشته (مصاحبه‌ی کاری: «Toen ik bij … werkte…») و در قرار گذاشتن («Als ik klaar ben…»). سه کلمه‌ای که مدام لازم می‌شوند.",
    [
        mc("___ ik klein was, woonde ik in Iran.", ["Toen", "Als", "Wanneer"], "Toen",
           "گذشته‌ی یک‌بار → toen.", concept=C_TOEN_ALS),
        mc("___ ik klaar ben, bel ik je.", ["Als", "Toen", "Wanneer"], "Als",
           "آینده → als.", concept=C_TOEN_ALS),
        mc("___ begint de vergadering?", ["Wanneer", "Toen", "Als"], "Wanneer",
           "سؤال مستقیم → wanneer.", concept=C_TOEN_ALS),
        mc("___ het regent, neem ik altijd de bus.", ["Als", "Toen", "Wanneer"], "Als",
           "کار تکرارشونده → als.", concept=C_TOEN_ALS),
        pick2("___ ik gisteren thuiskwam, was het donker.", ["Toen", "Als"], "Toen",
              "یک اتفاق مشخص در گذشته → toen.", concept=C_TOEN_ALS),
        blank("Ik weet niet ___ hij komt.", "wanneer",
              "در سؤال غیرمستقیم هم wanneer می‌آید.", concept=C_TOEN_ALS),
        fix("Als ik in Iran woonde, was ik ingenieur.",
            "Toen ik in Iran woonde, was ik ingenieur.",
            "دوره‌ای مشخص در گذشته → toen.", concept=C_TOEN_ALS),
        transform("Ik was klein. Ik woonde in Iran. → (met «toen»)",
                  "Toen ik klein was, woonde ik in Iran.",
                  "toen + جمله‌واره با فعل آخر، بعد کاما و فعل جمله‌ی اصلی.",
                  concept=C_TOEN_ALS),
        fa2nl("«وقتی کارم تمام شد، بهت زنگ می‌زنم.»", "Als ik klaar ben, bel ik je.",
              "آینده → als، و بعد از کاما فعل اول می‌آید.", concept=C_TOEN_ALS),
        scenario("In een sollicitatiegesprek vertel je over je vorige baan in Iran.",
                 "Hoe begin je?",
                 ["Toen ik in Iran werkte, had ik een eigen team.",
                  "Als ik in Iran werkte, had ik een eigen team.",
                  "Wanneer ik in Iran werkte, had ik een eigen team."],
                 "Toen ik in Iran werkte, had ik een eigen team.",
                 "دوره‌ای مشخص در گذشته → toen.", concept=C_TOEN_ALS),
    ])

lesson(
    "b1-l16", "b1-objecten", "B1",
    "Ik geef hem het boek", "ترتیب دو مفعول",
    [C_TWO_OBJ],
    discover(
        ["Ik geef mijn collega het rapport.",
         "Ik geef hem het rapport.",
         "Ik geef het aan hem."],
        "در جمله‌ی سوم چرا ترتیب عوض شد و aan اضافه شد؟",
        "وقتی مفعولِ مستقیم ضمیر باشد (het)، اول می‌آید و گیرنده با aan بعدش می‌آید."),
    rule("wie krijgt het → eerst · maar: het/hem als lijdend voorwerp → vooraan + aan",
         "با اسم: گیرنده اول. با ضمیرِ چیز: آن ضمیر اول و گیرنده با aan.",
         "I give him the book / I give it to him"),
    pattern([("Ik geef", "verb"), ("hem", "indirect"), ("het rapport", "direct"),
             ("|", "sep"), ("Ik geef", "verb"), ("het", "direct-pron"), ("aan hem", "aan-phrase")],
            "همین قاعده برای sturen، laten zien، vertellen و uitleggen هم صادق است."),
    [
        ex("Ik geef mijn collega het rapport.", "گزارش را به همکارم می‌دهم."),
        ex("Ik geef hem het rapport.", "گزارش را به او می‌دهم."),
        ex("Ik geef het aan hem.", "آن را به او می‌دهم."),
        ex("Kun je me de e-mail sturen?", "می‌شود ایمیل را برایم بفرستی؟"),
        ex("Ik stuur het je vanavond.", "امشب برایت می‌فرستمش."),
        ex("Zal ik het je even laten zien?", "می‌خواهی نشانت بدهم؟"),
    ],
    [
        wrong("Ik geef het rapport hem.", "Ik geef hem het rapport.",
              "وقتی هر دو اسم/ضمیرِ شخص و چیز هستند، گیرنده اول می‌آید."),
        wrong("Ik geef aan hem het.", "Ik geef het aan hem.",
              "ضمیرِ چیز (het) باید مستقیم بعد از فعل بیاید."),
    ],
    "در محیط کار مدام: فرستادن فایل، نشان دادن چیزی، توضیح دادن به کسی. «Ik stuur het je morgen» جمله‌ی روزمره‌ی هر دفتری است.",
    [
        pickorder("کدام درست است؟",
                  ["Ik geef hem het rapport.", "Ik geef het rapport hem.",
                   "Ik geef het rapport aan hem het."],
                  "Ik geef hem het rapport.",
                  "گیرنده (hem) قبل از چیز می‌آید.", concept=C_TWO_OBJ),
        pickorder("کدام درست است؟",
                  ["Ik geef het aan hem.", "Ik geef hem het.", "Ik geef aan hem het."],
                  "Ik geef het aan hem.",
                  "وقتی چیز به شکل ضمیر (het) بیاید، اول می‌آید و گیرنده با aan.",
                  concept=C_TWO_OBJ),
        mc("Kun je ___ de e-mail sturen?", ["me", "aan mij het", "mij het"], "me",
           "گیرنده به شکل ضمیر، قبل از اسمِ چیز.", concept=C_TWO_OBJ),
        order("Ik stuur het je vanavond.",
              why="ضمیرِ چیز (het) اول، بعد گیرنده (je)، بعد زمان.", concept=C_TWO_OBJ),
        blank("Ik heb het rapport af. Ik stuur ___ morgen naar je toe.", "het",
              "چیزی که فرستاده می‌شود با het جایگزین می‌شود.", concept=C_TWO_OBJ),
        transform("Ik geef mijn collega het rapport. → (چیز را با «het» جایگزین کن)",
                  "Ik geef het aan mijn collega.",
                  "با ضمیرِ چیز، گیرنده به aan-عبارت تبدیل می‌شود.", concept=C_TWO_OBJ),
        fix("Ik stuur de e-mail je morgen.", "Ik stuur je de e-mail morgen.", 
            "گیرنده (je) قبل از اسمِ چیز می‌آید.", alt=["Ik stuur je morgen de e-mail."], concept=C_TWO_OBJ),
        fa2nl("«فردا برایت می‌فرستمش.»", "Ik stuur het je morgen.", 
              "ضمیرِ چیز اول، بعد گیرنده.", alt=["Ik stuur het morgen naar je toe."], concept=C_TWO_OBJ),
        dialogue("— Heb je het contract?", "— Ja, ik mail ___ zo even.",
                 ["het je", "je het", "aan jou het"], "het je",
                 "ضمیرِ چیز (het) قبل از گیرنده (je) می‌آید.", concept=C_TWO_OBJ),
    ])

# ----------------------------------------------------------------- modules

module("a2-tijdzinnen", "A2", "Toen, als en wanneer", "زمان در جمله‌واره",
       "سه کلمه‌ای که در فارسی همه «وقتی» می‌شوند، ولی در هلندی سه کاربرد کاملاً جدا دارند.",
       ["a2-l21"], icon="clock")

module("b1-objecten", "B1", "Twee objecten", "دو مفعول",
       "وقتی هم می‌گویی چه چیزی و هم به چه کسی — ترتیبش قاعده‌ی خودش را دارد.",
       ["b1-l16"], icon="arrow")
