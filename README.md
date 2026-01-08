# 💊 Medication AI - Smart Medication Assistant

![Python](https://img.shields.io/badge/Backend-Python%20%7C%20FastAPI-blue)
![Flutter](https://img.shields.io/badge/Mobile-Flutter%20%7C%20Dart-02569B)
![Gemini AI](https://img.shields.io/badge/AI-Google%20Gemini%202.0-orange)
![License](https://img.shields.io/badge/License-MIT-green)

**Medication AI** is an AI-powered mobile assistant designed specifically for visually impaired individuals and the elderly. It recognizes medication boxes via camera, reads prospectuses, and provides audio guidance using Google Gemini Vision technology.

---

## 📂 Project Structure (Monorepo)

This project consists of two main components:

* **`backend/`**: Server-side application developed with Python and FastAPI. This handles the Google Gemini AI integration.
* **`mobile/`**: Mobile application interface developed with Flutter. Users interact with the camera and voice assistant here.

---

## 🚀 Key Features

* 📸 **Visual Recognition:** Instantly identifies medication by scanning the box or bottle.
* 🤖 **AI Analysis:** Uses the Google Gemini Vision model to explain the purpose and side effects of the medication.
* 🗣️ **Voice Assistant:** Reads the results aloud for visually impaired users (Text-to-Speech).
* ⚡ **High Performance:** Built on FastAPI for millisecond-level response times.

---

## ⚙️ Installation Guide

Follow these steps to run the project on your local machine.

### 1. Clone the Repository
Open your terminal and clone the project:
```bash
git clone [https://github.com/brknfk/MedicalBillProject.git]
cd MedicalBillApp
