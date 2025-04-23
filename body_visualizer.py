import streamlit as st
from PIL import Image
import os
import base64
from io import BytesIO
import numpy as np
import matplotlib.pyplot as plt
import urllib.request
import shutil

class BodyVisualizer:
    """Class for interactive body visualization to select symptoms by body part"""
    
    def __init__(self, data_processor):
        self.data_processor = data_processor
        self.body_parts = {
            "head": {
                "name": "Head",
                "region": [150, 50, 250, 120],
                "symptoms": ["headache", "dizziness", "anxiety", "depression"]
            },
            "throat": {
                "name": "Throat",
                "region": [180, 120, 220, 150],
                "symptoms": ["patches_in_throat", "cough", "continuous_sneezing"]
            },
            "chest": {
                "name": "Chest",
                "region": [150, 150, 250, 210],
                "symptoms": ["chest_pain", "breathlessness", "high_fever", "mild_fever", "congestion"]
            },
            "abdomen": {
                "name": "Abdomen",
                "region": [150, 210, 250, 270],
                "symptoms": ["stomach_pain", "vomiting", "nausea", "acidity", "indigestion", "diarrhea", "constipation"]
            },
            "arms": {
                "name": "Arms",
                "region": [100, 150, 150, 230, 250, 150, 300, 230],
                "symptoms": ["muscle_weakness", "swelling_joints", "joint_pain"]
            },
            "legs": {
                "name": "Legs",
                "region": [150, 270, 180, 380, 220, 270, 250, 380],
                "symptoms": ["joint_pain", "swelling_joints", "muscle_weakness", "knee_pain"]
            },
            "skin": {
                "name": "Skin",
                "region": [0, 0, 400, 400],  # The entire body
                "symptoms": ["itching", "skin_rash", "nodal_skin_eruptions", "yellowish_skin"]
            },
            "neck": {
                "name": "Neck",
                "region": [170, 120, 230, 150],
                "symptoms": ["neck_pain", "stiff_neck"]
            },
            "back": {
                "name": "Back",
                "region": [150, 150, 250, 270],
                "symptoms": ["back_pain"]
            }
        }
          # Create directory for images if it doesn't exist
        os.makedirs('assets', exist_ok=True)
        
        # Get the body diagram (only download if needed)
        self._get_body_diagram(force_download=False)
        
    def _get_body_diagram(self, force_download=False):
        """Get or download a medical body diagram"""
        # Path to the body diagram
        body_diagram_path = os.path.join('assets', 'body_diagram.png')
        
        # Check for the backup image in assets folder
        human_body_path = os.path.join('assets', 'human_body.png')
        
        # First check if the file already exists
        if os.path.exists(body_diagram_path) and not force_download:
            print(f"Using existing body diagram at {body_diagram_path}")
            return body_diagram_path
        
        # If we need to create/download a new image
        try:
            # First try to copy from the backup human_body.png if it exists
            if os.path.exists(human_body_path):
                print(f"Using backup image from {human_body_path}")
                shutil.copy(human_body_path, body_diagram_path)
                return body_diagram_path
                
            # If no backup image, try to download
            if force_download or not os.path.exists(body_diagram_path):
                # URLs to high-quality anatomical diagrams from public domain
                image_urls = [
                    "https://upload.wikimedia.org/wikipedia/commons/b/b7/Human_anatomy_1.jpg",  # Detailed front view
                    "https://upload.wikimedia.org/wikipedia/commons/4/4d/Grays_Anatomy_image389_Musculature.png",  # Gray's Anatomy muscular
                    "https://upload.wikimedia.org/wikipedia/commons/c/c5/Gray%27s_Anatomy_image_with_muscle_labels.png"  # Gray's with labels
                ]
                
                # Try each URL in order until one works
                for image_url in image_urls:
                    try:
                        print(f"Downloading new anatomical image from {image_url}")
                        urllib.request.urlretrieve(image_url, body_diagram_path)
                        print(f"New image downloaded to {body_diagram_path}")
                        return body_diagram_path
                    except Exception as e:
                        print(f"Failed to download from {image_url}: {e}")
                        continue
                
                # If all downloads fail, create a placeholder
                print("All download attempts failed, creating placeholder image")
                self._create_placeholder_image(body_diagram_path)
        except Exception as e:
            print(f"Error obtaining body diagram: {e}")
            # If all else fails, create a simple placeholder
            self._create_placeholder_image(body_diagram_path)
        
        return body_diagram_path
        
    def _create_placeholder_image(self, path):
        """Create a simple placeholder image if download fails"""
        # Create a simple image using matplotlib as fallback
        fig, ax = plt.subplots(figsize=(6, 12))
        ax.text(0.5, 0.5, "Human Body Diagram", ha='center', va='center', fontsize=20)
        ax.axis('off')
        plt.savefig(path, bbox_inches='tight')
        plt.close()
      def get_body_diagram_path(self):
        """Get the path to the body diagram"""
        return os.path.join('assets', 'body_diagram.png')
    
    def get_image_as_base64(self, path):
        """Convert an image to base64 encoding"""
        img = Image.open(path)
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode()
    
    def display(self):
        """Display the body map interface (wrapper for render_body_map)"""
        self.render_body_map()
    
    def render_body_map(self):
        """Render the interactive body map"""
        st.subheader("🔍 Interactive Body Map")
        st.write("Select a body part to see related symptoms")
        
        # Display image of human body
        body_diagram_path = self.get_body_diagram_path()
        
        # Use columns for layout: body image and selected body part
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # Display the image
            st.image(body_diagram_path, use_container_width=True)
            
            # Create clickable areas using radio buttons
            selected_part = st.radio(
                "Select a body part:", 
                options=[part["name"] for part in self.body_parts.values()]
            )
        
        # Initialize or get selected symptoms from session state
        if 'selected_symptoms' not in st.session_state:
            st.session_state.selected_symptoms = []
            
        # Display symptoms for the selected body part
        with col2:
            # Find the selected body part details
            selected_part_key = next((key for key, part in self.body_parts.items() 
                                   if part["name"] == selected_part), None)
            
            if selected_part_key:
                part_details = self.body_parts[selected_part_key]
                
                st.write(f"### {part_details['name']} Symptoms")
                
                # Display checkboxes for each symptom in this body part
                for symptom in part_details["symptoms"]:
                    # Format the symptom name for display
                    display_name = symptom.replace('_', ' ').title()
                    
                    # Get description for tooltip
                    description = self.data_processor.get_symptom_description(symptom)
                    
                    # Check if symptom is already selected
                    is_selected = symptom in st.session_state.selected_symptoms
                    
                    # Display checkbox with tooltip
                    if st.checkbox(
                        f"{display_name}", 
                        value=is_selected,
                        help=description,
                        key=f"body_map_{symptom}"
                    ):
                        # Add to selected symptoms if not already there
                        if symptom not in st.session_state.selected_symptoms:
                            st.session_state.selected_symptoms.append(symptom)
                    else:
                        # Remove from selected symptoms if it was there
                        if symptom in st.session_state.selected_symptoms:
                            st.session_state.selected_symptoms.remove(symptom)
        
        # Return the list of selected symptoms
        return st.session_state.selected_symptoms
