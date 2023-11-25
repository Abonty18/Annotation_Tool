import string
import os
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer

# Ensure NLTK resources are downloaded
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

def preprocess_privacy_policy(text):
    # Convert to lowercase
    text = text.lower()

    # Remove digits
    text = ''.join([i for i in text if not i.isdigit()])

    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))

    # Tokenize
    tokens = word_tokenize(text)

    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]

    # Apply lemmatization
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word) for word in tokens]

    # Join tokens back to text
    preprocessed_text = ' '.join(tokens)

    return preprocessed_text

# Path to your privacy policy text file
privacy_policy_path = 'messenger.txt'

# Read the privacy policy text
with open(privacy_policy_path, 'r', encoding='utf-8') as file:
    privacy_policy_text = file.read()

# Preprocess the privacy policy text
preprocessed_privacy_policy = preprocess_privacy_policy(privacy_policy_text)

# Create a folder for preprocessed text if it doesn't exist
output_folder = 'preprocessed_text'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Save the preprocessed privacy policy text
output_file_path = os.path.join(output_folder, 'preprocessed_privacy_policy_msngr.txt')
with open(output_file_path, 'w', encoding='utf-8') as file:
    file.write(preprocessed_privacy_policy)

print("Preprocessed privacy policy text saved in:", output_file_path)
