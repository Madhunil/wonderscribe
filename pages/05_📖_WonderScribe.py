import streamlit as st
from PIL import Image
import requests
import json
import base64
from io import BytesIO
import boto3
from botocore.exceptions import NoCredentialsError, ClientError

# Set the page configuration
st.set_page_config(page_title="Interactive Storybook", page_icon="📖", layout="wide")

# Background image URL
background_image_url = "https://raw.githubusercontent.com/Natsnet/WS_Back_img/main/WonderScribe_bk_blue_page_1.jpg"
#background_image_url = "https://raw.githubusercontent.com/Natsnet/WS_Back_img/main/WonderScribe_bk2_page_1.jpg"

# CSS for setting the background
background_css = f"""
<style>
[data-testid="stAppViewContainer"] {{
    background-image: url("{background_image_url}");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
    filter: opacity(0.8);
    background-color: rgba(255, 255, 255, 0.8);
}}
</style>
"""

# Sidebar CSS
sidebar_css = """
<style>
[data-testid="stSidebar"] {
    #background-color: #7dd8ff;
    border-right: 2px solid #bfa989;
}

[data-testid="stSidebar"] h1 {
    color: #4e342e;
    font-size: 1.5em;
    font-family: 'Merriweather', serif;
    font-weight: bold;
}

[data-testid="stSidebar"] button {
    background-color: #d4c1a7;
    border-radius: 10px;
    border: 2px solid #bfa989;
    padding: 10px;
    font-size: 1.2em;
    color: #4e342e;
    margin-bottom: 15px;
}

[data-testid="stSidebar"] button:hover {
    background-color: #e0d3b8;
    color: #4e342e;
}
</style>
"""
# ==============
# Custom CSS to apply the background gradient and create a box
page_bg = """
<style>
/* Apply background gradient to the main container */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #8c52ff, #5ce1e6);
    background-attachment: fixed;
}

/* Optional: Adjust text color and other styles */
[data-testid="stAppViewContainer"] .stMarkdown {
    color: white;  /* Adjust text color for contrast */
}

/* Style for the content box */
.custom-box {
    background-color: #eaf1ff; /* Light background color for the box */
    border-radius: 10px; /* Rounded corners */
    padding: 20px; /* Spacing inside the box */
    box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1); /* Subtle shadow for a raised effect */
    color: black; /* Text color inside the box */
    margin-top: 20px; /* Space above the box */
}

/* Position the logo in the top-left corner */
img[alt="WonderScribeLogo"] {
    position: absolute;
    top: 40px;
    left: 40px;
    width: 150px; /* Adjust width if needed */
    z-index: 10;
}

/* Add padding to avoid overlap with the content */
[data-testid="stAppViewContainer"] {
    padding-top: 80px; /* Add padding to avoid logo overlapping */
}
</style>
"""
# ==============
# Apply CSS
st.markdown(background_css, unsafe_allow_html=True)
st.markdown(sidebar_css, unsafe_allow_html=True)

# ============
# Apply the custom CSS
st.markdown(page_bg, unsafe_allow_html=True)
st.markdown(
    """
    <style>
    /* Style for the sidebar content */
    [data-testid="stSidebarContent"] {
        background-color: #7dd8ff; /*#7dd8ff; Sidebar background color */
        
    }
    /* Set color for all text inside the sidebar */
    [data-testid="stSidebar"] * {
        color: #8c52ff !important;  /* Text color */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.image("pages/images/WonderScribeLogo.png", width=150)
# ============

# S3 Client setup
s3client = boto3.client("s3")

# Decode base64 image
def image_decode(image_data_decode):
    image_data = base64.b64decode(image_data_decode)
    return Image.open(BytesIO(image_data))

def encode_image_to_base64(image_path):
    try:
        with open(image_path, "rb") as image_file:
            # Read the binary data and encode to base64
            encoded_string = base64.b64encode(image_file.read())
        
            #convert bytes to string for easier handling
            return encoded_string.decode('utf-8')
        
    except exception as e:
        print(f"Error encoding image: {e}")
        return None
        

# Fetch story data
@st.cache_data
def fetch_story_data(payload, _force_refresh=False):
    if _force_refresh:
        st.cache_data.clear()
    AWS_API_URL = "https://wacnqhon34.execute-api.us-east-1.amazonaws.com/dev/"
    headers = {"Content-Type": "application/json"}

    response = requests.post(AWS_API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        data = response.json()
        return data["story_texts"], data["captions"], data["storyfiles"]
    return [], [], []

# Fetch and decode images
@st.cache_data
def fetch_and_decode_images(captions, _force_refresh=False):
    if _force_refresh:
        st.cache_data.clear()
    AWS_API_URL = "https://wacnqhon34.execute-api.us-east-1.amazonaws.com/dev/"
    headers = {"Content-Type": "application/json"}
    decoded_images = []
    
    for index, caption in enumerate(captions):
        if index == 0:
            payload2 = {
                "api_Path": "getImage",
                "storyPrompt": caption,
                "previousPrompt": ''
            }
        else:
            payload2 = {
                "api_Path": "getImage",
                "storyPrompt": caption,
                "previousPrompt": captions[index - 1]     # if index > 0 else "",
            }
            
        json_data = payload2            
        response = requests.post(AWS_API_URL, headers=headers, json=json_data)
        
        if response.status_code == 200:
            data = response.json()

            if data["image_data_decode1"] == "INVALID_PROMPT":
                invalid_image = "pages/images/invalid_img.jpg"
                decoded_images.append(encoded_image_to_base64(invalid_image))
            else:
                decoded_images.append(data["image_data_decode1"])
    return decoded_images

# Main app
def main():

    # st.title("📖 Welcome to WonderScribe!")
    # st.write("Craft personalized stories that bring adventure to life.")
    
    if 'cache_cleared' not in st.session_state:
        st.session_state.cache_cleared = False

    #=================
        # Set the page configuration with a wide layout for a book-like feel
    # Add custom CSS for the storybook theme
    
    st.markdown("""
    <style>
        /* Overall background styling */
        body {
            #background-color: #f5f0e1;
            font-family: 'Merriweather', serif;
            #color: #4e342e;
            [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg,#8c52ff, #5ce1e6);
            background-attachment: fixed;
            # background-color: #7dd8ff;  /* #c0dc8f Light gray-green #d2e7ae; Purple=#8c52ff, #5f20eb*/
        }

 
        /* Sidebar styling to resemble a table of contents */
        .css-1d391kg {
            #background-color: #e8e0d2 !important;
            background-color: #7dd8ff; /*#7dd8ff; Sidebar background color */
            #background-color: #7dd8ff !important;
            border-right: 2px solid #bfa989;
        }
 
        /* Sidebar Title */
        .css-1544g2n {
            color: #4e342e !important;
            font-size: 1.5em;
            font-family: 'Merriweather', serif;
            font-weight: bold;
        }
 
        /* Menu buttons in the sidebar */
        .css-1vbd788 {
            background-color: #d4c1a7;
            border-radius: 10px;
            border: 2px solid #bfa989;
            padding: 10px;
            font-size: 1.2em;
            color: #4e342e !important;
            margin-bottom: 15px;
        }
 
        .css-1vbd788:hover {
            background-color: #e0d3b8;
            color: #4e342e !important;
        }
 
        /* Main content area - text background with borders */
        .storybook-text {
            background-color: #faf3e7;
            padding: 30px;
            border-radius: 15px;
            border: 3px solid #bfa989;
            box-shadow: 3px 3px 10px rgba(0, 0, 0, 0.1);
            font-family: 'Merriweather', serif;
            font-size: 18px;
            line-height: 1.6;
            text-align: justify;
        }
 
        /* Image styling */
        .storybook-image {
            border-radius: 15px;
            border: 3px solid #bfa989;
            box-shadow: 3px 3px 10px rgba(0, 0, 0, 0.1);
            max-width: 100%;
            height: auto;
        }
 
        /* Styling for the page navigation buttons */
        .stButton > button {
            background-color: #d4c1a7;
            color: #4e342e;
            border: 2px solid #bfa989;
            border-radius: 8px;
            padding: 10px 20px;
            font-size: 1.2em;
        }
 
        .stButton > button:hover {
            background-color: #e0d3b8;
            color: #4e342e;
        }
    </style>
    """, unsafe_allow_html=True)

    if 'validation_errors' not in st.session_state:
        st.session_state.validation_errors = []

    #=================
        
    with st.form("form_key"):
        st.write("Craft personalized stories that bring adventure to life.")
        gender = st.selectbox("Your Gender", ["Male", "Female", "Non Binary", "Don't want to share"])
        main_character = st.text_input("Main Character Name", placeholder="Enter the name of the main character")
        audience = st.selectbox("Audience", ["Children", "Young Adult", "Adult", "Senior"])
        story_setting = st.selectbox("Story Setting", options=["Magical Kingdoms", "Underwater Kingdoms", "Pirate Ships", "Exotic locations", "Imaginary Worlds", "Digital words", "Other"])
        story_type = st.selectbox("Story Type", options=["Fantasy", "Fairy Tales", "Mythology", "Bedtime stories", "Adventure", "Mystery", "Love", "Horror"])
        story_theme = st.text_input("What would be the topic of the story?", placeholder="Enter brief idea of a story")
        moral_lesson = st.text_input("What would be the moral of this story?", placeholder="Enter a moral lesson from this story")
        story_length = st.selectbox("Story Length (in words)", options=["300", "400", "500","700"])
        story_lang = st.selectbox("Story Language", options=["English", "Spanish", "French", "German", "Mandarin", "Hindi", "Urdu", "Arabic", "Italian", "Vietnamese","Tagalog"])

        submit_btn = st.form_submit_button("submit")

    try:
        if submit_btn:
            # Clear previous validation errors
            st.session_state.validation_errors = []
        
            # Validate main character
            if not main_character or len(main_character.strip()) < 2:
                st.session_state.validation_errors.append("Main character name must be at least two characters long")
                # errors.append("Main character name must be at least 2 characters.")
            elif not main_character.replace(" ", "").isalpha():
                st.session_state.validation_errors.append("Main character name should only contain letters")

            # Validate story theme
            if not story_theme or len(story_theme.strip()) < 10:
                st.session_state.validation_errors.append("Story theme must be at least 10 characters long.")
            elif len(story_theme.split()) < 2:
                st.session_state.validation_errors.append("Story theme should contain at least two words.")

            # Validate moral lesson
            if not moral_lesson or len(moral_lesson.strip()) < 10:
                st.session_state.validation_errors.append("Moral lesson must be at least 10 characters long.")
            elif len(moral_lesson.split()) < 2:
                st.session_state.validation_errors.append("Moral lesson should contain at least two words.")

            # Display all validation errors if any
    
            if st.session_state.validation_errors:
                error_message = "Please fix the following errors:\n" + "\n".join(f".{error}" for error in st.session_state.validation_errors)
                st.error(error_message)
                st.stop() # Stop further execution if there are validation errors

            # if no validation errors, proceed with form submission
            st.session_state.submit_btn = True

        menu_options = ["About", "Storybook"]
        st.session_state.current_page = 'Storybook"

        if submit_btn:
            st.cache_data.clear()
            st.session_state.cache_cleared = True
            st.succcess("Cache has been cleared! Refresh the page to fetch new data.")
            st.session_state.submit_btn = True
            st.session_state.page_index = 0

        if st.session_state.submit_btn and st.session_state.current_page == "Storybook":
            # Create payload
            payload = {
                "audience": audience,
                "story_type": story_type,
                "main_character": main_character,
                "story_theme": story_theme,
                "moral_lesson": moral_lesson,
                "setting": story_setting,
                "word_count": story_length,
                "story_lang": story_lang,
                "api_Path": "getStory"
                }

        # Fetch data
        story_texts, captions, storyfiles = fetch_story_data(payload)
        decoded_images = fetch_and_decode_images(captions)

        #===============
        #===============

        # Display story
        for idx, text in enumerate(story_texts):
            col1, col2 = st.columns([1, 1])
            with col1:
                st.markdown(f"### Page {idx + 1}")
                st.markdown(f"<div>{text}</div>", unsafe_allow_html=True)
            with col2:
                st.image(image_decode(decoded_images[idx]), use_column_width=True)

if __name__ == "__main__":
    if "submit_btn" not in st.session_state:
        st.session_state.submit_btn = False
    main()
