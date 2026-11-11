"""English speakers learning Kurdish Sorani (cream, English)."""
import json
def ku(s, size=42):
    return f'<span class="ar" style="font-size:{size}px;direction:rtl">{s}</span>'
def lat(s, size=30):
    return f'<span class="lat" style="font-size:{size}px;font-weight:700;color:#1E8FB8">{s}</span>'
def mean(s, size=30):
    return f'<span style="font-size:{size}px;font-weight:700;color:#041730;font-family:P,V,sans-serif">{s}</span>'

S = {"_meta": dict(theme="cream", foot="Learn Kurdish (Sorani) · Leen", cta="Order on WhatsApp", badge="7-lesson guarantee",
                   unit="IQD", phone="+964 770 013 7670")}
COLS = ["Kurdish", "Say it", "Meaning"]
S["E01_greetings"] = dict(layout="table", scene="e01_greeting", kick="Your first Kurdish words",
    h1="Say hello<br><span class='acc'>in Kurdish (Sorani)</span>", hs=58, cols=COLS, rh=80, card_top=700,
    rows=[[ku("سڵاو"), lat("slaw"), mean("Hello")], [ku("چۆنیت؟"), lat("chonit?"), mean("How are you?")],
          [ku("باشم، سوپاس", 38), lat("bashim, supas", 28), mean("I'm good, thanks")], [ku("بەخێربێیت", 40), lat("bexêrbêyt"), mean("Welcome")]],
    note="Save this and try it on the next Kurdish person you meet.")
S["E02_new_sounds"] = dict(layout="list", scene="e02_listen", kick="Pronunciation",
    h1="7 Kurdish sounds<br><span class='acc'>English doesn't have</span>", hs=58, photo_h=470, list_top=640, fs=31, gap=12,
    items=["ح <b>ḥ</b>: a breathy h from deep in the throat", "خ <b>kh</b>: like ch in Scottish “loch”", "ع <b>ʕ</b>: a squeeze in the throat",
           "غ <b>gh</b>: like a French r", "ق <b>q</b>: a k from the back of the throat", "ڕ <b>rr</b>: a rolled r, like Spanish “perro”",
           "ڵ <b>ł</b>: a heavy l, like the ll in “full”"],
    note="Take them slowly. Listen first, then repeat out loud.", note_y=1180)
S["E03_numbers"] = dict(layout="table", scene="k03_count", kick="Numbers",
    h1="Count to 5<br><span class='acc'>in Kurdish</span>", hs=60, cols=["Number", "Kurdish", "Say it"], rh=74, card_top=690,
    rows=[[lat("1", 40), ku("یەک"), lat("yek")], [lat("2", 40), ku("دوو"), lat("dû")], [lat("3", 40), ku("سێ"), lat("sê")],
          [lat("4", 40), ku("چوار"), lat("chwar")], [lat("5", 40), ku("پێنج"), lat("pênj")]],
    note="Try it: how old are you in Kurdish? Tell us below.")
S["E04_market"] = dict(layout="table", scene="e04_bazaar", kick="At the bazaar",
    h1="Shop in Kurdish<br><span class='acc'>from day one</span>", hs=60, cols=COLS, rh=84, card_top=700,
    rows=[[ku("ئەمە بە چەندە؟", 38), lat("eme be chende?", 26), mean("How much is this?")], [ku("زۆر گرانە", 40), lat("zor girane", 28), mean("It's too expensive")],
          [ku("باشە", 42), lat("bashe"), mean("OK")], [ku("سوپاس", 42), lat("supas"), mean("Thank you")]],
    note="“Be chende?” is the most useful question in any Kurdish bazaar.")
S["E05_tourist"] = dict(layout="table", scene="k06_citadel", kick="Travelling to Erbil?",
    h1="4 Kurdish phrases<br><span class='acc'>for your trip</span>", hs=60, cols=COLS, rh=84, card_top=700,
    rows=[[ku("قەڵا لە کوێیە؟", 38), lat("qela le kwêye?", 26), mean("Where is the citadel?")], [ku("تکایە", 42), lat("tikaye"), mean("Please")],
          [ku("ببورە", 42), lat("bibure"), mean("Sorry / excuse me")], [ku("ماڵئاوا", 42), lat("maława"), mean("Goodbye")]],
    note="People here light up when you try a few words.")
S["E06_food"] = dict(layout="table", scene="k07_breakfast", kick="At the table",
    h1="Food words<br><span class='acc'>in Kurdish</span>", hs=60, cols=COLS, rh=80, card_top=700,
    rows=[[ku("نان"), lat("nan"), mean("Bread")], [ku("ئاو"), lat("aw"), mean("Water")], [ku("چا"), lat("cha"), mean("Tea")],
          [ku("نۆشی گیان!", 40), lat("noshî gyan!", 28), mean("Enjoy your meal!")]],
    note="Say “noshî gyan” to someone eating with you. Watch them smile.")
S["E07_why"] = dict(layout="list", scene="e07_ngo", kick="Why Kurdish?",
    h1="5 reasons to learn<br><span class='acc'>Kurdish (Sorani)</span>", hs=58, photo_h=540, list_top=740, fs=33, gap=20,
    items=["Work and live in Kurdistan with ease", "Get closer to Kurdish friends, family and colleagues",
           "Travel and talk to people directly", "Understand Kurdish music and films", "People love it when you speak their language"],
    note="Which one is yours?", note_y=1186)
S["E08_kind_words"] = dict(layout="table", scene="e08_host", kick="Kind words",
    h1="Words that open doors<br><span class='acc'>in Kurdish</span>", hs=56, cols=COLS, rh=84, card_top=700,
    rows=[[ku("سەرچاو", 42), lat("serchaw"), mean("With pleasure")], [ku("دەستت خۆش بێت", 36), lat("destit xosh bêt", 26), mean("Thanks for your effort")],
          [ku("زۆر سوپاس", 40), lat("zor supas"), mean("Thank you very much")], [ku("گیان", 42), lat("gyan"), mean("Dear")]],
    note="Which one will you use today?")
S["E09_facts"] = dict(layout="list", scene="e09_writing", kick="Did you know?",
    h1="Kurdish is easier<br><span class='acc'>than it looks</span>", hs=58, photo_h=520, list_top=720, fs=33, gap=20,
    items=["Sorani is written right to left", "Almost every vowel is written, so you read it as it sounds",
           "Many letters sound just like English: b, p, t, d, s, sh, k, g", "Short real dialogues get you speaking fast",
           "20 minutes a day is enough to start"],
    note="Follow for one Kurdish phrase a day.", note_y=1186)
S["E10_two_people"] = dict(layout="full", scene="e10_portrait", where="bottom", y=920,
    h1="You are two people<br><span class='acc'>when you know two languages</span>", hs=66,
    sub="One of you laughs in English, the other in Kurdish.", ss=34)

SZ = [[1080, 1350], [1080, 1920]]
FOLLOW = dict(cta="Follow for a phrase a day", phone="", icon="follow", badge="")
WAIT = dict(cta="Join the waitlist on WhatsApp", badge="", cta_size=32)
S["EA01_learn"] = dict(layout="ad", sizes=SZ, scene="e01_greeting", kick="Kurdish through conversation",
    h1="Learn Kurdish,<br>one small step a day", hs=66, sub="Listen, repeat out loud, speak. Short real-life dialogues with native audio.", **FOLLOW)
S["EA02_expat"] = dict(layout="ad", sizes=SZ, scene="e07_ngo", kick="Living in Kurdistan?",
    h1="Talk to your colleagues<br>in their language", hs=62, sub="Kurdish (Sorani) for expats, NGO staff and newcomers. Our Kurdish course is coming soon.", **WAIT)
S["EA03_book_soon"] = dict(layout="ad", sizes=SZ, scene="ka03_desk", kick="Coming soon",
    h1="The Leen course<br>for Kurdish (Sorani)", hs=66, sub="100 dialogue lessons with native Kurdish audio. Join the waitlist to hear first.", **WAIT)
S["EA04_traveller"] = dict(layout="ad", sizes=SZ, scene="k06_citadel", kick="Visiting Erbil?",
    h1="A new Kurdish phrase<br>every day", hs=64, sub="Greetings, the bazaar, the restaurant, the taxi: what you need for your trip.", **FOLLOW)
S["EA05_not_hard"] = dict(layout="ad", sizes=SZ, scene="e09_writing", kick="Kurdish isn't that hard",
    h1="Every vowel is written.<br>You read it as it sounds.", hs=58, sub="Start with five words today. Follow us for one phrase a day.", **FOLLOW)
TEAM = "Ask about team orders"
S["EA06_team_arabic"] = dict(layout="ad", sizes=SZ, scene="ea06_team", kick="For NGOs and companies",
    h1="Iraqi Arabic training<br>for your Kurdish team", hs=60, sub="Leen Book 1: 100 lessons from Kurdish to Iraqi Arabic, with native audio. " + TEAM + ".",
    price="24,000", old="29,000", deadline="Special price until 30 November")
S["EA07_onboarding"] = dict(layout="ad", sizes=SZ, scene="ea07_meeting", kick="Mixed teams work better",
    h1="When your team<br>shares a language", hs=64, sub="Help Kurdish staff work confidently with Arabic-speaking partners and clients.",
    price="24,000", old="29,000", deadline="Special price until 30 November")
S["EA08_gift"] = dict(layout="ad", sizes=SZ, scene="ka06_gift", kick="A gift with meaning",
    h1="Give your Kurdish colleague<br>a new language", hs=58, sub="Leen Book 1: from Kurdish to Iraqi Arabic, 100 lessons with native audio.", price="29,000")
S["EA09_per_lesson"] = dict(layout="ad", sizes=SZ, scene="ea06_team", kick="Training on a budget",
    h1="290 IQD per lesson,<br>per employee", hs=62, sub="A 100-lesson course in one book, with audio for every lesson. " + TEAM + ".", price="29,000")
S["EA10_guarantee"] = dict(layout="ad", sizes=SZ, scene="ea07_meeting", kick="Risk-free",
    h1="Try 7 lessons.<br>Not helpful? Get your money back.", hs=56, sub="Leen Book 1 for Kurdish speakers learning Iraqi Arabic.", price="29,000")

json.dump(S, open("spec_enku.json", "w"), ensure_ascii=False, indent=1)
print(len(S) - 1)
