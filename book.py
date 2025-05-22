from openai import OpenAI
from PIL import Image
import streamlit as st
import streamlit.components.v1 as components
import random

partner_traits = {
    "A robot": "a shiny silver robot with blinking lights and long mechanical arms",
    "An ant": "a curious little ant wearing glasses and carrying a tiny backpack",
    "An astronaut": "a brave astronaut with a star-covered helmet and glowing boots",
    "A dragon": "a playful green dragon with glittery wings and a gentle smile",
    "A fairy": "a tiny fairy with sparkly wings, pink hair, and a glowing wand",
    "A turtle": "a slow but wise turtle wearing a wizard's hat and glasses",
    "A lion": "a noble lion with a golden mane, wearing a crown and cape",
    "A penguin": "a waddling penguin with a scarf, goggles, and snow boots",
    "A squirrel": "a chattering squirrel with fluffy fur and a nut pouch",
    "A unicorn": "a magical unicorn with a rainbow horn and shimmering tail",
    "A raccoon": "a sneaky raccoon with a striped mask and treasure map",
    "A dolphin": "a friendly dolphin with a seashell necklace and splashy tail",
    "A witch": "a clever witch with a crooked hat and a broom made of stars",
    "A monkey": "a silly monkey with sunglasses and a banana-shaped guitar",
    "A kangaroo": "a bouncy kangaroo with boxing gloves and a satchel full of maps",
    "A cat": "a curious cat with a bow tie and glowing green eyes",
    "A robot dog": "a robotic dog with jet paws and a glowing tail",
    "A snowman": "a cheerful snowman with a carrot nose, scarf, and mittens",
    "A bee": "a buzzing bee with a crown and a honeycomb shield",
    "A cloud": "a fluffy cloud wearing a rainbow sash and raining sparkles",
    "A wizard": "a wise old wizard with a starry cloak and a glowing orb",
    "A painter": "a joyful painter with a beret, rainbow brush, and messy apron",
    "A ghost": "a friendly ghost wearing a bowtie and floating gently",
    "A pirate": "a jolly pirate with a parrot and a wooden leg",
    "A knight": "a shiny knight in heart-shaped armor and a feather plume",
    "A bat": "a sleepy bat with purple wings and tiny headphones",
    "A cloud sheep": "a sheep made of clouds with tiny wings and sleepy eyes",
    "A fox": "a sneaky fox with a cape, monocle, and cane",
    "A giraffe": "a tall giraffe with a flower crown and telescope",
    "A jellyfish": "a glowing jellyfish with rainbow tentacles and glasses"
}


client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
st.set_page_config(page_title="Choose Your Story", layout="centered")

# Styles
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
            transition: 0.3s ease !important;
        }
        .stButton > button:hover {
            background-color: #90EE90 !important;
            color: black !important;
        }
    </style>
""", unsafe_allow_html=True)

# Init session state
if "page" not in st.session_state:
    st.session_state.page = 0
    st.session_state.character = ""
    st.session_state.action = ""
    st.session_state.location = ""
    st.session_state.partner = ""
    st.session_state.story = ""
    st.session_state.random_actions = []

def next_page():
    st.session_state.page += 1

def option_buttons(options, key_prefix, store_key):
    cols = st.columns(len(options))
    for idx, (label, value) in enumerate(options):
        with cols[idx]:
            if st.button(label, key=f"{key_prefix}_{idx}"):
                st.session_state[store_key] = value
                next_page()
                

# PAGE 0
if st.session_state.page == 0:
    st.markdown('<div class="big-title">👧 Pick a character</div>', unsafe_allow_html=True)
    st.image(Image.open("images/characters.png"), use_container_width=True)

    characters = [("Peter", "Peter"), ("Red Riding Hood", "Red Riding Hood"),
                  ("Mr. Rabbit", "Mr. Rabbit"), ("Rapunzel", "Rapunzel")]
    option_buttons(characters, "char", "character")

    custom = st.text_input("Or describe your own character...")
    if st.button("Use custom character"):
        if custom.strip():
            st.session_state.character = custom.strip()
            next_page()

# PAGE 1
elif st.session_state.page == 1:
    st.markdown('<div class="big-title">🧪 What will they do?</div>', unsafe_allow_html=True)

    # Generate 3 random actions only once per new story
    if not st.session_state.random_actions:
        all_actions = [
            "Climb a giant sunflower",
            "Discover a treasure map",
            "Bake a magical cake",
            "Swim in a chocolate river",
            "Fly using a giant leaf",
            "Talk to a singing tree",
            "Catch a falling star",
            "Plant a glowing flower",
            "Find a sparkling mushroom",
            "Explore a land made of candy",
            "Build a house in the sky",
            "Skate across rainbow ice",
            "Read a book that talks back",
            "Sail a leaf boat across a puddle",
            "Bounce on jelly mountains",
            "Make a wish on a firefly",
            "Paint the sky with colors",
            "Slide down a moonbeam",
            "Climb a floating staircase",
            "Dance on a cloud",
            "Follow a trail of golden pebbles",
            "Build a tower from bubbles",
            "Dig for hidden crystals",
            "Hop across giant lilypads",
            "Collect glowing pebbles",
            "Invent a flying umbrella",
            "Chase your reflection in a lake",
            "Spin a story into the wind",
            "Ride a wave of music",
            "Open a door in a tree trunk"

        ]
        st.session_state.random_actions = random.sample(all_actions, 3)

    options = [(a, a) for a in st.session_state.random_actions]
    option_buttons(options, "act", "action")

    custom = st.text_input("Or write what they'll do...")
    if st.button("Use custom action"):
        if custom.strip():
            st.session_state.action = custom.strip()
            next_page()

# PAGE 2
elif st.session_state.page == 2:
    st.markdown('<div class="big-title">🌍 Where will they be?</div>', unsafe_allow_html=True)

    if "random_locations" not in st.session_state:
        all_locations = [
            "A lush jungle", "A sunny beach", "A magical castle", "A floating island", "A desert of stars",
            "A candy forest", "A city in the clouds", "An underwater kingdom", "A volcano cave", "A meadow of whispers",
            "A frozen palace", "A talking mountain", "A rainbow bridge", "A library made of leaves", "A time-travel town",
            "A jungle of mirrors", "A village of clocks", "A pumpkin village", "A land of bouncing pillows", "A treehouse village",
            "A glowing cave", "A sleepy valley", "A music waterfall", "A moonlit meadow", "A marshmallow swamp",
            "A spiral staircase forest", "A sky pirate ship", "A hidden glade", "A spinning island", "A mushroom meadow"
        ]
        st.session_state.random_locations = random.sample(all_locations, 3)

    locations = [(loc, loc) for loc in st.session_state.random_locations]
    option_buttons(locations, "loc", "location")

    custom = st.text_input("Or describe the location:")
    if st.button("Use custom location"):
        if custom.strip():
            st.session_state.location = custom.strip()
            next_page()


# PAGE 3
elif st.session_state.page == 3:
    st.markdown('<div class="big-title">🧑‍🚀 Who will they be with?</div>', unsafe_allow_html=True)

    # Only generate new partners if they haven't been generated yet
    if not st.session_state.get("random_partners"):
        all_partners = list(partner_traits.keys())
        st.session_state.random_partners = random.sample(all_partners, 3)

    # Use stored partners for button display
    partners = [(p, p) for p in st.session_state.random_partners]
    option_buttons(partners, "comp", "partner")

    custom = st.text_input("Or describe the companion:")
    if st.button("Use custom companion"):
        if custom.strip():
            st.session_state.partner = custom.strip()
            next_page()


# PAGE 4
elif st.session_state.page == 4:
    st.title("Generating story...")
    with st.spinner("Crafting your story..."):
        prompt = f"""
        Write a short and imaginative children's story (under 300 words) with this structure:

        1. ✨ Begin by introducing a character named {st.session_state.character}.
        2. 🧱 They go on an adventure to {st.session_state.action}, in {st.session_state.location}, with their companion {partner_traits.get(st.session_state.partner, st.session_state.partner)}.
        3. 🚧 During the adventure, they encounter a small problem or obstacle that is appropriate for young children.
        4. 🎉 Show how they solve the problem using creativity, kindness, or teamwork.
        5. 💡 End with a heartwarming and simple lesson that children can easily understand.

        Please use gender-neutral language (like "they/them"), and keep the tone playful, magical, and suited for children aged 5–9.
        """


        try:
            # Generate story
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

            # Reset random options
            st.session_state.random_actions = []
            st.session_state.random_locations = []
            st.session_state.random_partners = []

            # Generate one image based on the full story
            image_prompt = f"Children's book illustration in watercolor style, DO NOT SHOW ANY TEXT IN THE IMAGE, showing the story: {full_story[:500]}"
            image_response = client.images.generate(
                model="dall-e-3",
                prompt=image_prompt,
                size="1024x1024",
                quality="standard",
                n=1
            )
            st.session_state.story_image_url = image_response.data[0].url

            # Go to story page
            st.session_state.page = 5
            st.rerun()

        except Exception as e:
            st.error(f"Something went wrong: {e}")

# PAGE 5
elif st.session_state.page == 5:
    st.title("📖 Story Time!")

    if st.session_state.get("story_image_url"):
        st.image(st.session_state.story_image_url, caption="✨ Illustration", use_container_width=True)

    st.markdown(st.session_state.story)

    if st.button("Start Over"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
