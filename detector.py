from transformers import pipeline
import re

class FakeNewsDetector:
    def __init__(self):
        """Initialize the detector with working model"""
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """Load the fake news detection model"""
        try:
            self.model = pipeline(
                "text-classification",
                model="cardiffnlp/twitter-roberta-base-fake-news",
                top_k=None
            )
            print("✅ Model loaded successfully!")
        except Exception as e:
            print(f"⚠️ Model load failed: {e}")
            self.model = None
    
    def detect(self, text):
        """
        Detect if news is fake or real
        Returns: dict with label, score, and confidence
        """
        if not text or not text.strip():
            return {'label': 'UNCERTAIN', 'score': 0.5, 'reason': 'Empty text'}
        
        # Try model detection first
        if self.model:
            try:
                result = self.model(text[:512])  # Truncate if too long
                label = result[0]['label']
                score = result[0]['score']
                
                # Map labels correctly
                if label == 'LABEL_1':
                    final_label = 'FAKE'
                else:
                    final_label = 'REAL'
                
                # 🔧 IMPROVED THRESHOLDS
                # For FAKE: Lower threshold to catch more fakes
                if final_label == 'FAKE' and score < 0.40:
                    final_label = 'UNCERTAIN'
                # For REAL: Lower threshold so more real news is detected
                elif final_label == 'REAL' and score < 0.50:
                    final_label = 'UNCERTAIN'
                
                return {
                    'label': final_label,
                    'score': score,
                    'reason': f'Model prediction: {label} with score {score:.2f}'
                }
            except Exception as e:
                print(f"⚠️ Model error: {e}")
        
        # Fallback: Keyword-based detection
        return self._keyword_detection(text)
    
    def _keyword_detection(self, text):
        """Keyword-based fallback detection"""
        text_lower = text.lower()
        
        # Fake news indicators
        fake_words = [
            'breaking', 'shocking', 'exclusive', 'secret', 'exposed',
            'scandal', 'amazing', 'unbelievable', 'you won\'t believe',
            'must share', 'gone viral', 'conspiracy', 'rumors',
            'allegedly', 'miracle', 'sudden', 'leaked', 'officials confirm',
            'viral', 'exposed', 'truth revealed', 'they don\'t want you to know'
        ]
        
        # Real news indicators
        real_words = [
            'according to', 'research shows', 'study finds',
            'scientists discovered', 'officials said', 'data shows',
            'reported that', 'announced', 'confirmed', 'verified',
            'investigation reveals', 'official statement'
        ]
        
        fake_count = sum(1 for word in fake_words if word in text_lower)
        real_count = sum(1 for word in real_words if word in text_lower)
        
        total = fake_count + real_count
        if total == 0:
            return {'label': 'UNCERTAIN', 'score': 0.5, 'reason': 'No keywords found'}
        
        fake_ratio = fake_count / total
        
        # Adjusted thresholds
        if fake_ratio > 0.3:
            return {'label': 'FAKE', 'score': fake_ratio, 'reason': 'High fake keyword ratio'}
        elif fake_ratio < 0.15:
            return {'label': 'REAL', 'score': 1 - fake_ratio, 'reason': 'Low fake keyword ratio'}
        else:
            return {'label': 'UNCERTAIN', 'score': 0.5, 'reason': 'Mixed signals'}

# Singleton instance
detector = FakeNewsDetector()

def detect_fake_news(text):
    """Simple function to use the detector"""
    return detector.detect(text)

if __name__ == "__main__":
    # Test the detector
    test_cases = [
        "Narendra Modi is alive and healthy",
        "Breaking shocking exclusive: Modi died",
        "Scientists discovered new planet",
        "You won't believe what happened next",
        "Breaking News: Scientists discovered new planet. According to sources, "
    ]
    
    print("=== Testing Fake News Detector ===\n")
    for text in test_cases:
        result = detect_fake_news(text)
        print(f"Text: {text[:50]}...")
        print(f"Prediction: {result['label']}")
        print(f"Score: {result['score']:.2f}")
        print(f"Reason: {result.get('reason', 'N/A')}")
        print("-" * 50)