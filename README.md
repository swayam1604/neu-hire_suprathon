# NeuHire – AI-Powered Interview Evaluation System 🧠🎙️

NeuHire is an AI/ML-based automated interviewing and candidate evaluation tool, developed as a prototype submission for **SuPrathon 2K25** (AI/ML Track). The system is designed to simulate mock technical interviews, capture candidate responses, and generate intelligent feedback using Natural Language Processing (NLP) and AI-driven analysis.

---

## 📌 Project Overview

**NeuHire** aims to streamline and scale the interview process through automation and AI. It enables:
- Conducting **mock interviews** with predefined questions.
- Capturing candidate **textual or verbal responses**.
- Generating detailed feedback using **ML models** that analyze fluency, relevance, sentiment, and confidence.
- Helping candidates **self-evaluate** and recruiters **pre-screen** efficiently.

Even though the project is currently **incomplete**, it demonstrates a functional concept, backend planning, and UI/UX mockup direction.

---

## 🧠 Motivation

Recruiters and hiring managers spend a lot of time manually interviewing candidates, often introducing subjectivity and inefficiency. On the other side, candidates lack structured feedback to improve.  
**NeuHire** bridges this gap using AI for:
- **Bias-free, scalable evaluations**
- **NLP-based content analysis**
- **Speech & sentiment feedback** (future enhancement)

---

## 🔍 Use Cases

- 🚀 Technical hiring assessments
- 🎓 AI-powered mock interviews for students/jobseekers
- 🤖 Resume-to-Interview integration (planned)
- 📊 Data-driven hiring pipelines

---

## 💡 Features (Planned / Implemented)

| Feature | Status |
|--------|--------|
| Question-Response Interview Interface | 🟡 Planned |
| Text Input-Based Candidate Response | ✅ Implemented |
| Speech Recognition Support | 🟡 Planned |
| GPT/BERT-based NLP Scoring | 🟡 Planned |
| Sentiment & Fluency Evaluation | 🟡 Planned |
| AI Feedback Report Generation | 🟡 Planned |
| Admin Portal / Recruiter View | 🔲 Future Scope |
| UI Flow & Mock Screens | ✅ Designed |

---

## ⚙️ Tech Stack

| Component | Technology |
|----------|------------|
| Backend  | Python, Flask |
| NLP/AI   | HuggingFace Transformers, NLTK, SpaCy |
| Audio Analysis (Planned) | SpeechRecognition, pyaudio |
| UI / Frontend | HTML/CSS (Prototype), React.js (Planned) |
| Hosting | GitHub Pages / Netlify (optional) |
| Data | Custom Q&A dataset for interviews |
| Deployment | Not Deployed (Prototype Phase) |

---

## 🧾 Sample Interview Flow
User starts interview → Prompted with questions → Answers via text/speech → Backend parses responses → NLP scoring model analyzes → Feedback generated & displayed in UI or saved to report.


---

## 📁 Repository Structure

neu-hire_suprathon/
├── backend/
│ ├── app.py # Flask backend
│ ├── interview_analyzer.py # NLP-based analysis logic
│ ├── utils.py # Helper functions
│ └── requirements.txt
├── frontend/
│ ├── index.html # Simple prototype UI
│ └── styles.css
├── model/
│ └── sample_model.pkl # Placeholder for trained model
├── data/
│ └── sample_questions.txt # Mock interview questions
├── static/
│ └── logo.png # Branding assets
├── templates/
│ └── interview.html # Flask template
├── PPT/
│ └── NeuHire_Suprathon_Presentation.pptx
├── screenshots/
│ └── ui_mockup.png
├── README.md


  -- Author --
Name: Swayam Sharma
Email: swayams1604@gmail.com
Hackathon: SuPrathon 2K25 – AI/ML Track


