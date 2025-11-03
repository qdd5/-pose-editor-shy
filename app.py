import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# API Hugging Face (Stable Diffusion Inpaint)
API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-inpainting"
API_TOKEN = "hf_YOUR_TOKEN_HERE"  # غيّرها بتوكنك (مجاني)

headers = {"Authorization": f"Bearer {API_TOKEN}"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.content

st.title("🔥 NSFW AI Nude Generator – كشف واقعي 100%")
st.write("ارفع صورة + ارسم على الملابس = جسم عاري حقيقي!")

uploaded_file = st.file_uploader("ارفع الصورة", type=["png", "jpg", "jpeg"])
mask_file = st.file_uploader("ارفع القناع (ارسم بالأبيض على الملابس)", type=["png"])

if uploaded_file and mask_file:
    image = Image.open(uploaded_file).convert("RGB")
    mask = Image.open(mask_file).convert("RGB")
    
    st.image(image, caption="الأصلية", use_column_width=True)
    st.image(mask, caption="القناع (أبيض = عاري)", use_column_width=True)

    prompt = st.text_input("وصف العري", "nude arab woman, large breasts, pink nipples, wet pussy, thick ass, realistic, 8k")

    if st.button("ولّد العري الواقعي"):
        with st.spinner("جاري التوليد... (10-30 ثانية)"):
            # تحويل الصور
            img_bytes = BytesIO()
            image.save(img_bytes, format="PNG")
            img_bytes = img_bytes.getvalue()

            mask_bytes = BytesIO()
            mask.save(mask_bytes, format="PNG")
            mask_bytes = mask_bytes.getvalue()

            payload = {
                "inputs": prompt,
                "image": img_bytes,
                "mask_image": mask_bytes,
            }

            output = query(payload)

            if output:
                result_image = Image.open(BytesIO(output))
                st.image(result_image, caption="النتيجة: عاري واقعي 100%", use_column_width=True)
                buf = BytesIO()
                result_image.save(buf, format="PNG")
                st.download_button("حمل الصورة العارية", buf.getvalue(), "real_nude.png")
            else:
                st.error("فشل التوليد – تأكد من التوكن!")
