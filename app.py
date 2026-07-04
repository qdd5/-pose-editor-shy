import time
import random

class Character:
    def __init__(self, name, age, relation, personality):
        self.name = name
        self.age = age
        self.relation = relation
        self.lust = 25
        self.mood = "طبيعي"  # طبيعي, خجول, مشتعل, متردد
        self.personality = personality  # "خجولة", "شرموطة", "أمومية"

    def respond(self, action):
        responses = []
        if self.lust < 40:
            responses = ["يا ولدي شو هالكلام...", "أنت مجنون...", "لا... حرام"]
        elif self.lust < 70:
            responses = ["جسمي سخن...", "لا تكلم كذا...", f"تعال قرب يا {self.relation}"]
        else:
            responses = ["خذني...", "أبغى أكثر...", "أنا قحبتك دلوقتي 💦"]
        
        return random.choice(responses)

# الشخصيات
mom = Character("نورة", 40, "الأم", "أمومية")
sis = Character("لين", 18, "الأخت", "خجولة")
aunt = Character("ريم", 28, "الخالة", "شرموطة")

family = {"امي": mom, "اختي": sis, "خالتي": aunt}

def slow_print(text):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(0.025)
    print()

def status():
    print("\n" + "═"*60)
    print(f"رغبتك: {player_lust}/100")
    for name, char in family.items():
        print(f"{name} ({char.name} - {char.age}) | Lust: {char.lust} | Mood: {char.mood}")
    print("═"*60)

player_lust = 40
current_location = "الصالة"

slow_print("🌙 مرحبًا في محاكاة العائلة السعودية - النسخة المطورة 🔥")
slow_print("اكتب ما تريد تفعله (مثال: أقبل أمي، ألمس طيز لين، أقول لخالتي كلام قذر...)")

while True:
    status()
    print(f"\nالمكان الحالي: {current_location}")
    action = input("\nماذا تفعل؟ (اكتب بالعربي): ").strip()
    
    if action.lower() in ["خروج", "exit", "0"]:
        slow_print("يلا مع السلامة يا ابن العائلة 😉")
        break
    
    # تحليل الفعل
    target = None
    if "امي" in action or "نورة" in action:
        target = mom
        char_name = "امي"
    elif "اختي" in action or "لين" in action:
        target = sis
        char_name = "اختي"
    elif "خالتي" in action or "ريم" in action:
        target = aunt
        char_name = "خالتي"
    
    if target:
        slow_print(f"\n→ تتفاعل مع {target.name}...")
        response = target.respond(action)
        slow_print(f"{target.name}: {response}")
        
        # تأثير على Lust
        if any(word in action for word in ["لمس", "قبل", "طيز", "بزاز", "نيك", "قحبة"]):
            target.lust += 22
            player_lust += 18
        elif any(word in action for word in ["كلام", "قول", "دلع"]):
            target.lust += 12
            player_lust += 8
        else:
            target.lust += 8
            player_lust += 5
            
        # تحديث المود
        if target.lust > 70:
            target.mood = "مشتعلة جداً"
        elif target.lust > 45:
            target.mood = "مثارة"
    else:
        slow_print("ما فهمت الفعل... حاول تصف تصرفك بشكل أوضح.")
    
    # كاب
    if player_lust > 100: player_lust = 100
    for char in family.values():
        if char.lust > 100: char.lust = 100

print("\nانتهت الجلسة.")
