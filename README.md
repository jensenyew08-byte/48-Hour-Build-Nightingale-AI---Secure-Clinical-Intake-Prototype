# 48-Hour-Build-Nightingale-AI---Secure-Clinical-Intake-Prototype
**PROTOTYPE**
Nightingale AI - Secure Clinical Intake Prototype

**DISCLAIMER: This software is a prototype developed for the Nightingale 48-Hour Engineering Challenge. It is not intended for actual clinical, diagnostic, or emergency use. The AI is strictly non-diagnostic and programmed to escalate potential medical emergencies. All data processed in this repository should be synthetic; do not input real Personal Health Information (PHI). The AI runs locally and is not connected to any online services. This software is also my first attempt in making an AI. The code does not contain a GUI and instead runs in a terminal window. Code written is referred either from online Internet resources or AI. Use caution when trying out the software.

Setup & Run Instructions
This application uses a local LLM via Ollama to ensure complete data privacy and zero API latency.

1. Prerequisites

Python 3.9+ installed.

Ollama installed and running on your machine.

2. Installation
   
Clone this repository and install the required Python packages:

PowerShell
pip install openai pytest

3. Starting the Local AI Server
Before running the application, you must start the local LLM in a dedicated terminal window:

PowerShell
ollama run llama3.2

Leave this terminal open in the background.

4. Running the Application
   
Open a new terminal window in the project directory and run the terminal prototype:

PowerShell
python test.py


Where Redaction Happens

PHI redaction is strictly enforced server-side before any data is transmitted to the LLM[cite: 1]. The redact_phi() function intercepts incoming strings and applies regex-based masking for Southeast Asian naming conventions, phone numbers, and NRIC/ID formats (e.g., replacing them with [REDACTED_NAME])[cite: 1]. The raw PHI never enters the LLM prompt and is scrubbed from all generated system audit logs[cite: 1].

RBAC (Role-Based Access Control) Enforcement

Access control is enforced at the state level[cite: 1]. In a full production deployment, RBAC is handled via backend server checks where a LeadSession cannot access a PatientSession without passing through the Authentication and Consent gateway[cite: 1]. Patient users are strictly isolated to their own internal_id, while simulated staff/clinician accounts have scoped access to the Escalations_DB[cite: 1]. Unauthorized access attempts are rejected before state retrieval[cite: 1].
