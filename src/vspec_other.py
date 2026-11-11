import json
# ---------------- Arabic speakers learning Kurdish (Standard Arabic captions)
A = {"_meta": dict(theme="navy", sub="لين · الكردية السورانية بالحوار", cta="تابعنا: جملة كردية كل يوم", phone="", book=False, dir="rtl", asr="fa")}
def ae(title, phrase):
    return dict(title=title, phrase=phrase)
A["KV01_hotel"] = dict(src="kv01_hotel", hook="أول جملة ستسمعها في أربيل",
    lines=[["بەخێربێیت! چۆنی؟", "أهلاً وسهلاً! كيف حالك؟"], ["باشم، سوپاس!", "بخير، شكراً!"]],
    end=ae("قلها بالكردية", ["بەخێربێیت", "bexêrbêyt", "أهلاً وسهلاً"]))
A["KV02_market"] = dict(src="kv02_market", hook="كيف تساوم بالكردية؟",
    lines=[["ئەمە بە چەندە؟", "بكم هذا؟"], ["پێنج هەزار.", "خمسة آلاف."], ["زۆر گرانە!", "غالٍ جداً!"], ["باشە، چوار هەزار.", "حسناً، أربعة آلاف."]],
    end=ae("أهم سؤال في السوق", ["بە چەندە؟", "be chende?", "بكم؟"]))
A["KV03_taxi"] = dict(src="kv03_taxi", hook="في تاكسي أربيل",
    lines=[["بۆ قەڵا، تکایە.", "إلى القلعة، من فضلك."], ["سەرچاو!", "على عيني!"]],
    end=ae("كلمة تفتح القلوب", ["سەرچاو", "serchaw", "على عيني"]))
A["KV04_restaurant"] = dict(src="kv04_restaurant", hook="في المطعم الكردي",
    lines=[["نان و ئاو، تکایە.", "خبز وماء، من فضلك."], ["سەرچاو، نۆشی گیان!", "على عيني، بالعافية!"]],
    end=ae("قلها لمن يأكل معك", ["نۆشی گیان", "noshî gyan", "بالعافية"]))
A["KV05_neighbours"] = dict(src="kv05_neighbours", hook="صباح الخير بالكردية",
    lines=[["بەیانی باش!", "صباح الخير!"], ["بەیانی باش، چۆنی؟", "صباح الخير، كيف حالك؟"], ["باشم، سوپاس.", "بخير، شكراً."]],
    end=ae("ابدأ يومك بالكردية", ["بەیانی باش", "beyanî bash", "صباح الخير"]))
A["KV06_thanks"] = dict(src="kv06_thanks", hook="كيف تشكر من طبخ لك؟",
    lines=[["دەستت خۆش بێت!", "تسلم إيدك!"], ["نۆشی گیان!", "بالعافية!"]],
    end=ae("تسلم إيدك بالكردية", ["دەستت خۆش بێت", "destit xosh bêt", "تسلم إيدك"]))
A["KV07_numbers"] = dict(src="kv07_numbers", hook="عُدّ معنا بالكردية",
    lines=[["یەک، دوو، سێ", "واحد، اثنان، ثلاثة"], ["چوار، پێنج!", "أربعة، خمسة!"]],
    end=ae("الأرقام من 1 إلى 5", ["یەک · دوو · سێ · چوار · پێنج", "yek · dû · sê · chwar · pênj", "واحد · اثنان · ثلاثة · أربعة · خمسة"]))
A["KV08_bab"] = dict(src="kv08_bab", hook="«باب» بالكردية… ليست باب البيت!",
    lines=[["باب! باب!", "بابا! بابا!"]],
    texts=[[5.5, 10.0, "في الكردية: باب = أب"]],
    end=ae("كلمة تشبه العربية… بمعنى مختلف", ["باب", "bab", "أب"]))
A["KV09_office"] = dict(src="kv09_office", hook="أول كلمة كردية تتعلّمها في العمل",
    lines=[["سوپاس.", "شكراً."], ["سوپاس!", "شكراً!"]],
    end=ae("كلمة واحدة تكفي لتبدأ", ["سوپاس", "supas", "شكراً"]))
A["KV10_two_people"] = dict(src="kv10_two_people", hook="أنت شخصان حين تعرف لغتين",
    lines=[["سڵاو گیان، چۆنی؟", "مرحباً عزيزتي، كيف حالك؟"]],
    end=ae("أنت شخصان حين تعرف لغتين", ["سڵاو گیان", "slaw gyan", "مرحباً عزيزي"]))
json.dump(A, open("vspec_arku.json", "w"), ensure_ascii=False, indent=1)

# ---------------- English speakers learning Kurdish
E = {"_meta": dict(theme="cream", sub="Leen · Kurdish (Sorani) through conversation", cta="Follow for a phrase a day", phone="", book=False, dir="ltr", asr="fa")}
E["EV01_cafe"] = dict(src="ev01_cafe", hook="Order tea in Kurdish",
    lines=[["چایەک، تکایە.", "A tea, please."], ["سەرچاو!", "With pleasure!"]],
    end=ae("Say it in Kurdish", ["چایەک، تکایە", "chayek, tikaye", "A tea, please"]))
E["EV02_colleague"] = dict(src="ev02_colleague", hook="Greet your Kurdish colleague",
    lines=[["سڵاو! چۆنیت؟", "Hi! How are you?"], ["باشم، سوپاس! تۆ چۆنیت؟", "I'm good, thanks! And you?"]],
    end=ae("Your first Kurdish words", ["سڵاو، چۆنیت؟", "slaw, chonit?", "Hi, how are you?"]))
E["EV03_bazaar"] = dict(src="ev03_bazaar", hook="Shopping at the bazaar",
    lines=[["ئەمە بە چەندە؟", "How much is this?"], ["پێنج هەزار.", "Five thousand."], ["سوپاس!", "Thank you!"]],
    end=ae("The bazaar question", ["بە چەندە؟", "be chende?", "How much?"]))
E["EV04_taxi"] = dict(src="ev04_taxi", hook="Taking a taxi in Erbil",
    lines=[["بۆ قەڵا، تکایە.", "To the citadel, please."], ["سەرچاو!", "With pleasure!"]],
    end=ae("Locals love this word", ["سەرچاو", "serchaw", "With pleasure"]))
E["EV05_neighbour"] = dict(src="ev05_neighbour", hook="Good morning in Kurdish",
    lines=[["بەیانی باش!", "Good morning!"], ["بەیانی باش، چۆنی؟", "Good morning, how are you?"]],
    end=ae("Start your day in Kurdish", ["بەیانی باش", "beyanî bash", "Good morning"]))
E["EV06_dinner"] = dict(src="ev06_dinner", hook="Thank your Kurdish host",
    lines=[["دەستت خۆش بێت!", "Thanks for your effort!"], ["نۆشی گیان!", "Enjoy your meal!"]],
    end=ae("The host's favourite words", ["دەستت خۆش بێت", "destit xosh bêt", "Thanks for your effort"]))
E["EV07_numbers"] = dict(src="ev07_numbers", hook="Count to five in Kurdish",
    lines=[["یەک، دوو، سێ", "One, two, three"], ["چوار، پێنج!", "Four, five!"]],
    end=ae("Numbers 1 to 5", ["یەک · دوو · سێ · چوار · پێنج", "yek · dû · sê · chwar · pênj", "1 · 2 · 3 · 4 · 5"]))
E["EV08_classroom"] = dict(src="ev08_classroom", hook="When Kurdish kids greet their teacher",
    lines=[["بەیانی باش، مامۆستا!", "Good morning, teacher!"], ["بەیانی باش!", "Good morning!"]],
    end=ae("Teacher in Kurdish", ["مامۆستا", "mamosta", "Teacher"]))
E["EV09_goodbye"] = dict(src="ev09_goodbye", hook="How to say goodbye",
    lines=[["ماڵئاوا!", "Goodbye!"], ["ماڵئاوا، گیان!", "Goodbye, dear!"]],
    end=ae("Say goodbye in Kurdish", ["ماڵئاوا", "maława", "Goodbye"]))
E["EV10_two_people"] = dict(src="ev10_two_people", hook="You are two people when you know two languages",
    lines=[["سڵاو گیان، چۆنی؟", "Hi dear, how are you?"]],
    end=ae("You are two people<br>when you know two languages", ["سڵاو گیان", "slaw gyan", "Hi dear"]))
json.dump(E, open("vspec_enku.json", "w"), ensure_ascii=False, indent=1)
print(len(A) - 1, len(E) - 1)
