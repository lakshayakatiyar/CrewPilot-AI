import os
import time
import gradio as gr
import requests
import random
from pathlib import Path

# Set your Gemini API Key here
GEMINI_API_KEY = ""  # <-- Add your Gemini API Key

# Create a folder to store generated files
output_dir = Path("generated project")
output_dir.mkdir(exist_ok=True)

# Function to call Gemini API
def call_gemini_api(prompt: str) -> str:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {'Content-Type': 'application/json'}
    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        return result['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        return f"Error during API request: {e}"

# Agent to simulate real code generation
def generate_code_files(prompt: str):
    if not GEMINI_API_KEY:
        return "Please provide a valid Gemini API Key.", None, None, None, None

    # Prompts for code generation
    prompts = {
        "frontend": f"Generate complete React frontend code for the following project. Include main App component and basic UI: {prompt}",
        "backend": f"Generate complete FastAPI backend for the following project. Include main.py, with endpoints and basic logic: {prompt}",
        "testing": f"Generate pytest tests for the backend of this project: {prompt}"
    }

    # Generate code
    frontend_code = call_gemini_api(prompts["frontend"])
    backend_code = call_gemini_api(prompts["backend"])
    testing_code = call_gemini_api(prompts["testing"])

    # Save files
    frontend_path = output_dir / "frontend_app.jsx"
    backend_path = output_dir / "backend_main.py"
    testing_path = output_dir / "test_backend.py"

    frontend_path.write_text(frontend_code)
    backend_path.write_text(backend_code)
    testing_path.write_text(testing_code)

    # Completion message
    summary = "🎉 All source code has been generated."

    return summary, frontend_code, backend_code, testing_code, str(output_dir)

# Simulated voice input
def simulate_voice_input():
    prompts = [
        "Build a fitness tracking app with user profiles and workout logs",
        "Create a cryptocurrency dashboard with real-time price updates",
        "Develop a blogging platform with markdown support and image uploads",
        "Build an e-commerce store with payment integration and product filters",
        "Create a note-taking app with rich text support and cloud sync"
    ]
    return random.choice(prompts)

# Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("# 🚀 AI Project Code Generator\nGenerate full code files using Gemini AI")

    with gr.Row():
        prompt_box = gr.Textbox(lines=3, label="Project Prompt")
        simulate_btn = gr.Button("🎤 Simulate Voice Input")

    simulate_btn.click(simulate_voice_input, outputs=prompt_box)

    run_btn = gr.Button("🧠 Generate Project Code")

    summary = gr.Textbox(label="Summary Message", interactive=False)
    frontend_box = gr.Code(label="Frontend Code")
    backend_box = gr.Code(label="Backend Code")
    testing_box = gr.Code(label="Testing Code")
    folder_path = gr.Textbox(label="Files Saved To", interactive=False)

    run_btn.click(
        generate_code_files,
        inputs=prompt_box,
        outputs=[summary, frontend_box, backend_box, testing_box, folder_path]
    )

demo.launch()
