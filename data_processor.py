import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import LabelEncoder

class DataProcessor:
    def __init__(self):
        self.label_encoder = LabelEncoder()
        self.symptoms = None
        self.symptom_descriptions = {
            'itching': 'Itching of the skin',
            'skin_rash': 'Visible skin rash',
            'nodal_skin_eruptions': 'Nodular skin eruptions',
            'continuous_sneezing': 'Persistent sneezing',
            'shivering': 'Involuntary trembling',
            'chills': 'Feeling of coldness',
            'joint_pain': 'Pain in the joints',
            'stomach_pain': 'Abdominal pain',
            'acidity': 'Excessive stomach acid',
            'vomiting': 'Forcing contents from stomach',
            'fatigue': 'Extreme tiredness',
            'anxiety': 'Feeling of worry or nervousness',
            'mood_swings': 'Rapid changes in emotion',
            'weight_loss': 'Decrease in body weight',
            'restlessness': 'Inability to rest or relax',
            'lethargy': 'Lack of energy or enthusiasm',
            'patches_in_throat': 'Visible patches in throat',
            'cough': 'Sudden expulsion of air',
            'high_fever': 'Body temperature above normal',
            'breathlessness': 'Difficulty breathing',
            # Additional symptoms from the larger dataset
            'headache': 'Pain in the head',
            'back_pain': 'Pain in the back',
            'chest_pain': 'Pain in the chest',
            'dizziness': 'Feeling lightheaded or unsteady',
            'nausea': 'Feeling of sickness with an inclination to vomit',
            'muscle_weakness': 'Reduced strength in muscles',
            'stiff_neck': 'Difficulty moving the neck',
            'swelling_joints': 'Inflammation of the joints',
            'obesity': 'Excessive body weight',
            'depression': 'Persistent feeling of sadness'
        }
        
        # Dictionary to store disease descriptions
        self.disease_info = {
            'Fungal infection': 'A fungal infection caused by fungi that commonly affects the skin, hair, and nails.',
            'Allergy': 'An immune system response to a substance that most people tolerate well.',
            'GERD': 'Gastroesophageal reflux disease, a digestive disorder that affects the lower esophageal sphincter.',
            'Chronic cholestasis': 'A condition where bile flow from the liver is reduced or blocked.',
            'Drug Reaction': 'An adverse reaction to medication that may present as a rash or other symptoms.',
            'Peptic ulcer disease': 'A condition where open sores develop in the lining of the stomach or upper part of the small intestine.',
            'AIDS': 'Acquired immunodeficiency syndrome, a chronic condition caused by HIV that damages the immune system.',
            'Diabetes': 'A group of diseases that affect how your body uses blood sugar (glucose).',
            'Gastroenteritis': 'Inflammation of the lining of the intestines caused by a virus, bacteria, or parasites.',
            'Bronchial Asthma': 'A condition where airways narrow and swell, producing extra mucus and making it difficult to breathe.',
            'Hypertension': 'High blood pressure that can lead to serious health problems.',
            'Migraine': 'A headache disorder characterized by recurrent headaches that are moderate to severe.',
            'Cervical spondylosis': 'Age-related wear and tear affecting the spinal disks in your neck.',
            'Paralysis': 'Loss of muscle function in part of your body, often caused by damage to the nervous system.',
            'Jaundice': 'Yellowing of the skin and whites of the eyes caused by an accumulation of bilirubin in the blood.',
            'Malaria': 'A disease caused by a parasite, transmitted by the bite of infected mosquitoes.',
            'Chicken pox': 'A highly contagious viral infection causing an itchy, blister-like rash.',
            'Dengue': 'A mosquito-borne viral disease causing fever and flu-like symptoms.',
            'Typhoid': 'A bacterial infection caused by Salmonella typhi, spread through contaminated food and water.',
            'Common Cold': 'A viral infectious disease of the upper respiratory tract affecting the nose, throat, and sinuses.',
            'Pneumonia': 'Infection that inflames air sacs in one or both lungs, which may fill with fluid.',
            'Anxiety': 'A feeling of worry, nervousness, or unease about something with an uncertain outcome.',
            'Psoriasis': 'A skin condition causing red, flaky, crusty patches of skin covered with silvery scales.'
        }
        
    def load_data(self):
        """Load and preprocess the disease dataset"""
        try:
            # First try to use the larger Testing.csv dataset
            dataset_path = os.path.join('dataset', 'Testing.csv')
            
            # If not available, fall back to smaller dataset
            if not os.path.exists(dataset_path):
                dataset_path = os.path.join('dataset', 'disease_dataset.csv')
                if not os.path.exists(dataset_path):
                    raise FileNotFoundError(f"No dataset files found in the dataset directory")
            
            # Load data
            data = pd.read_csv(dataset_path)
            
            if data.empty:
                raise ValueError("Dataset is empty")
                
            # Get list of all symptoms (all columns except prognosis)
            self.symptoms = list(data.columns[:-1])
            
            # Separate features and target variable
            X = data.drop('prognosis', axis=1)
            y = data['prognosis']
            
            # Encode disease labels
            y_encoded = self.label_encoder.fit_transform(y)
            
            # Convert to numpy arrays
            X = X.to_numpy()
            
            return X, y_encoded
            
        except Exception as e:
            print(f"Error loading data: {str(e)}")
            return np.array([]), np.array([])
    
    def prepare_input(self, symptoms):
        """Prepare user input for model prediction"""
        if self.symptoms is None:
            self.load_data()
            
        if not self.symptoms:  # If symptoms list is empty
            raise ValueError("Could not load symptoms list. Please check the dataset files.")
            
        # Create input array
        input_data = np.zeros(len(self.symptoms))
        
        # Set 1 for present symptoms
        for symptom in symptoms:
            if symptom in self.symptoms:
                input_data[self.symptoms.index(symptom)] = 1
                
        return input_data.reshape(1, -1)
    
    def get_all_symptoms(self):
        """Return list of all possible symptoms"""
        if self.symptoms is None:
            self.load_data()
        return self.symptoms if self.symptoms else []
        
    def get_symptom_description(self, symptom):
        """Return description for a given symptom"""
        return self.symptom_descriptions.get(symptom, "Description not available")
        
    def get_disease_info(self, disease):
        """Return information about a disease"""
        return self.disease_info.get(disease, "No detailed information available for this condition.")
