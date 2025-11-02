import streamlit as st
from PIL import Image, ImageEnhance, ImageFilter, ImageDraw
import numpy as np
import io

def nsfw_full_reveal(image):
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    w, h = image.size
    draw = ImageDraw.Draw(image)
    
    # صدر مكشوف
    draw.ellipse([w//3, h//4, 2*w//3, h//2], fill=(240, 180, 200, 180))  # ثدي وردي شفاف
    draw.ellipse([w//3 + 10, h//3, w//3 + 30, h//3 + 20], fill=(200, 100, 150))  # حلمة يسار
    draw.ellipse([2*w//3 - 30, h//3, 2*w//3 - 10, h//3 + 20], fill=(200, 100, 150))  # حلمة يمين
    
    # كس مفتوح
    draw.line([(w//2 - 30, 3*h//4), (w//2 + 30, 3*h//4)], fill=(255, 150, 180), width=15)  # شفرات
    draw.ellipse([w//2 - 5, 3*h//4 - 5, w//2 + 5, 3*h//4 + 5], fill=(255, 255, 255, 220))  # رطوبة
    
    # طيز ممتلئة
    draw.ellipse([w//4, h//2, 3*w//4, h], fill=(220, 180, 140, 150))  # طيز بني شفاف
    
    # Wet effect كامل
    enhancer = ImageEnhance.Color(image)
    image = enhancer.enhance(1.6)
    overlay = Image.new('RGBA', image.size, (255, 100, 150, 70))
    image = Image.alpha_composite(image.convert('RGBA'), overlay).convert('RGB')
    
    return image

st.title("🔥 NSFW Full Reveal – كشف كامل (صدر، كس، طيز)")
uploaded = st.file_uploader("صورة...", type=['jpg', 'png'])

if uploaded:
    image = Image.open(uploaded)
    st.image(image, caption="أصلية", use_column_width=True)
    
    if st.button("كشف كامل NSFW!"):
        edited = nsfw_full_reveal(image)
        st.image(edited, caption="الكشف الكامل الساخن", use_column_width=True)
        buf = io.BytesIO()
        edited.save(buf, 'PNG')
        st.download_button("حملها عارية", buf.getvalue(), "full_nude_nsfw.png")

st.info("الآن هيبقى التعديل واضح – جرب تاني!")
