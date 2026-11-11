"""Arabic speakers learning Kurdish (Standard Arabic, navy)."""
import json
def ku(s, size=42):
    return f'<span class="ar" style="font-size:{size}px">{s}</span>'
def lat(s, size=30):
    return f'<span class="lat" style="font-size:{size}px;font-weight:700;color:#1673C0">{s}</span>'
def mean(s, size=32):
    return f'<span style="font-size:{size}px;font-weight:700;color:#0B2A6B">{s}</span>'

S = {"_meta": dict(theme="navy", foot="تعلّم الكردية السورانية · لين", cta="اطلب عبر واتساب", badge="ضمان 7 دروس", unit="دينار")}
COLS = ["بالكردية", "النطق", "المعنى"]
S["K01_greetings"] = dict(layout="table", scene="k01_greeting", kick="أول كلمات بالكردية",
    h1="قل مرحباً<br><span class='acc'>بالكردية السورانية</span>", hs=58, cols=COLS, rh=80, card_top=700,
    rows=[[ku("سڵاو"), lat("slaw"), mean("مرحباً")], [ku("چۆنیت؟"), lat("chonit?"), mean("كيف حالك؟")],
          [ku("باشم، سوپاس", 38), lat("bashim, supas", 28), mean("بخير، شكراً")], [ku("بەخێربێیت", 40), lat("bexêrbêyt"), mean("أهلاً وسهلاً")]],
    note="احفظ المنشور، وقلها لأول صديق كردي تقابله.")
S["K02_false_friends"] = dict(layout="table", scene="k02_tree", kick="انتبه!",
    h1="كلمات تشبه العربية…<br><span class='acc'>لكن معناها مختلف</span>", hs=58, cols=COLS, rh=90, card_top=720,
    rows=[[ku("باب", 46), lat("bab"), mean("أب")], [ku("دار", 46), lat("dar"), mean("شجرة")], [ku("شار", 46), lat("shar"), mean("مدينة")]],
    note="لهذا نتعلّم الكلمات داخل جُمل، لا وحدها.")
S["K03_numbers"] = dict(layout="table", scene="k03_count", kick="الأرقام",
    h1="من 1 إلى 5<br><span class='acc'>بالكردية</span>", hs=60, cols=["الرقم", "بالكردية", "النطق"], rh=74, card_top=690,
    rows=[[lat("1", 40), ku("یەک"), lat("yek")], [lat("2", 40), ku("دوو"), lat("dû")], [lat("3", 40), ku("سێ"), lat("sê")],
          [lat("4", 40), ku("چوار"), lat("chwar")], [lat("5", 40), ku("پێنج"), lat("pênj")]],
    note="جرّب: كم عمرك بالكردية؟ اكتبها في التعليقات.")
S["K04_market"] = dict(layout="table", scene="k04_bazaar", kick="في السوق",
    h1="اشترِ بالكردية<br><span class='acc'>من أول مرة</span>", hs=60, cols=COLS, rh=84, card_top=700,
    rows=[[ku("ئەمە بە چەندە؟", 38), lat("eme be chende?", 26), mean("بكم هذا؟")], [ku("زۆر گرانە", 40), lat("zor girane", 28), mean("غالٍ جداً")],
          [ku("باشە", 42), lat("bashe"), mean("حسناً")], [ku("سوپاس", 42), lat("supas"), mean("شكراً")]],
    note="«بە چەندە؟» أهم سؤال في أي سوق كردي.")
S["K05_letters"] = dict(layout="list", scene="k05_student", kick="الحروف الكردية",
    h1="7 حروف كردية<br><span class='acc'>ليست في العربية</span>", hs=58, photo_h=470, list_top=640, fs=33, gap=14,
    items=["پ مثل <span class='lat'>P</span> في <span class='lat'>Pizza</span>", "چ مثل <span class='lat'>Ch</span> في <span class='lat'>Chocolate</span>",
           "ژ مثل <span class='lat'>s</span> في <span class='lat'>Television</span>", "ڤ مثل <span class='lat'>V</span> في <span class='lat'>Video</span>",
           "گ مثل <span class='lat'>G</span> في <span class='lat'>Google</span>", "ڵ لام مفخّمة، كاللام في «الله»", "ڕ راء قوية مكرّرة"],
    note="والحركات تُكتب حروفاً: لا تحتاج إلى تشكيل.", note_y=1180)
S["K06_erbil_tourist"] = dict(layout="table", scene="k06_citadel", kick="للسائح",
    h1="4 جمل كردية<br><span class='acc'>لرحلتك إلى أربيل</span>", hs=58, cols=COLS, rh=84, card_top=700,
    rows=[[ku("قەڵا لە کوێیە؟", 38), lat("qela le kwêye?", 26), mean("أين القلعة؟")], [ku("تکایە", 42), lat("tikaye"), mean("من فضلك")],
          [ku("ببورە", 42), lat("bibure"), mean("عفواً / آسف")], [ku("ماڵئاوا", 42), lat("maława"), mean("مع السلامة")]],
    note="الناس هنا يفرحون كثيراً حين تحاول بلغتهم.")
S["K07_food"] = dict(layout="table", scene="k07_breakfast", kick="على المائدة",
    h1="كلمات الطعام<br><span class='acc'>بالكردية</span>", hs=60, cols=COLS, rh=80, card_top=700,
    rows=[[ku("نان"), lat("nan"), mean("خبز")], [ku("ئاو"), lat("aw"), mean("ماء")], [ku("چا"), lat("cha"), mean("شاي")],
          [ku("نۆشی گیان!", 40), lat("noshî gyan!", 28), mean("بالعافية!")]],
    note="قل «نۆشی گیان» لمن يأكل معك، وسترى الابتسامة.")
S["K08_why"] = dict(layout="list", scene="k08_friends", kick="لماذا الكردية؟",
    h1="5 أسباب لتتعلّم<br><span class='acc'>الكردية السورانية</span>", hs=58, photo_h=540, list_top=740, fs=34, gap=20,
    items=["لتعمل وتعيش في كردستان براحة", "لتقترب من أصدقائك وجيرانك الكرد", "لتسافر وتتحدث مع الناس مباشرة",
           "لتفهم الأغاني والأفلام الكردية", "لأن الناس يفرحون حين تكلّمهم بلغتهم"],
    note="أي سبب هو سببك؟", note_y=1186)
S["K09_kind_words"] = dict(layout="table", scene="k09_host", kick="تعابير لطيفة",
    h1="كلمات تفتح القلوب<br><span class='acc'>بالكردية</span>", hs=58, cols=COLS, rh=84, card_top=700,
    rows=[[ku("سەرچاو", 42), lat("serchaw"), mean("على عيني")], [ku("دەستت خۆش بێت", 36), lat("destit xosh bêt", 26), mean("تسلم إيدك")],
          [ku("زۆر سوپاس", 40), lat("zor supas"), mean("شكراً جزيلاً")], [ku("گیان", 42), lat("gyan"), mean("عزيزي")]],
    note="أيّها ستقولها اليوم؟")
S["K10_two_people"] = dict(layout="full", scene="k10_portrait", where="bottom", y=900,
    h1="أنت شخصان<br><span class='acc'>حين تعرف لغتين</span>", hs=76, sub="واحد يضحك بالعربية، والآخر بالكردية.", ss=36)

SZ = [[1080, 1350], [1080, 1920]]
WAIT = dict(cta="سجّل في قائمة الانتظار عبر واتساب", badge="", cta_size=32)
S["KA01_learn_kurdish"] = dict(layout="ad", sizes=SZ, scene="ka01_cafe", kick="الكردية السورانية بالحوار",
    h1="تعلّم الكردية<br>خطوة لطيفة كل يوم", hs=68, sub="درس قصير كل يوم: استمع، كرّر، تكلّم. وكتاب لين للكردية قادم قريباً.", **WAIT)
S["KA02_live_in_kurdistan"] = dict(layout="ad", sizes=SZ, scene="ka02_neighbors", kick="تعيش في كردستان؟",
    h1="كلّم جيرانك وزملاءك<br>بلغتهم", hs=64, sub="الكردية السورانية بالحوار، من التحية إلى العمل. سجّل اسمك لتعرف موعد الإطلاق أولاً.", **WAIT)
S["KA03_book_soon"] = dict(layout="ad", sizes=SZ, scene="ka03_desk", kick="قريباً",
    h1="كتاب لين<br>للكردية السورانية", hs=70, sub="100 درس بالحوار، بصوت كردي أصيل. سجّل الآن وكن أول من يعرف.", **WAIT)
S["KA04_tourist"] = dict(layout="ad", sizes=SZ, scene="k06_citadel", kick="مسافر إلى أربيل؟",
    h1="جملة كردية جديدة<br>كل يوم", hs=68, sub="تابع صفحتنا وتعلّم ما تحتاجه في رحلتك: التحية، السوق، المطعم، التاكسي.",
    cta="تابعنا الآن", phone="", icon="follow", badge="")
S["KA05_not_hard"] = dict(layout="ad", sizes=SZ, scene="k05_student", kick="الكردية ليست صعبة",
    h1="تقرأ العربية؟<br>قطعت نصف الطريق", hs=68, sub="الكردية تُكتب بالحروف العربية، والحركات تُكتب حروفاً. ابدأ اليوم.",
    cta="تابعنا الآن", phone="", icon="follow", badge="")
NOV = "السعر الخاص حتى نهاية الشهر 11"
S["KA06_gift_friend"] = dict(layout="ad", sizes=SZ, scene="ka06_gift", kick="هدية لصديقك الكردي",
    h1="صديقك الكردي يحتاج<br>العربية العراقية؟", hs=62, sub="أهدِه كتاب لين: 100 درس من الكردية إلى العربية العراقية، بصوت عراقي أصيل.",
    price="24,000", old="29,000", deadline=NOV)
S["KA07_team"] = dict(layout="ad", sizes=SZ, scene="ka07_office", kick="لأصحاب الشركات",
    h1="فريقك الكردي<br>والعربية العراقية", hs=64, sub="100 درس من الحياة والعمل، مع صوت عراقي أصيل. اسأل عن طلبات الفرق.",
    price="24,000", old="29,000", deadline=NOV)
S["KA08_new_year"] = dict(layout="ad", sizes=SZ, scene="ka08_newyear", kick="هدية رأس السنة",
    h1="أهدِ زميلك الكردي<br>لغة جديدة", hs=64, sub="كتاب لين: من الكردية إلى العربية العراقية، 100 درس وصوت أصيل.", price="29,000")
S["KA09_shared_language"] = dict(layout="ad", sizes=SZ, scene="ka07_office", kick="لغة مشتركة في العمل",
    h1="حين يتكلّم الجميع<br>نفس اللغة", hs=64, sub="عندما يتعلّم زملاؤك الكرد العربية العراقية، يصبح العمل أسهل للجميع.", price="29,000")
S["KA10_gift_language"] = dict(layout="ad", sizes=SZ, scene="ka06_gift", kick="هدية مختلفة",
    h1="أهدِ لغة،<br>لا مجرد كتاب", hs=70, sub="لصديقك أو زميلك الكردي: 100 درس من الكردية إلى العربية العراقية.", price="29,000")

json.dump(S, open("spec_arku.json", "w"), ensure_ascii=False, indent=1)
print(len(S) - 1)
