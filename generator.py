from transformers import pipeline

class FakeNewsGenerator:
    def __init__(self):
        """Initialize the text generation model"""
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """Load GPT-2 model for text generation"""
        try:
            self.model = pipeline('text-generation', model='gpt2')
            print("✅ Generator model loaded successfully!")
        except Exception as e:
            print(f"⚠️ Generator load failed: {e}")
            self.model = None
    
    def generate(self, topic):
        """
        Generate fake news based on topic
        Returns: Generated news text
        """
        if not self.model:
            return "Error: Model not loaded"
        
        if not topic or not topic.strip():
            return "Error: Please provide a topic"
        
        try:
            # Better prompt for news generation
            prompt = f"Breaking News: {topic}. According to sources, "
            
            result = self.model(
                prompt,
                max_length=150,
                num_return_sequences=1,
                temperature=0.8,
                top_p=0.92,
                do_sample=True,
                pad_token_id=50256
            )
            
            return result[0]['generated_text']
        
        except Exception as e:
            return f"Error: {str(e)}"

# Singleton instance
generator = FakeNewsGenerator()

def generate_fake_news(topic):
    """Simple function to use the generator"""
    return generator.generate(topic)

if __name__ == "__main__":
    # Test the generator
    topics = [
        "climate change",
        "election results",
        "new health discovery",
        "space exploration"
    ]
    
    print("=== Testing Fake News Generator ===\n")
    for topic in topics:
        print(f"Topic: {topic}")
        print("Generated News:")
        print(generate_fake_news(topic))
        print("-" * 50)