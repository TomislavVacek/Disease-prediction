# AI Disease Detector

A Streamlit-based application that uses AI and machine learning to predict possible diseases based on user symptoms, profile, and lifestyle. The app provides:

- Symptom checker and diagnostic questionnaire
- AI-generated recommendations (lifestyle, diet, medical, prevention) in English
- PDF export of user info, symptoms, and diagnoses (no AI advice in PDF)
- Modern, user-friendly interface

## Features
- Select symptoms or answer a diagnostic questionnaire
- Personalized results based on age, sex, chronic conditions, allergies, and lifestyle
- Visual probability chart for top diagnoses
- Downloadable PDF report
- AI recommendations panel for each diagnosis

## How to Run
1. Install requirements:
   ```
   pip install -r requirements.txt
   pip install python-dotenv
   ```
2. Create a `.env` file in the project root (see `.env.example`) and add your Google Gemini API key:
   ```
   GEMINI_API_KEY=your_google_gemini_api_key_here
   ```
3. Start the app:
   ```
   streamlit run app.py
   ```

## Disclaimer
This tool is for educational purposes only and does not replace professional medical advice. Always consult a qualified healthcare provider for diagnosis and treatment.
