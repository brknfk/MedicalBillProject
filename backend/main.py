from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import google.generativeai as genai
import uvicorn
from PIL import Image
import io
import time
import os
from dotenv import load_dotenv

# 1. SETUP
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    print("HATA: API Key bulunamadı! .env dosyasını kontrol et.")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

app = FastAPI()

# --- ENGLISH MOCK DATABASE (VERIFIED) ---
DRUG_DATABASE = {
    "parol": {
        "full_name": "Parol 500 mg Tablet",
        "active_ingredient": "Paracetamol",
        "usage": "Used for mild to moderate pain relief and fever reduction.",
        "warning": "Do not exceed 4 grams per day. Consult a doctor if you have liver issues."
    },
    "arveles": {
        "full_name": "Arveles 25 mg Film Tablet",
        "active_ingredient": "Dexketoprofen",
        "usage": "Used for musculoskeletal pain, menstrual pain, and toothache.",
        "warning": "May cause stomach upset, should be taken on a full stomach."
    },
    "aspirin": {
        "full_name": "Aspirin 100 mg",
        "active_ingredient": "Acetylsalicylic Acid",
        "usage": "Used as a blood thinner and pain reliever.",
        "warning": "Should not be used by those with bleeding disorders."
    },
    "calpol": {
        "full_name": "Calpol 6 Plus Suspension",
        "active_ingredient": "Paracetamol",
        "usage": "Pain and fever relief for children.",
        "warning": "Contains paracetamol. Check dosage by age."
    }
}

# --- HELPER: AUTO-RETRY ---
def generate_safe_response(prompt_content):
    max_retries = 3
    wait_time = 10
    for i in range(max_retries):
        try:
            return model.generate_content(prompt_content)
        except Exception as e:
            if "429" in str(e):
                print(f"⚠️ Quota exceeded! Waiting {wait_time}s...")
                time.sleep(wait_time)
                wait_time *= 2
            else:
                raise e
    raise Exception("Server busy.")

# --- API ENDPOINTS ---

class QuestionModel(BaseModel):
    ilac_adi: str
    soru: str

@app.post("/ilac-sor")
async def ask_drug(data: QuestionModel):
    
    prompt = f"Drug: {data.ilac_adi}. Question: {data.soru}. Answer briefly as a pharmacist."
    try:
        response = generate_safe_response(prompt)
        return {"cevap": response.text}
    except Exception as e:
        return {"hata": str(e)}

@app.post("/fotograf-analiz")
async def analyze_photo(file: UploadFile = File(...)):
    print("📸 Processing photo...")
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        
        name_prompt = "Read the most prominent drug brand name on this box. Output ONLY the name."
        ai_response = generate_safe_response([name_prompt, image])
        detected_name = ai_response.text.strip().lower()
        print(f"Detected Name: {detected_name}")

        
        found_info = None
        for key in DRUG_DATABASE:
            if key in detected_name:
                found_info = DRUG_DATABASE[key]
                break
        
        
        if found_info:
            return {
                "analiz": f"✅ VERIFIED DATABASE MATCH\n"
                          f"Name: {found_info['full_name']}\n\n"
                          f"💊 Usage: {found_info['usage']}\n\n"
                          f"⚠️ Warning: {found_info['warning']}"
            }
        
        
        else:
            print("Database miss. Asking Gemini General Knowledge...")
            general_prompt = f"""
            The user uploaded a photo of a drug named '{detected_name}'.
            It is NOT in my local verified database.
            
            Using your general medical knowledge, please provide a brief summary.
            Format exactly like this:
            Name: [Correct Capitalized Name]
            💊 Usage: [Short usage info]
            ⚠️ Warning: [Key warnings]
            
            Add a disclaimer at the end that this is AI generated.
            """
            general_response = generate_safe_response(general_prompt)
            
            return {
                "analiz": f" AI GENERATED INFO (Not Verified)\n"
                          f"System read: '{detected_name}'\n\n"
                          f"{general_response.text}"
            }
            
    except Exception as e:
        return {"hata": f"Error: {str(e)}"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)