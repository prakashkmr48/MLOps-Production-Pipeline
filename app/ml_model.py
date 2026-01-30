import joblib
import numpy as np
from pathlib import Path
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class MLModel:
    """Machine Learning model wrapper for prediction."""
    
    def __init__(self, model_path: str = "models/model.pkl"):
        self.model_path = Path(model_path)
        self.model = None
        self.feature_names = None
        self.load_model()
    
    def load_model(self):
        """Load the trained model from disk."""
        try:
            if self.model_path.exists():
                self.model = joblib.load(self.model_path)
                logger.info(f"Model loaded from {self.model_path}")
            else:
                logger.warning(f"Model file not found at {self.model_path}")
                self.model = self._create_dummy_model()
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            self.model = self._create_dummy_model()
    
    def _create_dummy_model(self):
        """Create a simple dummy model for demonstration."""
        from sklearn.linear_model import LogisticRegression
        from sklearn.datasets import make_classification
        
        X, y = make_classification(n_samples=100, n_features=4, random_state=42)
        model = LogisticRegression()
        model.fit(X, y)
        return model
    
    def predict(self, features: Dict[str, float]) -> Dict[str, Any]:
        """Make predictions using the loaded model."""
        try:
            # Convert features dict to numpy array
            feature_array = np.array(list(features.values())).reshape(1, -1)
            
            # Get prediction
            prediction = self.model.predict(feature_array)[0]
            probability = self.model.predict_proba(feature_array)[0]
            
            return {
                "prediction": int(prediction),
                "probability": probability.tolist(),
                "confidence": float(max(probability))
            }
        except Exception as e:
            logger.error(f"Prediction error: {e}")
            raise ValueError(f"Failed to make prediction: {str(e)}")
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the loaded model."""
        return {
            "model_type": type(self.model).__name__,
            "model_path": str(self.model_path),
            "is_loaded": self.model is not None
        }
