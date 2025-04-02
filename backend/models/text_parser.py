from transformers import pipeline

# Load the pipeline for T5 (Text-to-Text Transfer Transformer) to convert input text into structured descriptions.
nlp_model = pipeline('text2text-generation', model = "t5-small")

# Input text
def parse_text(user_text):
    structured_description = nlp_model(user_text, max_length = 50, truncation = True)[0]['generated_text']
    
    return structured_description

# 100% free & open source
# runs locally on CPU and GPU