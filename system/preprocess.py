import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from transformers import AutoModel, AutoTokenizer
from sklearn.metrics.pairwise import cosine_similarity
import torch
import numpy as np
from deep_translator import GoogleTranslator

# Download NLTK data files
nltk.download('punkt')
nltk.download('stopwords')

# Define stop words for English
stop_words = set(stopwords.words('english'))

# Load pre-trained model and tokenizer
model_name = "ai4bharat/indic-bert"  # Nepali-compatible model
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

# Translator instance using deep-translator
translator = GoogleTranslator(source='ne', target='en')

# Preprocessing function
def preprocess_text(text):
    # Tokenize text
    tokens = word_tokenize(text.lower())
    # Remove stop words
    filtered_tokens = [word for word in tokens if word.isalnum() and word not in stop_words]
    return ' '.join(filtered_tokens)

# Generate embeddings for FAQ questions (translated to English)
def embed_question(question):
    question_in_english = translator.translate(question)
    processed_question = preprocess_text(question_in_english)
    inputs = tokenizer(processed_question, return_tensors="pt", truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).numpy()

# Function to get the answer by comparing the translated query with the FAQ data
def get_answer(user_question, faq_data):
    # Embed FAQ questions
    faq_embeddings = [embed_question(faq['question']) for faq in faq_data]
    
    # Embed the user question
    user_embedding = embed_question(user_question)
    
    # Calculate similarities
    similarities = [cosine_similarity(user_embedding, faq_emb) for faq_emb in faq_embeddings]
    
    # Find the most similar question
    max_similarity = max(similarities)
    if max_similarity > 0.7:  # Adjust threshold as needed
        return faq_data[np.argmax(similarities)]['answer']
    else:
        return "Sorry, I don't know the answer to this question."
