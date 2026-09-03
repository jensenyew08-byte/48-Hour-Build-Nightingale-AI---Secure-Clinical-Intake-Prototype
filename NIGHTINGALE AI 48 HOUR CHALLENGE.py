import re
import json
import uuid
from datetime import datetime
from openai import OpenAI

# 1. Point client to local Ollama server
client = OpenAI(
    base_url='http://localhost:11434/v1',
    api_key='ollama'
)

# ==========================================
# 1. ATTRIBUTION & STATE (Living Memory)
# ==========================================
patient_profile = {
    "internal_id": str(uuid.uuid4()),
    "attribution": {
        "channel": "instagram_ad_click",
        "landing_timestamp": str(datetime.now())
    },
    "symptoms": [],
    "medications": [],
    "escalated": False
}

# ==========================================
# 2. PHI REDACTION PIPELINE
# ==========================================
PHONE_REGEX = r'(\+?\d{1,4}[\s-]?)?\(?\d{2,4}\)?[\s-]?\d{3,4}[\s-]?\d{3,4}'
IC_NRIC_REGEX = r'\b[A-Za-z]\d{7}[A-Za-z]\b|\b\d{6}[\s\-]?\d{2}[\s\-]?\d{4}\b'
NAME_PATTERNS = r'(?i)\b(my name is|i am|i\'m|call me)\s+([a-z\s\/\-\']+?)(?=\.|\,|\band\b|$)'

def redact_phi(text: str) -> str:
    redacted = re.sub(PHONE_REGEX, '[REDACTED_PHONE]', text)
    redacted = re.sub(IC_NRIC_REGEX, '[REDACTED_ID]', redacted)
    def name_replacer(match):
        return f'{match.group(1)} [REDACTED_NAME]'
    return re.sub(NAME_PATTERNS, name_replacer, redacted)

# ==========================================
# 3. RISK GATING LOGIC
# ==========================================
EMERGENCY_KEYWORDS = ["crushing chest pain", "difficulty breathing", "heavy bleeding", "want to hurt myself"]

def evaluate_risk(message: str):
    lowered = message.lower()
    for keyword in EMERGENCY_KEYWORDS:
        if keyword in lowered:
            return {"level": "High", "reason": keyword, "escalate": True}
    if "chest" in lowered or "breath" in lowered:
        return {"level": "Medium", "reason": "Ambiguous respiratory", "escalate": True}
    return {"level": "Low", "reason": "General inquiry", "escalate": False}

# ==========================================
# 4. LLM INTEGRATION (Ollama)
# ==========================================
SYSTEM_PROMPT = """
You are Nightingale AI, a medical intake assistant. 
Rules:
1. Be empathetic but strictly non-diagnostic. Never say "you have X" or recommend treatments.
2. If asked for a diagnosis, state honestly you are an AI, cannot diagnose, and recommend consulting a clinician.

Output your response STRICTLY as a JSON object:
{
  "ai_message": "Your conversational reply.",
  "extracted_symptoms": ["list", "of", "symptoms"],
  "extracted_medications": ["list", "of", "medications"]
}
"""

def call_llm(clean_prompt: str):
    try:
        response = client.chat.completions.create(
            model="llama3.2", 
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": clean_prompt}
            ],
            temperature=0.1,
            response_format={ "type": "json_object" } 
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        return {
            "ai_message": "I'm routing your inquiry securely. Please hold.",
            "extracted_symptoms": [],
            "extracted_medications": []
        }

# ==========================================
# 5. TERMINAL DEMO INTERFACE
# ==========================================
def run_demo():
    print("\n" + "="*60)
    print("🏥 NIGHTINGALE AI - TERMINAL INTAKE PROTOTYPE")
    print("Simulating arrival via: Instagram Ad Click")
    print("Type 'exit' to end the simulation.")
    print("="*60 + "\n")
    
    while True:
        user_input = input("👤 Patient: ")
        if user_input.lower() in ['exit', 'quit']:
            print("Ending session.")
            break
            
        if patient_profile["escalated"]:
            print("🏥 Nightingale: Your case is pending nurse review. Please hold.")
            continue

        timestamp = str(datetime.now())
        
        # 1. Redact
        clean_input = redact_phi(user_input)
        
        # 2. Risk Gate
        risk_info = evaluate_risk(clean_input)
        
        # 3. LLM Processing
        llm_response = call_llm(clean_input)
        
        # 4. Update Memory with Provenance
        for sym in llm_response.get("extracted_symptoms", []):
            if not any(s['value'].lower() == sym.lower() for s in patient_profile["symptoms"]):
                patient_profile["symptoms"].append({"value": sym, "provenance_time": timestamp})
                
        for med in llm_response.get("extracted_medications", []):
            if not any(m['value'].lower() == med.lower() for m in patient_profile["medications"]):
                patient_profile["medications"].append({"value": med, "provenance_time": timestamp})

        # 5. Output Logs (Proving the backend constraints)
        print("\n" + "-"*40)
        print("🔍 SYSTEM AUDIT LOG (PHI-Free):")
        print(f"🔒 Clean Prompt : {clean_input}")
        print(f"⚠️ Risk Level   : {risk_info['level']} ({risk_info['reason']})")
        print(f"🧠 Mem Symptoms : {[s['value'] for s in patient_profile['symptoms']]}")
        print(f"🧠 Mem Meds     : {[m['value'] for m in patient_profile['medications']]}")
        print("-" * 40)

        # 6. Escalation or Chat
        if risk_info["escalate"]:
            patient_profile["escalated"] = True
            print("\n🚨 ESCALATION TRIGGERED 🚨")
            print("Payload Sent to Clinic:")
            print(json.dumps(patient_profile, indent=2))
            print("\n🏥 Nightingale: I have logged your symptoms. Because this may require medical attention, I am routing your details to a nurse right now. If this is an immediate emergency, please dial 999.\n")
        else:
            print(f"\n🏥 Nightingale: {llm_response.get('ai_message')}\n")

if __name__ == "__main__":
    run_demo()