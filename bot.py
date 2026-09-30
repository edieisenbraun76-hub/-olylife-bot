# -*- coding: utf-8 -*-
"""
OLYLIFE Info- & Bestellbot (Deutsch) — Version 3.0
===================================================
NEU: Kein images-Ordner noetig! Fotos werden direkt im Bot gespeichert:
     1. Bot starten
     2. Als Admin /setup senden
     3. Produkt waehlen -> Foto aus der Galerie senden (6x)
     Fertig! Der Bot merkt sich alle Fotos.

Vor dem Start eintragen:
    1) BOT_TOKEN        -> "8975184474:AAE8eQ5pZztF1Oxb7son3KpmK9tPcSHRPUI"
    2) ADMIN_ID         -> "710161270"
    3) ADMIN_WHATSAPP   -> Ihre WhatsApp-Nummer, Format4917660409847 (ohne +)
"""

import os
import json
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import (
    Message, CallbackQuery,
    InlineKeyboardMarkup, InlineKeyboardButton,
)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

import asyncio

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ================== KONFIGURATION ==================
BOT_TOKEN = "HIER_TOKEN_EINTRAGEN"
ADMIN_ID = 123456789
ADMIN_WHATSAPP = "49XXXXXXXXXX"

# ================== FOTO-SPEICHER (automatisch) ==================
PHOTO_FILE = os.path.join(BASE_DIR, "photo_map.json")

def load_photos():
    if os.path.exists(PHOTO_FILE):
        try:
            with open(PHOTO_FILE, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_photos():
    with open(PHOTO_FILE, "w", encoding="utf-8") as f:
        json.dump(PHOTOS, f)

PHOTOS = load_photos()

# ================== INHALT (DEUTSCH) ==================

START_TEXT = """Willkommen beim OlyLife Bot! 🌿

Entdecken Sie innovative Gesundheits- und Beauty-Technologien von OlyLife – PEMF, Terahertz und mehr – alles an einem Ort.

Worum möchten Sie mehr erfahren? 👇"""

ABOUT_TEXT = """🏢 Über OlyLife

OlyLife (OLYLIFE LIMITED) wurde 2022 gegründet. Hauptsitz: Hongkong, mit Standorten in Malaysia (Kuala Lumpur, Johor).

🎯 Mission: „Gesundheit durch Technologie".

💡 Kerntechnologien:
• PEMF (Pulsed Electromagnetic Field) – magnetfeldgestützte Zell-Aktivierung
• Terahertz-Energie (3–3000 μm) – „das Licht des Lebens", dringt bis zu 4–5 cm unter die Haut ein und unterstützt die Mikrozirkulation
• Bama-Konzept – ganzheitlicher Ansatz: gesundes Wasser + Gesundheitsgeräte
• IoT, Big Data & KI als technologische Basis des Ökosystems

Neu: Die OTRALIFE-Linie (2026–2027) – Brillen, Wärme-Pflegegeräte und Wasserstoff-Wasser-Produkte."""

PRODUCTS = {
    "p90": {
        "name": "Tera-P90",
        "desc": """💠 Tera-P90

Das Flaggschiff: Fußtherapie-Gerät mit PEMF + Terahertz-Technologie.

✔ Unterstützt die Mikrozirkulation
✔ Entspannung und Wohlbefinden
✔ Einfache Anwendung zu Hause – täglich nur wenige Minuten

Preis: ca. 1.000 USD"""
    },
    "p90plus": {
        "name": "Tera-P90+",
        "desc": """💠 Tera-P90+ (All-in-One-Set)

Alles in einem Paket:
• Tera-P90 (PEMF + Terahertz Fußtherapie)
• Frost Age Beauty Device (RF + EMS Anti-Aging)
• Revitaluxe Massager
• Pflege-Gels

Die komplette Lösung für Körper- und Hautpflege."""
    },
    "gone": {
        "name": "Galaxy G-One",
        "desc": """💠 Galaxy G-One

Intelligentes Augen-Massagegerät mit PEMF-Technologie.

✔ 7 Pflegemodi
✔ Entspannung für müde Augen
✔ Modernes, tragbares Design

Preis: ca. 500 USD"""
    },
    "shaken": {
        "name": "Shaken",
        "desc": """💠 Shaken – Körper- & Skulptur-Massagegerät

✔ Ultraschall
✔ Radiofrequenz (RF)
✔ Vibration & rotes Licht
✔ KI-gestützte Personalisierung

Für Körperpflege und ein strafferes Hautbild."""
    },
    "bamaair": {
        "name": "A9 BamaAir",
        "desc": """💠 A9 BamaAir – Luftreiniger

✔ Effiziente Luftreinigung
✔ Anionen-Technologie (negative Ionen)
✔ App-Steuerung & Licht-Rhythmus
✔ Für Wohn- und Schlafbereiche

Frische, saubere Luft für Ihr Zuhause."""
    },
    "wand": {
        "name": "Vitality Wand",
        "desc": """💠 Vitality Wand

Tragbares, handliches Terahertz-Therapiegerät im edlen Koffer-Set.

✔ Kompakt – für unterwegs
✔ Einfache Punkt-Anwendung
✔ Ergänzung zum Tera-P90"""
    },
}

PLAN_INTRO = """💎 OlyLife Business – Schritt für Schritt

Der OlyLife-Vergütungsplan basiert auf einem Binärsystem mit 2 Teams (links & rechts). Sie verdienen an Ihren eigenen Empfehlungen UND am Wachstum Ihres Teams.

Wählen Sie ein Thema: 👇"""

PLAN_STEP1 = """📌 SCHRITT 1 – Einstieg: Die 3 Pakete

1️⃣ P3 – $1.000-Paket
   • Persönliches Volumen: 750 PV
   • Binär-Rate: 11% | Tageslimit: $1.000
   • Tier-Bonus: $375

2️⃣ P4 – $2.000-Paket
   • Persönliches Volumen: 1.500 PV
   • Binär-Rate: 12% | Tageslimit: $2.000
   • Tier-Bonus: $750

3️⃣ P5 – $6.000-Paket
   • Persönliches Volumen: 4.500 PV
   • Binär-Rate: 13% | Tageslimit: $7.000
   • Tier-Bonus: $2.250

📌 Alle Pakete qualifizieren für ALLE Bonustypen. Upgrade jederzeit möglich."""

PLAN_STEP2 = """📌 SCHRITT 2 – Sofort verdienen: Fast Start

🚀 Fast-Start-Bonus: 10% des PV jeder direkten Empfehlung – SOFORT nach der Registrierung Ihres Neupartners.

Beispiel: Ein P3-Paket (750 PV) → $75 Fast Start sofort für Sie."""

PLAN_STEP3 = """📌 SCHRITT 3 – Binär-Provision (Performance Bonus)

Das Herzstück: Ihr Team wächst in 2 Beinen (links/rechts).

✔ Sie erhalten 11–13% (je nach Paket) des Volumens der SCHWÄCHEREN Seite
✔ Tageslimit: $1.000 / $2.000 / $7.000 (je nach Paket)
✔ Umsatz der stärkeren Seite wird übertragen (kein Verlust)

💡 Tipp: Balance beider Beine = maximaler Bonus."""

PLAN_STEP4 = """📌 SCHRITT 4 – Tier Bonus (Level-Matching)

Für jedes neue Tier (Ebene) in Ihrer Struktur:

✔ P3: $375 | P4: $750 | P5: $2.250
✔ KEINE Begrenzung der Anzahl und der Ebenen!

Je tiefer Ihr Team wächst, desto mehr Tier-Boni laufen automatisch auf Ihr Konto."""

PLAN_STEP5 = """📌 SCHRITT 5 – Team Bonus & Coaching Bonus

👥 Team Bonus:
✔ 5% auf die Boni Ihres Placement-Uplines – bis zu 3x (max. $4.050)
✔ Level 1: 10% deren Boni
✔ Level 2: 5% | Level 3: 5%

🎓 Coaching Bonus:
✔ 10% auf Stufe 1 (direkte Partner)
✔ 5% auf Stufe 2–6
✔ Voraussetzung: mindestens 3 direkt gesponserte Personen"""

PLAN_STEP6 = """📌 SCHRITT 6 – Führungsboni (für Leader)

👑 Leadership Bonus: 3–10% über den OlyMall

🌍 Globaler Pool & Jahresbonus:
✔ Global Pool ab 14L + 14R
✔ Jahresbonus: 5% des weltweiten PV – wird an Top-Performer verteilt"""

PLAN_EXAMPLE = """🧮 Beispiel-Rechnung (P3-Paket)

Sie bringen 2 Partner (je P3, 750 PV):
→ Fast Start: 2 × $75 = $150

Ihre Struktur wächst auf 7 / 15 PV links/rechts:
→ Performance Bonus: bis zu $135/Tag

Dazu Tier-Boni je neuer Ebene + Team-Boni...

⚠️ Wichtig: Einkommen ist niemals garantiert. Ergebnisse hängen von persönlichem Einsatz, Teamleistung und Marktbedingungen ab."""

CAREER_TEXT = """🚀 Ihr Einstieg – so einfach geht's

1️⃣ Kontakt aufnehmen – schreiben Sie uns über den Kontakt-Button
2️⃣ Kostenlose Beratung – wir erklären den Plan persönlich
3️⃣ Paket wählen – P3, P4 oder P5
4️⃣ Registrierung – Online in wenigen Minuten
5️⃣ Loslegen – mit Schulungen, Webinaren und persönlichem Coaching

🌍 Global tätig – von überall aus, flexibel in Zeit und Ort."""

FAQ = {
    "Was ist PEMF?": "PEMF steht für Pulsed Electromagnetic Field. Dabei werden niederfrequente elektromagnetische Impulse eingesetzt, um das allgemeine Wohlbefinden und die Entspannung zu unterstützen.",
    "Was ist Terahertz-Technologie?": "Terahertz-Wellen (3–3000 μm) werden auch als das 'Licht des Lebens' bezeichnet. Sie dringen bis zu 4–5 cm unter die Haut ein und unterstützen die Mikrozirkulation.",
    "Wo kann ich Produkte bestellen?": "Über den Button 'Jetzt bestellen' beim jeweiligen Produkt. Ihre Anfrage geht direkt an unseren Berater, der sich umgehend bei Ihnen meldet.",
    "Gibt es ein Partnerprogramm?": "Ja! OlyLife bietet einen binären Vergütungsplan mit 6+ Bonustypen. Alle Details finden Sie unter 'Business'.",
    "Woran arbeitet OlyLife in Zukunft?": "Die neue OTRALIFE-Linie (2026–2027): Brillen, Wärme-Pflegegeräte sowie Wasserstoff-Wasser-Produkte – Innovationen rund um Gesundheit und Beauty.",
    "Ist ein Einkommen garantiert?": "Nein. Wie bei jedem Geschäft hängen die Ergebnisse von Ihrem Einsatz, Ihrem Team und dem Markt ab. Seriöse Berater versprechen niemals garantierte Gewinne.",
}

CONTACT_TEXT = """📞 Kontakt & Beratung

Schreiben Sie uns direkt – wir beraten Sie persönlich und unverbindlich:

• WhatsApp: https://wa.me/{wa}

Oder nutzen Sie den 'Bestellen'-Button bei jedem Produkt."""

# ================== TASTATUREN ==================

def kb_main() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏢 Über OlyLife", callback_data="about")],
        [InlineKeyboardButton(text="💠 Produkte & Technologien", callback_data="products")],
        [InlineKeyboardButton(text="💎 Business & Marketingplan", callback_data="plan")],
        [InlineKeyboardButton(text="🪬 Häufige Fragen (FAQ)", callback_data="faq")],
        [InlineKeyboardButton(text="📞 Kontakt", callback_data="contact")],
    ])

def kb_products() -> InlineKeyboardMarkup:
    rows = [[InlineKeyboardButton(text=f"💠 {p['name']}", callback_data=f"prod_{k}")]
            for k, p in PRODUCTS.items()]
    rows.append([InlineKeyboardButton(text="⬅️ Zurück", callback_data="back_main")])
    return InlineKeyboardMarkup(inline_keyboard=rows)

def kb_product(key: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📦 Jetzt bestellen", callback_data=f"order_{key}")],
        [InlineKeyboardButton(text="⬅️ Alle Produkte", callback_data="products")],
    ])

def kb_plan() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📌 Schritt 1: Die 3 Pakete", callback_data="plan_s1")],
        [InlineKeyboardButton(text="🚀 Schritt 2: Fast Start (10%)", callback_data="plan_s2")],
        [InlineKeyboardButton(text="⚖️ Schritt 3: Binär-Provision", callback_data="plan_s3")],
        [InlineKeyboardButton(text="🏆 Schritt 4: Tier Bonus", callback_data="plan_s4")],
        [InlineKeyboardButton(text="👥 Schritt 5: Team- & Coaching Bonus", callback_data="plan_s5")],
        [InlineKeyboardButton(text="👑 Schritt 6: Führungsboni", callback_data="plan_s6")],
        [InlineKeyboardButton(text="🧮 Beispiel-Rechnung", callback_data="plan_ex")],
        [InlineKeyboardButton(text="🚀 Jetzt einsteigen", callback_data="plan_career")],
        [InlineKeyboardButton(text="⬅️ Zurück", callback_data="back_main")],
    ])

def kb_faq() -> InlineKeyboardMarkup:
    rows = [[InlineKeyboardButton(text=q, callback_data=f"faq_{i}")]
            for i, q in enumerate(FAQ.keys())]
    rows.append([InlineKeyboardButton(text="⬅️ Zurück", callback_data="back_main")])
    return InlineKeyboardMarkup(inline_keyboard=rows)

def kb_contact() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💬 WhatsApp schreiben", url=f"https://wa.me/{ADMIN_WHATSAPP}")],
        [InlineKeyboardButton(text="⬅️ Zurück", callback_data="back_main")],
    ])

def kb_order_confirm(key: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Bestellung bestätigen", callback_data=f"confirm_{key}")],
        [InlineKeyboardButton(text="❌ Abbrechen", callback_data="cancel_order")],
    ])

def kb_setup() -> InlineKeyboardMarkup:
    rows = []
    for k, p in PRODUCTS.items():
        mark = "✅ " if k in PHOTOS else ""
        rows.append([InlineKeyboardButton(text=f"{mark}📷 {p['name']}", callback_data=f"setup_{k}")])
    rows.append([InlineKeyboardButton(text="✅ Fertig", callback_data="setup_done")])
    return InlineKeyboardMarkup(inline_keyboard=rows)

# ================== STATUS ==================

class OrderStates(StatesGroup):
    name = State()
    phone = State()

class SetupStates(StatesGroup):
    waiting_photo = State()

# ================== HANDLER ==================

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(START_TEXT, reply_markup=kb_main())

@dp.callback_query(F.data == "back_main")
async def back_main(cb: CallbackQuery):
    await cb.message.answer(START_TEXT, reply_markup=kb_main())
    await cb.answer()

@dp.callback_query(F.data == "about")
async def show_about(cb: CallbackQuery):
    await cb.message.edit_text(ABOUT_TEXT, reply_markup=kb_main())

@dp.callback_query(F.data == "products")
async def show_products(cb: CallbackQuery):
    await cb.message.edit_text("💠 Unsere Produkte – wählen Sie eines aus:",
                               reply_markup=kb_products())

@dp.callback_query(F.data.startswith("prod_"))
async def show_product(cb: CallbackQuery):
    key = cb.data.split("_", 1)[1]
    p = PRODUCTS[key]
    if key in PHOTOS:
        await cb.message.answer_photo(PHOTOS[key], caption=p["desc"],
                                      reply_markup=kb_product(key))
    else:
        await cb.message.answer(p["desc"], reply_markup=kb_product(key))
    await cb.answer()

@dp.callback_query(F.data == "plan")
async def show_plan(cb: CallbackQuery):
    await cb.message.edit_text(PLAN_INTRO, reply_markup=kb_plan())

@dp.callback_query(F.data.startswith("plan_s"))
async def show_plan_step(cb: CallbackQuery):
    steps = {
        "plan_s1": PLAN_STEP1, "plan_s2": PLAN_STEP2, "plan_s3": PLAN_STEP3,
        "plan_s4": PLAN_STEP4, "plan_s5": PLAN_STEP5, "plan_s6": PLAN_STEP6,
    }
    await cb.message.edit_text(steps[cb.data], reply_markup=kb_plan())

@dp.callback_query(F.data == "plan_ex")
async def show_plan_example(cb: CallbackQuery):
    await cb.message.edit_text(PLAN_EXAMPLE, reply_markup=kb_plan())

@dp.callback_query(F.data == "plan_career")
async def show_plan_career(cb: CallbackQuery):
    await cb.message.edit_text(CAREER_TEXT, reply_markup=kb_plan())

@dp.callback_query(F.data == "faq")
async def show_faq(cb: CallbackQuery):
    await cb.message.edit_text("🪬 Häufige Fragen – wählen Sie eine Frage:",
                               reply_markup=kb_faq())

@dp.callback_query(F.data.startswith("faq_"))
async def show_faq_answer(cb: CallbackQuery):
    i = int(cb.data.split("_", 1)[1])
    q = list(FAQ.keys())[i]
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Zurück zu den Fragen", callback_data="faq")],
    ])
    await cb.message.edit_text(f"❓ {q}\n\n{FAQ[q]}", reply_markup=kb)

@dp.callback_query(F.data == "contact")
async def show_contact(cb: CallbackQuery):
    await cb.message.edit_text(CONTACT_TEXT.format(wa=ADMIN_WHATSAPP),
                               reply_markup=kb_contact())

# ----- FOTO-SETUP (Admin) -----
@dp.message(Command("setup"))
async def cmd_setup(message: Message):
    if message.from_user.id != ADMIN_ID:
        return
    await message.answer("📷 Foto-Setup\n\nWählen Sie ein Produkt und senden "
                         "Sie dann das Foto dafür (aus Ihrer Galerie). "
                         "✅ = Foto bereits gespeichert.",
                         reply_markup=kb_setup())

@dp.callback_query(F.data.startswith("setup_"))
async def setup_pick(cb: CallbackQuery, state: FSMContext):
    if cb.from_user.id != ADMIN_ID:
        await cb.answer("Nur für Admin!", show_alert=True)
        return
    if cb.data == "setup_done":
        await cb.message.edit_text("✅ Foto-Setup abgeschlossen!", reply_markup=kb_main())
        await state.clear()
        return
    key = cb.data.split("_", 1)[1]
    await state.update_data(setup_product=key)
    await state.set_state(SetupStates.waiting_photo)
    await cb.message.edit_text(f"📷 Senden Sie jetzt das Foto für: {PRODUCTS[key]['name']}")
    await cb.answer()

@dp.message(SetupStates.waiting_photo, F.photo)
async def setup_photo(message: Message, state: FSMContext):
    data = await state.get_data()
    key = data.get("setup_product")
    if not key:
        await state.clear()
        return
    PHOTOS[key] = message.photo[-1].file_id
    save_photos()
    await state.clear()
    await message.answer(f"✅ Foto für {PRODUCTS[key]['name']} gespeichert!\n\nNächstes Produkt wählen:",
                         reply_markup=kb_setup())

@dp.message(SetupStates.waiting_photo)
async def setup_not_photo(message: Message):
    await message.answer("⚠️ Bitte senden Sie ein FOTO (nicht als Datei, nicht als Text).\n\n"
                         "Tipp: Galerie öffnen → Foto wählen → als Foto senden.")

# ----- Bestellablauf -----
@dp.callback_query(F.data.startswith("order_"))
async def order_start(cb: CallbackQuery, state: FSMContext):
    key = cb.data.split("_", 1)[1]
    await state.update_data(product=key)
    await state.set_state(OrderStates.name)
    await cb.message.answer("📦 Bestellung aufgeben\n\nBitte geben Sie Ihren Vor- und Nachnamen ein:")
    await cb.answer()

@dp.message(OrderStates.name)
async def order_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text.strip())
    await state.set_state(OrderStates.phone)
    await message.answer("☎️ Bitte geben Sie Ihre Telefonnummer ein "
                         "(inkl. Ländervorwahl, z. B. +49170XXXXXXX):")

@dp.message(OrderStates.phone)
async def order_phone(message: Message, state: FSMContext):
    phone = message.text.strip()
    data = await state.get_data()
    data["phone"] = phone
    p = PRODUCTS[data["product"]]
    await state.update_data(phone=phone)
    await state.set_state(None)
    summary = (f"🧾 Ihre Bestellung:\n\n"
               f"Produkt: {p['name']}\n"
               f"Name: {data['name']}\n"
               f"Telefon: {phone}\n\n"
               f"Bitte bestätigen Sie die Bestellung:")
    await message.answer(summary, reply_markup=kb_order_confirm(data["product"]))

@dp.callback_query(F.data.startswith("confirm_"))
async def order_confirm(cb: CallbackQuery, state: FSMContext):
    key = cb.data.split("_", 1)[1]
    data = await state.get_data()
    name, phone = data.get("name", "?"), data.get("phone", "?")
    p = PRODUCTS[key]
    wa_digits = "".join(ch for ch in phone if ch.isdigit())
    wa_link = f"https://wa.me/{wa_digits}"
    admin_msg = (f"🆕 NEUE BESTELLUNG\n\n"
                 f"Produkt: {p['name']}\n"
                 f"Kunde: {name}\n"
                 f"Telefon: {phone}\n"
                 f"Telegram-Kunde: @{cb.from_user.username or 'kein'}\n\n"
                 f"👉 Kunde per WhatsApp kontaktieren: {wa_link}")
    try:
        await bot.send_message(ADMIN_ID, admin_msg)
    except Exception:
        pass
    await state.clear()
    await cb.message.answer(
        "✅ Vielen Dank für Ihre Bestellung!\n\n"
        "Unser Berater wird sich in Kürze bei Ihnen melden.\n"
        "Bei Fragen erreichen Sie uns unter 'Kontakt'.",
        reply_markup=kb_main())

@dp.callback_query(F.data == "cancel_order")
async def order_cancel(cb: CallbackQuery, state: FSMContext):
    await state.clear()
    await cb.message.edit_text("❌ Bestellung abgebrochen.", reply_markup=kb_main())

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
