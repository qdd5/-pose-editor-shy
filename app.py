import streamlit as st
from PIL import Image, ImageEnhance, ImageFilter, ImageDraw
import numpy as np
import io

def nsfw_edit_full(image):
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # تعزيز عام
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(1.5)
    
    # Full reveal: overlay جلد عاري + wet
    w, h = image.size
    draw = ImageDraw.Draw(image)
    # صدر مكشوف (دائرتان ورديتان)
    draw.ellipse([w//3, h//4, 2*w//3, h//2], fill=(255, 182, 193, 150))  # صدر وردي شفاف
    # كس (خط مفتوح مع لمعان)
    draw.line([(w//2 - 20, 3*h//4), (w//2 + 20, 3*h//4)], fill=(255, 100, 150), width=10)  # شفرات
    draw.ellipse([w//2 - 5, 3*h//4 - 5, w//2 + 5, 3*h//4 + 5], fill=(255, 255, 255, 200))  # رطوبة
    # طيز (منحنيات خلفية)
    draw.arc([w//4, h//2, 3*w//4, 9*h//10], 0, 180, fill=(200, 150, 100, 120))  # طيز ممتلئة
    
    # Wet effect كامل
    overlay = Image.new('RGBA', image.size, (255, 100, 150, 50))
    image = Image.alpha_composite(image.convert('RGBA'), overlay).convert('RGB')
    
    return image

st.title("🔥 NSFW Full Reveal Editor - كشف كامل ساخن")
uploaded = st.file_uploader("صورة...", type=['jpg', 'png'])

if uploaded:
    image = Image.open(uploaded)
    st.image(image, caption="أصلية", use_column_width=True)
    
    if st.button("كشف كامل NSFW الآن!"):
        edited = nsfw_edit_full(image)
        st.image(edited, caption="الكشف الكامل: صدر، كس، طيز رطبة", use_column_width=True)
        buf = io.BytesIO()
        edited.save(buf, 'PNG')
        st.download_button("حمل النسخة المفتوحة", buf.getvalue(), "full_nsfw.png")
