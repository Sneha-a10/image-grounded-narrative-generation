# 🔥 Controlled Multimodal Story Generation System

## 📌 Overview

This project is a **controlled multimodal AI system** that generates descriptive stories from images while enforcing strict validation constraints.

Unlike traditional AI generators, this system does **not blindly generate output**.
Instead, it follows a structured pipeline:

```
Image → Caption → Signals → Story → Validation → Decision → Retry
```

If a generated story does not align with the image, it is **automatically not aligned and regenerated** with stricter constraints.

---

## 🎯 Key Features

* 🧠 **Multimodal Understanding**

  * Image → Caption (BLIP)
  * Caption → Structured Signals (NLP)

* ✍️ **Controlled Story Generation**

  * Uses local LLM (Ollama - phi3)
  * Generates structured JSON output

* ✅ **Validation Layer**

  * Image alignment scoring (CLIP)
  * Caption alignment scoring
  * Signal consistency checking

* 🔁 **Regeneration Loop**

  * Automatically retries on validation mismatch
  * Applies stricter constraints each time

* 🎛️ **User Controls**

  * Upload image
  * Provide optional caption
  * Select generation preset
  * View full retry trace

* 🖥️ **Transparent UI**

  * Shows intermediate attempts
  * Displays constraints and decisions

* 🔊 **Text-to-Speech (Optional)**

  * Converts final story into audio

---

## 🧱 System Architecture

```
                ┌──────────────┐
                │   Image      │
                └──────┬───────┘
                       ↓
              ┌──────────────────┐
              │ Vision Encoder   │ (CLIP)
              └──────────────────┘
                       ↓
              ┌──────────────────┐
              │ Caption Generator│ (BLIP)
              └──────────────────┘
                       ↓
              ┌──────────────────┐
              │ Signal Extraction│ (spaCy/rules)
              └──────────────────┘
                       ↓
              ┌──────────────────┐
              │ Language Layer   │ (phi3 via Ollama)
              └──────────────────┘
                       ↓
              ┌──────────────────┐
              │ Validation Layer │
              └──────────────────┘
                       ↓
              ┌──────────────────┐
              │ Decision Engine  │
              └──────────────────┘
                       ↓
              ┌──────────────────┐
              │ Retry Controller │
              └──────────────────┘
```

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone <your-repo-link>
cd image-grounded-narrative-generation
```

---

### 2. Create Virtual Environment

```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🤖 Ollama Setup (REQUIRED)

This project uses **Ollama** to run a local LLM (phi3).

---

### 🔹 Step 1: Install Ollama

Download from:
https://ollama.com/download

---

### 🔹 Step 2: Pull Model

```bash
ollama pull phi3
```

---

### 🔹 Step 3: Run Ollama (Optional check)

```bash
ollama run phi3
```

If it responds, setup is correct.

---

### 🔹 Important Notes

* Ollama runs **outside the Python environment**
* Your Python code connects to it as a local service
* No API key required

---

## 🚀 Running the Project

### Start Flask App

```bash
python app.py
```

---

### Open in Browser

```
http://127.0.0.1:5000
```

---

## 🧪 How to Use

1. Upload an image
2. (Optional) Enter a custom caption
3. Select a preset style
4. Click **Generate Story**

---

## 📊 Output Explanation

The UI displays:

### 🟢 Input Section

* Image
* Caption
* Extracted signals

### 🟡 Generation Process

* Attempt-wise story generation
* Score per attempt
* Constraint changes

### 🔵 Final Result

* Final validated story
* Decision (Accepted / Not Aligned)
* Number of attempts

---

## ⚠️ Important Notes

* The system may **reject outputs** if they don’t align with the image
* This is **intentional behavior**, not an error
* User-provided captions improve accuracy significantly

---

## 🧠 Design Philosophy

This project follows:

```
LLM = Worker
System = Controller
```

The LLM does **not decide correctness**.
All outputs are verified through deterministic validation.

---

## 🛠️ Tech Stack

* Python
* Flask
* PyTorch
* Transformers (HuggingFace)
* spaCy
* Ollama (phi3)
* HTML + CSS + JS

---

## 📦 Project Structure

```
├── app.py
├── main_pipeline.py
├── vision_layer/
├── caption_layer/
├── language_layer/
├── validation_layer/
├── constraint_generation/
├── templates/
├── static/
└── tests/
```

---

## 🚨 Known Limitations

* Caption quality may vary for artistic images
* Signal extraction is rule-based (not perfect)
* Performance depends on system RAM (8GB minimum recommended)

---

## ✅ Future Improvements

* Better caption models
* Stronger signal extraction
* Improved constraint learning
* Faster inference

---

## 👩💻 Author

Sneha Agarwal
BTech Computer Science

---

## 🧾 License

For academic use only
