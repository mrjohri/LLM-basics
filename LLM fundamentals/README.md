# PromptLab - Compare LLM Behavior

A 3-panel chat interface for experimenting with LLM parameters side by side. Send the same message to three independently configured panels and compare how different system prompts and parameters affect the model's responses.

![Python](https://img.shields.io/badge/Python-3.8+-blue) ![Flask](https://img.shields.io/badge/Flask-2.x-lightgrey) ![Groq](https://img.shields.io/badge/Groq-LLaMA_3.1-orange)

## Features

- 3 independent chat panels running simultaneously
- Per-panel configuration: system prompt, temperature, top-p, max tokens
- Persistent chat history per panel
- Powered by Groq's `llama-3.1-8b-instant` model

## Setup

1. Clone the repo
   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
   ```

2. Install dependencies
   ```bash
   pip install flask groq python-dotenv
   ```

3. Create your `.env` file
   ```bash
   cp .env.example .env
   ```
   Then open `.env` and add your [Groq API key](https://console.groq.com/keys):
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```

4. Run the app
   ```bash
   python app.py
   ```

5. Open `http://localhost:5000` in your browser

## Usage

- Set a different **system prompt** in each panel to give the model a different persona or role
- Adjust **temperature** (0–1) to control randomness — lower is more focused, higher is more creative
- Adjust **top-p** to control diversity of token sampling
- Set **max tokens** to limit response length
- Type a message and hit **Send** — all 3 panels respond to the same input simultaneously

## Project Structure

```
├── app.py              # Flask backend
├── templates/
│   └── index.html      # Frontend UI
├── static/
│   ├── script.js       # Chat logic
│   └── style.css       # Styles
├── .env                # Your API key (not committed)
├── .env.example        # Template for .env
└── .gitignore
```
