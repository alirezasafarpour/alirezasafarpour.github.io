"""A0 — de eerste zinnen. Van nul tot je jezelf kunt voorstellen."""

from _kit import (concept, lesson, module, ex, wrong, pattern, discover, rule,
                  mc, dehet, nietgeen, pickorder, pick2, dialogue, scenario,
                  blank, conjugate, transform, fa2nl, fix, type_all,
                  order, question)

# ---------------------------------------------------------------- concepts

C_PRON_SUB = concept(
    "pron-subject", "Persoonlijk voornaamwoord (onderwerp)", "ضمیر فاعلی", "A0",
    keywords=["ik", "jij", "je", "u", "hij", "zij", "wij", "jullie", "pronoun", "ضمیر"],
    summary_fa="ik، jij، hij، zij، wij، jullie، ze — کسی که کار را انجام می‌دهد.")

C_ZIJN = concept(
    "verb-zijn", "Het werkwoord zijn", "فعل zijn (بودن)", "A0",
    keywords=["zijn", "ben", "bent", "is", "bent u", "بودن"],
    summary_fa="ik ben / jij bent / hij is / wij zijn — «هستم، هستی، است، هستیم».")

C_HEBBEN = concept(
    "verb-hebben", "Het werkwoord hebben", "فعل hebben (داشتن)", "A0",
    keywords=["hebben", "heb", "hebt", "heeft", "داشتن"],
    summary_fa="ik heb / jij hebt / hij heeft / wij hebben — «دارم، داری، دارد، داریم».")

C_ART_EEN = concept(
    "article-een", "Het lidwoord een", "حرف تعریف نکره een", "A0",
    keywords=["een", "a", "an", "نکره"],
    summary_fa="een = «یک»؛ وقتی چیزی برای اولین بار گفته می‌شود.")

C_ART_DEHET = concept(
    "article-dehet", "De of het", "de یا het", "A0",
    keywords=["de", "het", "lidwoord", "article", "حرف تعریف"],
    summary_fa="هر اسم هلندی یا de است یا het — باید با خودِ کلمه حفظ شود.")

C_GEEN = concept(
    "neg-geen-basic", "Geen bij een zelfstandig naamwoord", "منفی کردن با geen", "A0",
    keywords=["geen", "niet", "منفی"],
    summary_fa="جای een را geen می‌گیرد: een auto → geen auto.")

C_YESNO = concept(
    "q-yesno", "Ja/nee-vraag door omdraaien", "سؤال بله/خیر با جابه‌جایی", "A0",
    keywords=["vraag", "ja nee", "inversie", "سؤال"],
    summary_fa="فعل می‌آید اول: Je bent moe → Ben je moe?")

C_QWORD = concept(
    "q-words", "Vraagwoorden", "کلمات پرسشی", "A0",
    keywords=["wat", "wie", "waar", "hoe", "wanneer", "waarom", "vraagwoord"],
    summary_fa="wat، wie، waar، hoe، wanneer، waarom — بعدش فعل می‌آید.")

C_PRES_SG = concept(
    "present-singular", "Tegenwoordige tijd: ik, jij, hij", "زمان حال: مفرد", "A0",
    keywords=["tegenwoordige tijd", "present", "stam", "werk werkt", "زمان حال"],
    summary_fa="ik = ریشه، jij/hij = ریشه + t.")

C_PRES_PL = concept(
    "present-plural", "Tegenwoordige tijd: wij, jullie, zij", "زمان حال: جمع", "A0",
    keywords=["meervoud", "wij werken", "infinitief", "جمع"],
    summary_fa="جمع همیشه شکل کاملِ فعل است: wij/jullie/zij werken.")

# ----------------------------------------------------------------- lessons

lesson(
    "a0-l01", "a0-ik", "A0",
    "Ik ben, jij bent", "من هستم، تو هستی",
    [C_PRON_SUB, C_ZIJN],
    discover(
        ["Ik ben Sara.", "Jij bent Ali.", "Bent u meneer De Vries?"],
        "به فعل نگاه کن. با ik چه شکلی دارد؟ با jij چطور؟",
        "با ik می‌شود ben و با jij می‌شود bent. یعنی فعل با فاعل عوض می‌شود — دقیقاً مثل فارسی: «هستم / هستی»."),
    rule("ik ben · jij bent · u bent",
         "ik ben = هستم، jij bent = هستی. u هم bent می‌گیرد، ولی مؤدبانه است.",
         "I am / you are"),
    pattern([("Ik", "subject"), ("ben", "verb"), ("Sara", "rest")],
            "فاعل + فعل + بقیه. ساده‌ترین جمله‌ی هلندی همین است."),
    [
        ex("Ik ben Sara.", "من سارا هستم."),
        ex("Jij bent nieuw hier.", "تو اینجا جدید هستی."),
        ex("Ik ben moe.", "خسته‌ام."),
        ex("Bent u de docent?", "شما معلم هستید؟", "u = «شما»ی مؤدبانه"),
        ex("Je bent te laat.", "دیر کردی.", "je شکل بدون تأکید jij است"),
    ],
    [
        wrong("Ik ben moe zijn.", "Ik ben moe.",
              "در فارسی «خسته هستم» یک فعل دارد؛ در هلندی هم فقط ben کافی است. zijn را دوباره نگو."),
        wrong("Ik zijn Sara.", "Ik ben Sara.",
              "zijn شکل پایه (مصدر) است. با ik باید ben بگویی."),
    ],
    "این اولین جمله‌ای است که در هلند می‌سازی: اسمت، شغلت، حالت. در معرفی، کلاس، مغازه و مصاحبه‌ی کاری هر روز به کارش می‌بری.",
    [
        mc("Ik ___ Ali.", ["ben", "bent", "is"], "ben",
           "با ik همیشه ben. bent مالِ jij و u است.", concept=C_ZIJN),
        mc("Jij ___ aardig.", ["ben", "bent", "zijn"], "bent",
           "با jij فعل یک t می‌گیرد: bent.", concept=C_ZIJN),
        mc("___ u meneer Jansen?", ["Bent", "Ben", "Is"], "Bent",
           "u همیشه bent می‌گیرد، حتی وقتی به یک نفر می‌گویی.", concept=C_ZIJN),
        blank("Ik ___ Nederlander.", "ben",
              "فاعل ik است، پس ben.", concept=C_ZIJN),
        blank("___ bent te laat.", "Jij", 
              "فعل bent است، پس فاعل jij (یا je) است.", alt=["Je"], concept=C_PRON_SUB),
        order("Ik ben ziek vandaag.",
              why="ترتیب پایه: فاعل، بعد فعل، بعد بقیه.", concept=C_ZIJN),
        fa2nl("«من خسته هستم.»", "Ik ben moe.",
              "ik ben + صفت. کلمه‌ی اضافه لازم نیست.", concept=C_ZIJN),
        fa2nl("«تو معلم هستی.»", "Jij bent docent.", 
              "با شغل‌ها در هلندی معمولاً een نمی‌آید: Jij bent docent.", alt=["Je bent docent.", "Jij bent leraar.", "Je bent leraar."], concept=C_ZIJN),
        dialogue("— Hallo, ik ben Karim. En jij?",
                 "— Hoi, ___ Emma.", ["ik ben", "jij bent", "ben ik"], "ik ben",
                 "خودش را معرفی می‌کند، پس ik ben. «ben ik» فقط در سؤال می‌آید.",
                 concept=C_ZIJN),
    ])

lesson(
    "a0-l02", "a0-ik", "A0",
    "Hij is, zij is, het is", "او هست",
    [C_PRON_SUB, C_ZIJN],
    discover(
        ["Hij is mijn broer.", "Zij is mijn zus.", "Het is koud."],
        "سه فاعل مختلف، ولی فعل چه شکلی دارد؟",
        "هر سه is می‌گیرند. سوم‌شخص مفرد در هلندی خیلی راحت است: همیشه is."),
    rule("hij / zij / het + is",
         "برای «او» و برای چیزها فعل همیشه is است.",
         "he / she / it is"),
    pattern([("Hij", "subject"), ("is", "verb"), ("moe", "rest")],
            "hij (مرد)، zij (زن)، het (چیز یا هوا)."),
    [
        ex("Hij is mijn collega.", "او همکار من است."),
        ex("Zij is arts.", "او پزشک است."),
        ex("Het is warm vandaag.", "امروز هوا گرم است.", "برای هوا همیشه het"),
        ex("Ze is er niet.", "او اینجا نیست.", "ze شکل بدون تأکید zij است"),
        ex("Het is tien uur.", "ساعت ده است."),
    ],
    [
        wrong("Hij zijn moe.", "Hij is moe.",
              "با hij فقط is."),
        wrong("Is warm vandaag.", "Het is warm vandaag.",
              "در فارسی می‌گوییم «گرم است» بدون فاعل، ولی جمله‌ی هلندی همیشه فاعل می‌خواهد: het."),
    ],
    "برای حرف زدن درباره‌ی دیگران و درباره‌ی هوا، ساعت و قیمت‌ها. جمله‌های het is… را هلندی‌ها روزی چند بار می‌گویند.",
    [
        mc("Hij ___ mijn buurman.", ["is", "bent", "ben"], "is",
           "hij همیشه is می‌گیرد.", concept=C_ZIJN),
        mc("___ is koud buiten.", ["Het", "Hij", "Zij"], "Het",
           "برای هوا از het استفاده می‌شود.", concept=C_PRON_SUB),
        mc("Mijn zus? ___ is verpleegkundige.", ["Zij", "Hij", "Het"], "Zij",
           "zus (خواهر) مؤنث است، پس zij.", concept=C_PRON_SUB),
        blank("___ is mijn vader.", "Hij", 
              "برای یک مرد hij می‌گویی.", alt=["Dit", "Dat"], concept=C_PRON_SUB),
        blank("Het ___ half acht.", "is",
              "با het فعل is.", concept=C_ZIJN),
        fix("Hij ben ziek.", "Hij is ziek.",
            "ben فقط با ik می‌آید. با hij باید is بگویی.", concept=C_ZIJN),
        fa2nl("«هوا سرد است.»", "Het is koud.",
              "جمله‌های هوا با het شروع می‌شوند — نمی‌شود het را حذف کرد.", concept=C_PRON_SUB),
        order("Zij is mijn collega.",
              why="فاعل + is + بقیه.", concept=C_ZIJN),
        scenario("Iemand vraagt: «Hoe is het weer?»",
                 "Wat zeg je?", ["Het is mooi weer.", "Is mooi weer.", "Hij is mooi weer."],
                 "Het is mooi weer.",
                 "جمله‌ی هلندی بدون فاعل نمی‌شود؛ برای هوا het می‌آید.",
                 concept=C_PRON_SUB),
    ])

lesson(
    "a0-l03", "a0-ik", "A0",
    "Wij zijn, jullie zijn", "ما هستیم، شما هستید",
    [C_PRON_SUB, C_ZIJN],
    discover(
        ["Wij zijn cursisten.", "Jullie zijn te laat.", "Zij zijn op vakantie."],
        "این سه جمله جمع هستند. فعل در هر سه چه شکلی دارد؟",
        "همیشه zijn. در جمع، فعل همان شکل پایه است — این قانون برای تقریباً همه‌ی فعل‌های هلندی صادق است."),
    rule("wij / jullie / zij + zijn",
         "در جمع همیشه zijn. سه فاعل، یک شکل.",
         "we / you (pl.) / they are"),
    pattern([("Wij", "subject"), ("zijn", "verb"), ("cursisten", "rest")],
            "wij = ما، jullie = شما (چند نفر)، zij = آن‌ها."),
    [
        ex("Wij zijn cursisten.", "ما زبان‌آموز هستیم."),
        ex("Jullie zijn welkom.", "خوش آمدید (شما چند نفر)."),
        ex("Zij zijn er al.", "آن‌ها همین حالا اینجا هستند."),
        ex("We zijn klaar.", "ما آماده‌ایم.", "we شکل بدون تأکید wij است"),
        ex("Ze zijn thuis.", "آن‌ها خانه‌اند."),
    ],
    [
        wrong("Wij is klaar.", "Wij zijn klaar.",
              "is فقط برای یک نفر است. در جمع zijn."),
        wrong("Jullie bent te laat.", "Jullie zijn te laat.",
              "jullie جمع است، حتی وقتی مؤدبانه حرف می‌زنی؛ پس zijn، نه bent."),
    ],
    "وقتی درباره‌ی گروه خودت حرف می‌زنی: خانواده، همکارها، هم‌کلاسی‌ها. در محیط کار «we» را خیلی می‌شنوی.",
    [
        mc("Wij ___ collega's.", ["zijn", "is", "bent"], "zijn",
           "wij جمع است → zijn.", concept=C_ZIJN),
        mc("Jullie ___ vroeg vandaag.", ["zijn", "bent", "is"], "zijn",
           "jullie همیشه zijn می‌گیرد.", concept=C_ZIJN),
        pick2("Mijn ouders? ___ zijn in Turkije.",
              ["Zij", "Hij"], "Zij",
              "ouders (والدین) جمع است، پس zij.", concept=C_PRON_SUB),
        blank("___ zijn moe na het werk.", "Wij", 
              "فعل zijn است، پس فاعل باید جمع باشد.", alt=["We", "Zij", "Ze", "Jullie"], concept=C_PRON_SUB),
        conjugate("wij (zijn) → wij ___", "zijn",
                  "در جمع شکل فعل تغییر نمی‌کند.", concept=C_ZIJN),
        fix("We is bijna klaar.", "We zijn bijna klaar.",
            "we جمع است → zijn.", concept=C_ZIJN),
        fa2nl("«ما آماده‌ایم.»", "We zijn klaar.", 
              "wij/we + zijn + صفت.", alt=["Wij zijn klaar."], concept=C_ZIJN),
        order("Jullie zijn altijd te laat.",
              why="فاعل، فعل، بعد بقیه.", concept=C_ZIJN),
    ])

lesson(
    "a0-l04", "a0-hebben", "A0",
    "Hebben: ik heb, jij hebt", "داشتن",
    [C_HEBBEN],
    discover(
        ["Ik heb een vraag.", "Jij hebt tijd.", "Hij heeft een auto.", "Wij hebben honger."],
        "چهار شکل مختلف از یک فعل. کدام‌ها شبیه هم‌اند؟",
        "ik heb، jij hebt، hij heeft، و در جمع hebben. فقط سوم‌شخص مفرد (heeft) کمی غیرمنتظره است."),
    rule("ik heb · jij hebt · hij/zij heeft · wij hebben",
         "چهار شکل که باید حفظ شوند. heeft تنها شکل عجیب است.",
         "have / has"),
    pattern([("Ik", "subject"), ("heb", "verb"), ("een vraag", "object")],
            "hebben تقریباً همیشه یک مفعول دارد: چیزی که داری."),
    [
        ex("Ik heb een vraag.", "من یک سؤال دارم."),
        ex("Heb je even tijd?", "یک لحظه وقت داری؟"),
        ex("Zij heeft twee kinderen.", "او دو بچه دارد."),
        ex("We hebben honger.", "گرسنه‌ایم.", "hebben honger = گرسنه بودن"),
        ex("Ik heb het druk.", "سرم شلوغ است.", "عبارت ثابت و بسیار پرکاربرد"),
    ],
    [
        wrong("Ik ben honger.", "Ik heb honger.",
              "گرسنگی و تشنگی در هلندی «داشته» می‌شوند، نه «بودن»: heb honger، heb dorst."),
        wrong("Hij hebt een auto.", "Hij heeft een auto.",
              "با hij/zij/het شکل خاص heeft می‌آید."),
    ],
    "hebben بعد از zijn پرکاربردترین فعل هلندی است: وقت داشتن، سؤال داشتن، کار داشتن، بچه داشتن. بدون آن نمی‌شود روزمره حرف زد.",
    [
        mc("Ik ___ een vraag.", ["heb", "hebt", "heeft"], "heb",
           "با ik شکل heb.", concept=C_HEBBEN),
        mc("Zij ___ een nieuwe baan.", ["heeft", "hebt", "heb"], "heeft",
           "سوم‌شخص مفرد → heeft.", concept=C_HEBBEN),
        mc("Jullie ___ gelijk.", ["hebben", "heeft", "hebt"], "hebben",
           "jullie جمع است → hebben.", concept=C_HEBBEN),
        conjugate("hij (hebben) → hij ___", "heeft",
                  "hij همیشه heeft می‌گیرد، نه hebt.", concept=C_HEBBEN),
        blank("___ je even tijd?", "Heb",
              "در سؤال فعل اول می‌آید و با je شکل heb است (t می‌افتد).",
              concept=C_HEBBEN),
        fix("Ik ben dorst.", "Ik heb dorst.",
            "تشنگی را در هلندی «داری»، نه «هستی».", concept=C_HEBBEN),
        fa2nl("«ما گرسنه‌ایم.»", "We hebben honger.", 
              "honger با hebben می‌آید، نه با zijn.", alt=["Wij hebben honger."], concept=C_HEBBEN),
        order("Hij heeft twee kinderen.",
              why="فاعل + فعل + مفعول.", concept=C_HEBBEN),
        dialogue("— Kom je mee naar de kantine?",
                 "— Sorry, ik ___ het druk.", ["heb", "ben", "hebt"], "heb",
                 "«het druk hebben» یعنی سرت شلوغ است — با hebben.", concept=C_HEBBEN),
    ])

lesson(
    "a0-l05", "a0-hebben", "A0",
    "Een, de en het", "een، de و het",
    [C_ART_EEN, C_ART_DEHET],
    discover(
        ["Ik heb een auto. De auto is rood.", "Ik heb een huis. Het huis is groot."],
        "چرا بار اول een آمده و بار دوم de یا het؟",
        "een برای چیزی است که تازه معرفی می‌شود. وقتی طرف مقابل می‌داند از چه حرف می‌زنی، de یا het می‌آید."),
    rule("een = نامعلوم · de / het = معلوم",
         "اول een، بعد de یا het. اینکه اسم de است یا het را باید با خود کلمه حفظ کنی.",
         "a → the"),
    pattern([("een", "article"), ("auto", "noun"), ("→", "arrow"), ("de", "article"), ("auto", "noun")],
            "یک اسم یا de می‌گیرد یا het — هیچ قاعده‌ی صددرصدی ندارد، ولی الگوهایی هست."),
    [
        ex("Ik zoek een kamer.", "دنبال یک اتاق می‌گردم."),
        ex("De kamer is klein.", "اتاق کوچک است."),
        ex("Het boek ligt op tafel.", "کتاب روی میز است."),
        ex("Dat is een goede vraag.", "سؤال خوبی است."),
        ex("Waar is het toilet?", "دستشویی کجاست؟"),
    ],
    [
        wrong("Ik zoek kamer.", "Ik zoek een kamer.",
              "در فارسی می‌شود گفت «دنبال اتاق می‌گردم»، ولی هلندی جلوی اسم مفرد تقریباً همیشه یک حرف تعریف می‌خواهد."),
        wrong("Het auto is rood.", "De auto is rood.",
              "auto جزو کلمات de است. de/het را همیشه همراه خودِ کلمه یاد بگیر."),
    ],
    "هر بار که یک اسم می‌گویی این انتخاب را داری. اشتباه در de/het جمله را نامفهوم نمی‌کند، ولی خیلی زود لو می‌دهد که تازه‌کار هستی — برای همین از اول با خود کلمه حفظش کن.",
    [
        dehet("___ boek", "het", "boek جزو کلمات het است.", concept=C_ART_DEHET),
        dehet("___ tafel", "de", "tafel جزو کلمات de است.", concept=C_ART_DEHET),
        dehet("___ huis", "het", "huis با het می‌آید.", concept=C_ART_DEHET),
        dehet("___ man", "de", "آدم‌ها تقریباً همیشه de می‌گیرند: de man, de vrouw.", concept=C_ART_DEHET),
        mc("Ik heb ___ vraag.", ["een", "de", "het"], "een",
           "سؤال تازه مطرح می‌شود، پس een.", concept=C_ART_EEN),
        mc("Waar is ___ station?", ["het", "een", "de"], "het",
           "طرف می‌داند کدام ایستگاه را می‌گویی → het station.", concept=C_ART_DEHET),
        blank("Ik zoek ___ woning in Delft.", "een",
              "اولین بار که از آن حرف می‌زنی → een.", concept=C_ART_EEN),
        fix("Ik heb vraag.", "Ik heb een vraag.",
            "جلوی اسم مفرد در هلندی حرف تعریف لازم است.", concept=C_ART_EEN),
        fa2nl("«کتاب روی میز است.»", "Het boek ligt op tafel.",
              "boek با het می‌آید. «op tafel» عبارت ثابت است و بدون حرف تعریف می‌آید.",
              concept=C_ART_DEHET),
    ])

lesson(
    "a0-l06", "a0-hebben", "A0",
    "Geen: ik heb geen tijd", "منفی کردن با geen",
    [C_GEEN],
    discover(
        ["Ik heb een auto. → Ik heb geen auto.", "Ik heb tijd. → Ik heb geen tijd."],
        "چه اتفاقی برای een افتاد؟ و در جمله‌ی دوم که een نداشت چطور؟",
        "geen دقیقاً جای een را می‌گیرد. اگر اسم بدون حرف تعریف باشد، باز هم geen جلویش می‌آید."),
    rule("een → geen · هیچ حرف تعریفی → geen",
         "برای منفی کردن اسم‌ها از geen استفاده کن، نه از niet.",
         "no / not a / not any"),
    pattern([("Ik", "subject"), ("heb", "verb"), ("geen", "neg"), ("tijd", "object")],
            "geen مستقیم جلوی اسم می‌آید."),
    [
        ex("Ik heb geen tijd.", "وقت ندارم."),
        ex("We hebben geen suiker meer.", "دیگر شکر نداریم."),
        ex("Hij heeft geen werk.", "او کار ندارد."),
        ex("Ik heb geen idee.", "اصلاً نمی‌دانم.", "عبارت روزمره و بسیار پرکاربرد"),
        ex("Er is geen probleem.", "مشکلی نیست."),
    ],
    [
        wrong("Ik heb niet tijd.", "Ik heb geen tijd.",
              "جلوی اسم geen می‌آید، نه niet. این یکی از پرتکرارترین اشتباه‌های فارسی‌زبان‌هاست."),
        wrong("Ik heb geen de auto.", "Ik heb geen auto.",
              "geen خودش جای حرف تعریف را می‌گیرد؛ بعدش دیگر de/een نمی‌آید."),
    ],
    "هر بار که چیزی را نداری: وقت، پول، سؤال، مشکل. جمله‌ی «ik heb geen…» را در هلند روزی چند بار می‌شنوی.",
    [
        nietgeen("Ik heb ___ tijd.", "geen",
                 "tijd یک اسم است → geen.", concept=C_GEEN),
        nietgeen("Ik heb ___ auto.", "geen",
                 "جلوی اسم همیشه geen.", concept=C_GEEN),
        mc("Hij heeft ___ werk.", ["geen", "niet", "geen een"], "geen",
           "کار نداشتن: geen werk.", concept=C_GEEN),
        transform("Ik heb een fiets. → (منفی کن)", "Ik heb geen fiets.",
                  "een مستقیم به geen تبدیل می‌شود.", concept=C_GEEN),
        transform("We hebben suiker. → (منفی کن)", "We hebben geen suiker.",
                  "اسم بدون حرف تعریف هم با geen منفی می‌شود.", concept=C_GEEN),
        fix("Ik heb niet geld.", "Ik heb geen geld.",
            "geld اسم است، پس geen.", concept=C_GEEN),
        fa2nl("«وقت ندارم.»", "Ik heb geen tijd.",
              "منفی کردن اسم با geen.", concept=C_GEEN),
        order("Wij hebben geen problemen.",
              why="فاعل + فعل + geen + اسم.", concept=C_GEEN),
        dialogue("— Heb je een pen voor mij?",
                 "— Sorry, ik heb ___ pen.", ["geen", "niet", "geen een"], "geen",
                 "een pen → geen pen.", concept=C_GEEN),
    ])

lesson(
    "a0-l07", "a0-vragen", "A0",
    "Ben je…? Heb je…?", "سؤال بله/خیر",
    [C_YESNO],
    discover(
        ["Je bent moe. → Ben je moe?", "Je hebt tijd. → Heb je tijd?"],
        "برای ساختن سؤال چه چیزی جابه‌جا شد؟",
        "فعل و فاعل جای خود را عوض کردند. همین. کلمه‌ی اضافه‌ای مثل «آیا» لازم نیست."),
    rule("werkwoord + onderwerp + rest?",
         "برای سؤال بله/خیر فقط فعل را اول بیاور. jij بعد از فعل معمولاً je می‌شود و t فعل می‌افتد.",
         "Are you…? Do you have…?"),
    pattern([("Ben", "verb"), ("je", "subject"), ("moe", "rest"), ("?", "mark")],
            "فعل، بعد فاعل، بعد بقیه — دقیقاً برعکس جمله‌ی خبری."),
    [
        ex("Ben je klaar?", "آماده‌ای؟"),
        ex("Heb je even tijd?", "یک لحظه وقت داری؟"),
        ex("Is hij thuis?", "او خانه است؟"),
        ex("Werk je hier?", "اینجا کار می‌کنی؟"),
        ex("Bent u meneer Yilmaz?", "شما آقای ییلماز هستید؟"),
    ],
    [
        wrong("Jij bent moe?", "Ben je moe?",
              "فقط علامت سؤال کافی نیست؛ در هلندی باید فعل را اول بیاوری."),
        wrong("Heb jij tijd? → Hebt je tijd?", "Heb je tijd?",
              "وقتی je بعد از فعل بیاید، t حذف می‌شود: je hebt → heb je."),
    ],
    "در مغازه، پشت تلفن، سر کار: هر سؤال ساده‌ای با همین ساختار شروع می‌شود. اگر فقط لحن را بالا ببری، هلندی‌ها می‌فهمند ولی غیرطبیعی است.",
    [
        question("Ben je moe", tiles=["Ben", "je", "moe"],
                 why="در سؤال، فعل اول می‌آید.", concept=C_YESNO),
        question("Heb je tijd", tiles=["Heb", "je", "tijd"],
                 why="فعل، بعد فاعل، بعد بقیه.", concept=C_YESNO),
        transform("Je bent nieuw hier. → (سؤال کن)", "Ben je nieuw hier?",
                  "فعل و فاعل جا عوض می‌کنند و t می‌افتد.", concept=C_YESNO),
        transform("Hij is ziek. → (سؤال کن)", "Is hij ziek?",
                  "is اول می‌آید.", concept=C_YESNO),
        pickorder("کدام سؤال درست است؟",
                  ["Heb je een vraag?", "Je hebt een vraag?", "Hebt je een vraag?"],
                  "Heb je een vraag?",
                  "فعل اول، و بعد از je دیگر t نمی‌آید.", concept=C_YESNO),
        mc("___ u de manager?", ["Bent", "Ben", "Is"], "Bent",
           "u همیشه bent می‌گیرد، هم در جمله‌ی خبری هم در سؤال.", concept=C_YESNO),
        fix("Jij hebt een auto?", "Heb je een auto?",
            "برای سؤال باید فعل را اول بیاوری.", concept=C_YESNO),
        fa2nl("«آماده‌ای؟»", "Ben je klaar?", 
              "فعل اول + فاعل.", alt=["Ben jij klaar?"], concept=C_YESNO),
    ])

lesson(
    "a0-l08", "a0-vragen", "A0",
    "Wat, wie, waar, hoe", "کلمات پرسشی",
    [C_QWORD],
    discover(
        ["Wat is dat?", "Wie is die man?", "Waar woon je?", "Hoe gaat het?"],
        "بعد از کلمه‌ی پرسشی چه چیزی می‌آید؟",
        "همیشه فعل. ترتیب این است: کلمه‌ی پرسشی + فعل + فاعل."),
    rule("vraagwoord + werkwoord + onderwerp",
         "wat، wie، waar، hoe، wanneer، waarom — بعدش مستقیم فعل می‌آید.",
         "what / who / where / how"),
    pattern([("Waar", "qword"), ("woon", "verb"), ("je", "subject"), ("?", "mark")],
            "کلمه‌ی پرسشی جای اول را می‌گیرد، پس فاعل می‌رود بعد از فعل."),
    [
        ex("Wat is dit?", "این چیست؟"),
        ex("Wie ben jij?", "تو کی هستی؟"),
        ex("Waar woon je?", "کجا زندگی می‌کنی؟"),
        ex("Hoe gaat het met je?", "حالت چطور است؟"),
        ex("Wanneer begint de les?", "کلاس کِی شروع می‌شود؟"),
        ex("Waarom ben je te laat?", "چرا دیر کردی؟"),
    ],
    [
        wrong("Waar je woont?", "Waar woon je?",
              "بعد از کلمه‌ی پرسشی باید فعل بیاید، نه فاعل."),
        wrong("Wat is het betekenis?", "Wat betekent dat?",
              "برای پرسیدن معنی، هلندی‌ها فعل betekenen را به کار می‌برند."),
    ],
    "این شش کلمه در هر مکالمه‌ای لازم‌اند: پرسیدن آدرس، ساعت، دلیل، اسم. در مصاحبه‌ی کاری هم اولین چیزی است که باید بفهمی.",
    [
        mc("___ woon je?", ["Waar", "Wat", "Wie"], "Waar",
           "برای مکان waar.", concept=C_QWORD),
        mc("___ is dat?", ["Wat", "Waar", "Hoe"], "Wat",
           "برای چیزها wat.", concept=C_QWORD),
        mc("___ gaat het?", ["Hoe", "Wat", "Wie"], "Hoe",
           "«Hoe gaat het?» عبارت ثابتِ حال‌واحوال‌پرسی است.", concept=C_QWORD),
        mc("___ begint de film?", ["Wanneer", "Waar", "Wie"], "Wanneer",
           "برای زمان wanneer.", concept=C_QWORD),
        question("Waar werk je", tiles=["Waar", "werk", "je"],
                 why="کلمه‌ی پرسشی، بعد فعل، بعد فاعل.", concept=C_QWORD),
        question("Wie is die vrouw", tiles=["Wie", "is", "die", "vrouw"],
                 why="wie + فعل + بقیه.", concept=C_QWORD),
        fix("Waarom jij bent boos?", "Waarom ben je boos?",
            "بعد از waarom فعل می‌آید، بعد فاعل.", concept=C_QWORD),
        fa2nl("«کجا زندگی می‌کنی؟»", "Waar woon je?", 
              "waar + فعل + فاعل.", alt=["Waar woon jij?"], concept=C_QWORD),
        dialogue("— ___ heet je?", "— Ik heet Amir.",
                 ["Hoe", "Wat", "Wie"], "Hoe",
                 "برای پرسیدن اسم، هلندی‌ها «Hoe heet je?» می‌گویند — نه «Wat».",
                 concept=C_QWORD),
    ])

lesson(
    "a0-l09", "a0-werkwoorden", "A0",
    "Ik werk, jij werkt", "زمان حال: من و تو",
    [C_PRES_SG],
    discover(
        ["werken → ik werk", "wonen → ik woon", "jij werkt", "hij woont"],
        "برای ساختن ik چه چیزی از مصدر حذف شد؟ و برای jij چه چیزی اضافه شد؟",
        "مصدر منهای -en می‌شود ریشه (stam). ik = ریشه. jij و hij = ریشه + t."),
    rule("stam = infinitief − en · ik = stam · jij/hij = stam + t",
         "werken منهای en می‌شود werk. ik werk، jij werkt، hij werkt.",
         "I work / you work / he works"),
    pattern([("ik", "subject"), ("werk", "verb"), ("·", "sep"), ("jij", "subject"), ("werkt", "verb")],
            "فقط یک t فرق دارند."),
    [
        ex("Ik woon in Rotterdam.", "در روتردام زندگی می‌کنم."),
        ex("Jij spreekt goed Nederlands.", "تو هلندی را خوب حرف می‌زنی."),
        ex("Hij werkt bij een bank.", "او در یک بانک کار می‌کند."),
        ex("Zij leert snel.", "او سریع یاد می‌گیرد."),
        ex("Ik begrijp het niet.", "متوجه نمی‌شوم.", "جمله‌ای که در کلاس زیاد لازمش داری"),
    ],
    [
        wrong("Ik werken bij een school.", "Ik werk bij een school.",
              "با ik شکل کوتاه (ریشه) می‌آید، نه مصدر."),
        wrong("Hij werk hier.", "Hij werkt hier.",
              "سوم‌شخص مفرد همیشه t می‌گیرد."),
    ],
    "هر جمله‌ای درباره‌ی کار، خانه، درس و زندگی روزمره با همین ساخته می‌شود. این پایه‌ی تمام زمان حال هلندی است.",
    [
        conjugate("ik (wonen) → ik ___", "woon",
                  "wonen منهای en می‌شود woon. (دو o می‌ماند تا صدا بلند بماند.)",
                  concept=C_PRES_SG),
        conjugate("jij (werken) → jij ___", "werkt",
                  "ریشه + t.", concept=C_PRES_SG),
        conjugate("hij (leren) → hij ___", "leert",
                  "سوم‌شخص مفرد → ریشه + t.", concept=C_PRES_SG),
        mc("Ik ___ in Delft.", ["woon", "woont", "wonen"], "woon",
           "با ik فقط ریشه.", concept=C_PRES_SG),
        mc("Zij ___ bij een ziekenhuis.", ["werkt", "werk", "werken"], "werkt",
           "zij (یک نفر) → ریشه + t.", concept=C_PRES_SG),
        blank("Hij ___ heel goed Nederlands. (spreken)", "spreekt",
              "ریشه spreek + t.", concept=C_PRES_SG),
        fix("Ik werkt bij een winkel.", "Ik werk bij een winkel.",
            "t فقط برای jij و hij/zij/het است، نه برای ik.", concept=C_PRES_SG),
        fa2nl("«در آمستردام زندگی می‌کنم.»", "Ik woon in Amsterdam.",
              "ik + ریشه.", concept=C_PRES_SG),
        order("Hij werkt bij een bank.",
              why="فاعل + فعل + بقیه.", concept=C_PRES_SG),
    ])

lesson(
    "a0-l10", "a0-werkwoorden", "A0",
    "Wij werken", "زمان حال: جمع",
    [C_PRES_PL, C_PRES_SG],
    discover(
        ["ik werk", "jij werkt", "hij werkt", "wij werken", "jullie werken", "zij werken"],
        "کل جدول را ببین. جمع چه شکلی دارد؟",
        "هر سه شکل جمع دقیقاً مثل مصدرند: werken. یعنی از شش شکل، فقط سه شکل واقعاً باید یاد گرفته شود."),
    rule("wij / jullie / zij + infinitief",
         "در جمع، فعل همان شکل پایه است — هیچ تغییری ندارد.",
         "we / you / they work"),
    pattern([("ik", "subject"), ("werk", "verb"), ("|", "sep"),
             ("jij/hij", "subject"), ("werkt", "verb"), ("|", "sep"),
             ("wij/jullie/zij", "subject"), ("werken", "verb")],
            "کل زمان حال هلندی در همین سه ستون خلاصه می‌شود."),
    [
        ex("Wij werken samen.", "ما با هم کار می‌کنیم."),
        ex("Jullie spreken goed Nederlands.", "شما هلندی را خوب حرف می‌زنید."),
        ex("Ze wonen in Utrecht.", "آن‌ها در اوترخت زندگی می‌کنند."),
        ex("Mijn ouders komen uit Iran.", "پدر و مادرم اهل ایران هستند.",
           "فاعل جمع → فعل جمع"),
        ex("De kinderen spelen buiten.", "بچه‌ها بیرون بازی می‌کنند."),
    ],
    [
        wrong("Wij werkt samen.", "Wij werken samen.",
              "t فقط برای مفرد است. جمع همیشه شکل کامل فعل را می‌گیرد."),
        wrong("Mijn ouders woont in Iran.", "Mijn ouders wonen in Iran.",
              "ouders جمع است، پس فعل هم باید جمع باشد."),
    ],
    "به محض اینکه درباره‌ی خانواده، همکارها یا مردم حرف بزنی به شکل جمع نیاز داری. خبر تلویزیون و روزنامه پر از همین شکل است.",
    [
        conjugate("wij (werken) → wij ___", "werken",
                  "جمع = شکل پایه.", concept=C_PRES_PL),
        conjugate("de kinderen (spelen) → de kinderen ___", "spelen",
                  "فاعل جمع → فعل جمع.", concept=C_PRES_PL),
        mc("Jullie ___ hard.", ["werken", "werkt", "werk"], "werken",
           "jullie جمع است.", concept=C_PRES_PL),
        mc("Mijn broers ___ in Den Haag.", ["wonen", "woont", "woon"], "wonen",
           "broers جمع است → wonen.", concept=C_PRES_PL),
        pick2("De studenten ___ veel vragen.",
              ["hebben", "heeft"], "hebben",
              "studenten جمع است.", concept=C_PRES_PL),
        fix("Wij werkt bij dezelfde firma.", "Wij werken bij dezelfde firma.",
            "در جمع t نمی‌گیریم.", concept=C_PRES_PL),
        fa2nl("«ما با هم کار می‌کنیم.»", "We werken samen.", 
              "فاعل جمع + شکل پایه‌ی فعل.", alt=["Wij werken samen."], concept=C_PRES_PL),
        order("Zij wonen al drie jaar in Nederland.",
              why="فاعل + فعل + بقیه.", concept=C_PRES_PL),
        blank("Mijn collega's ___ altijd koffie in de pauze. (drinken)", "drinken",
              "collega's جمع است → drinken.", concept=C_PRES_PL),
    ])

# ----------------------------------------------------------------- modules

module("a0-ik", "A0", "Ik en jij", "من و تو",
       "بتوانی خودت و دیگران را معرفی کنی: ik ben، jij bent، hij is، wij zijn.",
       ["a0-l01", "a0-l02", "a0-l03"], icon="user")

module("a0-hebben", "A0", "Hebben en dingen", "داشتن و چیزها",
       "بگویی چه داری و چه نداری، و اولین برخورد با een/de/het.",
       ["a0-l04", "a0-l05", "a0-l06"], icon="cards")

module("a0-vragen", "A0", "Vragen stellen", "سؤال پرسیدن",
       "سؤال بله/خیر بسازی و با wat، wie، waar و hoe اطلاعات بگیری.",
       ["a0-l07", "a0-l08"], icon="target")

module("a0-werkwoorden", "A0", "Gewone werkwoorden", "فعل‌های معمولی",
       "زمان حال را کامل بسازی: ik werk، jij werkt، wij werken.",
       ["a0-l09", "a0-l10"], icon="spark")
