"""A2, deel 2 — bijvoeglijke naamwoorden, wederkerend, te + infinitief, toekomst en er."""

from _kit import (concept, lesson, module, ex, wrong, pattern, discover, rule,
                  mc, dehet, nietgeen, pickorder, pick2, dialogue, scenario,
                  blank, conjugate, transform, fa2nl, fix, type_all,
                  order, question, subclause)

# ---------------------------------------------------------------- concepts

C_ADJ = concept(
    "adjective-e", "Bijvoeglijk naamwoord: -e of niet", "صفت: e می‌گیرد یا نه", "A2",
    keywords=["bijvoeglijk naamwoord", "adjectief", "een groot huis", "de grote man", "صفت"],
    summary_fa="صفت تقریباً همیشه -e می‌گیرد؛ استثنا: een + کلمه‌ی het مفرد.")

C_COMP = concept(
    "adjective-comparative", "Vergrotende en overtreffende trap", "صفت تفضیلی و عالی", "A2",
    keywords=["groter", "grootst", "beter", "best", "vergelijking", "تفضیلی"],
    summary_fa="er- برای «تر»، st- برای «ترین»: groot → groter → grootst.")

C_COMPARE = concept(
    "comparison-dan-als", "Vergelijken: dan en net zo … als", "مقایسه کردن", "A2",
    keywords=["dan", "net zo als", "even als", "meer dan", "مقایسه"],
    summary_fa="نابرابر: … -er dan. برابر: net zo … als / even … als.")

C_REFL = concept(
    "verb-reflexive", "Wederkerende werkwoorden", "افعال انعکاسی", "A2",
    keywords=["zich", "me", "je", "zich voelen", "zich wassen", "انعکاسی"],
    summary_fa="me/je/zich/ons به فعل می‌چسبد: ik voel me، hij voelt zich.")

C_TE_INF = concept(
    "te-infinitive", "Te + infinitief", "te + مصدر", "A2",
    keywords=["te", "proberen te", "vergeten te", "beginnen te", "مصدر با te"],
    summary_fa="بعد از فعل‌هایی مثل proberen، vergeten، beginnen: te + مصدر در آخر.")

C_OM_TE = concept(
    "om-te", "Om … te (doel)", "om … te برای بیان هدف", "A2",
    keywords=["om te", "doel", "waarom", "om te leren", "هدف"],
    summary_fa="برای گفتن «برای اینکه…»: om + بقیه + te + مصدر.")

C_FUTURE = concept(
    "future-gaan-zullen", "Toekomst met gaan en zullen", "آینده با gaan و zullen", "A2",
    keywords=["gaan", "zullen", "toekomst", "zal", "zullen we", "آینده"],
    summary_fa="نقشه‌ی قطعی → gaan؛ پیشنهاد و قول → zullen. زمان حال هم اغلب کافی است.")

C_ER_EXIST = concept(
    "er-existential", "Er is / er zijn", "er برای «وجود دارد»", "A2",
    keywords=["er is", "er zijn", "er staat", "existentieel", "وجود دارد"],
    summary_fa="er + فعل = «هست/وجود دارد»: Er is een probleem.")

C_ER_COUNT = concept(
    "er-quantity", "Er bij een aantal", "er همراه عدد", "A2",
    keywords=["er drie", "ik heb er twee", "aantal", "er + getal"],
    summary_fa="وقتی اسم تکرار نمی‌شود ولی عدد می‌آید: Ik heb er drie.")

# ----------------------------------------------------------------- lessons

lesson(
    "a2-l12", "a2-bijvoeglijk", "A2",
    "Een groot huis, de grote man", "صفت: e می‌گیرد یا نه؟",
    [C_ADJ],
    discover(
        ["de grote man", "het grote huis", "een grote man", "een groot huis"],
        "فقط یکی از این چهارتا -e ندارد. کدام؟ و چه فرقی با بقیه دارد؟",
        "«een groot huis»: هم een دارد و هم کلمه‌ی het است. این تنها حالتی است که صفت -e نمی‌گیرد."),
    rule("altijd -e · behalve: een + het-woord (enkelvoud)",
         "یک استثنا بیشتر ندارد. اگر شک کردی، -e بگذار — در بیشتر موارد درست است.",
         "adjectives take -e, except after 'een' with a het-word"),
    pattern([("een", "article"), ("groot", "adj-no-e"), ("huis", "het-noun"),
             ("|", "sep"), ("het", "article"), ("grote", "adj-e"), ("huis", "het-noun")],
            "بعد از de، het، deze، die، mijn و در جمع همیشه -e می‌آید."),
    [
        ex("Dat is een mooi huis.", "آن یک خانه‌ی قشنگ است.", "een + het-woord → بدون e"),
        ex("Het mooie huis staat te koop.", "خانه‌ی قشنگ برای فروش است."),
        ex("Ik zoek een goede baan.", "دنبال یک شغل خوب می‌گردم.", "baan کلمه‌ی de است → e"),
        ex("Wij hebben een nieuwe collega.", "همکار جدیدی داریم."),
        ex("Dit zijn moeilijke vragen.", "این‌ها سؤال‌های سختی‌اند.", "جمع → همیشه e"),
        ex("Mijn oude fiets is kapot.", "دوچرخه‌ی قدیمی‌ام خراب است."),
    ],
    [
        wrong("een goed baan", "een goede baan",
              "baan کلمه‌ی de است، پس صفت -e می‌گیرد."),
        wrong("het groot huis", "het grote huis",
              "بعد از het همیشه -e می‌آید؛ استثنا فقط با een است."),
    ],
    "هر بار که چیزی را توصیف می‌کنی. در مصاحبه‌ی کاری («een goede ervaring»، «een nieuwe uitdaging») و در آگهی خانه دائم به کار می‌رود.",
    [
        mc("Dat is een ___ huis.", ["mooi", "mooie", "mooies"], "mooi",
           "een + کلمه‌ی het → صفت بدون e.", concept=C_ADJ),
        mc("Het ___ huis staat te koop.", ["mooie", "mooi", "mooier"], "mooie",
           "بعد از het همیشه -e.", concept=C_ADJ),
        mc("Ik zoek een ___ baan.", ["goede", "goed", "goeder"], "goede",
           "baan کلمه‌ی de است → -e.", concept=C_ADJ),
        mc("Dit zijn ___ vragen.", ["moeilijke", "moeilijk", "moeilijker"], "moeilijke",
           "جمع همیشه -e می‌گیرد.", concept=C_ADJ),
        blank("Mijn ___ fiets is kapot. (oud)", "oude",
              "بعد از ضمیر ملکی همیشه -e.", concept=C_ADJ),
        blank("We hebben een ___ probleem. (klein)", "klein",
              "probleem کلمه‌ی het است و een دارد → بدون e.", concept=C_ADJ),
        fix("Ik heb een nieuw collega.", "Ik heb een nieuwe collega.",
            "collega کلمه‌ی de است → -e.", concept=C_ADJ),
        fa2nl("«دنبال یک شغل خوب می‌گردم.»", "Ik zoek een goede baan.",
              "baan کلمه‌ی de است، پس goede.", concept=C_ADJ),
        pick2("Dat is een ___ idee.", ["goed", "goede"], "goed",
              "idee کلمه‌ی het است و een دارد → بدون e.", concept=C_ADJ),
    ])

lesson(
    "a2-l13", "a2-bijvoeglijk", "A2",
    "Groter, grootst", "تفضیلی و عالی",
    [C_COMP],
    discover(
        ["groot → groter → grootst", "goed → beter → best",
         "interessant → interessanter → interessantst"],
        "چه چیزی به آخر صفت اضافه می‌شود؟ و کدام‌شان بی‌قاعده است؟",
        "er- برای «تر» و st- برای «ترین». فقط goed/veel/weinig بی‌قاعده‌اند."),
    rule("+er (vergelijken) · +st (de beste)",
         "برخلاف انگلیسی، هلندی حتی صفت‌های بلند را هم با -er می‌سازد: interessanter، belangrijker.",
         "-er / -st"),
    pattern([("groot", "base"), ("→", "arrow"), ("groter", "comp"), ("→", "arrow"),
             ("het grootst", "sup")],
            "بی‌قاعده‌ها: goed → beter → best · veel → meer → meest · weinig → minder → minst."),
    [
        ex("Deze fiets is goedkoper.", "این دوچرخه ارزان‌تر است."),
        ex("Amsterdam is groter dan Delft.", "آمستردام از دلفت بزرگ‌تر است."),
        ex("Dit is de beste oplossing.", "این بهترین راه‌حل است."),
        ex("Nederlands is moeilijker dan ik dacht.", "هلندی از آنچه فکر می‌کردم سخت‌تر است."),
        ex("Hij werkt het hardst van iedereen.", "او از همه سخت‌تر کار می‌کند."),
    ],
    [
        wrong("Dit is meer interessant.", "Dit is interessanter.",
              "هلندی برای صفت‌های بلند هم -er به کار می‌برد، نه meer."),
        wrong("Dit is de goedste oplossing.", "Dit is de beste oplossing.",
              "goed بی‌قاعده است: beter، best."),
    ],
    "برای مقایسه‌ی قیمت، مسکن، شغل و خیلی چیزهای دیگر. در مصاحبه‌ی کاری هم مدام لازم است: «een betere kans»، «het belangrijkst».",
    [
        mc("Amsterdam is ___ dan Delft.", ["groter", "grootst", "meer groot"], "groter",
           "برای مقایسه -er.", concept=C_COMP),
        mc("Dit is de ___ oplossing.", ["beste", "goedste", "betere"], "beste",
           "goed → beter → best (بی‌قاعده).", concept=C_COMP),
        mc("Deze cursus is ___ dan de vorige.", ["interessanter", "meer interessant", "interessantst"],
           "interessanter",
           "حتی صفت بلند هم -er می‌گیرد.", concept=C_COMP),
        blank("Deze fiets is ___ dan die. (goedkoop)", "goedkoper",
              "goedkoop + er.", concept=C_COMP),
        blank("Hij is de ___ werknemer van het team. (jong)", "jongste",
              "jong + ste (بعد از -ng پسوند -ste می‌آید).", concept=C_COMP),
        fix("Dit is meer moeilijk dan gisteren.", "Dit is moeilijker dan gisteren.",
            "در هلندی -er، نه meer.", concept=C_COMP),
        fa2nl("«هلندی از انگلیسی سخت‌تر است.»", "Nederlands is moeilijker dan Engels.",
              "moeilijk + er + dan.", concept=C_COMP),
        transform("Deze auto is duur. → (تفضیلی + dan die)", "Deze auto is duurder dan die.",
                  "duur + der (بعد از -r حرف d اضافه می‌شود).", concept=C_COMP),
    ])

lesson(
    "a2-l14", "a2-bijvoeglijk", "A2",
    "Net zo groot als", "مقایسه‌ی برابر و نابرابر",
    [C_COMPARE],
    discover(
        ["Hij is groter dan ik.", "Hij is net zo groot als ik.",
         "Hij is even groot als ik."],
        "چه وقت dan می‌آید و چه وقت als؟",
        "با تفضیلی (groter) → dan. با برابری (net zo/even) → als. این دو را قاطی نکن."),
    rule("-er + dan · net zo / even + als",
         "نابرابر با dan، برابر با als. «zo … als» هم درست است.",
         "than / as … as"),
    pattern([("groter", "comp"), ("dan", "than"), ("ik", "ref"), ("|", "sep"),
             ("net zo groot", "equal"), ("als", "as"), ("ik", "ref")],
            "در گفتار روزمره گاهی «groter als» شنیده می‌شود، ولی رسماً غلط است."),
    [
        ex("Mijn broer is ouder dan ik.", "برادرم از من بزرگ‌تر است."),
        ex("Deze fiets is net zo duur als die.", "این دوچرخه به گرانی آن است."),
        ex("Het is vandaag even koud als gisteren.", "امروز به سردی دیروز است."),
        ex("Ik werk minder dan vorig jaar.", "کمتر از سال گذشته کار می‌کنم."),
        ex("Hij spreekt beter Nederlands dan ik.", "او از من بهتر هلندی حرف می‌زند."),
    ],
    [
        wrong("Hij is groter als ik.", "Hij is groter dan ik.",
              "بعد از تفضیلی همیشه dan می‌آید."),
        wrong("Het is net zo koud dan gisteren.", "Het is net zo koud als gisteren.",
              "با net zo همیشه als."),
    ],
    "در گفتگو درباره‌ی قیمت، سن، سختی و تجربه. اشتباه dan/als چیزی است که هلندی‌ها فوراً می‌شنوند (خودشان هم گاهی اشتباه می‌کنند!).",
    [
        pick2("Hij is ouder ___ ik.", ["dan", "als"], "dan",
              "بعد از تفضیلی (ouder) → dan.", concept=C_COMPARE),
        pick2("Het is net zo duur ___ vorig jaar.", ["als", "dan"], "als",
              "با net zo → als.", concept=C_COMPARE),
        mc("Deze cursus is ___ moeilijk als de vorige.", ["net zo", "meer", "moeilijker"],
           "net zo", "برای برابری net zo … als.", concept=C_COMPARE),
        blank("Amsterdam is groter ___ Utrecht.", "dan",
              "تفضیلی → dan.", concept=C_COMPARE),
        blank("Ik ben even oud ___ mijn collega.", "als",
              "even … als برای برابری.", concept=C_COMPARE),
        fix("Hij werkt harder als ik.", "Hij werkt harder dan ik.",
            "بعد از harder باید dan بیاید.", concept=C_COMPARE),
        fa2nl("«برادرم از من بزرگ‌تر است.»", "Mijn broer is ouder dan ik.",
              "ouder + dan.", concept=C_COMPARE),
        fa2nl("«امروز به سردی دیروز است.»", "Het is vandaag net zo koud als gisteren.", 
              "برابری با net zo … als.", alt=["Het is vandaag even koud als gisteren."], concept=C_COMPARE),
    ])

lesson(
    "a2-l15", "a2-teinf", "A2",
    "Ik voel me goed", "افعال انعکاسی",
    [C_REFL],
    discover(
        ["Ik voel me goed.", "Hij voelt zich niet lekker.", "We vergissen ons."],
        "بعد از فعل یک کلمه‌ی کوچک آمده. با ik چه شکلی دارد؟ با hij چطور؟",
        "me برای ik، je برای jij، zich برای hij/zij/zij(جمع)، ons برای wij. این کلمه بخشی از خود فعل است."),
    rule("me · je · zich · ons · je · zich",
         "بعضی فعل‌ها همیشه با این ضمیر می‌آیند: zich voelen، zich vergissen، zich haasten، zich aankleden.",
         "reflexive verbs"),
    pattern([("Ik", "subject"), ("voel", "verb"), ("me", "reflexive"), ("niet lekker", "rest")],
            "«Hoe voel je je?» — دو تا je: یکی فاعل، یکی انعکاسی."),
    [
        ex("Ik voel me niet lekker.", "حالم خوب نیست.", "پرکاربردترین جمله‌ی مریضی"),
        ex("Hoe voel je je vandaag?", "امروز چطوری؟"),
        ex("Hij vergist zich.", "او اشتباه می‌کند."),
        ex("We moeten ons haasten.", "باید عجله کنیم."),
        ex("Ik kleed me snel aan.", "سریع لباس می‌پوشم."),
    ],
    [
        wrong("Ik voel niet lekker.", "Ik voel me niet lekker.",
              "voelen در این معنی همیشه ضمیر انعکاسی می‌خواهد — بدون me جمله ناقص است."),
        wrong("Hij voelt hem niet lekker.", "Hij voelt zich niet lekker.",
              "برای سوم‌شخص zich می‌آید، نه hem."),
    ],
    "برای گفتن حالت جسمی و روحی: در مطب دکتر، وقتی مرخصی می‌گیری، در گفتگوی روزمره. «Ik voel me niet lekker» را حتماً باید بلد باشی.",
    [
        mc("Ik voel ___ vandaag beter.", ["me", "mij zich", "zich"], "me",
           "با ik ضمیر انعکاسی me است.", concept=C_REFL),
        mc("Hij voelt ___ niet lekker.", ["zich", "hem", "zijn"], "zich",
           "سوم‌شخص → zich.", concept=C_REFL),
        mc("We moeten ___ haasten.", ["ons", "onze", "zich"], "ons",
           "با wij ضمیر انعکاسی ons است.", concept=C_REFL),
        blank("Hoe voel je ___ vandaag?", "je",
              "با jij ضمیر انعکاسی je است.", concept=C_REFL),
        blank("Zij vergist ___ soms.", "zich",
              "سوم‌شخص → zich.", concept=C_REFL),
        fix("Ik voel niet lekker vandaag.", "Ik voel me niet lekker vandaag.",
            "بدون me جمله ناقص است.", concept=C_REFL),
        fa2nl("«حالم خوب نیست.»", "Ik voel me niet lekker.",
              "ik + voel + me.", concept=C_REFL),
        dialogue("— Hoe gaat het?", "— Niet zo goed, ik voel ___ ziek.",
                 ["me", "mij zich", "zich"], "me",
                 "با ik همیشه me.", concept=C_REFL),
    ])

lesson(
    "a2-l16", "a2-teinf", "A2",
    "Ik probeer te komen", "te + مصدر",
    [C_TE_INF],
    discover(
        ["Ik probeer te komen.", "Ik vergeet vaak te bellen.",
         "Hij begint te werken.", "maar: Ik kan komen."],
        "چرا در جمله‌ی آخر te نیامده؟",
        "بعد از فعل‌های وجهی (kunnen، willen، moeten، mogen، gaan) هیچ‌وقت te نمی‌آید. بعد از بقیه معمولاً می‌آید."),
    rule("te + infinitief — maar niet na kunnen/willen/moeten/mogen/gaan",
         "proberen، vergeten، beginnen، hopen، besluiten و beloven همه te می‌خواهند.",
         "to + infinitive"),
    pattern([("Ik", "subject"), ("probeer", "verb"), ("elke dag", "time"),
             ("Nederlands", "object"), ("te spreken", "te-inf")],
            "te + مصدر با هم آخر جمله می‌روند."),
    [
        ex("Ik probeer elke dag Nederlands te spreken.", "هر روز سعی می‌کنم هلندی حرف بزنم."),
        ex("Vergeet niet te tekenen.", "یادت نرود امضا کنی."),
        ex("Hij begint morgen te werken.", "فردا شروع به کار می‌کند."),
        ex("Ik hoop je snel te zien.", "امیدوارم زود ببینمت."),
        ex("We hebben besloten te verhuizen.", "تصمیم گرفتیم اسباب‌کشی کنیم."),
    ],
    [
        wrong("Ik probeer komen.", "Ik probeer te komen.",
              "بعد از proberen حتماً te لازم است."),
        wrong("Ik kan te komen.", "Ik kan komen.",
              "بعد از فعل وجهی te نمی‌آید."),
    ],
    "در ایمیل کاری و مکالمه‌ی رسمی خیلی زیاد است: «Ik probeer…»، «Ik hoop…»، «Vergeet niet…». تفاوتش با فعل وجهی را باید بلد باشی.",
    [
        pick2("Ik probeer ___ komen.", ["te", "—"], "te",
              "بعد از proberen حتماً te.", concept=C_TE_INF),
        pick2("Ik kan morgen ___ komen.", ["—", "te"], "—",
              "بعد از فعل وجهی te نمی‌آید.", concept=C_TE_INF),
        mc("Vergeet niet ___ bellen!", ["te", "om", "voor"], "te",
           "vergeten + te + مصدر.", concept=C_TE_INF),
        blank("Hij begint volgende week ___ werken.", "te",
              "beginnen + te.", concept=C_TE_INF),
        order("Ik hoop je snel te zien.",
              why="te + مصدر آخر جمله.", concept=C_TE_INF),
        fix("Ik probeer elke dag Nederlands spreken.",
            "Ik probeer elke dag Nederlands te spreken.",
            "بعد از proberen باید te بیاید.", concept=C_TE_INF),
        fix("Ik moet te werken vandaag.", "Ik moet vandaag werken.",
            "بعد از moeten هیچ te نمی‌آید.", concept=C_TE_INF),
        fa2nl("«سعی می‌کنم هر روز هلندی حرف بزنم.»",
              "Ik probeer elke dag Nederlands te spreken.",
              "proberen + te + مصدر در انتها.", concept=C_TE_INF),
    ])

lesson(
    "a2-l17", "a2-teinf", "A2",
    "Om … te: waarom doe je het?", "om … te برای هدف",
    [C_OM_TE],
    discover(
        ["Ik leer Nederlands om werk te vinden.",
         "Ik ga naar de winkel om brood te kopen."],
        "این جمله‌ها به چه سؤالی جواب می‌دهند؟",
        "به «چرا؟» — هدف را نشان می‌دهند. ساختارش: om + بقیه + te + مصدر."),
    rule("om + … + te + infinitief",
         "برای گفتن هدف. te و مصدر همیشه با هم و در انتها می‌آیند.",
         "in order to"),
    pattern([("Ik leer Nederlands", "main"), ("om", "om"), ("werk", "object"),
             ("te vinden", "te-inf")],
            "«om … te» جواب «waarom?» است — یکی از پرکاربردترین ساختارها در مصاحبه."),
    [
        ex("Ik leer Nederlands om hier te kunnen werken.", "هلندی یاد می‌گیرم تا بتوانم اینجا کار کنم."),
        ex("Ik bel je om een afspraak te maken.", "زنگ می‌زنم تا قرار بگذاریم."),
        ex("Hij spaart om een huis te kopen.", "پس‌انداز می‌کند تا خانه بخرد."),
        ex("We komen om te helpen.", "می‌آییم که کمک کنیم."),
        ex("Ik heb tijd nodig om na te denken.", "وقت لازم دارم تا فکر کنم."),
    ],
    [
        wrong("Ik leer Nederlands voor werk vinden.",
              "Ik leer Nederlands om werk te vinden.",
              "برای بیان هدف با فعل، om … te به کار می‌رود، نه voor."),
        wrong("Ik bel je om maken een afspraak.", "Ik bel je om een afspraak te maken.",
              "te + مصدر باید آخر بیایند."),
    ],
    "این جمله‌ی طلایی مصاحبه‌ی کاری است: «Ik solliciteer om mijn ervaring te gebruiken.» هر بار که دلیل یا هدفی توضیح می‌دهی به آن نیاز داری.",
    [
        mc("Ik leer Nederlands ___ werk te vinden.", ["om", "voor", "voor te"], "om",
           "هدف با om … te.", concept=C_OM_TE),
        pickorder("کدام درست است؟",
                  ["Ik bel je om een afspraak te maken.",
                   "Ik bel je om te maken een afspraak.",
                   "Ik bel je voor een afspraak maken."],
                  "Ik bel je om een afspraak te maken.",
                  "te + مصدر در انتها می‌آیند.", concept=C_OM_TE),
        order("Hij spaart om een huis te kopen.",
              why="om + مفعول + te + مصدر.", concept=C_OM_TE),
        blank("Ik ga naar de winkel ___ brood te kopen.", "om",
              "هدف → om.", concept=C_OM_TE),
        transform("Ik leer Nederlands. Ik wil hier werken. → (met «om … te»)",
                  "Ik leer Nederlands om hier te werken.",
                  "هدف در جمله‌ی دوم با om … te بیان می‌شود.", concept=C_OM_TE),
        fix("Ik werk hard voor geld verdienen.", "Ik werk hard om geld te verdienen.",
            "برای هدف با فعل: om … te.", concept=C_OM_TE),
        fa2nl("«زنگ می‌زنم تا قرار بگذارم.»", "Ik bel om een afspraak te maken.", 
              "om + مفعول + te + مصدر.", alt=["Ik bel je om een afspraak te maken."], concept=C_OM_TE),
        scenario("In een sollicitatiegesprek vragen ze waarom je Nederlands leert.",
                 "Wat zeg je?",
                 ["Ik leer Nederlands om hier te kunnen werken.",
                  "Ik leer Nederlands voor hier werken.",
                  "Ik leer Nederlands om hier werken."],
                 "Ik leer Nederlands om hier te kunnen werken.",
                 "om … te + مصدر؛ و kunnen قبل از مصدر پایانی می‌آید.", concept=C_OM_TE),
    ])

lesson(
    "a2-l18", "a2-toekomst", "A2",
    "Gaan en zullen", "آینده",
    [C_FUTURE],
    discover(
        ["Ik ga morgen naar de dokter.", "Ik ga volgend jaar verhuizen.",
         "Zullen we koffie drinken?", "Ik zal het morgen doen."],
        "کدام‌شان پیشنهاد است و کدام نقشه؟",
        "gaan برای نقشه‌ای که داری. zullen بیشتر برای پیشنهاد («Zullen we…?») و قول دادن."),
    rule("gaan = plan · zullen = voorstel of belofte · presens = vaak genoeg",
         "«Ik werk morgen» هم کاملاً درست است؛ هلندی برای آینده اغلب زمان حال به کار می‌برد.",
         "going to / will"),
    pattern([("Zullen we", "suggest"), ("vanavond", "time"), ("koffie", "object"),
             ("drinken?", "infinitive")],
            "«Zullen we…?» رایج‌ترین راه پیشنهاد دادن در هلندی است."),
    [
        ex("Ik ga volgende week op vakantie.", "هفته‌ی آینده به تعطیلات می‌روم."),
        ex("Zullen we samen lunchen?", "با هم ناهار بخوریم؟"),
        ex("Ik zal het morgen regelen.", "فردا ترتیبش را می‌دهم.", "قول دادن"),
        ex("De les begint morgen om negen uur.", "کلاس فردا ساعت نه شروع می‌شود.", "زمان حال برای برنامه‌ی ثابت"),
        ex("Wat ga je dit weekend doen?", "آخر هفته چه کار می‌کنی؟"),
    ],
    [
        wrong("Ik wil morgen naar de dokter gaan. (als je een plan bedoelt)",
              "Ik ga morgen naar de dokter.",
              "willen یعنی «می‌خواهم»؛ برای نقشه‌ی قطعی gaan طبیعی‌تر است."),
        wrong("Zullen wij koffie drinken gaan?", "Zullen we koffie drinken?",
              "بعد از zullen فقط یک مصدر لازم است."),
    ],
    "«Zullen we…?» را برای هر دعوت و پیشنهادی به کار می‌بری. و «Ik ga…» برای گفتن برنامه‌هایت — در هر گفتگوی روزمره‌ای لازم است.",
    [
        pick2("___ we vanavond samen eten?", ["Zullen", "Gaan"], "Zullen",
              "برای پیشنهاد از zullen استفاده می‌شود.", concept=C_FUTURE),
        pick2("Ik ___ volgende maand verhuizen.", ["ga", "zal"], "ga",
              "نقشه‌ی قطعی → gaan.", concept=C_FUTURE),
        mc("Wat ___ je dit weekend doen?", ["ga", "zal", "zult"], "ga",
           "برای پرسیدن برنامه gaan طبیعی‌ترین شکل است.", concept=C_FUTURE),
        blank("___ ik je even helpen?", "Zal",
              "«Zal ik…?» یعنی «می‌خواهی کمکت کنم؟» — پیشنهاد کمک.", concept=C_FUTURE),
        order("Ik ga volgende week op vakantie.",
              why="gaan جای دوم، بقیه بعدش.", concept=C_FUTURE),
        fa2nl("«با هم ناهار بخوریم؟»", "Zullen we samen lunchen?",
              "پیشنهاد با «Zullen we…?».", concept=C_FUTURE),
        fix("Ik zal morgen naar de dokter gaan wil.", "Ik ga morgen naar de dokter.",
            "برای نقشه‌ی ساده gaan کافی است.", concept=C_FUTURE),
        scenario("Je collega ziet er gestrest uit en je wilt helpen.",
                 "Wat zeg je?",
                 ["Zal ik je even helpen?", "Ga ik je even helpen?", "Wil ik je even helpen?"],
                 "Zal ik je even helpen?",
                 "«Zal ik…?» شکل استاندارد پیشنهاد کمک است.", concept=C_FUTURE),
    ])

lesson(
    "a2-l19", "a2-er", "A2",
    "Er is, er zijn", "er: وجود داشتن",
    [C_ER_EXIST],
    discover(
        ["Er is een probleem.", "Er zijn veel mensen.",
         "Er staat een auto voor de deur."],
        "این جمله‌ها با چه چیزی شروع می‌شوند؟ آیا er معنی خاصی دارد؟",
        "er تقریباً هیچ معنی‌ای ندارد — فقط جای فاعل را پر می‌کند تا جمله شکل درست بگیرد. مثل «there is» انگلیسی."),
    rule("er + werkwoord = «hier bestaat / is»",
         "وقتی چیزی نامعیّن (een، veel، twee…) وجود دارد، جمله با er شروع می‌شود.",
         "there is / there are"),
    pattern([("Er", "er"), ("is", "verb"), ("een probleem", "indefinite")],
            "فعل با اسم مطابقت می‌کند: Er is een… / Er zijn veel…"),
    [
        ex("Er is een probleem met de trein.", "قطار مشکلی دارد."),
        ex("Er zijn veel mensen op straat.", "آدم‌های زیادی توی خیابان‌اند."),
        ex("Er staat iemand voor de deur.", "کسی جلوی در ایستاده."),
        ex("Er is geen brood meer.", "دیگر نان نمانده."),
        ex("Is er nog koffie?", "هنوز قهوه هست؟"),
        ex("Er wonen hier veel studenten.", "دانشجوهای زیادی اینجا زندگی می‌کنند."),
    ],
    [
        wrong("Is een probleem.", "Er is een probleem.",
              "جمله‌ی هلندی بدون فاعل نمی‌شود؛ er آن جای خالی را پر می‌کند."),
        wrong("Er is veel mensen.", "Er zijn veel mensen.",
              "فعل با اسم جمع مطابقت می‌کند: zijn."),
    ],
    "برای گزارش دادن هر وضعیتی: مشکل، صف، جای خالی، آدم پشت در. در محل کار و اداره خیلی می‌شنوی: «Er is een vergadering.»",
    [
        mc("___ is een probleem.", ["Er", "Het", "Dat"], "Er",
           "برای وجود داشتن چیزی نامعیّن، جمله با er شروع می‌شود.", concept=C_ER_EXIST),
        pick2("Er ___ veel mensen op straat.", ["zijn", "is"], "zijn",
              "mensen جمع است → zijn.", concept=C_ER_EXIST),
        pick2("Er ___ nog koffie.", ["is", "zijn"], "is",
              "koffie مفرد است → is.", concept=C_ER_EXIST),
        blank("___ staat iemand voor de deur.", "Er",
              "برای «کسی هست» جمله با er شروع می‌شود.", concept=C_ER_EXIST),
        order("Er is geen brood meer.",
              why="er + فعل + بقیه.", concept=C_ER_EXIST),
        fix("Is een vergadering vanmiddag.", "Er is vanmiddag een vergadering.",
            "بدون er جمله فاعل ندارد.", concept=C_ER_EXIST),
        fa2nl("«آدم‌های زیادی اینجا کار می‌کنند.»", "Er werken hier veel mensen.",
              "er + فعل + بقیه؛ فعل با جمع مطابقت می‌کند.", concept=C_ER_EXIST),
        dialogue("— Is ___ nog thee?", "— Ja, in de keuken.",
                 ["er", "het", "dat"], "er",
                 "در سؤال هم er لازم است: «Is er nog…?»", concept=C_ER_EXIST),
    ])

lesson(
    "a2-l20", "a2-er", "A2",
    "Ik heb er drie", "er همراه عدد",
    [C_ER_COUNT],
    discover(
        ["— Hoeveel kinderen heb je?  — Ik heb er twee.",
         "— Wil je een koekje?  — Ik heb er al één gehad."],
        "چرا «kinderen» تکرار نشده؟ و چرا فقط عدد کافی نیست؟",
        "er جای اسمِ حذف‌شده را می‌گیرد. در هلندی نمی‌شود فقط «Ik heb twee» گفت."),
    rule("getal zonder zelfstandig naamwoord → er verplicht",
         "هر وقت عدد می‌گویی ولی اسم را تکرار نمی‌کنی، er لازم است.",
         "I have three (of them)"),
    pattern([("Ik", "subject"), ("heb", "verb"), ("er", "er"), ("twee", "number")],
            "این er همان er «وجود داشتن» نیست — این یکی جانشین اسم است."),
    [
        ex("— Hoeveel broers heb je?  — Ik heb er drie.", "— چند تا برادر داری؟ — سه تا دارم."),
        ex("Ik heb er geen zin in.", "حالش را ندارم.", "عبارت ثابت"),
        ex("Er zijn er nog twee over.", "دو تا دیگر مانده."),
        ex("Ik neem er één.", "یکی برمی‌دارم."),
        ex("Hij heeft er veel van.", "خیلی از آن دارد."),
    ],
    [
        wrong("Ik heb twee.", "Ik heb er twee.",
              "این پرتکرارترین اشتباه در جواب دادن به «hoeveel?» است — er حذف‌شدنی نیست."),
        wrong("Ik neem één.", "Ik neem er één.",
              "بدون اسم، عدد باید er همراه داشته باشد."),
    ],
    "هر بار که کسی می‌پرسد «چند تا؟» و تو نمی‌خواهی اسم را تکرار کنی — یعنی در مغازه، در گفتگو، همه‌جا.",
    [
        mc("— Hoeveel kinderen heb je?  — Ik heb ___ twee.", ["er", "het", "die"], "er",
           "بدون تکرار اسم، er لازم است.", concept=C_ER_COUNT),
        pickorder("کدام درست است؟",
                  ["Ik heb er drie.", "Ik heb drie.", "Ik drie heb er."],
                  "Ik heb er drie.",
                  "er قبل از عدد می‌آید.", concept=C_ER_COUNT),
        blank("— Wil je koekjes?  — Ik neem ___ twee.", "er",
              "er جانشین «koekjes» است.", concept=C_ER_COUNT),
        order("Ik heb er nog twee.",
              why="فاعل + فعل + er + عدد.", concept=C_ER_COUNT),
        fix("Ik heb drie.", "Ik heb er drie.",
            "بدون اسم، عدد به er نیاز دارد.", concept=C_ER_COUNT),
        fa2nl("«سه تا دارم.» (جواب به «چند تا برادر داری؟»)", "Ik heb er drie.",
              "er + عدد.", concept=C_ER_COUNT),
        dialogue("— Hoeveel talen spreek je?", "— Ik spreek ___ drie.",
                 ["er", "het", "die"], "er",
                 "اسم (talen) تکرار نمی‌شود، پس er لازم است.", concept=C_ER_COUNT),
        scenario("In de winkel vraagt de verkoper hoeveel broodjes je wilt.",
                 "Wat zeg je?", ["Ik neem er twee.", "Ik neem twee.", "Ik twee neem."],
                 "Ik neem er twee.",
                 "با عدد و بدون اسم همیشه er.", concept=C_ER_COUNT),
    ])

# ----------------------------------------------------------------- modules

module("a2-bijvoeglijk", "A2", "Bijvoeglijke naamwoorden", "صفت‌ها",
       "چیزها را توصیف و مقایسه کنی: پایان -e، تفضیلی و عالی، و dan/als.",
       ["a2-l12", "a2-l13", "a2-l14"], icon="star")

module("a2-teinf", "A2", "Wederkerend en te + infinitief", "انعکاسی و te + مصدر",
       "بگویی چه حسی داری، و با te و om … te جمله‌های هدفمند بسازی.",
       ["a2-l15", "a2-l16", "a2-l17"], icon="target")

module("a2-toekomst", "A2", "De toekomst", "آینده",
       "برنامه بگویی و پیشنهاد بدهی با gaan و zullen.",
       ["a2-l18"], icon="arrow")

module("a2-er", "A2", "Het woordje er", "کلمه‌ی er",
       "کوچک‌ترین و پرکاربردترین کلمه‌ی هلندی که در فارسی معادلی ندارد.",
       ["a2-l19", "a2-l20"], icon="spark")
