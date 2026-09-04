"""A1, deel 1 — woordvolgorde, werkwoorden, naamwoorden, ontkennen."""

from _kit import (concept, lesson, module, ex, wrong, pattern, discover, rule,
                  mc, dehet, nietgeen, pickorder, pick2, dialogue, scenario,
                  blank, conjugate, transform, fa2nl, fix, type_all,
                  order, question)

# ---------------------------------------------------------------- concepts

C_V2 = concept(
    "order-v2", "Werkwoord op plaats twee", "فعل در جایگاه دوم", "A1",
    keywords=["woordvolgorde", "v2", "hoofdzin", "word order", "ترتیب کلمات"],
    summary_fa="در جمله‌ی خبری، فعلِ صرف‌شده همیشه دومین بخش جمله است.")

C_INV = concept(
    "order-inversion", "Inversie", "وارونگی (جابه‌جایی فاعل و فعل)", "A1",
    keywords=["inversie", "morgen ga ik", "inversion", "وارونگی"],
    summary_fa="اگر جمله با چیزی جز فاعل شروع شود، فاعل می‌رود بعد از فعل.")

C_TMP = concept(
    "order-tmp", "Tijd – manier – plaats", "زمان – حالت – مکان", "A1",
    keywords=["tijd manier plaats", "tmp", "volgorde", "زمان مکان"],
    summary_fa="در هلندی اول زمان، بعد چگونگی، آخر مکان می‌آید.")

C_IRR_PRES = concept(
    "present-irregular", "Onregelmatige werkwoorden in het heden", "افعال بی‌قاعده در زمان حال", "A1",
    keywords=["gaan", "doen", "komen", "staan", "zien", "onregelmatig", "بی‌قاعده"],
    summary_fa="gaan، doen، komen، staan، zien — شکل‌هایشان را باید حفظ کرد.")

C_SPELL = concept(
    "present-spelling", "Spelling bij het vervoegen", "قواعد املایی در صرف فعل", "A1",
    keywords=["spelling", "schrijven schrijf", "lezen lees", "v f", "z s", "املا"],
    summary_fa="v→f، z→s، و مصوت بلند دوتایی می‌شود: schrijven → ik schrijf.")

C_DEHET_RULES = concept(
    "article-patterns", "Patronen bij de en het", "الگوهای de و het", "A1",
    keywords=["de het", "meervoud de", "verkleinwoord het", "lidwoord"],
    summary_fa="جمع همیشه de؛ کلمات کوچک‌شده همیشه het؛ بقیه الگوهای کمکی.")

C_PLURAL = concept(
    "noun-plural", "Meervoud", "جمع بستن اسم", "A1",
    keywords=["meervoud", "plural", "en", "s", "جمع"],
    summary_fa="اغلب -en، ولی بعد از هجای بی‌تأکید -s: tafels، meisjes.")

C_DIM = concept(
    "noun-diminutive", "Verkleinwoord", "اسم مصغر (کوچک‌شده)", "A1",
    keywords=["verkleinwoord", "je", "tje", "kje", "diminutive", "مصغر"],
    summary_fa="-je/-tje اضافه می‌شود و کلمه همیشه het می‌گیرد.")

C_NIET_GEEN = concept(
    "neg-niet-geen", "Niet of geen", "niet یا geen", "A1",
    keywords=["niet", "geen", "ontkenning", "negation", "منفی"],
    summary_fa="جلوی اسمِ نامعیّن geen، در بقیه‌ی موارد niet.")

C_NIET_POS = concept(
    "neg-niet-position", "De plaats van niet", "جای niet در جمله", "A1",
    keywords=["niet plaats", "positie niet", "woordvolgorde niet"],
    summary_fa="niet آخر جمله می‌آید، مگر قبل از صفت، حرف اضافه یا فعل دوم.")

# ----------------------------------------------------------------- lessons

lesson(
    "a1-l01", "a1-volgorde", "A1",
    "Het werkwoord staat op plaats twee", "فعل در جایگاه دوم",
    [C_V2],
    discover(
        ["Ik ga morgen naar Amsterdam.", "Morgen ga ik naar Amsterdam.",
         "Naar Amsterdam ga ik morgen."],
        "در هر سه جمله فعل ga چندمین بخش جمله است؟",
        "همیشه دومین. هر چیزی می‌تواند اول بیاید، ولی فعلِ صرف‌شده جای دوم را ول نمی‌کند."),
    rule("Het werkwoord staat altijd op plaats 2.",
         "در جمله‌ی خبری هلندی، فعل صرف‌شده همیشه دومین «بخش» جمله است. این مهم‌ترین قانون ترتیب کلمات در هلندی است.",
         "The verb is always the second element."),
    pattern([("1: Morgen", "slot"), ("2: ga", "verb"), ("ik", "subject"), ("naar huis", "rest")],
            "«بخش» یعنی یک واحد معنایی — «morgen» یک بخش است، «volgende week» هم یک بخش."),
    [
        ex("Ik werk vandaag thuis.", "امروز خانه کار می‌کنم."),
        ex("Vandaag werk ik thuis.", "امروز خانه کار می‌کنم.", "با تأکید روی «امروز»"),
        ex("Om acht uur begint de les.", "کلاس ساعت هشت شروع می‌شود."),
        ex("Volgende week ga ik op vakantie.", "هفته‌ی آینده به تعطیلات می‌روم."),
        ex("In Nederland regent het vaak.", "در هلند اغلب باران می‌بارد."),
    ],
    [
        wrong("Morgen ik ga naar Amsterdam.", "Morgen ga ik naar Amsterdam.",
              "این پرتکرارترین اشتباه فارسی‌زبان‌هاست. اگر جمله با «morgen» شروع شود، فاعل باید بعد از فعل بیاید."),
        wrong("Vandaag ik werk thuis.", "Vandaag werk ik thuis.",
              "جای دوم مالِ فعل است، نه فاعل."),
    ],
    "این قانون در هر جمله‌ای که می‌سازی کار می‌کند. هلندی‌ها خیلی دوست دارند جمله را با زمان یا مکان شروع کنند، پس بدون این قانون جمله‌هایت همیشه کمی غلط می‌مانند.",
    [
        pickorder("کدام جمله درست است؟",
                  ["Morgen ga ik werken.", "Morgen ik ga werken.", "Ik morgen ga werken."],
                  "Morgen ga ik werken.",
                  "morgen جای اول، فعل جای دوم، بعد فاعل.", concept=C_V2),
        pickorder("کدام جمله درست است؟",
                  ["Vandaag het is koud.", "Vandaag is het koud.", "Is vandaag het koud."],
                  "Vandaag is het koud.",
                  "بعد از vandaag باید فعل بیاید.", concept=C_V2),
        order("Morgen ga ik naar de dokter.",
              why="جای اول: morgen. جای دوم: ga. بعد فاعل.", concept=C_V2),
        order("Om zeven uur begint de film.",
              why="«Om zeven uur» یک بخش است، پس فعل بلافاصله بعد از آن می‌آید.", concept=C_V2),
        fix("Vandaag ik heb geen tijd.", "Vandaag heb ik geen tijd.",
            "فعل باید دومین بخش باشد: Vandaag heb ik…", concept=C_V2),
        fix("In Nederland het regent veel.", "In Nederland regent het veel.",
            "«In Nederland» جای اول را گرفته، پس فعل بلافاصله بعدش می‌آید.", concept=C_V2),
        fa2nl("«فردا به آمستردام می‌روم.» (جمله را با «فردا» شروع کن)",
              "Morgen ga ik naar Amsterdam.",
              "با شروع از morgen، ترتیب می‌شود: morgen + ga + ik.", concept=C_V2),
        transform("Ik ga vanavond sporten. → (جمله را با vanavond شروع کن)",
                  "Vanavond ga ik sporten.",
                  "چیزی که اول می‌آید عوض می‌شود، ولی فعل سر جای دوم می‌ماند.", concept=C_V2),
    ])

lesson(
    "a1-l02", "a1-volgorde", "A1",
    "Inversie: de zin begint anders", "وارونگی",
    [C_INV, C_V2],
    discover(
        ["Ik drink 's ochtends koffie.", "'s Ochtends drink ik koffie.",
         "Koffie drink ik 's ochtends."],
        "وقتی جمله با چیزی جز ik شروع می‌شود، ik کجا می‌رود؟",
        "بلافاصله بعد از فعل. به این جابه‌جایی می‌گویند inversie."),
    rule("iets anders + werkwoord + onderwerp",
         "هر وقت جای اول را چیزی غیر از فاعل بگیرد، فاعل می‌پرد بعد از فعل.",
         "Then comes the verb, then the subject."),
    pattern([("'s Ochtends", "slot"), ("drink", "verb"), ("ik", "subject"), ("koffie", "rest")],
            "فاعل حذف نمی‌شود — فقط جابه‌جا می‌شود."),
    [
        ex("Daarom ben ik hier.", "برای همین اینجا هستم."),
        ex("Gelukkig heeft hij het gevonden.", "خوشبختانه پیدایش کرد."),
        ex("Na het werk ga ik sporten.", "بعد از کار ورزش می‌کنم."),
        ex("Dan bel ik je morgen.", "پس فردا بهت زنگ می‌زنم."),
        ex("Hier woon ik al vijf jaar.", "پنج سال است اینجا زندگی می‌کنم."),
    ],
    [
        wrong("Daarom ik ben hier.", "Daarom ben ik hier.",
              "بعد از daarom فعل می‌آید، بعد فاعل."),
        wrong("Dan ik bel je.", "Dan bel ik je.",
              "dan جای اول را گرفته، پس فاعل بعد از فعل می‌آید."),
    ],
    "کلماتی مثل dan، daarom، dus، toen، gelukkig و هر عبارت زمانی، جمله را شروع می‌کنند و بلافاصله inversie می‌آورند. بدون این، هلندی‌ات همیشه «ترجمه‌شده» به نظر می‌رسد.",
    [
        mc("Daarom ___ ik naar de cursus.", ["ga", "ik ga", "gaan"], "ga",
           "بعد از daarom مستقیم فعل می‌آید.", concept=C_INV),
        mc("Vanavond ___ we thuis.", ["blijven", "we blijven", "blijft"], "blijven",
           "فعل جای دوم؛ فاعل we جمع است پس blijven.", concept=C_INV),
        pickorder("کدام درست است؟",
                  ["Dan bel ik je terug.", "Dan ik bel je terug.", "Bel dan ik je terug."],
                  "Dan bel ik je terug.",
                  "dan + فعل + فاعل.", concept=C_INV),
        order("Na het werk ga ik naar huis.",
              why="«Na het werk» یک بخش است → بعدش فعل، بعد فاعل.", concept=C_INV),
        order("Hier werk ik sinds januari.",
              why="hier جای اول، werk جای دوم، بعد ik.", concept=C_INV),
        transform("Ik ga daarom eerder weg. → (با daarom شروع کن)",
                  "Daarom ga ik eerder weg.",
                  "daarom اول، فعل دوم، فاعل سوم.", concept=C_INV),
        fix("Gisteren ik was ziek.", "Gisteren was ik ziek.",
            "بعد از gisteren باید فعل بیاید.", concept=C_INV),
        fa2nl("«بعد از کار ورزش می‌کنم.» (جمله را با «بعد از کار» شروع کن)",
              "Na het werk ga ik sporten.",
              "عبارت زمانی اول، فعل دوم، فاعل بعدش.", concept=C_INV),
        dialogue("— Wanneer heb je tijd?",
                 "— ___ heb ik tijd.", ["Morgen", "Ik morgen", "Morgen ik"], "Morgen",
                 "morgen جای اول را می‌گیرد و فعل بلافاصله بعدش می‌آید.", concept=C_INV),
    ])

lesson(
    "a1-l03", "a1-volgorde", "A1",
    "Tijd, manier, plaats", "زمان، حالت، مکان",
    [C_TMP],
    discover(
        ["Ik ga morgen met de trein naar Utrecht.",
         "Wij fietsen elke dag rustig naar school."],
        "سه بخش «کِی»، «چطور» و «کجا» به چه ترتیبی آمده‌اند؟",
        "اول زمان، بعد حالت، آخر مکان. برعکس فارسی که معمولاً مکان را زودتر می‌گوییم."),
    rule("Tijd → Manier → Plaats",
         "کِی؟ چطور؟ کجا؟ — همیشه به همین ترتیب. (به اختصار: TMP)",
         "time – manner – place"),
    pattern([("Ik ga", "verb"), ("morgen", "time"), ("met de trein", "manner"), ("naar Utrecht", "place")],
            "اگر یکی از سه‌تا نبود، بقیه ترتیبشان را حفظ می‌کنند."),
    [
        ex("Ik ga morgen met de auto naar mijn werk.", "فردا با ماشین می‌روم سر کار."),
        ex("Zij fietst elke ochtend snel naar school.", "او هر صبح تند تا مدرسه دوچرخه می‌راند."),
        ex("We eten vanavond gezellig bij mijn ouders.", "امشب دورهمی خانه‌ی پدر و مادرم شام می‌خوریم."),
        ex("Hij werkt sinds maart fulltime in Rotterdam.", "او از مارس تمام‌وقت در روتردام کار می‌کند."),
    ],
    [
        wrong("Ik ga naar Utrecht morgen.", "Ik ga morgen naar Utrecht.",
              "زمان قبل از مکان می‌آید — این در فارسی برعکس است، برای همین راحت اشتباه می‌شود."),
        wrong("Ik ga met de trein morgen.", "Ik ga morgen met de trein.",
              "زمان قبل از «چطور» می‌آید."),
    ],
    "هر بار که می‌گویی کجا می‌روی و کِی و چطور — یعنی تقریباً هر روز. اگر ترتیب را رعایت کنی، جمله‌ات فوراً هلندی‌تر می‌شود.",
    [
        pickorder("کدام ترتیب درست است؟",
                  ["Ik ga morgen naar Amsterdam.", "Ik ga naar Amsterdam morgen."],
                  "Ik ga morgen naar Amsterdam.",
                  "زمان (morgen) قبل از مکان می‌آید.", concept=C_TMP),
        pickorder("کدام ترتیب درست است؟",
                  ["Hij fietst elke dag naar zijn werk.", "Hij fietst naar zijn werk elke dag."],
                  "Hij fietst elke dag naar zijn werk.",
                  "اول زمان، بعد مکان.", concept=C_TMP),
        order("Ik ga vanavond met de bus naar de stad.",
              why="زمان (vanavond) → حالت (met de bus) → مکان (naar de stad).", concept=C_TMP),
        order("We werken morgen rustig thuis.",
              why="زمان، بعد چگونگی، آخر مکان.", concept=C_TMP),
        fix("Ik ga naar de dokter morgen.", "Ik ga morgen naar de dokter.",
            "زمان باید قبل از مکان بیاید.", concept=C_TMP),
        fix("Zij gaat met de fiets elke dag naar school.",
            "Zij gaat elke dag met de fiets naar school.",
            "زمان (elke dag) قبل از «چطور» می‌آید.", concept=C_TMP),
        fa2nl("«فردا با قطار به لاهه می‌روم.»", "Ik ga morgen met de trein naar Den Haag.",
              "TMP: morgen → met de trein → naar Den Haag.", concept=C_TMP),
        blank("Ik werk ___ in Delft. (elke dinsdag)", "elke dinsdag",
              "زمان قبل از مکان می‌آید، و اینجا مکان (in Delft) از قبل در جمله است.",
              concept=C_TMP),
    ])

lesson(
    "a1-l04", "a1-werkwoorden", "A1",
    "Onregelmatig: gaan, doen, komen, staan", "افعال بی‌قاعده‌ی پرکاربرد",
    [C_IRR_PRES],
    discover(
        ["ik ga · jij gaat · wij gaan", "ik doe · jij doet · wij doen",
         "ik kom · jij komt · wij komen"],
        "کدام‌شان از قانون «ریشه + t» پیروی می‌کنند و کدام نه؟",
        "شکل jij و hij همیشه t دارد، ولی ریشه‌ی ik غیرمنتظره است: ga، doe، kom. این‌ها را باید حفظ کرد."),
    rule("ga / gaat / gaan · doe / doet / doen · kom / komt / komen",
         "این فعل‌ها کوتاه و پرکاربردند و ریشه‌شان با مصدر فرق دارد.",
         "go / do / come"),
    pattern([("ik", "subject"), ("ga", "verb"), ("|", "sep"), ("jij, hij", "subject"),
             ("gaat", "verb"), ("|", "sep"), ("wij", "subject"), ("gaan", "verb")],
            "همان سه ستون همیشگی، فقط ریشه غیرعادی است."),
    [
        ex("Ik ga naar huis.", "می‌روم خانه."),
        ex("Hoe gaat het met je?", "حالت چطور است؟"),
        ex("Wat doe je in het weekend?", "آخر هفته چه کار می‌کنی؟"),
        ex("Hij komt uit Marokko.", "او اهل مراکش است."),
        ex("De kopjes staan in de kast.", "فنجان‌ها توی کابینت‌اند."),
        ex("Ik zie je morgen!", "فردا می‌بینمت!"),
    ],
    [
        wrong("Ik gaan naar huis.", "Ik ga naar huis.",
              "با ik شکل کوتاه ga می‌آید."),
        wrong("Hij komt van Iran.", "Hij komt uit Iran.",
              "برای «اهل کجا بودن» هلندی uit به کار می‌برد، نه van."),
    ],
    "این پنج فعل در هر مکالمه‌ای هستند: رفتن، کردن، آمدن، ایستادن/بودنِ چیزها و دیدن. بدون آن‌ها حتی یک روز هم نمی‌شود گذراند.",
    [
        conjugate("ik (gaan) → ik ___", "ga",
                  "ریشه‌ی gaan می‌شود ga.", concept=C_IRR_PRES),
        conjugate("jij (doen) → jij ___", "doet",
                  "ریشه doe + t.", concept=C_IRR_PRES),
        conjugate("hij (komen) → hij ___", "komt",
                  "ریشه kom + t.", concept=C_IRR_PRES),
        mc("Hoe ___ het met u?", ["gaat", "gaan", "ga"], "gaat",
           "het سوم‌شخص مفرد است → gaat.", concept=C_IRR_PRES),
        mc("Wij ___ vanavond naar de bioscoop.", ["gaan", "gaat", "ga"], "gaan",
           "wij جمع → شکل پایه.", concept=C_IRR_PRES),
        blank("Waar ___ jij vandaan? (komen)", "kom",
              "بعد از فعل وقتی jij بیاید، t می‌افتد: kom jij.", concept=C_IRR_PRES),
        fix("Ik gaat naar de winkel.", "Ik ga naar de winkel.",
            "t فقط برای jij/hij است.", concept=C_IRR_PRES),
        fa2nl("«آخر هفته چه کار می‌کنی؟»", "Wat doe je in het weekend?",
              "بعد از وارونگی، doe je (بدون t).", concept=C_IRR_PRES),
        dialogue("— Waar kom je vandaan?", "— Ik ___ uit Iran.",
                 ["kom", "komt", "komen"], "kom",
                 "با ik شکل kom.", concept=C_IRR_PRES),
    ])

lesson(
    "a1-l05", "a1-werkwoorden", "A1",
    "Spelling bij het vervoegen", "قواعد املایی در صرف فعل",
    [C_SPELL],
    discover(
        ["schrijven → ik schrijf", "lezen → ik lees", "wonen → ik woon", "zitten → ik zit"],
        "هنگام ساختن ریشه، چه چیزهایی در املا عوض شد؟",
        "v به f و z به s تبدیل شد؛ مصوت بلند دوتایی نوشته شد؛ و همخوان دوتایی تک شد. هدف: صدا نباید عوض شود."),
    rule("v → f · z → s · lange klank dubbel · dubbele medeklinker enkel",
         "املا عوض می‌شود تا تلفّظ ثابت بماند: leven → ik leef، lezen → ik lees، zitten → ik zit.",
         "spelling keeps the sound the same"),
    pattern([("schrijven", "inf"), ("−en", "op"), ("schrijv", "stem"), ("→", "arrow"), ("schrijf", "result")],
            "آخر کلمه در هلندی هیچ‌وقت v یا z نمی‌ماند."),
    [
        ex("Ik schrijf een e-mail.", "یک ایمیل می‌نویسم."),
        ex("Ik lees de krant.", "روزنامه می‌خوانم."),
        ex("Hij leeft nog.", "او هنوز زنده است."),
        ex("Ik zit in de trein.", "توی قطارم."),
        ex("Zij belt haar moeder.", "به مادرش زنگ می‌زند."),
    ],
    [
        wrong("Ik schrijv een brief.", "Ik schrijf een brief.",
              "کلمه‌ی هلندی به v ختم نمی‌شود؛ v می‌شود f."),
        wrong("Ik leez de krant.", "Ik lees de krant.",
              "z آخر کلمه می‌شود s، و مصوت بلند دوتایی نوشته می‌شود."),
    ],
    "هر بار که یک فعل جدید یاد می‌گیری، همین دو سه قاعده تعیین می‌کنند چطور بنویسی‌اش. برای نوشتن ایمیل کاری و پر کردن فرم‌ها ضروری است.",
    [
        conjugate("ik (schrijven) → ik ___", "schrijf",
                  "v آخر کلمه به f تبدیل می‌شود.", concept=C_SPELL),
        conjugate("ik (lezen) → ik ___", "lees",
                  "z به s تبدیل می‌شود و ee دوتایی می‌ماند تا صدا بلند بماند.", concept=C_SPELL),
        conjugate("ik (zitten) → ik ___", "zit",
                  "همخوان دوتایی در پایان تک می‌شود.", concept=C_SPELL),
        conjugate("hij (leven) → hij ___", "leeft",
                  "ریشه leef + t.", concept=C_SPELL),
        mc("Ik ___ elke dag met mijn moeder. (bellen)", ["bel", "belt", "bell"], "bel",
           "ll در پایان تک می‌شود: bel.", concept=C_SPELL),
        mc("Zij ___ in Amsterdam. (wonen)", ["woont", "wont", "woond"], "woont",
           "ریشه woon (با دو o) + t.", concept=C_SPELL),
        fix("Ik werk en leev in Delft.", "Ik werk en leef in Delft.",
            "v پایانی همیشه f می‌شود.", concept=C_SPELL),
        blank("___ jij Nederlandse boeken? (lezen)", "Lees",
              "ریشه lees؛ در سؤال با jij، t نمی‌گیرد.", concept=C_SPELL),
        fa2nl("«هر روز یک ایمیل می‌نویسم.»", "Ik schrijf elke dag een e-mail.",
              "schrijven → ik schrijf.", concept=C_SPELL),
    ])

lesson(
    "a1-l06", "a1-naamwoorden", "A1",
    "Patronen bij de en het", "الگوهای de و het",
    [C_DEHET_RULES],
    discover(
        ["de tafel, de stoel, de man", "het boek, het huis, het meisje",
         "de tafels, de boeken, de huizen"],
        "به خط سوم نگاه کن: در جمع، حرف تعریف چه می‌شود؟",
        "در جمع همیشه de — بدون استثنا. این اولین قاعده‌ی مطمئنی است که می‌توانی به آن تکیه کنی."),
    rule("meervoud → altijd de · verkleinwoord → altijd het",
         "دو قاعده‌ی صددرصد مطمئن. برای بقیه، الگوها فقط کمک می‌کنند: آدم‌ها و شغل‌ها معمولاً de؛ کلمات با -ing و -heid همیشه de؛ زبان‌ها و رنگ‌ها het.",
         "plurals take de, diminutives take het"),
    pattern([("het huis", "single"), ("→", "arrow"), ("de huizen", "plural")],
            "همان کلمه در جمع de می‌گیرد."),
    [
        ex("De tafel is groot.", "میز بزرگ است."),
        ex("Het boek ligt daar.", "کتاب آنجاست."),
        ex("De boeken liggen daar.", "کتاب‌ها آنجایند.", "جمع → de"),
        ex("Het meisje speelt buiten.", "دخترک بیرون بازی می‌کند.", "کلمه‌ی کوچک‌شده → het"),
        ex("De vergadering begint om tien uur.", "جلسه ساعت ده شروع می‌شود.", "-ing → همیشه de"),
    ],
    [
        wrong("Het boeken liggen daar.", "De boeken liggen daar.",
              "در جمع همیشه de، حتی اگر مفردش het باشد."),
        wrong("De meisje speelt.", "Het meisje speelt.",
              "meisje کوچک‌شده است (-je)، پس het می‌گیرد — گرچه معنی‌اش «دختر» است."),
    ],
    "de/het را نمی‌شود کامل حدس زد، ولی این چند الگو حدود نیمی از کلمات را پوشش می‌دهد. بقیه را همیشه همراه با حرف تعریف حفظ کن.",
    [
        dehet("___ huizen", "de", "جمع همیشه de.", concept=C_DEHET_RULES),
        dehet("___ kopje", "het", "کلمه‌ی کوچک‌شده با -je همیشه het.", concept=C_DEHET_RULES),
        dehet("___ vergadering", "de", "کلمات با -ing همیشه de.", concept=C_DEHET_RULES),
        dehet("___ Nederlands", "het", "نام زبان‌ها het می‌گیرند.", concept=C_DEHET_RULES),
        mc("___ kinderen spelen buiten.", ["De", "Het", "Een"], "De",
           "kinderen جمع است → de.", concept=C_DEHET_RULES),
        mc("___ gezondheid is belangrijk.", ["De", "Het", "Een"], "De",
           "کلمات با -heid همیشه de.", concept=C_DEHET_RULES),
        fix("Het tafels staan buiten.", "De tafels staan buiten.",
            "جمع همیشه de می‌گیرد.", concept=C_DEHET_RULES),
        blank("___ meisje heet Nora.", "Het",
              "meisje با -je ساخته شده، پس het.", concept=C_DEHET_RULES),
        pick2("Ik zoek ___ oplossing.", ["de", "het"], "de",
              "کلمات با -ing جزو de هستند.", concept=C_DEHET_RULES),
    ])

lesson(
    "a1-l07", "a1-naamwoorden", "A1",
    "Meervoud: -en of -s", "جمع: en- یا s-",
    [C_PLURAL],
    discover(
        ["boek → boeken", "tafel → tafels", "huis → huizen", "auto → auto's"],
        "چه وقت -en می‌آید و چه وقت -s؟",
        "پیش‌فرض -en است. کلماتی که به هجای بی‌تأکید ختم می‌شوند (-el، -er، -je، -en) و کلمات خارجی -s می‌گیرند."),
    rule("meestal -en · na een onbeklemtoonde lettergreep -s",
         "boek → boeken، ولی tafel → tafels و meisje → meisjes. کلمات با مصوت پایانی آپاستروف می‌گیرند: auto's.",
         "-en is the default plural"),
    pattern([("boek", "single"), ("+ en", "op"), ("→", "arrow"), ("boeken", "plural"),
             ("|", "sep"), ("tafel", "single"), ("+ s", "op"), ("→", "arrow"), ("tafels", "plural")],
            "املا هم عوض می‌شود: huis → huizen، brief → brieven (s→z، f→v بین دو مصوت)."),
    [
        ex("Ik heb twee boeken gekocht.", "دو تا کتاب خریدم."),
        ex("De tafels staan in de kantine.", "میزها در سالن غذاخوری‌اند."),
        ex("We hebben drie kinderen.", "سه تا بچه داریم.", "kind → kinderen، بی‌قاعده"),
        ex("De huizen hier zijn duur.", "خانه‌های اینجا گران‌اند."),
        ex("Er staan twee auto's voor de deur.", "دو تا ماشین جلوی در است."),
    ],
    [
        wrong("Ik heb twee boek.", "Ik heb twee boeken.",
              "در فارسی بعد از عدد اسم مفرد می‌ماند («دو کتاب»)، ولی هلندی حتماً جمع می‌خواهد."),
        wrong("de tafelen", "de tafels",
              "کلماتی که به -el ختم می‌شوند -s می‌گیرند، نه -en."),
    ],
    "بعد از هر عدد، در هر لیستی و در هر جمله‌ای درباره‌ی چند چیز. اشتباه در جمع بلافاصله شنیده می‌شود.",
    [
        mc("Meervoud van «boek»?", ["boeken", "boeks", "boekes"], "boeken",
           "پیش‌فرض -en است.", concept=C_PLURAL),
        mc("Meervoud van «tafel»?", ["tafels", "tafelen", "tafeles"], "tafels",
           "بعد از هجای بی‌تأکید -el، پسوند -s می‌آید.", concept=C_PLURAL),
        mc("Meervoud van «kind»?", ["kinderen", "kinden", "kinds"], "kinderen",
           "kind یکی از چند کلمه‌ی بی‌قاعده است.", concept=C_PLURAL),
        blank("Ik heb drie ___ gekocht. (boek)", "boeken",
              "بعد از عدد حتماً جمع.", concept=C_PLURAL),
        blank("De ___ hier zijn duur. (huis)", "huizen",
              "huis → huizen: s بین دو مصوت z می‌شود.", concept=C_PLURAL),
        fix("Ik heb twee broer.", "Ik heb twee broers.",
            "بعد از عدد اسم باید جمع باشد.", concept=C_PLURAL),
        fa2nl("«ما سه تا بچه داریم.»", "We hebben drie kinderen.", 
              "kind → kinderen.", alt=["Wij hebben drie kinderen."], concept=C_PLURAL),
        pick2("Er staan twee ___ voor de deur.", ["auto's", "autos"], "auto's",
              "کلماتی که به مصوت ختم می‌شوند در جمع آپاستروف می‌گیرند.", concept=C_PLURAL),
    ])

lesson(
    "a1-l08", "a1-naamwoorden", "A1",
    "Verkleinwoorden: een kopje koffie", "اسم مصغر",
    [C_DIM, C_DEHET_RULES],
    discover(
        ["kop → kopje", "boek → boekje", "auto → autootje", "meisje, kwartiertje"],
        "چه چیزی به آخر کلمه‌ها اضافه شد؟ و حرف تعریف‌شان چه می‌شود؟",
        "پسوند -je (یا -tje/-pje). و هر کلمه‌ی کوچک‌شده het می‌گیرد، بدون استثنا."),
    rule("-je / -tje · altijd het",
         "کوچک‌شده فقط «کوچک» نیست: اغلب یعنی «کم»، «راحت» یا مؤدبانه‌تر.",
         "diminutive: -je, always het"),
    pattern([("een kop koffie", "single"), ("→", "arrow"), ("een kopje koffie", "dim")],
            "هلندی‌ها بسیار بیشتر از فارسی‌زبان‌ها از این شکل استفاده می‌کنند."),
    [
        ex("Wil je een kopje koffie?", "یک فنجان قهوه می‌خوری؟"),
        ex("Heb je even een momentje?", "یک لحظه وقت داری؟"),
        ex("Ik kom over een kwartiertje.", "یک ربعِ دیگر می‌آیم.", "«تقریباً یک ربع» — نرم‌تر و غیررسمی‌تر"),
        ex("Het meisje is drie jaar.", "دخترک سه ساله است."),
        ex("Zullen we een blokje om?", "یک دوری بزنیم؟", "عبارت روزمره برای «قدم زدن»"),
    ],
    [
        wrong("de kopje", "het kopje",
              "هر کلمه‌ی کوچک‌شده het می‌گیرد."),
        wrong("Ik wil een kop koffie, alsjeblieft.", "Ik wil graag een kopje koffie.",
              "«een kop koffie» غلط نیست ولی خشک است؛ هلندی‌ها تقریباً همیشه kopje می‌گویند."),
    ],
    "در کافه، در دفتر، در تعارف روزمره. با -je حرف زدنت فوراً دوستانه‌تر و طبیعی‌تر می‌شود — این یکی از راه‌های سریع «هلندی‌تر» شدن است.",
    [
        dehet("___ kopje", "het", "کوچک‌شده همیشه het.", concept=C_DIM),
        dehet("___ momentje", "het", "با -je همیشه het.", concept=C_DIM),
        mc("Verkleinwoord van «boek»?", ["boekje", "boekjes", "boekje's"], "boekje",
           "boek + je.", concept=C_DIM),
        mc("Verkleinwoord van «auto»?", ["autootje", "autoje", "autotje"], "autootje",
           "بعد از مصوت بلند، o تکرار می‌شود و -tje می‌آید.", concept=C_DIM),
        blank("Wil je een ___ koffie? (kop)", "kopje",
              "در تعارف کردن قهوه همیشه kopje.", concept=C_DIM),
        blank("Ik kom over een ___. (kwartier)", "kwartiertje",
              "بعد از -r معمولاً -tje می‌آید.", concept=C_DIM),
        fix("Heb je even een moment?", "Heb je even een momentje?",
            "در گفتار روزمره momentje طبیعی‌تر است.", concept=C_DIM),
        scenario("Je bent bij iemand op bezoek en wilt iets drinken aanbieden.",
                 "Wat zeg je?",
                 ["Wil je een kopje thee?", "Wil je een kop thee?", "Wil je thee kopje?"],
                 "Wil je een kopje thee?",
                 "در تعارف، شکل کوچک‌شده مؤدبانه‌تر و طبیعی‌تر است.", concept=C_DIM),
    ])

lesson(
    "a1-l09", "a1-ontkennen", "A1",
    "Niet of geen?", "niet یا geen؟",
    [C_NIET_GEEN],
    discover(
        ["Ik heb geen auto.", "Ik ken de auto niet.", "Ik werk niet."],
        "چرا در جمله‌ی اول geen آمده ولی در دومی niet؟",
        "geen فقط جلوی اسمِ بدون حرف تعریفِ معیّن می‌آید. اگر اسم de/het/mijn داشته باشد یا اصلاً اسمی در کار نباشد، niet می‌آید."),
    rule("geen bij een/geen lidwoord · anders niet",
         "een auto → geen auto. ولی de auto → de auto niet. فعل، صفت و قید همیشه با niet منفی می‌شوند.",
         "geen replaces a/an; otherwise niet"),
    pattern([("een boek", "noun"), ("→", "arrow"), ("geen boek", "neg"),
             ("|", "sep"), ("het boek", "noun"), ("→", "arrow"), ("het boek niet", "neg")],
            "سؤال کلیدی: آیا اسم حرف تعریفِ معیّن یا ضمیر ملکی دارد؟"),
    [
        ex("Ik heb geen tijd.", "وقت ندارم."),
        ex("Ik ken die man niet.", "آن مرد را نمی‌شناسم."),
        ex("Hij werkt niet.", "او کار نمی‌کند."),
        ex("Dat is geen probleem.", "مشکلی نیست."),
        ex("Ik vind het niet mooi.", "به نظرم قشنگ نیست."),
        ex("Zij heeft geen zin.", "حوصله ندارد.", "عبارت روزمره"),
    ],
    [
        wrong("Ik heb niet tijd.", "Ik heb geen tijd.",
              "tijd اسمی بدون حرف تعریف است → geen."),
        wrong("Ik ken geen die man.", "Ik ken die man niet.",
              "die یک اشاره‌گر معیّن است، پس باید niet بیاید و آخر جمله برود."),
    ],
    "این انتخاب هر روز پیش می‌آید و اشتباهش خیلی شنیده می‌شود. یک ترفند: اگر می‌توانی جای آن کلمه een بگذاری، پس geen درست است.",
    [
        nietgeen("Ik heb ___ geld.", "geen",
                 "geld اسم بدون حرف تعریف است → geen.", concept=C_NIET_GEEN),
        nietgeen("Ik ken de buurman ___.", "niet",
                 "de buurman معیّن است → niet.", concept=C_NIET_GEEN),
        nietgeen("Hij werkt hier ___.", "niet",
                 "اینجا اسمی منفی نمی‌شود، بلکه فعل → niet.", concept=C_NIET_GEEN),
        nietgeen("Dat is ___ probleem.", "geen",
                 "een probleem → geen probleem.", concept=C_NIET_GEEN),
        nietgeen("Ik vind dit boek ___ interessant.", "niet",
                 "صفت را با niet منفی می‌کنیم.", concept=C_NIET_GEEN),
        transform("Ik heb een fiets. → (منفی)", "Ik heb geen fiets.",
                  "een مستقیم geen می‌شود.", concept=C_NIET_GEEN),
        transform("Ik ken haar. → (منفی)", "Ik ken haar niet.",
                  "ضمیر مفعولی با niet منفی می‌شود و niet بعدش می‌آید.", concept=C_NIET_GEEN),
        fix("Ik heb niet kinderen.", "Ik heb geen kinderen.",
            "اسم بدون حرف تعریف → geen.", concept=C_NIET_GEEN),
        fa2nl("«حوصله ندارم.»", "Ik heb geen zin.",
              "zin اسم است → geen. عبارت ثابت روزمره.", concept=C_NIET_GEEN),
    ])

lesson(
    "a1-l10", "a1-ontkennen", "A1",
    "Waar staat niet?", "جای niet در جمله",
    [C_NIET_POS],
    discover(
        ["Ik werk vandaag niet.", "Ik ben niet moe.", "Hij gaat niet naar huis.",
         "Ik kan vandaag niet komen."],
        "niet کجا ایستاده؟ قبل از چه چیزهایی و بعد از چه چیزهایی؟",
        "niet آخر جمله می‌رود، مگر اینکه بعدش صفت، حرف اضافه یا فعل دوم باشد — آن‌وقت درست قبل از آن‌ها می‌آید."),
    rule("niet achteraan — behalve vóór een bijvoeglijk naamwoord, voorzetsel of tweede werkwoord",
         "پیش‌فرض: آخر جمله. استثناها: قبل از صفت (niet moe)، قبل از حرف اضافه (niet naar huis)، قبل از فعل دوم (niet komen).",
         "niet goes last, unless…"),
    pattern([("Ik", "subject"), ("kan", "verb"), ("vandaag", "time"), ("niet", "neg"), ("komen", "verb2")],
            "زمان قبل از niet می‌آید، مکان و فعل دوم بعدش."),
    [
        ex("Ik werk morgen niet.", "فردا کار نمی‌کنم."),
        ex("Zij is niet ziek.", "او مریض نیست."),
        ex("We gaan niet naar de les.", "به کلاس نمی‌رویم."),
        ex("Ik kan vanavond niet komen.", "امشب نمی‌توانم بیایم."),
        ex("Hij belt mij niet.", "او به من زنگ نمی‌زند."),
    ],
    [
        wrong("Ik niet werk morgen.", "Ik werk morgen niet.",
              "در فارسی «نمی‌» به فعل می‌چسبد، ولی در هلندی niet یک کلمه‌ی جداست و معمولاً آخر می‌آید."),
        wrong("Ik ben moe niet.", "Ik ben niet moe.",
              "قبل از صفت، niet جلو می‌آید."),
    ],
    "جای اشتباه niet جمله را عجیب می‌کند، حتی اگر بقیه‌اش درست باشد. این یکی از چیزهایی است که فرق بین A1 و A2 را نشان می‌دهد.",
    [
        pickorder("کدام درست است؟",
                  ["Ik werk vandaag niet.", "Ik niet werk vandaag.", "Niet ik werk vandaag."],
                  "Ik werk vandaag niet.",
                  "niet آخر جمله می‌آید.", concept=C_NIET_POS),
        pickorder("کدام درست است؟",
                  ["Zij is niet ziek.", "Zij is ziek niet.", "Zij niet is ziek."],
                  "Zij is niet ziek.",
                  "قبل از صفت، niet جلوتر می‌آید.", concept=C_NIET_POS),
        order("Wij gaan niet naar de bioscoop.",
              why="قبل از عبارت حرف اضافه‌ای، niet می‌آید.", concept=C_NIET_POS),
        order("Ik kan vanavond niet komen.",
              why="زمان، بعد niet، بعد فعل دوم.", concept=C_NIET_POS),
        transform("Ik werk morgen. → (منفی)", "Ik werk morgen niet.",
                  "niet آخر می‌رود.", concept=C_NIET_POS),
        transform("Hij is aardig. → (منفی)", "Hij is niet aardig.",
                  "صفت → niet قبلش.", concept=C_NIET_POS),
        fix("Ik ga naar huis niet.", "Ik ga niet naar huis.",
            "قبل از naar (حرف اضافه) niet می‌آید.", concept=C_NIET_POS),
        fa2nl("«امشب نمی‌توانم بیایم.»", "Ik kan vanavond niet komen.",
              "فعل دوم آخر می‌ماند و niet درست قبلش می‌آید.", concept=C_NIET_POS),
    ])

# ----------------------------------------------------------------- modules

module("a1-volgorde", "A1", "Woordvolgorde", "ترتیب کلمات",
       "مهم‌ترین قانون هلندی را مسلط شوی: فعل جای دوم، و وارونگی بعد از آن.",
       ["a1-l01", "a1-l02", "a1-l03"], icon="list")

module("a1-werkwoorden", "A1", "Werkwoorden verder", "فعل‌ها، عمیق‌تر",
       "فعل‌های بی‌قاعده‌ی پرکاربرد و قواعد املایی صرف فعل.",
       ["a1-l04", "a1-l05"], icon="spark")

module("a1-naamwoorden", "A1", "Zelfstandige naamwoorden", "اسم‌ها",
       "de/het، جمع بستن و اسم‌های کوچک‌شده — سه چیزی که هر اسم لازم دارد.",
       ["a1-l06", "a1-l07", "a1-l08"], icon="book")

module("a1-ontkennen", "A1", "Ontkennen", "منفی کردن",
       "بین niet و geen درست انتخاب کنی و niet را در جای درست بگذاری.",
       ["a1-l09", "a1-l10"], icon="x")
