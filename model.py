from sklearn.ensemble import RandomForestClassifier
import numpy as np

class DiseasePredictor:
    def __init__(self):
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            class_weight='balanced'
        )
        
    def train(self, X, y):
        """Train the model on given data"""
        self.model.fit(X, y)
        
    def predict(self, X):
        """Make predictions for given input"""
        return self.model.predict_proba(X)
