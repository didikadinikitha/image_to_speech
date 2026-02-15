import streamlit as st
import google.generativeai as genai
from PIL import Image
from gtts import gTTS
import tempfile
from config import GEMINI_API_KEY

# -------------------------
# Configure Gemini
# -------------------------
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

# -------------------------
# Page Settings
# -------------------------
st.set_page_config(
    page_title="Image to Speech - Gemini",
    layout="centered"
)

st.title("🖼️ Image to Speech using Gemini")
st.write(
    "Upload an image. Gemini analyzes it and converts the description into speech."
)

# -------------------------
# Language Selection
# -------------------------
languages = {
    "English": "en",
    "Hindi": "hi",
    "Telugu": "te",
    "Spanish": "es",
    "French": "fr"
}

selected_lang = st.selectbox(
    "Select Speech Language",
    list(languages.keys())
)

lang_code = languages[selected_lang]

# -------------------------
# Image Upload
# -------------------------
uploaded_file = st.file_uploader(
    "Upload Image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:

    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

    if st.button("Generate Description & Speech"):

        try:
            with st.spinner("Analyzing image using Gemini..."):

                prompt = """
                Describe this image clearly for a visually impaired person.
                Mention:
                - main objects
                - environment
                - actions happening
                - overall scene summary
                Keep the explanation simple and natural.
                """

                response = model.generate_content([prompt, image])
                description = response.text

                st.subheader("📝 Image Description")
                st.write(description)

                # Text to Speech
                tts = gTTS(text=description, lang=lang_code)

                temp_audio = tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=".mp3"
                )
                tts.save(temp_audio.name)

                st.subheader("🔊 Audio Output")
                st.audio(temp_audio.name, format="audio/mp3")

                # Download Button
                with open(temp_audio.name, "rb") as audio_file:
                    st.download_button(
                        label="Download Audio",
                        data=audio_file,
                        file_name="image_description.mp3",
                        mime="audio/mp3"
                    )

        except Exception as e:
            st.error(f"Error occurred: {str(e)}")
