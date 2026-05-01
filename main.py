import streamlit as st
import time
import cv2
import os
import av
import numpy as np
import cloudinary
import cloudinary.uploader
import io


# Cloudinary ချိတ်ဆက်ခြင်း
cloudinary.config( 
  cloud_name = st.secrets["CLOUDINARY_NAME"], 
  api_key = st.secrets["CLOUDINARY_API_KEY"], 
  api_secret = st.secrets["CLOUDINARY_API_SECRET"] 
)

# ပုံကို Cloudinary ပေါ် တင်တဲ့ Function
def upload_to_cloud(image_bytes, folder_name, filename):
    # image_bytes က ကင်မရာက ရိုက်လိုက်တဲ့ ပုံဖြစ်ရပါမယ်
    response = cloudinary.uploader.upload(
        image_bytes, 
        folder = f"face_dataset/{folder_name}", 
        public_id = filename
    )
    return response['secure_url']
# Page Configuration
#st.set_page_config(page_title="Face Data Collector", layout="wide")

st.title("Smart Face Data")
st.write(" ** သင်၏ မျက်နှာပုံစံများကို စနစ်တကျ မှတ်တမ်းတင်ရန် အောက်ပါအဆင့်များကို လိုက်နာပါ")
st.write("(2) ကင်မရာဖွင့်ရန် ခွင့်ပြုချက် (Allow) ပေးပါ") 
st.write("(3) မျက်မှန်ချွတ်ပေးပါ")


# Cloudinary Setup
cloudinary.config( 
  cloud_name = st.secrets["CLOUDINARY_NAME"], 
  api_key = st.secrets["CLOUDINARY_API_KEY"], 
  api_secret = st.secrets["CLOUDINARY_API_SECRET"],
  secure = True
)


# လူနာမည်တောင်းခြင်း
name = st.text_input("Enter User Name:", "")

if name:
    # ပုံအရေအတွက်မှတ်ရန် Session State
    if 'count' not in st.session_state:
        st.session_state.count = 0

    img_file_buffer = st.camera_input("Take a photo")

    if img_file_buffer is not None:
        # ပုံကို Bytes အဖြစ်ပြောင်းခြင်း
        bytes_data = img_file_buffer.getvalue()
        
        # Cloudinary ပေါ်သို့ တင်ခြင်း
        with st.spinner(f"Uploading image {st.session_state.count + 1}/3..."):
            try:
                result = cloudinary.uploader.upload(
                    bytes_data,
                    folder = f"face_dataset/{name}",
                    public_id = f"img_{st.session_state.count + 1}"
                )
                st.success(f"Image {st.session_state.count + 1} saved to Cloud!")
                st.session_state.count += 1
            except Exception as e:
                st.error(f"Error: {e}")

    if st.session_state.count >= 3:
        st.balloons()
        st.write("🎉 Dataset collection complete! All 20 images are in the cloud.")
        if st.button("Reset for new user"):
            st.session_state.count = 0
            st.rerun()