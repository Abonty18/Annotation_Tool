import re
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from bnlp import BasicTokenizer

# Function to preprocess English text
def preprocess_english_text(text):
    # Convert the text to lowercase
    text = text.lower()

    # Remove special characters and numbers
    text = re.sub(r'[^a-zA-Z]', ' ', text)

    # Tokenize the English text using nltk's word_tokenize
    words = nltk.word_tokenize(text)

    # Load the English stopwords list
    stop_words = set(stopwords.words('english'))

    # Remove stopwords
    words = [word for word in words if word not in stop_words]

    # Join the words back to a single string
    preprocessed_text = ' '.join(words)

    return preprocessed_text

# Function to preprocess Bengali text
def preprocess_bengali_text(text):
    # Tokenize the Bengali text using bnlp_toolkit's BasicTokenizer
    tokenizer = BasicTokenizer()
    words = tokenizer.tokenize(text)

    # Load the Bengali stopwords list
    stop_words = set(stopwords.words('bengali'))

    # Remove stopwords and punctuation marks
    words = [word for word in words if word not in stop_words and word.isalnum()]

    # Remove Bengali numbers from the list
    words = [word for word in words if not word.isdigit()]

    # Join the words back to a single string
    preprocessed_text = ' '.join(words)

    return preprocessed_text

# Read the English privacy policy text
with open('preprocessed_text/preprocessed_privacy_policy.txt', 'r', encoding='utf-8') as file:
    english_privacy_policy_text = file.read()



# Preprocess the English text
preprocessed_english_text = preprocess_english_text(english_privacy_policy_text)



# Create a TF-IDF vectorizer for English with min_df=1 and remove English stopwords during vectorization
english_tfidf_vectorizer = TfidfVectorizer(min_df=1)



# Fit and transform the English vectorizer on the preprocessed English text
english_tfidf_matrix = english_tfidf_vectorizer.fit_transform([preprocessed_english_text])



# Get feature names (words) from the English vectorizer
english_feature_names = english_tfidf_vectorizer.get_feature_names_out()



# Get the TF-IDF scores for each word in English text
english_tfidf_scores = english_tfidf_matrix.toarray()[0]



# Combine English words with their TF-IDF scores into a dictionary
english_word_tfidf_scores = dict(zip(english_feature_names, english_tfidf_scores))



# Sort the dictionaries based on TF-IDF scores in descending order
sorted_english_word_tfidf_scores = {k: v for k, v in sorted(english_word_tfidf_scores.items(), key=lambda item: item[1], reverse=True)}

# Extract the top 50 keywords from English text (excluding common stopwords)
english_stop_words = set(stopwords.words('english'))
top_english_keywords = [word for word in sorted_english_word_tfidf_scores.keys() if word not in english_stop_words][:15]


print("\nTop 50 English Keywords:")
print(top_english_keywords)

