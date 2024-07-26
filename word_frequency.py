import os
from collections import Counter
from nltk.tokenize import word_tokenize

directory = 'digitarium_project/text_files_no_obituaries'

word_freq = Counter()

# Tokenization and building vocabulary
for document in os.listdir(directory):
    file_path = os.path.join(directory, document)
    if file_path.endswith('.txt'):
        with open(file_path, 'r', encoding='utf-16') as file:
            text = file.read()
            tokens = word_tokenize(text)
            word_freq.update(tokens)

# Determine threshold for rare words
threshold = 20  # You can adjust this threshold 

rare_words = [word for word, freq in word_freq.items() if freq < threshold]

# Write rare words and frequencies to a file
output_file = 'digitarium_project/rare_words.txt'
with open(output_file, 'w', encoding='utf-8') as file:
  for word, freq in word_freq.items():
       if freq < threshold:
           file.write(f"{word},{freq}\n")
    

print("Rare words and frequencies have been written to 'rare_words.txt'.")

# Print the 20 most frequent terms and their frequencies
print("20 Most Frequent Terms:")
sorted_freq = word_freq.most_common(100)

output_file = 'output_files/frequent_words.txt'
with open(output_file, 'w', encoding='utf-8') as file:
    for word, freq in sorted_freq:
        file.write(f"{word},{freq}\n")
