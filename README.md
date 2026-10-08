# PromptCanvas 🎨

> **Turn rough ideas into stunning images.**

PromptCanvas is an AI-powered text-to-image studio built with **Streamlit**. It takes a simple image idea, uses an LLM to enhance it into a detailed diffusion prompt, and generates an image using **FLUX** through the Pollinations API.

## ✨ Features

- 📝 **Natural-language image prompts** — describe an image in simple words
- ✨ **AI prompt enhancement** — Groq's `openai/gpt-oss-20b` expands short ideas into detailed image prompts
- 🎨 **Style presets**
  - Realistic
  - Cinematic
  - Anime
  - Digital Art
  - 3D Render
- 🖼️ **FLUX image generation**
- 📐 Multiple image sizes
- 🎲 Reproducible generation with seed control
- 🚫 AI-generated negative prompts
- 💬 Chat-style generation history
- 🖼️ Session gallery
- ⬇️ Download generated images
- 🔐 API keys stored securely through environment variables / Streamlit Secrets

## 🏗️ Architecture

```text
User
  │
  │ Simple idea
  ▼
┌─────────────────────────┐
│      Streamlit UI       │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│ Groq / GPT-OSS-20B      │
│ Prompt Enhancement      │
└────────────┬────────────┘
             │
             │ Enhanced prompt
             ▼
┌─────────────────────────┐
│ Pollinations API        │
│ FLUX Image Generation   │
└────────────┬────────────┘
             │
             ▼
          🖼️ Image
             │
             ▼
┌─────────────────────────┐
│ Gallery + Download      │
└─────────────────────────┘
```

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core application |
| Streamlit | Web UI |
| Groq | LLM-based prompt enhancement |
| GPT-OSS-20B | Prompt enhancement model |
| Pollinations | Image generation API |
| FLUX | Text-to-image generation |
| Pillow | Image processing |
| Requests | API communication |
| python-dotenv | Local environment configuration |

## 📁 Project Structure

```text
promptcanvas/
│
├── app.py              # Streamlit application and UI
├── enhancer.py         # LLM prompt enhancement
├── generator.py        # Pollinations image generation
├── styles.py           # Image style presets
├── requirements.txt    # Python dependencies
├── .gitignore          # Files excluded from Git
├── .env                # Local API keys (not committed)
└── README.md
```

## 🚀 Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/promptcanvas.git
cd promptcanvas
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

macOS/Linux:

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API keys

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
POLLINATIONS_API_KEY=your_pollinations_api_key
```

**Never commit `.env` to GitHub.**

### 5. Run the application

```bash
streamlit run app.py
```

The application will open locally in your browser.

## 🧪 Example

Input:

```text
a lone astronaut in a flower field
```

With the **Cinematic** style selected, the LLM transforms the idea into a more detailed prompt containing elements such as:

- subject details
- environment
- lighting
- composition
- mood
- camera/visual characteristics

The resulting prompt is then sent to FLUX for image generation.

## 🎯 Design Goal

PromptCanvas is designed around a simple idea:

> **Users shouldn't need to know how to write complex image-generation prompts.**

Instead of requiring users to understand diffusion-model terminology, PromptCanvas provides a simple interface where they describe what they want and let the LLM handle prompt engineering.

## 🔐 Security

API keys are loaded through environment variables:

```python
os.getenv("GROQ_API_KEY")
os.getenv("POLLINATIONS_API_KEY")
```

The `.env` file should **never** be committed to the repository.

For Streamlit Cloud, configure the keys through **Streamlit Secrets** instead.

## ☁️ Deployment

PromptCanvas can be deployed using **Streamlit Community Cloud**.

Deployment flow:

```text
GitHub Repository
       │
       ▼
Streamlit Community Cloud
       │
       ├── Install requirements.txt
       ├── Load Streamlit Secrets
       └── Run app.py
              │
              ▼
        Public Web App
```

Required Streamlit secrets:

```toml
GROQ_API_KEY = "your_groq_api_key"
POLLINATIONS_API_KEY = "your_pollinations_api_key"
```

## 🔮 Future Improvements

- [ ] Image-to-image generation
- [ ] More advanced style presets
- [ ] Persistent user galleries
- [ ] User authentication
- [ ] Image comparison / variations
- [ ] Prompt history and favorites
- [ ] More image-generation models
- [ ] Advanced generation parameters
- [ ] Cloud image storage


---

**PromptCanvas — describe it simply, create it beautifully.**
