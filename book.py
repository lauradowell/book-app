import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
st.set_page_config(page_title="Choose Your Story", layout="centered")

# Initialize state
if "page" not in st.session_state:
    st.session_state.page = 0
    st.session_state.character = ""
    st.session_state.action = ""
    st.session_state.location = ""
    st.session_state.partner = ""
    st.session_state.story = ""

def next_page():
    st.session_state.page += 1

# Page 0: Pick a character
if st.session_state.page == 0:
    st.title("👧 Pick a character")
    st.image(["https://example.com/peter.png", "https://example.com/red.png", "https://example.com/rabbit.png"], width=150)
    options = ["Peter", "Red Riding Hood", "Mr. Rabbit"]
    choice = st.radio("Choose one:", options)
    custom = st.text_input("Or describe your own character...")
    if st.button("Next"):
        st.session_state.character = custom if custom else choice
        next_page()

# Page 1: What will she do?
elif st.session_state.page == 1:
    st.title("🧪 What will she do?")
    options = ["Fall asleep", "Make a magic potion", "Get on a spaceship"]
    choice = st.radio("Choose an action:", options)
    custom = st.text_input("Or write what she'll do...")
    if st.button("Next"):
        st.session_state.action = custom if custom else choice
        next_page()

# Page 2: Where will she be?
elif st.session_state.page == 2:
    st.title("🌍 Where will she be?")
    st.image(["https://example.com/jungle.png", "https://example.com/beach.png"], width=150)
    options = ["A lush jungle", "A sunny beach"]
    choice = st.radio("Choose a location:", options)
    custom = st.text_input("Or describe the location:")
    if st.button("Next"):
        st.session_state.location = custom if custom else choice
        next_page()

# Page 3: Who will she be with?
elif st.session_state.page == 3:
    st.title("🧑‍🚀 Who will she be with?")
    options = ["A robot", "An ant", "An astronaut"]
    choice = st.radio("Choose a companion:", options)
    custom = st.text_input("Or describe the companion:")
    if st.button("Next"):
        st.session_state.partner = custom if custom else choice
        next_page()

elif st.session_state.page == 4:
    st.title("Generating story...")
    with st.spinner("Crafting your story..."):
        prompt = f"""
        Create a creative and vivid children's story. The character is {st.session_state.character}, who decides to {st.session_state.action}. 
        She is in {st.session_state.location}, and she is accompanied by {st.session_state.partner}. 
        Make the story imaginative, charming, and suited for children.
        """
        try:
            st.write("Sending prompt to OpenAI...")
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a friendly and imaginative children's storyteller."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.9,
                max_tokens=1000
            )
            st.session_state.story = response.choices[0].message.content
            st.session_state.page = 5
            st.rerun()
        except Exception as e:
            st.error(f"Something went wrong: {e}")



elif st.session_state.page == 5:
    st.title("📖 Story Time!")

    if "story_image_url" not in st.session_state:
        with st.spinner("Illustrating your story..."):
            try:
                image_prompt = f"Children's book illustration: {st.session_state.story[:400]}..."
                image_response = client.images.generate(
                    model="dall-e-3",
                    prompt=image_prompt,
                    size="1024x1024",
                    quality="standard",
                    n=1
                )
                st.session_state.story_image_url = image_response.data[0].url
            except Exception as e:
                st.error(f"Could not generate image: {e}")
                st.session_state.story_image_url = None

    # Show the generated image
    if st.session_state.story_image_url:
        st.image(st.session_state.story_image_url, caption="✨ AI-generated Illustration", use_column_width=True)

    # Show the story
    st.markdown(st.session_state.story)

    # Restart button
    if st.button("Start Over"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
