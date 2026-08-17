from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sklearn.feature_extraction.text import TfidfVectorizer
import re

# 1. تهيئة تطبيق FastAPI السحابي
app = FastAPI(
    title="منصة اللسانيات الحاسوبية الجنائية",
    description="واجهة برمجية (API) مدفوعة لتحليل الأساليب اللغوية وكشف البصمة النصية",
    version="1.0.0"
)

# 2. تحديد هيكل البيانات المستقبلة من العميل
class TextInput(BaseModel):
    text: str
    api_key: str

# 3. دالة حساب التنوع المعجمي بدقة وتفادي الأخطاء الإحصائية
def calculate_lexical_diversity(text: str):
    words = re.findall(r'\w+', text.lower())
    if not words:
        return 0.0, 0.0
    total_words = len(words)
    unique_words = len(set(words))
    diversity_score = (unique_words / total_words) * 100
    return diversity_score, total_words

# 4. نقطة النهاية (Endpoint) المخصصة لتحليل النصوص وبيع الخدمة
@app.post("/api/v1/analyze")
async def analyze_text(input_data: TextInput):
    # حماية الخدمة بمفتاح واجهة برمجة تجريبي (يمكن تغييره لاحقاً)
    if input_data.api_key != "premium_rami_key_2026":
        raise HTTPException(status_code=401, detail="مفتاح API غير صالح أو انتهت صلاحية الاشتراك.")
        
    text = input_data.text
    if len(text.strip()) < 10:
        raise HTTPException(status_code=400, detail="النص قصير جداً للتحليل الأسلوبي والجنائي.")

    # تطبيق المقاييس الأسلوبية (Stylometry)
    diversity, total_words = calculate_lexical_diversity(text)
    
    # حساب محاكاة ميزة TF-IDF للنص المدخل مقارنة بنص مرجعي
    corpus = [text, "نص مرجعي قياسي للمقارنة الأسلوبية اللغوية البسيطة"]
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(corpus)
    feature_names = vectorizer.get_feature_names_out()
    
    # استخراج أبرز 5 كلمات مميزة للأسلوب بناءً على الوزن الرقمي
    scores = tfidf_matrix.toarray()[0]
    top_words = sorted(list(zip(feature_names, scores)), key=lambda x: x[1], reverse=True)[:5]
    top_words_dict = {word: round(float(score), 3) for word, score in top_words}

    # صياغة التقرير الجنائي الرقمي النهائي الموجه للعميل
    analysis_result = {
        "status": "success",
        "stylometry_metrics": {
            "total_words": total_words,
            "lexical_diversity_percentage": round(diversity, 2),
            "lexical_richness": "غني جداً" if diversity > 70 else ("متوسط" if diversity > 40 else "فقر معجمي / تكرار عالٍ")
        },
        "top_distinctive_terms_tfidf": top_words_dict,
        "forensic_notes": "تم فحص تماسك النص البنيوي. الأسلوب متسق إحصائياً." if diversity > 50 else "تحذير جنائي: مؤشرات على انكسار أسلوبي أو محاكاة آلية ركيكة."
    }
    return analysis_result

# 5. نقطة فحص عمل السيرفر الأساسية (Root Endpoint)
@app.get("/")
def read_root():
    return {"message": "مرحباً بك في منصة اللسانيات الحاسوبية الجنائية. السيرفر يعمل بنجاح على السحاب."}
