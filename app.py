import streamlit as st
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import numpy as np
import io

# دالة التعديل الـNSFW
def nsfw_edit(image, mode):
    # تحويل إلى RGB إذا لزم
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # تعزيز عام للإغراء
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(1.2)  # زيادة التباين
    
    if mode == "Tease":
        # Blur خفيف على الخلفية، focus على الوسط
        image = image.filter(ImageFilter.GaussianBlur(radius=1))
        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(1.1)  # إضاءة دافئة
    elif mode == "Full NSFW":
        # Wet look: زيادة الـsaturation + لمعان
        enhancer = ImageEnhance.Color(image)
        image = enhancer.enhance(1.3)  # ألوان أحمر/وردي أقوى
        # إضافة overlay للرطوبة (بسيط)
        overlay = Image.new('RGBA', image.size, (255, 100, 150, 30))  # لون وردي شفاف
        image = Image.alpha_composite(image.convert('RGBA'), overlay).convert('RGB')
    elif mode == "Doggy Pose":
        # محاكاة doggy: rotate 90 درجة + crop للمؤخرة
        image = image.rotate(90, expand=True)
        width, height = image.size
        image = image.crop((width//4, 0, 3*width//4, height))  # zoom على الوسط
    elif mode == "Spread Pose":
        # محاكاة spread: zoom على المنطقة السفلية + فتح بـaffine
        width, height = image.size
        image = image.crop((0, height//2, width, height))  # crop سفلي
        # Affine transform للفتح (بسيط)
        matrix = np.float32([[1, 0, 0], [0.1, 1, 0], [0, 0, 1]])  # skew خفيف
        # هنا placeholder، في الواقع استخدم cv2.warpAffine لو OpenCV
        pass  # يمكن توسيع
    
    return image

# الواجهة
st.title("🔥 NSFW Pose Editor - محرر الوضعيات الساخنة")
st.write("ارفع صورة، اختر وضعية NSFW، وشوف السحر! (تأكيد مطلوب للـNSFW)")

uploaded_file = st.file_uploader("اختر صورة...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="الصورة الأصلية", use_column_width=True)
    
    # خيارات الوضعية
    mode = st.selectbox("اختر الوضعية/الوضع:", ["Tease", "Full NSFW", "Doggy Pose", "Spread Pose"])
    
    confirm = st.checkbox("أؤكد: أريد تعديل NSFW (18+ فقط)")
    
    if st.button("عدل الصورة الآن!") and confirm:
        st.write("جاري التعديل الساخن...")
        edited = nsfw_edit(image, mode)
        st.image(edited, caption=f"الصورة المعدلة: {mode}", use_column_width=True)
        # حفظ للتنزيل
        buf = io.BytesIO()
        edited.save(buf, format='PNG')
        st.download_button("تنزيل النسخة الساخنة", buf.getvalue(), f"nsfw_{mode}.png")
    else:
        st.warning("❌ يرجى التأكيد للمتابعة (NSFW mode مفعل).")

else:
    st.info("📁 ارفع صورة لنبدأ الإغراء!")
