import os
from dotenv import load_dotenv
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from data_processor import DataProcessor
from model import DiseasePredictor
from chat_diagnosis import DiagnosisChat
from diagnostic_test import DiagnosticTest
from health_knowledge_base import HealthKnowledgeBase
import requests

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    import streamlit as st
    st.error("GEMINI_API_KEY is not set! Please create a .env file in the project root with your API key. Example: GEMINI_API_KEY=your_key_here")
    st.stop()
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=" + GEMINI_API_KEY

def get_gemini_recommendations(disease_name):
    prompt = f"""
    Write recommendations for a patient diagnosed with: {disease_name}.
    Use sections: overview (short summary), lifestyle (habits), diet (recommended and to avoid foods, vitamins/minerals), medical (basic advice and therapy), prevention (prevention tips).
    Respond in English. Format the answer as JSON with keys: overview, lifestyle, diet, medical, prevention.
    Keep the answer concise and practical for a patient.
    """
    data = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    try:
        response = requests.post(GEMINI_API_URL, json=data, timeout=20)
        response.raise_for_status()
        text = response.json()["candidates"][0]["content"]["parts"][0]["text"]
        import json as _json
        # Try to parse JSON from the response
        try:
            recs = _json.loads(text)
        except Exception:
            # If not pure JSON, try to extract JSON from text
            import re
            match = re.search(r'\{.*\}', text, re.DOTALL)
            if match:
                recs = _json.loads(match.group(0))
            else:
                recs = {"overview": text}
        # If the answer is too long, summarize it
        def summarize(text):
            prompt = f"Summarize the following medical recommendations in English, keep it short and practical for a patient:\n{text}"
            data = {"contents": [{"parts": [{"text": prompt}]}]}
            try:
                resp = requests.post(GEMINI_API_URL, json=data, timeout=20)
                resp.raise_for_status()
                return resp.json()["candidates"][0]["content"]["parts"][0]["text"]
            except Exception:
                return text
        for k in list(recs.keys()):
            v = recs[k]
            if isinstance(v, str) and len(v) > 1200:
                recs[k] = summarize(v)
            elif isinstance(v, list) and sum(len(str(x)) for x in v) > 1200:
                recs[k] = [summarize(' '.join(str(x) for x in v))]
            elif isinstance(v, dict):
                for subk in list(v.keys()):
                    subv = v[subk]
                    if isinstance(subv, str) and len(subv) > 1200:
                        v[subk] = summarize(subv)
                    elif isinstance(subv, list) and sum(len(str(x)) for x in subv) > 1200:
                        v[subk] = [summarize(' '.join(str(x) for x in subv))]
        return recs
    except Exception as e:
        return {"overview": f"AI error: {str(e)}"}

class DiseaseDetectorApp:
    def __init__(self):
        self.data_processor = DataProcessor()
        self.model = DiseasePredictor()
        self.chat_diagnosis = DiagnosisChat()
        self.diagnostic_test = DiagnosticTest(self.data_processor, self.model)
        self.health_knowledge = HealthKnowledgeBase()
        
    def train_model(self):
        """Train the model with all available data"""
        X, y = self.data_processor.load_data()
        self.model.train(X, y)
        
    def collect_user_profile(self):
        st.header("👤 Personal Information")
        st.write("Please enter some basic information to personalize your recommendations.")
        with st.form("user_profile_form"):
            col1, col2 = st.columns(2)
            with col1:
                age = st.number_input("Age", min_value=0, max_value=120, value=30)
                sex = st.selectbox("Sex", ["Male", "Female"])
            with col2:
                chronic = st.text_area("Chronic conditions (comma separated)", help="e.g. diabetes, hypertension")
                allergies = st.text_area("Allergies (comma separated)", help="e.g. penicillin, pollen")
            lifestyle = st.multiselect(
                "Lifestyle factors",
                ["Smoker", "Alcohol use", "Physically active", "Sedentary lifestyle", "Vegetarian", "Vegan", "High stress"]
            )
            submitted = st.form_submit_button("Continue")
        if submitted:
            st.session_state["user_profile"] = {
                "age": age,
                "sex": sex,
                "chronic": [c.strip().lower() for c in chronic.split(",") if c.strip()],
                "allergies": [a.strip().lower() for a in allergies.split(",") if a.strip()],
                "lifestyle": lifestyle
            }
            st.session_state["profile_completed"] = True
            st.rerun()

    def run(self):
        st.title("🩺 AI Disease Detector")
        # Initialize session states if not already done
        if "active_tab" not in st.session_state:
            st.session_state["active_tab"] = None
        if "method_selected" not in st.session_state:
            st.session_state["method_selected"] = False
        if "profile_completed" not in st.session_state:
            st.session_state["profile_completed"] = False
        if "user_profile" not in st.session_state:
            st.session_state["user_profile"] = {}

        # Prikupi osobne podatke prije prikaza glavnih funkcionalnosti
        if not st.session_state["profile_completed"]:
            self.collect_user_profile()
            return

        # Show the welcome screen if no method is selected
        if not st.session_state["method_selected"]:
            st.header("Welcome to AI Disease Detection System!")
            st.write("Choose how you would like to use the application:")
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("🔍 Select Symptoms", use_container_width=True):
                    st.session_state["active_tab"] = "Symptom Checker"
                    st.session_state["method_selected"] = True
                    st.rerun()
                st.caption("Select your symptoms manually")
            with col2:
                if st.button("📝 Complete Questionnaire", use_container_width=True):
                    st.session_state["active_tab"] = "Diagnostic Test"
                    st.session_state["method_selected"] = True
                    st.rerun()
                st.caption("Answer a series of questions for diagnosis")
            with col3:
                if st.button("💬 AI Chat", use_container_width=True):
                    st.session_state["active_tab"] = "Chat Diagnosis"
                    st.session_state["method_selected"] = True
                    st.rerun()
                st.caption("Talk with the AI doctor")
            st.markdown("---")
            st.write("### About the Application")
            st.write("""    
            AI Disease Detector uses advanced artificial intelligence algorithms to assess possible health conditions based on symptoms.
            You can use three different ways to interact with the application:
            - **Select Symptoms**: Manually select the symptoms you're experiencing
            - **Diagnostic Questionnaire**: Answer a series of structured questions
            - **AI Chat**: Talk with the AI doctor and describe your symptoms in natural language
            **Note**: This is an educational tool and does not replace professional medical diagnosis.
            """)
            return

        # Show the back button when in a mode
        if st.session_state["method_selected"]:
            if st.button("← Return to Home Screen"):
                st.session_state["method_selected"] = False
                st.session_state["active_tab"] = None
                st.rerun()

        # Show only the selected mode
        if st.session_state["active_tab"] == "Symptom Checker":
            self.run_symptom_checker()
        elif st.session_state["active_tab"] == "Diagnostic Test":
            self.run_diagnostic_test()
        elif st.session_state["active_tab"] == "Chat Diagnosis":
            self.run_chat_diagnosis()
            
    def _ascii_safe(self, text):
        import unicodedata
        if not isinstance(text, str):
            return str(text)
        # Zamijeni crte, navodnike i slova sličnim ASCII znakovima
        text = text.replace('—', '-').replace('–', '-').replace('“', '"').replace('”', '"').replace('’', "'").replace('‘', "'")
        # Transliterate (npr. č -> c)
        text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
        return text

    def generate_pdf(self, selected_symptoms, top_diseases, top_probabilities):
        from fpdf import FPDF
        import datetime
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, self._ascii_safe("AI Disease Detector - Diagnostic Report"), ln=True, align='C')
        pdf.set_font("Arial", '', 12)
        pdf.cell(0, 10, self._ascii_safe(f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}"), ln=True)
        pdf.ln(5)
        user_profile = st.session_state.get("user_profile", {})
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, self._ascii_safe("User Information:"), ln=True)
        pdf.set_font("Arial", '', 12)
        pdf.cell(0, 8, self._ascii_safe(f"Age: {user_profile.get('age', '-')}"), ln=True)
        pdf.cell(0, 8, self._ascii_safe(f"Sex: {user_profile.get('sex', '-')}"), ln=True)
        pdf.cell(0, 8, self._ascii_safe(f"Chronic conditions: {', '.join(user_profile.get('chronic', [])) or '-'}"), ln=True)
        pdf.cell(0, 8, self._ascii_safe(f"Allergies: {', '.join(user_profile.get('allergies', [])) or '-'}"), ln=True)
        pdf.cell(0, 8, self._ascii_safe(f"Lifestyle: {', '.join(user_profile.get('lifestyle', [])) or '-'}"), ln=True)
        pdf.ln(5)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, self._ascii_safe("Selected Symptoms:"), ln=True)
        pdf.set_font("Arial", '', 12)
        for s in selected_symptoms:
            pdf.cell(0, 8, self._ascii_safe(f"- {s.replace('_', ' ').title()}"), ln=True)
        pdf.ln(5)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, self._ascii_safe("Top Diagnoses:"), ln=True)
        pdf.set_font("Arial", '', 12)
        for disease, prob in zip(top_diseases, top_probabilities):
            pdf.cell(0, 8, self._ascii_safe(f"- {disease}: {prob*100:.1f}%"), ln=True)
        pdf.ln(5)
        pdf.set_font("Arial", 'I', 10)
        pdf.multi_cell(0, 7, self._ascii_safe("IMPORTANT: This is an AI-generated prediction and does NOT replace professional medical diagnosis. Please consult a qualified medical professional for accurate diagnosis."))
        return pdf.output(dest='S').encode('latin-1')

    def run_symptom_checker(self):
        st.subheader("🔍 Symptom Checker")
        st.write("Select your symptoms from the list below:")

        symptom_categories = {
            "General": ["fatigue", "weight_loss", "weight_gain", "weakness", "restlessness", "lethargy"],
            "Pain": ["headache", "joint_pain", "stomach_pain", "back_pain", "chest_pain", "knee_pain", "neck_pain"],
            "Skin": ["itching", "skin_rash", "nodal_skin_eruptions", "yellowish_skin", "patches_in_throat"],
            "Respiratory": ["continuous_sneezing", "breathlessness", "cough", "phlegm", "congestion"],
            "Temperature": ["high_fever", "mild_fever", "shivering", "chills"],
            "Digestive": ["vomiting", "nausea", "diarrhea", "constipation", "acidity", "indigestion"],
            "Other": ["dizziness", "muscle_weakness", "stiff_neck", "swelling_joints", "obesity", "depression"]
        }

        all_symptoms = self.data_processor.get_all_symptoms()
        if not all_symptoms:
            st.error("No symptoms found in the dataset.")
            return

        search = st.text_input("Search symptoms:").strip().lower()
        # Pripremi ključeve za sve checkboxove
        for category, symptoms in symptom_categories.items():
            for symptom in symptoms:
                if symptom in all_symptoms:
                    key = f"symptom_{symptom}"
                    if key not in st.session_state:
                        st.session_state[key] = False

        with st.form("symptom_form"):
            for category, symptoms in symptom_categories.items():
                with st.expander(category, expanded=False):
                    for symptom in symptoms:
                        if symptom in all_symptoms:
                            display_name = symptom.replace('_', ' ').title()
                            if search and search not in display_name.lower():
                                continue
                            key = f"symptom_{symptom}"
                            st.checkbox(display_name, key=key)
            # Prikupi sve označene simptome iz session_state (IZVAN forme, ne unutar nje)
            # (Ovo je workaround jer Streamlit forme ne ažuriraju session_state dok se ne submitaju)
            submitted = st.form_submit_button("Analyze Symptoms")

        # Sada izvan forme, odmah nakon forme, izračunaj selected_symptoms
        selected_symptoms = [symptom for category, symptoms in symptom_categories.items() for symptom in symptoms if symptom in all_symptoms and st.session_state.get(f"symptom_{symptom}")]

        # Onemogući gumb samo ako je lista prazna
        if len(selected_symptoms) == 0:
            st.info("Please select at least one symptom to enable analysis.")

        if submitted and len(selected_symptoms) > 0:
            # Provjera hitnih simptoma
            emergency = False
            if ("chest_pain" in selected_symptoms or "chest pain" in selected_symptoms) and ("breathlessness" in selected_symptoms or "breathlessness" in selected_symptoms):
                st.error("🚨 WARNING: Chest pain combined with breathlessness may indicate a medical emergency. Please seek immediate medical attention!")
                emergency = True
            # Prikaz lifestyle preporuka prema profilu
            user_profile = st.session_state.get("user_profile", {})
            if user_profile.get("lifestyle"):
                st.info(f"Lifestyle factors you selected: {', '.join(user_profile['lifestyle'])}")
            if not emergency:
                self.train_model()
                input_data = self.data_processor.prepare_input(selected_symptoms)
                predictions = self.model.predict(input_data)
                top_n = min(3, len(self.data_processor.label_encoder.classes_))
                top_indices = np.argsort(predictions[0])[-top_n:][::-1]
                top_diseases = self.data_processor.label_encoder.inverse_transform(top_indices)
                top_probabilities = predictions[0][top_indices]
                # Dodatna upozorenja za kronične bolesti
                if user_profile.get("chronic"):
                    for chronic in user_profile["chronic"]:
                        if chronic in [d.lower() for d in top_diseases]:
                            st.warning(f"⚠️ You have a chronic condition ({chronic.title()}) that matches a possible diagnosis. Please consult your doctor for tailored advice.")
                st.subheader("🔍 Analysis Results")
                st.success("Analysis complete! Here are the potential conditions based on your symptoms.")

                fig, ax = plt.subplots(figsize=(10, 5))
                y_pos = np.arange(len(top_diseases))
                probs_percentage = [p * 100 for p in top_probabilities]
                bars = ax.barh(y_pos, probs_percentage, align='center')
                ax.set_yticks(y_pos)
                ax.set_yticklabels([f"{disease}" for disease in top_diseases])
                ax.invert_yaxis()
                ax.set_title('Potential Conditions')
                for i, bar in enumerate(bars):
                    width = bar.get_width()
                    label_position = width + 1
                    ax.text(label_position, bar.get_y() + bar.get_height()/2, f'{probs_percentage[i]:.1f}%', va='center')
                ax.set_xlim(0, 115)
                plt.xlabel('Probability (%)')
                st.pyplot(fig)

                st.subheader("🔍 Detailed Analysis")
                col_left, col_right = st.columns([1, 1])
                for idx, (disease, prob) in enumerate(zip(top_diseases, top_probabilities)):
                    current_col = col_left if idx % 2 == 0 else col_right
                    with current_col:
                        prob_percentage = prob * 100
                        color = "🔴" if prob_percentage > 70 else "🟡" if prob_percentage > 40 else "🟢"
                        severity = "High" if prob_percentage > 70 else "Medium" if prob_percentage > 40 else "Low"
                        st.write(f"{color} **{disease}**")
                        st.progress(prob_percentage / 100)
                        st.write(f"Probability: {prob_percentage:.1f}% ({severity} likelihood)")
                        disease_info = self.data_processor.get_disease_info(disease)
                        with st.expander("Learn more about this condition"):
                            st.write(disease_info)
                            st.write(f"**Selected symptoms**: {', '.join([s.replace('_', ' ').title() for s in selected_symptoms])}")
                        st.write("---")
                st.warning("""
                ⚠️ **IMPORTANT DISCLAIMER:**
                - This is an AI prediction only and does NOT replace professional medical diagnosis
                - Please consult a qualified medical professional for accurate diagnosis
                - Seek immediate medical attention for serious symptoms
                """)
                self.show_recommendations_and_pdf(selected_symptoms, top_diseases, top_probabilities)
                self.show_ai_recommendations_panel(top_diseases)

    def show_ai_recommendations_panel(self, top_diseases):
        import re
        def is_croatian(text):
            cro_words = ["lijek", "preporuke", "prehrana", "simptomi", "liječnik", "osipa", "svrbež", "život", "prepoznati", "pomoć", "odjeća", "voda", "hrana", "infekcija", "zdravlje", "liječničku", "imunološki"]
            return isinstance(text, str) and any(w in text.lower() for w in cro_words)
        def clean_html(text):
            if not isinstance(text, str):
                return text
            return re.sub(r'<[^>]+>', '', text)
        def gemini_translate(text):
            prompt = f"Please translate this to English (medical context, keep it concise):\n{clean_html(text)}"
            data = {"contents": [{"parts": [{"text": prompt}]}]}
            try:
                response = requests.post(GEMINI_API_URL, json=data, timeout=20)
                response.raise_for_status()
                return response.json()["candidates"][0]["content"]["parts"][0]["text"]
            except Exception:
                return clean_html(text)
        def translate_if_needed(text):
            t = clean_html(text)
            if is_croatian(t):
                return gemini_translate(t)
            return t
        def render_section(title, section):
            st.write(f"**{title}:**")
            if section is None:
                st.info("No data available.")
            elif isinstance(section, str):
                st.write(translate_if_needed(section))
            elif isinstance(section, list):
                for item in section:
                    st.write(f"- {translate_if_needed(item)}")
            elif isinstance(section, dict):
                for key, value in section.items():
                    st.write(f"- {translate_if_needed(str(key).replace('_', ' ').title())}")
                    if isinstance(value, list):
                        for item in value:
                            st.write(f"    - {translate_if_needed(item)}")
                    elif isinstance(value, dict):
                        for subkey, subval in value.items():
                            st.write(f"    - {translate_if_needed(str(subkey))}: {translate_if_needed(str(subval))}")
                    else:
                        st.write(f"    - {translate_if_needed(value)}")
            else:
                st.write(translate_if_needed(str(section)))
        with st.expander("💡 AI Recommendations for Your Diagnoses", expanded=True):
            for disease in top_diseases:
                st.markdown(f"### 🦠 {disease}")
                recs = self.health_knowledge.recommendations.get(disease, {})
                if not recs:
                    with st.spinner(f"Generating AI recommendations for {disease}..."):
                        recs = get_gemini_recommendations(disease)
                if recs:
                    for section_name in ["overview", "lifestyle", "diet", "medical", "prevention"]:
                        if section_name in recs:
                            render_section(section_name.capitalize(), recs[section_name])
                else:
                    st.info("No recommendations available for this condition.")
                st.markdown("---")

    def show_recommendations_and_pdf(self, selected_symptoms, top_diseases, top_probabilities):
        """Prikazuje PDF download gumb za dijagnoze (preporuke su sada u posebnom panelu)"""
        pdf_bytes = self.generate_pdf(selected_symptoms, top_diseases, top_probabilities)
        st.download_button(
            label="Download diagnosis as PDF",
            data=pdf_bytes,
            file_name="diagnosis_report.pdf",
            mime="application/pdf"
        )

    def run_diagnostic_test(self):
        self.train_model()
        self.diagnostic_test.run_test()

    def run_chat_diagnosis(self):
        self.chat_diagnosis.render_chat_interface()

# Main entry point
if __name__ == "__main__":
    app = DiseaseDetectorApp()
    app.run()
