import streamlit as st
import base64
from PIL import Image

# Set page configuration
st.set_page_config(page_title="Members - WonderScribe", page_icon="📖", layout="wide")

# Background image URL
background_image_url = "https://raw.githubusercontent.com/Natsnet/WS_Back_img/main/WonderScribe_bk_blue_page_1.jpg"

# CSS for gradient and background image
background_css = f"""
<style>
[data-testid="stAppViewContainer"] {{
    background-image: url("{background_image_url}");
    background-size: cover;  /* Ensure it covers the full viewport */
    background-position: center;  /* Center the image */
    background-repeat: no-repeat;  /* Do not repeat the image */
    background-attachment: fixed;  /* Keep the background fixed during scrolling */
    color: white;  /* Default text color for readability */
}}

.custom-box {{
    background-color: rgba(255, 255, 255, 0.8); /* Semi-transparent white */
    border-radius: 10px; /* Rounded corners */
    padding: 20px; /* Space inside the box */
    box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1); /* Subtle shadow effect */
    color: black; /* Text color inside the content box */
    margin-top: 20px; /* Space above the box */
}}

[data-testid="stSidebar"] * {{
    color: #8c52ff; /* Purple text for sidebar */
}}

[data-testid="stAppViewContainer"] .stMarkdown {{
    color: gray;
}}
</style>
"""

# Apply CSS styles
st.markdown(background_css, unsafe_allow_html=True)

# Function to add the logo to the sidebar
def add_logo_to_sidebar(logo_path, width="200px"):
    with open(logo_path, "rb") as f:
        encoded_logo = base64.b64encode(f.read()).decode("utf-8")
    st.sidebar.markdown(
        f"""
        <style>
            [data-testid="stSidebar"]::before {{
                content: '';
                display: block;
                background-image: url("data:image/png;base64,{encoded_logo}");
                background-size: {width}; /* Adjust the size of the logo */
                background-repeat: no-repeat;
                background-position: top center; /* Center the logo at the top */
                height: 152px; /* Adjust height to fit the logo */
                padding-top: 20px;
                margin-bottom: 20px;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )

# Add the WonderScribe logo
add_logo_to_sidebar("pages/images/Updated_WonderS_logo.png", width="200px")

# Function to process and resize images to 1:1 ratio
def process_image(image_path, size=(400, 400)):
    img = Image.open(image_path)
    # Crop image to square
    min_dimension = min(img.size)
    cropped_img = img.crop((
        (img.width - min_dimension) // 2,
        (img.height - min_dimension) // 2,
        (img.width + min_dimension) // 2,
        (img.height + min_dimension) // 2,
    ))
    # Resize to the specified size
    resized_img = cropped_img.resize(size)
    return resized_img

# Page Title
st.markdown(
    "<h1 style='color: #5481c4; text-align: center;'>Our Team</h1>",
    unsafe_allow_html=True,
)

# Define group members
members = [
    {
        "name": "Jay Prakash",
        "role": "Product Management, GenAI, AWS Architecture",
        "bio": "Jay is the technical backbone of WonderScribe, leading the development of the platform’s robust AWS architecture. With expertise in cloud-based solutions and Generative AI, Jay ensures the platform's seamless integration of services like API Gateway, Lambda, and Bedrock. His focus on scalability and efficiency has been instrumental in building a secure and reliable foundation for WonderScribe's innovative storytelling capabilities.",
        "image": "pages/images/Jay_Profile_pic.jpg",
        "email": "jprakash@berkeley.edu",
    },
    {
        "name": "Jailynne Estevez",
        "role": "Program Management, UI/UX Design, Presentation Development",
        "bio": "Jailynne brings creativity and precision to WonderScribe, playing a key role in crafting a user-friendly and engaging platform for children and parents. She has helped design an intuitive interface that ensures a seamless storytelling experience while also leading the development of presentations, scripts, and pitches to effectively showcase the project’s value. Jailynne’s efforts extend beyond design and communication, as she actively collaborates with the team to bridge technical development with user needs. Her dedication to WonderScribe’s mission has been pivotal in creating a platform that fosters creativity, learning, and imagination for all.",
        "image": "pages/images/JEN.jpeg",
        "email": "jestevez@berkeley.edu",
    },
    {
        "name": "Mian Haseeb",
        "role": "ML Engineering, GenAI",
        "bio": "Mian is the visionary behind WonderScribe, originally conceiving the idea to revolutionize storytelling through the power of Generative AI. Mian is one of the machine learning engineers for WonderScribe, driving the integration of cutting-edge generative AI models. From fine-tuning the RAG framework to deploying advanced text and image generation models, Mian’s work ensures that WonderScribe delivers creative, engaging, and contextually relevant stories. His passion for AI innovation and storytelling shines through in every technical detail.",
        "image": "pages/images/MianHaseeb.jfif",
        "email": "mhaseeb@berkeley.edu",
    },
    {
        "name": "Natsnet Demoz",
        "role": "Data & Analytics, UI/UX Design, Model Development",
        "bio": "Natsnet’s dual focus on data exploration and design brings WonderScribe’s creative vision to life. She leads exploratory data analysis, ensuring the platform leverages child-friendly and culturally diverse datasets. Additionally, her contributions to user interface design make WonderScribe an intuitive and engaging platform for children and parents alike. Her ability to merge data insights with user-centric design is a key driver of the project’s success.",
        "image": "pages/images/Natsnet Demoz.jpg",
        "email": "ndemoz@berkeley.edu",
    },
    {
        "name": "Wilford Bradford",
        "role": "SME, Model Development",
        "bio": "Wil lends his expertise as a subject matter expert to refine WonderScribe’s storytelling framework. His work focuses on aligning the platform’s AI capabilities with user expectations, ensuring every story element resonates with children and their imaginations. Wil also collaborates on model development, emphasizing inclusivity and quality across WonderScribe’s texts and images",
        "image": "pages/images/WilfordBradford.jfif",
        "email": "wbradford@berkeley.edu",
    },
]

# Display team members with processed images
for member in members:
    col1, col2 = st.columns([1, 3])  # Adjust column width for better layout
    with col1:
        processed_image = process_image(member["image"])
        st.image(processed_image, use_column_width=True)
    with col2:
        st.markdown(f"### {member['name']}")
        st.markdown(f"**Role:** {member['role']}")
        st.markdown(f"**Bio:** {member['bio']}")
        st.markdown(f"**Email:** [{member['email']}](mailto:{member['email']})")
    st.write("---")
