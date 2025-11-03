import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# Hugging Face API (غيّر الـTOKEN بتوكنك من huggingface.co/settings/tokens)
API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
API_TOKEN = "hf_YourTokenHere"  # سجل مجاناً وانسخ

headers = {"Authorization": f"Bearer {API_TOKEN}"}

def query(prompt, image):
    # تحويل الصورة إلى bytes
    img_bytes = BytesIO()
    image.save(img_bytes, format="PNG")
    img_bytes = img_bytes.getvalue()
    
    # إرسال كـform data (مش JSON) للـimg2img
    files = {"image": ("image.png", img_bytes, "image/png")}
    data = {"inputs": prompt, "parameters": {"num_inference_steps": 20, "guidance_scale": 7.5}}
    
    response = requests.post(API_URL, headers=headers, files=files, data=data)
    return response.content

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
            
            if output and len(output) > 0:
                result_image = Image.open(BytesIO(output))
                st.image(result_image, caption="الصورة الواقعية", use_column_width=True)
                
                # تنزيل
                buf = BytesIO()
                result_image.save(buf, format="PNG")
                st.download_button("حمل النتيجة", buf.getvalue(), "real_photo.png")
            else:
                st.error("فشل – تأكد من التوكن أو جرب تاني (API مشغول)")

else:
    st.info("📁 ارفع صورة أنمي لتبدأ!")

# تعليمات
st.sidebar.title("كيفية التشغيل")
st.sidebar.write("1. احصل على توكن مجاني من [Hugging Face](https://huggingface.co/settings/tokens).")
st.sidebar.write("2. شغّل: `streamlit run app.py`.")
st.sidebar.write("3. جرب صورة أنمي – النتيجة واقعية رهيبة!")
