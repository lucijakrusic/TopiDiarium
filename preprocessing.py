import os
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import spacy

nltk.download('punkt')  # Download punkt tokenizer (if not already downloaded)
nltk.download('stopwords')  # Download stopwords (if not already downloaded)

# Function to remove stopwords
def remove_stopwords(text, language):
    stop_words = set(stopwords.words('german'))
    tokens = word_tokenize(text)
    filtered_tokens = [token for token in tokens if token.lower() not in stop_words]
    return ' '.join(filtered_tokens)

# Function to lemmatize text
def lemmatize_text(text, language):
    nlp = spacy.load(language)
    doc = nlp(text)
    lemmatized_tokens = [token.lemma_ for token in doc]
    return ' '.join(lemmatized_tokens)

def clean_abbreviations(text):
    # pattern to match one or two letter words followed by a dot
    pattern = r'\b\w{1,3}\.' 
    
    # substitute the matched pattern with empty string
    cleaned_text = re.sub(pattern, '', text)
    
    return cleaned_text.strip()


# Function to remove numbers and non-alphabetic characters
def remove_numbers_non_alphabetic(text):
    cleaned_text = re.sub(r'[^a-zA-ZäöüÄÖÜ\s]', '', text)
    return cleaned_text

# Function to remove punctuation
def remove_punctuation(text):
    cleaned_text = re.sub(r'[^\w\s]', '', text)
    return cleaned_text

# Function to remove frequent words
def remove_frequent_words(text, frequent_words_file):
    frequent_words = set()
    with open(frequent_words_file, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            word, frequency = line.split(',')
            frequent_words.add(word)
    tokens = word_tokenize(text)
    filtered_tokens = [token for token in tokens if token not in frequent_words]
    return ' '.join(filtered_tokens)

def replace_german_ss(text):
    # Replace 'ß' with 'ss'
    replaced_text = text.replace('ß', 'ss')

    return replaced_text


def clean_roman_numerals(text):
    # Pattern to match Roman numerals. Note: does not check for valid Roman numerals, 
    # only for strings that could potentially be Roman numerals
    pattern = r'\b[MDCLXVI]+\b'
    
    # Substitute the matched pattern with empty string
    cleaned_text = re.sub(pattern, '', text, flags=re.IGNORECASE)
    
    return cleaned_text.strip()

def connect_words(text, words):
    for word in words:
        # Pattern to match whitespace between a word and 'word'
        pattern = r'(\b\w+)\s+(' + word + r'\b)'
        
        # Substitute the matched pattern with the connected word
        cleaned_text = re.sub(pattern, r'\1\2', text, flags=re.IGNORECASE)

        text = cleaned_text

    return text

def remove_hyphen_space(text):
    # Replace '-  ' with ''
    replaced_text = text.replace('-', ' ')

    return replaced_text


# Preprocess text
def preprocess_text(text, language, frequent_words_file=None):
    text = clean_abbreviations(text)
    text = remove_stopwords(text, language)
    text = lemmatize_text(text, language)
    text = remove_numbers_non_alphabetic(text)
    text = remove_punctuation(text)
    text = clean_roman_numerals(text)
    text = connect_words(text)
    text = replace_german_ss(text)
    text = remove_hyphen_space(text)
    if frequent_words_file:
        text = remove_frequent_words(text)
    return text

# Define language, corpus directory, and frequent words file
language = 'de_core_news_sm'
corpus_directory = 'digitarium_project/text_files_no_obituaries_unprocessed'
frequent_words_file = 'digitarium_project/to_delete.txt'
words_to_connect = ['lich', 'schen', 'che', 's', 'sche', 'chen']

# Tokenization and preprocessing
for document in os.listdir(corpus_directory):
    file_path = os.path.join(corpus_directory, document)
    if file_path.endswith('.txt'):
        with open(file_path, 'r', encoding='utf-16') as file:
            text = file.read()
            #preprocessed_text = preprocess_text(text, language, frequent_words_file)
            preprocessed_text = connect_words(text, words_to_connect)
            
        # Overwrite the existing file with the preprocessed text
        with open(file_path, 'w', encoding='utf-16') as file:
            file.write(preprocessed_text)
        
print("Preprocessing complete.")
