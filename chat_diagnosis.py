import streamlit as st
import pandas as pd
import numpy as np
import os
from data_processor import DataProcessor
from model import DiseasePredictor

class DiagnosisChat:
    def __init__(self):
        self.data_processor = DataProcessor()
        self.model = DiseasePredictor()
        self.symptom_questions = {
            "general": "Could you describe what symptoms you're experiencing?",
            "pain": "Are you experiencing any pain? If so, where and how severe?",
            "duration": "How long have you been experiencing these symptoms?",
            "fever": "Do you have a fever or elevated temperature?",
            "skin": "Have you noticed any changes in your skin like rashes or discoloration?",
            "respiratory": "Are you having any trouble breathing or coughing?",
            "digestive": "Do you have any digestive issues like nausea, vomiting, or diarrhea?",
            "head": "Are you experiencing headaches, dizziness, or vision problems?",
            "fatigue": "How are your energy levels? Do you feel unusually tired?",
            "other": "Are there any other symptoms or concerns you'd like to mention?"
        }
        self.symptom_keywords = {
            "itching": ["itch", "itchy", "itching", "scratch"],
            "skin_rash": ["rash", "red spots", "skin eruption", "red skin"],
            "nodal_skin_eruptions": ["skin lumps", "skin bumps", "nodules", "skin eruptions"],
            "continuous_sneezing": ["sneezing", "sneeze", "allergic reaction"],
            "shivering": ["shiver", "shaking", "trembling", "chills"],
            "chills": ["cold", "chills", "shaking", "cold feeling"],
            "joint_pain": ["joint pain", "sore joints", "painful joints", "arthritis"],
            "stomach_pain": ["stomach pain", "abdominal pain", "tummy ache", "belly pain"],
            "acidity": ["heartburn", "acid reflux", "sour taste", "acidity"],
            "vomiting": ["vomit", "throw up", "nausea", "sick"],
            "fatigue": ["tired", "exhausted", "fatigue", "no energy", "low energy", "weakness"],
            "anxiety": ["anxious", "worried", "panic", "fear"],
            "mood_swings": ["mood changes", "emotional", "irritable", "mood swings"],
            "weight_loss": ["lost weight", "weight loss", "getting thinner", "losing weight"],
            "restlessness": ["can't sit still", "restless", "agitated", "fidgety"],
            "lethargy": ["sluggish", "slow", "lethargic", "no energy"],
            "patches_in_throat": ["throat patches", "white spots in throat", "sore throat"],
            "cough": ["coughing", "cough", "hacking"],
            "high_fever": ["high fever", "high temperature", "feeling hot", "overheated"],
            "breathlessness": ["short of breath", "can't breathe", "breathing difficulty", "wheezing"],
            "neck_pain": ["neck pain", "sore neck", "stiff neck", "neck ache"],
            "back_pain": ["back pain", "sore back", "back ache", "back hurts", "back problem"]
        }
        
    def initialize_chat(self):
        """Initialize chat history and other session state variables"""
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
            self._add_message("AI Doctor", "Hello! I'm your AI medical assistant. I'll ask you some questions to help understand your symptoms. How can I help you today?", "assistant")
            
        if 'current_question' not in st.session_state:
            st.session_state.current_question = "general"
            
        if 'detected_symptoms' not in st.session_state:
            st.session_state.detected_symptoms = set()
            
        if 'conversation_stage' not in st.session_state:
            st.session_state.conversation_stage = "gathering_initial"
            
        if 'diagnosis_made' not in st.session_state:
            st.session_state.diagnosis_made = False
            
        if 'repetition_count' not in st.session_state:
            st.session_state.repetition_count = 0
            
        if 'last_message' not in st.session_state:
            st.session_state.last_message = ""
            
    def _add_message(self, sender, message, role):
        """Add a message to the chat history"""
        st.session_state.chat_history.append({
            "sender": sender,
            "message": message,
            "role": role
        })
        
    def detect_symptoms(self, user_input):
        """Detect symptoms from user input based on keywords"""
        user_input = user_input.lower()
        
        # Track if we found any symptoms in this message
        found_symptoms_in_message = False
        
        # Check for each symptom's keywords in the user input
        for symptom, keywords in self.symptom_keywords.items():
            for keyword in keywords:
                if keyword.lower() in user_input:
                    st.session_state.detected_symptoms.add(symptom)
                    found_symptoms_in_message = True
                    break
        
        # Smart detection for back pain
        if "back" in user_input and ("pain" in user_input or "hurt" in user_input or "ache" in user_input):
            st.session_state.detected_symptoms.add("back_pain")
            found_symptoms_in_message = True
            
        # Smart detection for fever
        if "fever" in user_input or "temperature" in user_input:
            if "high" in user_input or "severe" in user_input:
                st.session_state.detected_symptoms.add("high_fever")
            else:
                st.session_state.detected_symptoms.add("mild_fever")
            found_symptoms_in_message = True
            
        # Smart detection for fatigue
        if "tired" in user_input or "fatigue" in user_input or "no energy" in user_input or "don't have energy" in user_input:
            st.session_state.detected_symptoms.add("fatigue")
            found_symptoms_in_message = True
            
        # Store whether we found symptoms in this message
        if 'found_symptoms_in_message' not in st.session_state:
            st.session_state.found_symptoms_in_message = found_symptoms_in_message
        else:
            st.session_state.found_symptoms_in_message = st.session_state.found_symptoms_in_message or found_symptoms_in_message
                    
        return list(st.session_state.detected_symptoms)
        
    def get_next_question(self):
        """Determine the next question to ask based on conversation stage"""
        if st.session_state.conversation_stage == "gathering_initial":
            # After initial input, ask about pain
            st.session_state.current_question = "pain"
            st.session_state.conversation_stage = "gathering_details"
            return self.symptom_questions["pain"]
        
        elif st.session_state.conversation_stage == "gathering_details":
            # Cycle through remaining questions
            if st.session_state.current_question == "pain":
                st.session_state.current_question = "duration"
                return self.symptom_questions["duration"]
            elif st.session_state.current_question == "duration":
                st.session_state.current_question = "fever"
                return self.symptom_questions["fever"]
            elif st.session_state.current_question == "fever":
                st.session_state.current_question = "skin"
                return self.symptom_questions["skin"]
            elif st.session_state.current_question == "skin":
                st.session_state.current_question = "respiratory"
                return self.symptom_questions["respiratory"]
            elif st.session_state.current_question == "respiratory":
                st.session_state.current_question = "digestive"
                return self.symptom_questions["digestive"]
            elif st.session_state.current_question == "digestive":
                st.session_state.current_question = "fatigue"
                return self.symptom_questions["fatigue"]
            elif st.session_state.current_question == "fatigue":
                st.session_state.current_question = "other"
                return self.symptom_questions["other"]
            elif st.session_state.current_question == "other":
                st.session_state.conversation_stage = "finalizing"
                return "Thank you for providing all this information. Let me analyze your symptoms and provide a possible diagnosis. Is there anything else you'd like to add before I proceed?"
        
        elif st.session_state.conversation_stage == "finalizing":
            st.session_state.conversation_stage = "diagnosis"
            return "Based on the symptoms you've described, I can now provide a diagnosis."
            
        else:
            # Reset repetition counter if message is different from last one
            if st.session_state.chat_history[-1]["message"] != st.session_state.last_message:
                st.session_state.repetition_count = 0
                st.session_state.last_message = st.session_state.chat_history[-1]["message"]
            
            # If we've repeated the same general message too many times, try to conclude
            if st.session_state.repetition_count >= 2:
                return "I think I've provided all the information I can based on what you've shared. If you have a specific question about your symptoms or would like to start over, please let me know. Otherwise, I recommend consulting with a healthcare professional for a proper diagnosis. Thank you for using our AI Doctor service."

            # Advanced post-diagnosis responses based on user queries
            lower_input = st.session_state.chat_history[-1]["message"].lower()
            st.session_state.repetition_count += 1
            
            # Check if request for diagnosis
            if ("diagnosis" in lower_input or "what do i have" in lower_input or 
                "what's wrong" in lower_input or "tell me what" in lower_input or
                "can you please" in lower_input or "say me" in lower_input):
                # Force diagnosis
                return self.make_diagnosis()
                
            # Health concern questions
            elif "danger" in lower_input or "serious" in lower_input or "severe" in lower_input:
                return "Based on the information you've provided, I can't determine with certainty how serious your condition is. However, if you're experiencing severe or worsening symptoms, please seek immediate medical attention. A healthcare professional can provide a proper evaluation of your condition."
            
            # Treatment questions
            elif "treatment" in lower_input or "medicine" in lower_input or "medication" in lower_input or "what can" in lower_input or "what should" in lower_input:
                return "As an AI assistant, I cannot prescribe medications or treatments. For appropriate treatment, you should consult with a healthcare provider who can perform a thorough examination. They will consider your full medical history, may order tests if needed, and can prescribe appropriate treatment for your condition."
            
            # Goodbye/thanks
            elif "thank" in lower_input or "bye" in lower_input or "goodbye" in lower_input:
                return "You're welcome! I'm glad I could help. Take care of yourself and remember to consult with a healthcare professional for proper medical advice. Feel free to come back if you have more questions in the future!"
            
            # Not sure what to do / What now
            elif "what " in lower_input and ("do" in lower_input or "now" in lower_input or "next" in lower_input):
                return "Based on the symptoms you've described, I recommend consulting with a healthcare professional for a proper diagnosis and treatment plan. In the meantime, make sure to rest, stay hydrated, and monitor your symptoms. If they worsen, seek medical attention promptly."
            
            # Ask for more symptoms
            elif "ask" in lower_input or "more" in lower_input or "help me" in lower_input:
                if len(st.session_state.detected_symptoms) < 3:
                    return "I'd like to understand your symptoms better. Could you tell me if you're experiencing any pain, fever, or unusual changes in your body? The more specific you can be about your symptoms, their duration, and severity, the better I can help analyze your condition."
                else:
                    # If we have enough symptoms, make a diagnosis
                    return self.make_diagnosis()
            
            # Generic response
            else:
                if len(st.session_state.detected_symptoms) < 2:
                    return "I'm still having trouble identifying your symptoms clearly. Could you please describe in more detail what you're experiencing? For example, any specific pain, fever, or changes you've noticed recently?"
                else:
                    return self.make_diagnosis()
            
    def make_diagnosis(self):
        """Make a diagnosis based on detected symptoms"""
        try:
            # Check if enough symptoms are detected
            symptoms_list = list(st.session_state.detected_symptoms)
            
            if not symptoms_list:
                return "I couldn't identify specific symptoms from our conversation. Could you please be more specific about what you're experiencing? For example, tell me about any pain, fever, or other changes you've noticed."
            
            if len(symptoms_list) < 2 and not st.session_state.found_symptoms_in_message:
                return "I've identified some symptoms, but I need a bit more information to make a proper assessment. Could you tell me more about what you're experiencing? Any other symptoms besides what you've already mentioned?"
                
            # Train model
            X, y = self.data_processor.load_data()
            self.model.train(X, y)
            label_encoder = self.data_processor.label_encoder
            
            # Prepare input based on detected symptoms
            input_data = self.data_processor.prepare_input(symptoms_list)
            
            # Get prediction
            predictions = self.model.predict(input_data)
            
            # Get top 3 predictions
            top_n = min(3, len(label_encoder.classes_))
            top_indices = np.argsort(predictions[0])[-top_n:][::-1]
            top_diseases = label_encoder.inverse_transform(top_indices)
            top_probabilities = predictions[0][top_indices]
            
            # Format results
            results = "Based on the symptoms you've described ("
            results += ", ".join([s.replace('_', ' ') for s in symptoms_list])
            results += "), here are the possible conditions:\n\n"
            
            for disease, prob in zip(top_diseases, top_probabilities):
                prob_percentage = prob * 100
                confidence = "High" if prob_percentage > 70 else "Medium" if prob_percentage > 40 else "Low"
                results += f"• **{disease}** (Confidence: {confidence}, {prob_percentage:.1f}%)\n\n"
                
                # Add disease info if available
                disease_info = self.data_processor.get_disease_info(disease)
                if disease_info != "No detailed information available for this condition.":
                    results += f"*{disease_info}*\n\n"
                
            results += "\nIMPORTANT: This is an AI-generated assessment and not a professional medical diagnosis. Please consult with a healthcare professional for proper evaluation and treatment."
            results += "\n\nIs there anything specific about these conditions you'd like to know more about?"
            
            # Mark that diagnosis has been made
            st.session_state.diagnosis_made = True
            
            return results
            
        except Exception as e:
            return f"I'm sorry, I encountered an error while analyzing your symptoms: {str(e)}. Please consult with a healthcare professional."
            
    def process_user_input(self, user_input):
        """Process user input, detect symptoms, and determine next response"""
        # Initialize chat if not already done
        self.initialize_chat()
        
        if not user_input.strip():
            return "I didn't catch that. Could you please provide more details about your symptoms?"
            
        # Add user message to chat history
        self._add_message("You", user_input, "user")
        
        # Detect symptoms from user input
        self.detect_symptoms(user_input)
        
        # If we're at diagnosis stage or user explicitly asks for diagnosis
        if (st.session_state.conversation_stage == "diagnosis" and not st.session_state.diagnosis_made) or "diagnosis" in user_input.lower():
            diagnosis = self.make_diagnosis()
            self._add_message("AI Doctor", diagnosis, "assistant")
            return None
            
        # Get next question and add to chat
        next_question = self.get_next_question()
        self._add_message("AI Doctor", next_question, "assistant")
        
        return None
        
    def render_chat(self):
        """Render the chat interface (ONLY messages, not the input)"""
        # Initialize chat if not already done
        self.initialize_chat()
        
        st.subheader("💬 AI Doctor Conversation")
        
        # Display chat messages in a container for better scrolling
        chat_container = st.container()
        with chat_container:
            for message in st.session_state.chat_history:
                with st.chat_message(message["role"]):
                    st.markdown(message["message"])
                
    def render_chat_interface(self):
        """Render the complete chat interface with input field"""
        # First render the chat messages
        self.render_chat()
        
        # Create a container for the input area
        input_container = st.container()
        with input_container:
            # Create a form for better input handling
            with st.form(key="chat_form", clear_on_submit=True):
                user_input = st.text_area(
                    "Type your symptoms or questions here:", 
                    key="chat_input",
                    height=100
                )
                
                # Single button for submission - no need for unused columns
                submit_button = st.form_submit_button("Send", use_container_width=True)
                
                if submit_button and user_input.strip():
                    # Process user input when form is submitted
                    self.process_user_input(user_input)
                    # Rerun to update the chat
                    st.rerun()
                    
        # Add a reset button outside the form to restart conversation
        if st.button("Reset Conversation"):
            # Clear session state
            for key in ['chat_history', 'current_question', 'detected_symptoms', 
                      'conversation_stage', 'diagnosis_made', 'repetition_count',
                      'last_message', 'found_symptoms_in_message']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
            
        # After chat, if diagnosis is made, show PDF and recommendations
        if st.session_state.get('diagnosis_made', False):
            from app import DiseaseDetectorApp
            app = DiseaseDetectorApp()
            detected_symptoms = list(st.session_state.get('detected_symptoms', []))
            # Recalculate diagnosis to get top diseases and probabilities
            X, y = app.data_processor.load_data()
            app.model.train(X, y)
            input_data = app.data_processor.prepare_input(detected_symptoms)
            predictions = app.model.predict(input_data)
            top_n = min(3, len(app.data_processor.label_encoder.classes_))
            top_indices = np.argsort(predictions[0])[-top_n:][::-1]
            top_diseases = app.data_processor.label_encoder.inverse_transform(top_indices)
            top_probabilities = predictions[0][top_indices]
            app.show_recommendations_and_pdf(detected_symptoms, top_diseases, top_probabilities)
            app.show_ai_recommendations_panel(top_diseases)
