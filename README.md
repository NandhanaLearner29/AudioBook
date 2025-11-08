# 📖 PDF to Audiobook Converter

This Python script converts the text content of a PDF file into an audiobook (MP3 format) using **Google Cloud Text-to-Speech (TTS)**.  
It automatically extracts text from a PDF, splits it into manageable chunks, and generates natural-sounding audio in a voice of your choice — male, female, or neutral.

---

## 🚀 Features

- Extracts text from any `.pdf` file  
- Uses **Google Cloud Text-to-Speech** for realistic voice synthesis  
- Supports **male**, **female**, and **neutral** voices  
- Automatically splits long text into chunks under 5000 bytes (Google API limit)  
- Outputs high-quality **MP3 audio files**

---

## 🧰 Requirements

Before running the script, ensure you have the following installed:

- Python 3.8 or higher  
- [Google Cloud SDK](https://cloud.google.com/sdk/docs/install)  
- Google Cloud **Text-to-Speech API** enabled  
- A valid **service account key** (`.json` file) downloaded from Google Cloud Console  

### Python Libraries  
Install the required packages using pip:

```bash
pip install PyPDF2 google-cloud-texttospeech
