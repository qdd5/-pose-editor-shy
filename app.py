import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import base64

# Stability AI API (غيّر الـKEY بكي من stability.ai/dashboard)
API_URL = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/image-to-image"
API_KEY = "sk-your-stability-key-here"  # انسخ الكي هنا

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

def query(prompt, image):
    # تحويل الصورة إلى base64
    img_bytes = BytesIO()
    image.save(img_bytes, format="PNG")
    img_bytes = img_bytes.getvalue()
    image_base64 = base64.b64encode(img_bytes).decode('utf-8')
    
    payload = {
        "text_prompts": [{"text": prompt, "weight": 1}],
        "init_image": image_base64,
        "init_image_mode": "IMAGE_STRENGTH",
        "image_strength": 0.75,  # قوة التحويل (0.75 = واقعي مع الحفاظ على الشكل)
        "cfg_scale": 7.5,  # guidance scale
        "steps": 30,  # خطوات
        "samples": 1,  # عدد الصور
        "width": 1024,
        "height": 1024
    }
    
    response = requests.post(API_URL, headers=headers, json=payload)
    
    if response.status_code != 200:
        st.error(f"API Error: {response.status_code} - {response.text[:200]}...")
        return None
    
    data = response.json()
    if "artifacts" in data and len(data["artifacts"]) > 0:
        artifact = data["artifacts"][0]
        return base64.b64decode(artifact["base64"])
    else:
        st.error(f"API Response Error: {data}")
        return None

st.title("🎨 Anime to Real Converter – تحويل أنمي/هنتاي إلى واقعي")
st.write("ارفع صورة خيالية، وشوفها تبقى واقعية في ثواني!")

uploaded_file = st.file_uploader("اختر صورة أنمي/هنتاي...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="الصورة الخيالية", use_column_width=True)
    
    prompt = st.text_input("وصف التحويل (اختياري)", "photorealistic version of this anime character, high detail, real skin, 8k")
    
    if st.button("حوّل إلى واقعي!"):
        with st.spinner("جاري التحويل... (10-30 ثانية)"):
            output = query(prompt, image)
            
            if output:
                result_image = Image.open(BytesIO(output))
                st.image(result_image, caption="الصورة الواقعية", use_column_width=True)
                
                # تنزيل
                buf = BytesIO()
                result_image.save(buf, format="PNG")
                st.download_button("حمل النتيجة", buf.getvalue(), "real_photo.png")
            else:
                st.error("فشل – تأكد من الـKEY أو جرب تاني.")

else:
    st.info("📁 ارفع صورة أنمي لتبدأ!")

# تعليمات
st.sidebar.title("كيفية التشغيل")
st.sidebar.write("1. KEY مجاني: [Stability AI Dashboard](https://stability.ai/dashboard).")
st.sidebar.write("2. شغّل: `streamlit run app.py`.")
st.sidebar.write("3. النتيجة: واقعية مع جلد ناعم وتفاصيل حقيقية!")
