%pip install -r requirements.txt
import streamlit as st
from PIL import Image
import os
import subprocess
import time
# Set page configuration
st.set_page_config(page_title="Upscale.AI", layout="wide")

# --- Add custom CSS for styling ---
st.markdown(
    """
    <style>
    body {
        background-color: #f0f0f0;
    }
    .navbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 50px;
        position: sticky;
        top: 0;
        z-index: 1000;
        background-color: #0078ff;
    }
    .navbar a {
        text-decoration: none;
        color: white;
        margin: 0 15px;
        font-size: 18px;
        font-weight: bold;
        transition: color 0.3s ease;
    }
    .navbar a:hover {
        color: #005bb5;
    }
    .navbar .brand {
        font-size: 24px;
        font-weight: bold;
        color: #ffffff;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Add the navigation bar ---
st.markdown(
    """
    <div class="navbar">
        <div class="brand">Upscale.AI</div>
        <div>
            <a href="#home">Home</a>
            <a href="#how-it-works">How It Works</a>
            <a href="#faq">FAQ</a>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# --- Define sections ---
# Section: Home
st.markdown('<a name="home"></a>', unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    st.write("")  # Empty space

with col2:
    st.image("hero.png")
    st.markdown("### Upload and Upscale Your Image")

with col3:
    st.write("")  # Empty space

# Upload file
uploaded_file = st.file_uploader("Choose an image file to upscale", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # Save the uploaded file to the models/LR directory
    lr_dir = "LR"
    if not os.path.exists(lr_dir):
        os.makedirs(lr_dir)

    # Save the uploaded file
    input_image_path = os.path.join(lr_dir, uploaded_file.name)
    with open(input_image_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

    # Trigger the upscaling process by running test.py
    st.write("Processing the image with ESRGAN...")
    process_button = st.button("Upscale Image")

    if process_button:
        try:
            # Run the test.py script
            st.write("Running ESRGAN model...")
            subprocess.run(["python", "test.py"], check=True)

            # Display the upscaled image from the results directory
            results_dir = "results"
            # Ensure the upscaled image uses the correct extension
            file_base, _ = os.path.splitext(uploaded_file.name)
            upscaled_image_path = os.path.join(results_dir, f"{file_base}.png")

            # Debugging info
            st.write(f"Input image path: {input_image_path}")
            st.write(f"Upscaled image expected at: {upscaled_image_path}")
            st.write("Results directory contents:", os.listdir(results_dir))

            if os.path.exists(upscaled_image_path):
                try:
                    upscaled_image = Image.open(upscaled_image_path)
                    st.image(upscaled_image, caption="Upscaled Image", use_column_width=True)

                    # Option to download the upscaled image
                    with open(upscaled_image_path, "rb") as file:
                        st.download_button(
                            label="Download Upscaled Image",
                            data=file,
                            file_name=f"upscaled_{uploaded_file.name}",
                            mime="image/png",
                        )

                    # Add a separate delete button
                    if st.button("Delete Upscaled Image from Server"):
                        try:
                            os.remove(upscaled_image_path)
                            st.success("Upscaled image removed from the server.")
                        except Exception as e:
                            st.error(f"Error deleting the upscaled image: {e}")
                except Exception as e:
                    st.error(f"Failed to open the upscaled image: {e}")
            else:
                st.error("Upscaled image not found. Please check the processing script.")
        except subprocess.CalledProcessError as e:
            st.error(f"An error occurred during processing: {e}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")

# Section: How It Works
st.markdown('<a name="how-it-works"></a>', unsafe_allow_html=True)
st.markdown("## How It Works")
st.markdown("---")

st.write(
    """
    1. Upload your image, which is saved to the system for processing.
    2. The ESRGAN model processes the image, enhancing its quality and resolution.
    3. The processed image is displayed on the screen and available for download.
    """
)

# Section: FAQ
st.markdown('<a name="faq"></a>', unsafe_allow_html=True)
st.markdown("## Frequently Asked Questions")
st.markdown("---")

faq_expander = st.expander("What is Upscale.AI?")
faq_expander.write("Upscale.AI uses ESRGAN to enhance image quality and resolution.")

faq_expander = st.expander("What images are supported?")
faq_expander.write("Currently, JPEG and PNG images are supported.")

# Footer Section
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: gray; margin-top: 50px;">
        <p>&copy; 2024 Upscale.AI. All rights reserved.</p>
    </div>
    """,
    unsafe_allow_html=True,
)
