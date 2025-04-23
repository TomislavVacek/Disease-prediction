import streamlit as st
import pandas as pd
import numpy as np

class DiagnosticTest:
    """Class to handle the guided diagnostic test functionality"""
    
    def __init__(self, data_processor, model):
        self.data_processor = data_processor
        self.model = model
        self.questions = {
            "general": {
                "text": "Which general symptoms are you experiencing?",
                "options": ["fatigue", "weight_loss", "weight_gain", "weakness", "restlessness", "lethargy"],
                "type": "multiselect"
            },
            "pain": {
                "text": "Are you experiencing any pain? If so, where?",
                "options": ["headache", "joint_pain", "stomach_pain", "back_pain", "chest_pain", "knee_pain", "neck_pain"],
                "type": "multiselect"
            },
            "duration": {
                "text": "How long have you been experiencing these symptoms?",
                "options": ["Less than a day", "1-3 days", "3-7 days", "1-2 weeks", "More than 2 weeks"],
                "type": "radio"
            },
            "fever": {
                "text": "Do you have fever or elevated temperature?",
                "options": ["No fever", "Mild fever (37-38°C)", "High fever (above 38°C)", "Fever with chills"],
                "type": "radio"
            },
            "skin": {
                "text": "Have you noticed any skin changes?",
                "options": ["itching", "skin_rash", "nodal_skin_eruptions", "yellowish_skin", "patches_in_throat"],
                "type": "multiselect"
            },
            "respiratory": {
                "text": "Do you have any respiratory symptoms?",
                "options": ["continuous_sneezing", "breathlessness", "cough", "phlegm", "congestion"],
                "type": "multiselect"
            },
            "digestive": {
                "text": "Are you experiencing any digestive issues?",
                "options": ["vomiting", "nausea", "diarrhea", "constipation", "acidity", "indigestion"],
                "type": "multiselect"
            },
            "severity": {
                "text": "How would you rate the severity of your symptoms?",
                "options": ["Mild - they don't interfere with daily activities", 
                           "Moderate - somewhat interfere with daily activities", 
                           "Severe - significantly impact daily activities"],
                "type": "radio"
            }
        }
        
    def initialize_test(self):
        """Initialize test state"""
        if 'test_stage' not in st.session_state:
            st.session_state.test_stage = 0
            
        if 'selected_symptoms' not in st.session_state:
            st.session_state.selected_symptoms = []
            
        if 'test_answers' not in st.session_state:
            st.session_state.test_answers = {}
    
    def run_test(self):
        """Run the diagnostic test"""
        # Initialize test state
        self.initialize_test()
        
        # Create a header for the test
        st.subheader("🩺 Guided Diagnostic Test")
        st.write("Answer these questions to help us identify your condition.")
        
        # Progress bar to show test progress
        stages = list(self.questions.keys())
        total_stages = len(stages)
        
        if st.session_state.test_stage < total_stages:
            # Show progress
            progress = st.session_state.test_stage / total_stages
            st.progress(progress)
            
            # Get current question
            current_stage = stages[st.session_state.test_stage]
            question = self.questions[current_stage]
            
            # Display the current question
            st.write(f"### {question['text']}")
            
            # Based on question type, show different input types
            if question['type'] == 'multiselect':                # For symptoms, format the display names
                display_options = [opt.replace('_', ' ').title() for opt in question['options']]
                display_options.append("None of the above")  # Add none option
                mapping = dict(zip(display_options[:-1], question['options']))  # Exclude the "None" option from mapping
                
                # Show multiselect for symptoms
                selected = st.multiselect(
                    "Select all that apply:",
                    options=display_options
                )                    # Store answers when continuing
                if st.button("Continue", key=f"btn_{current_stage}"):
                    # Check if "None of the above" was selected along with symptoms
                    if "None of the above" in selected and len(selected) > 1:
                        st.error("Please select either 'None of the above' or specific symptoms, not both.")
                        return
                        
                    if "None of the above" not in selected:
                        # Map back to original symptom names
                        original_symptoms = [mapping[selected_opt] for selected_opt in selected]
                        st.session_state.test_answers[current_stage] = original_symptoms
                        st.session_state.selected_symptoms.extend(original_symptoms)
                    else:
                        # Store empty list for this stage
                        st.session_state.test_answers[current_stage] = []
                        
                    st.session_state.test_stage += 1
                    st.rerun()
                    
            elif question['type'] == 'radio':
                # Radio button for single selection questions
                selected = st.radio(
                    "Select one option:",
                    options=question['options']
                )
                  # Store answer and continue
                if st.button("Continue", key=f"btn_{current_stage}"):
                    st.session_state.test_answers[current_stage] = selected
                    
                    # For fever, map answers to symptoms
                    if current_stage == "fever" and selected != "No fever":
                        if "High fever" in selected:
                            st.session_state.selected_symptoms.append("high_fever")
                        else:
                            st.session_state.selected_symptoms.append("mild_fever")
                            
                    st.session_state.test_stage += 1
                    st.rerun()
        else:
            # Test completed, show results
            st.success("✅ Test completed! Analyzing your symptoms...")
            
            # Check if any symptoms were selected
            if not st.session_state.selected_symptoms:
                st.warning("⚠️ No specific symptoms were detected from your answers. Please try again or use the symptom checker for more specific selection.")
                  # Reset button
                if st.button("Start Over"):
                    for key in ['test_stage', 'selected_symptoms', 'test_answers']:
                        if key in st.session_state:
                            del st.session_state[key]
                    st.rerun()
                    
                return
            
            # Display selected symptoms
            st.write("### Detected Symptoms")
            st.write("Based on your answers, we identified the following symptoms:")
            
            for symptom in st.session_state.selected_symptoms:
                st.write(f"- {symptom.replace('_', ' ').title()}")
            
            # Prepare data for prediction
            try:
                # Prepare input based on selected symptoms
                input_data = self.data_processor.prepare_input(st.session_state.selected_symptoms)
                
                # Get prediction
                predictions = self.model.predict(input_data)
                
                # Get top 3 predictions
                top_n = min(3, len(self.data_processor.label_encoder.classes_))
                top_indices = np.argsort(predictions[0])[-top_n:][::-1]
                top_diseases = self.data_processor.label_encoder.inverse_transform(top_indices)
                top_probabilities = predictions[0][top_indices]
                
                # Display results
                st.subheader("🔍 Analysis Results")
                st.success("Analysis complete! Here are the potential conditions based on your symptoms.")
                
                # Create a bar chart for visualization
                import matplotlib.pyplot as plt
                fig, ax = plt.subplots(figsize=(10, 5))
                y_pos = np.arange(len(top_diseases))
                
                # Convert probabilities to percentages
                probs_percentage = [p * 100 for p in top_probabilities]
                
                # Create horizontal bar chart
                bars = ax.barh(y_pos, probs_percentage, align='center')
                ax.set_yticks(y_pos)
                ax.set_yticklabels([f"{disease}" for disease in top_diseases])
                ax.invert_yaxis()  # Labels read top-to-bottom
                ax.set_title('Potential Conditions')
                
                # Add percentage labels to the bars
                for i, bar in enumerate(bars):
                    width = bar.get_width()
                    label_position = width + 1  # Position the label right after the bar
                    ax.text(label_position, bar.get_y() + bar.get_height()/2, f'{probs_percentage[i]:.1f}%',
                            va='center')
                
                # Set x-axis limit to allow space for percentage labels
                ax.set_xlim(0, 115)  # Allow extra space for labels
                plt.xlabel('Probability (%)')
                st.pyplot(fig)
                
                # Show detailed results
                st.subheader("🔍 Detailed Analysis")
                
                # Create two columns for the detailed analysis
                col_left, col_right = st.columns([1, 1])
                
                for idx, (disease, prob) in enumerate(zip(top_diseases, top_probabilities)):
                    # Alternate between left and right columns
                    current_col = col_left if idx % 2 == 0 else col_right
                    
                    with current_col:
                        prob_percentage = prob * 100
                        color = "🔴" if prob_percentage > 70 else "🟡" if prob_percentage > 40 else "🟢"
                        severity = "High" if prob_percentage > 70 else "Medium" if prob_percentage > 40 else "Low"
                        
                        st.write(f"{color} **{disease}**")
                        st.progress(prob_percentage / 100)
                        st.write(f"Probability: {prob_percentage:.1f}% ({severity} likelihood)")
                        
                        # Add disease information
                        disease_info = self.data_processor.get_disease_info(disease)
                        with st.expander("Learn more about this condition"):
                            st.write(disease_info)
                            st.write(f"**Common symptoms**: {', '.join([s.replace('_', ' ').title() for s in st.session_state.selected_symptoms])}")
                        
                        st.write("---")
                
                st.warning("""
                ⚠️ **IMPORTANT DISCLAIMER:**
                - This is an AI prediction only and does NOT replace professional medical diagnosis
                - Please consult a qualified medical professional for accurate diagnosis
                - Seek immediate medical attention for serious symptoms
                """)
                # === DODANO: Prikaz PDF gumba i AI preporuka ===
                from app import DiseaseDetectorApp
                app = DiseaseDetectorApp()
                app.show_recommendations_and_pdf(
                    st.session_state.selected_symptoms,
                    top_diseases,
                    top_probabilities
                )
                app.show_ai_recommendations_panel(top_diseases)
                # === KRAJ DODATKA ===
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                st.info("Please make sure all files are properly configured and try again.")
