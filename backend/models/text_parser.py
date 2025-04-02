from transformers import pipeline
import torch

# Initialize model
nlp_model = None

def load_model():
    """Load the T5-small model once to optimize performance."""
    global nlp_model
    if nlp_model is None:
        device = 0 if torch.cuda.is_available() else -1  # Use GPU if available
        nlp_model = pipeline('text2text-generation', model="t5-small", device=device)

def detect_task(user_text):
    """Detects the type of task and adjusts the input prompt."""
    if "?" in user_text:
        return f"Answer the question: {user_text}"
    elif len(user_text.split()) > 20:
        return f"Summarize: {user_text}"
    return user_text  # Default behavior

def parse_text(user_text, max_length=50):
    """Generates structured text output using T5-small."""
    load_model()
    processed_text = detect_task(user_text)
    structured_description = nlp_model(processed_text, max_length=max_length, truncation=True)[0]['generated_text']
    return structured_description

# Example usage
if __name__ == "__main__":
    text_input = "Why is the stock market volatile today?"
    result = parse_text(text_input)
    print("Generated Output:", result)


# 100% free & open source
# runs locally on CPU and GPU