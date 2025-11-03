import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# Hugging Face API الجديد (2025) – غيّر الـTOKEN بتوكنك من huggingface.co/settings/tokens
API_URL = "https://router.huggingface.co/hf-inference"
API_TOKEN = "hf_YourTokenHere"  # سجل مجاناً وانسخ التوكن

headers = {"Authorization": f"Bearer {API_TOKEN}"}

def query(prompt, image):
    img_bytes = BytesIO()
    image.save(img_bytes, format="PNG")
    img_bytes = img_bytes.getvalue()
    
    # Multipart form for img2img (الطريقة الجديدة)
    files = {"image": ("image.png", img_bytes, "image/png")}
    data = {
        "model": "CompVis/stable-diffusion-v1-4",  # المودل img2img
        "inputs": prompt,
        "parameters": {"num_inference_steps": 20, "guidance_scale": 7.5, "strength": 0.75}  # strength للتحويل
    }
    
    response = requests.post(API_URL, headers=headers, files=files, data=data)
    
    # معالجة الأخطاء الجديدة
    if response.status_code != 200:
        st.error(f"API Error: {response.status_code} - {response.text[:200]}...")  # طباعة جزء من الخطأ
        return None
    
    if len(response.content) < 100:  # لو response صغير (نص خطأ)
        st.error(f"API Response Error: {response.text}")
        return None
    
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
            
            if output:
                try:
                    result_image = Image.open(BytesIO(output))
                    st.image(result_image, caption="الصورة الواقعية", use_column_width=True)
                    
                    # تنزيل
                    buf = BytesIO()
                    result_image.save(buf, format="PNG")
                    st.download_button("حمل النتيجة", buf.getvalue(), "real_photo.png")
                except Exception as e:
                    st.error(f"خطأ في فتح الصورة: {e}. جرب prompt أقصر أو بعد دقيقة.")
            else:
                st.error("فشل الـAPI – تأكد من التوكن أو الـmodel مشغول. جرب بعد دقيقة.")

else:
    st.info("📁 ارفع صورة أنمي لتبدأ!")

# تعليمات
st.sidebar.title("كيفية التشغيل")
st.sidebar.write("1. توكن مجاني: [Hugging Face Tokens](https://huggingface.co/settings/tokens).")
st.sidebar.write("2. شغّل: `streamlit run app.py`.")
st.sidebar.write("3. لو خطأ 410، الـAPI جديد – الكود مصحح.")
st.sidebar.write("4. النتيجة: واقعية مع جلد ناعم وتفاصيل حقيقية!")
