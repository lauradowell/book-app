from openai import OpenAI
from PIL import Image
import streamlit as st
import random

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Set page config FIRST
st.set_page_config(page_title="Choose Your Story", layout="centered")

# Initialize page state
if "page" not in st.session_state:
    st.session_state.page = 0
    st.session_state.character = ""
    st.session_state.action = ""
    st.session_state.location = ""
    st.session_state.partner = ""
    st.session_state.story = ""
    st.session_state.random_actions = []
    st.session_state.random_locations = []
    st.session_state.random_partners = []
    st.session_state.language = "en"  # language toggle default

# Custom styling
st.markdown("""
    <style>
        html, body, [class*="css"] {
            background-color: #F8F1E1 !important;
            font-family: "Source Sans Pro", sans-serif !important;
        }
        .stApp { background-color: #F8F1E1 !important; }
        .big-title {
            font-size: 36px;
            font-weight: 700;
            text-align: center;
            margin-top: 30px;
            margin-bottom: 30px;
            color: #333;
        }
        .stButton > button {
            font-size: 18px !important;
            font-weight: bold !important;
            color: black !important;
            background-color: #89CFF0 !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 10px 20px !important;
            margin: 10px !important;
            transition: background-color 0.3s ease !important;
        }
        .stButton > button:hover {
            background-color: #90EE90 !important;
            color: black !important;
        }
    </style>
""", unsafe_allow_html=True)

# Translation dictionary for UI and options
translations = {
    "Pick a character": {"en": "Pick a character", "es": "Elige un personaje"},
    "What will they do?": {"en": "What will they do?", "es": "¿Qué harán?"},
    "Where will they be?": {"en": "Where will they be?", "es": "¿Dónde estarán?"},
    "Who will they be with?": {"en": "Who will they be with?", "es": "¿Con quién estarán?"},
    "Or describe your own character...": {"en": "Or describe your own character...", "es": "O describe tu propio personaje..."},
    "Or write what they'll do...": {"en": "Or write what they'll do...", "es": "O escribe lo que harán..."},
    "Or describe the location:": {"en": "Or describe the location:", "es": "O describe el lugar:"},
    "Or describe the companion:": {"en": "Or describe the companion:", "es": "O describe el compañero:"},
    "Use custom character": {"en": "Use custom character", "es": "Usar personaje personalizado"},
    "Use custom action": {"en": "Use custom action", "es": "Usar acción personalizada"},
    "Use custom location": {"en": "Use custom location", "es": "Usar ubicación personalizada"},
    "Use custom companion": {"en": "Use custom companion", "es": "Usar compañero personalizado"},
    "Generating story...": {"en": "Generating story...", "es": "Generando historia..."},
    "Crafting your story...": {"en": "Crafting your story...", "es": "Creando tu historia..."},
    "Story Time!": {"en": "Story Time!", "es": "¡Hora del cuento!"},
    "Start Over": {"en": "Start Over", "es": "Empezar de nuevo"},
    "✨ Illustration": {"en": "✨ Illustration", "es": "✨ Ilustración"},
    "Switch Language": {"en": "English", "es": "Español"}
}

# Sidebar radio toggle for language
with st.sidebar:
    lang_choice = st.radio("🌐 Language / Idioma", options=["en", "es"], index=0 if st.session_state.language == "en" else 1, format_func=lambda x: "🇬🇧 English" if x == "en" else "🇪🇸 Español")
    st.session_state.language = lang_choice


actions_translated = [
    ("Climb a giant sunflower", "Escalar un girasol gigante"),
    ("Discover a treasure map", "Descubrir un mapa del tesoro"),
    ("Bake a magical cake", "Hornear un pastel mágico"),
    ("Swim in a chocolate river", "Nadar en un río de chocolate"),
    ("Fly using a giant leaf", "Volar usando una hoja gigante"),
    ("Talk to a singing tree", "Hablar con un árbol que canta"),
    ("Catch a falling star", "Atrapar una estrella fugaz"),
    ("Plant a glowing flower", "Plantar una flor brillante"),
    ("Find a sparkling mushroom", "Encontrar un hongo brillante"),
    ("Explore a land made of candy", "Explorar una tierra hecha de dulces")
]

locations_translated = [
    ("A lush jungle", "Una jungla frondosa"),
    ("A sunny beach", "Una playa soleada"),
    ("A magical castle", "Un castillo mágico"),
    ("A floating island", "Una isla flotante"),
    ("A desert of stars", "Un desierto de estrellas"),
    ("A candy forest", "Un bosque de caramelos"),
    ("A city in the clouds", "Una ciudad en las nubes"),
    ("An underwater kingdom", "Un reino submarino"),
    ("A volcano cave", "Una cueva volcánica"),
    ("A meadow of whispers", "Un prado de susurros")
]

companions = [
    {"en": "A robot", "es": "Un robot", "description": "a shiny silver robot with blinking lights and long mechanical arms"},
    {"en": "An ant", "es": "Una hormiga", "description": "a curious little ant wearing glasses and carrying a tiny backpack"},
    {"en": "An astronaut", "es": "Un astronauta", "description": "a brave astronaut with a star-covered helmet and glowing boots"},
    {"en": "A dragon", "es": "Un dragón", "description": "a playful green dragon with glittery wings and a gentle smile"},
    {"en": "A fairy", "es": "Un hada", "description": "a tiny fairy with sparkly wings, pink hair, and a glowing wand"},
    {"en": "A turtle", "es": "Una tortuga", "description": "a slow but wise turtle wearing a wizard's hat and glasses"},
    {"en": "A lion", "es": "Un león", "description": "a noble lion with a golden mane, wearing a crown and cape"},
    {"en": "A penguin", "es": "Un pingüino", "description": "a waddling penguin with a scarf, goggles, and snow boots"},
    {"en": "A squirrel", "es": "Una ardilla", "description": "a chattering squirrel with fluffy fur and a nut pouch"},
    {"en": "A unicorn", "es": "Un unicornio", "description": "a magical unicorn with a rainbow horn and shimmering tail"},
    {"en": "A raccoon", "es": "Un mapache", "description": "a sneaky raccoon with a striped mask and treasure map"},
    {"en": "A dolphin", "es": "Un delfín", "description": "a friendly dolphin with a seashell necklace and splashy tail"},
    {"en": "A witch", "es": "Una bruja", "description": "a clever witch with a crooked hat and a broom made of stars"},
    {"en": "A monkey", "es": "Un mono", "description": "a silly monkey with sunglasses and a banana-shaped guitar"},
    {"en": "A kangaroo", "es": "Un canguro", "description": "a bouncy kangaroo with boxing gloves and a satchel full of maps"},
    {"en": "A cat", "es": "Un gato", "description": "a curious cat with a bow tie and glowing green eyes"},
    {"en": "A robot dog", "es": "Un perro robot", "description": "a robotic dog with jet paws and a glowing tail"},
    {"en": "A snowman", "es": "Un muñeco de nieve", "description": "a cheerful snowman with a carrot nose, scarf, and mittens"},
    {"en": "A bee", "es": "Una abeja", "description": "a buzzing bee with a crown and a honeycomb shield"},
    {"en": "A cloud", "es": "Una nube", "description": "a fluffy cloud wearing a rainbow sash and raining sparkles"},
    {"en": "A wizard", "es": "Un mago", "description": "a wise old wizard with a starry cloak and a glowing orb"},
    {"en": "A painter", "es": "Un pintor", "description": "a joyful painter with a beret, rainbow brush, and messy apron"},
    {"en": "A ghost", "es": "Un fantasma amistoso", "description": "a friendly ghost wearing a bowtie and floating gently"},
    {"en": "A pirate", "es": "Un pirata", "description": "a jolly pirate with a parrot and a wooden leg"},
    {"en": "A knight", "es": "Un caballero", "description": "a shiny knight in heart-shaped armor and a feather plume"},
    {"en": "A bat", "es": "Un murciélago", "description": "a sleepy bat with purple wings and tiny headphones"},
    {"en": "A cloud sheep", "es": "Una oveja de nube", "description": "a sheep made of clouds with tiny wings and sleepy eyes"},
    {"en": "A fox", "es": "Un zorro", "description": "a sneaky fox with a cape, monocle, and cane"},
    {"en": "A giraffe", "es": "Una jirafa", "description": "a tall giraffe with a flower crown and telescope"},
    {"en": "A jellyfish", "es": "Una medusa", "description": "a glowing jellyfish with rainbow tentacles and glasses"}
]


def t(label):
    lang = st.session_state.get("language", "en")
    return translations.get(label, {}).get(lang, label)

def option_buttons(options, key_prefix, store_key):
    lang = st.session_state.get("language", "en")
    cols = st.columns(len(options))
    for idx, (value_en, value_es) in enumerate(options):
        display = value_es if lang == "es" else value_en
        with cols[idx]:
            if st.button(display, key=f"{key_prefix}_{idx}"):
                st.session_state[store_key] = value_en
                st.session_state.page += 1

def translate_story(text):
    if st.session_state.language == "en":
        return text
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional translator who preserves the whimsical and magical tone of children's stories."},
                {"role": "user", "content": f"Translate this story to Spanish: {text}"}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception:
        return text  # fallback if translation fails


# PAGE 0 — Pick a character
if st.session_state.page == 0:
    st.markdown(f"<div class='big-title'>👧 {t('Pick a character')}</div>", unsafe_allow_html=True)
    st.image(Image.open("images/characters.png"), use_container_width=True)

    characters = [
        ("Peter", "Pedro"),
        ("Red Riding Hood", "Caperucita Roja"),
        ("Mr. Rabbit", "Señor Conejo"),
        ("Rapunzel", "Rapunzel")
    ]
    option_buttons(characters, "char", "character")

    custom = st.text_input(t("Or describe your own character..."))
    if st.button(t("Use custom character")):
        if custom.strip():
            st.session_state.character = custom.strip()
            st.session_state.page += 1

# PAGE 1 — What will they do?
elif st.session_state.page == 1:
    st.markdown(f"<div class='big-title'>🧪 {t('What will they do?')}</div>", unsafe_allow_html=True)

    if not st.session_state.random_actions:
        st.session_state.random_actions = random.sample(actions_translated, 3)

    option_buttons(st.session_state.random_actions, "act", "action")

    custom = st.text_input(t("Or write what they'll do..."))
    if st.button(t("Use custom action")):
        if custom.strip():
            st.session_state.action = custom.strip()
            st.session_state.page += 1

# PAGE 2 — Where will they be?
elif st.session_state.page == 2:
    st.markdown(f"<div class='big-title'>🌍 {t('Where will they be?')}</div>", unsafe_allow_html=True)

    if not st.session_state.random_locations:
        st.session_state.random_locations = random.sample(locations_translated, 3)

    option_buttons(st.session_state.random_locations, "loc", "location")

    custom = st.text_input(t("Or describe the location:"))
    if st.button(t("Use custom location")):
        if custom.strip():
            st.session_state.location = custom.strip()
            st.session_state.page += 1



# PAGE 3 — Who will they be with?
elif st.session_state.page == 3:
    st.markdown(f"<div class='big-title'>🧑‍🚀 {t('Who will they be with?')}</div>", unsafe_allow_html=True)

    # Generate random companions only once
    if not st.session_state.random_partners:
        st.session_state.random_partners = random.sample(companions, 3)

    # Display translated options
    options = [(comp["en"], comp["es"]) for comp in st.session_state.random_partners]

    option_buttons(options, "comp", "partner")

    # Custom companion input
    custom = st.text_input(t("Or describe the companion:"))
    if st.button(t("Use custom companion")):
        if custom.strip():
            st.session_state.partner = custom.strip()
            st.session_state.page += 1


# PAGE 4 — Generate story
elif st.session_state.page == 4:
    st.title(t("Generating story..."))
    with st.spinner(t("Crafting your story...")):
        # Get companion description from the new structure
        partner_desc = next(
            (c["description"] for c in companions if c["en"] == st.session_state.partner),
            st.session_state.partner
        )

        prompt = f"""
        Write a short and imaginative children's story (under 300 words) with this structure:

        1. ✨ Begin by introducing a character named {st.session_state.character}.
        2. 🧱 They go on an adventure to {st.session_state.action}, in {st.session_state.location}, with their companion {partner_desc}.
        3. 🚧 During the adventure, they encounter a small problem or obstacle that is appropriate for young children.
        4. 🎉 Show how they solve the problem using creativity, kindness, or teamwork.
        5. 💡 End with a heartwarming and simple lesson that children can easily understand.

        Please use gender-neutral language (like "they/them"), and keep the tone playful, magical, and suited for children aged 5–9.
        """

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a friendly and imaginative children's storyteller."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.9,
                max_tokens=1000
            )
            full_story = response.choices[0].message.content
            st.session_state.story = full_story

            st.session_state.random_actions = []
            st.session_state.random_locations = []
            st.session_state.random_partners = []

            image_prompt = (
                f"Children's book illustration in watercolor style, "
                f"showing a scene from this story: {full_story[:500]}. "
                "The image should visually represent the story, but must not contain any text, writing, letters, or captions."
            )

            image_response = client.images.generate(
                model="dall-e-3",
                prompt=image_prompt,
                size="1024x1024",
                quality="standard",
                n=1
            )
            st.session_state.story_image_url = image_response.data[0].url

            st.session_state.page = 5
            st.rerun()

        except Exception as e:
            st.error(f"Something went wrong: {e}")


# PAGE 5 — Show story
elif st.session_state.page == 5:
    st.title(t("Story Time!"))

    if st.session_state.get("story_image_url"):
        st.image(st.session_state.story_image_url, caption=t("✨ Illustration"), use_container_width=True)

    translated_story = translate_story(st.session_state.story)
    st.markdown(translated_story)

    if st.button(t("Start Over")):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
