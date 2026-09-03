# 48-Hour-Build-Nightingale-AI---Secure-Clinical-Intake-Prototype
**PROTOTYPE**
Nightingale AI - Secure Clinical Intake Prototype
**DISCLAIMER: This software is a prototype developed for the Nightingale 48-Hour Engineering Challenge. It is not intended for actual clinical, diagnostic, or emergency use. The AI is strictly non-diagnostic and programmed to escalate potential medical emergencies. All data processed in this repository should be synthetic; do not input real Personal Health Information (PHI).

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
