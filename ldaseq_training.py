import os
from gensim import corpora

from gensim.models import LdaSeqModel
from gensim.corpora import Dictionary
from gensim.corpora import MmCorpus


import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
import numpy as np


# Path to the directory containing the text files
data_dir = 'digitarium_project/text_files_no_obituaries'


# Get a list of all text file names
file_names = sorted([file for file in os.listdir(data_dir) if file.endswith('.txt')])

documents = []

# Tokenization of preprocessed documents
for file in file_names:
    with open(os.path.join(data_dir, file), 'r', encoding='utf-16') as f:
        document = f.read()
        # Tokenize the preprocessed document
        tokenized_document = document.split()
        # Add tokenized document to 'documents_1' list
        documents.append(tokenized_document)



# Create dictionaries for each time slice
dictionary = Dictionary(documents)
dictionary.save('dictionary')

# Create document-term matrices for each time slice
corpus = [dictionary.doc2bow(doc) for doc in documents]
time_slice = [156, 142]
corpora.MmCorpus.serialize('digitarium_project/my_corpus.mm', corpus)

'''
# Train the LdaSeqModel
ldaseq = LdaSeqModel(corpus=corpus, id2word=dictionary, time_slice=time_slice, num_topics=5,chain_variance=0.005, random_state=1, lda_inference_max_iter=5,em_max_iter =5)
ldaseq.save('ldaseq_model')




# Example usage: Get topics for a specific time slice
time_slice_index = 0  # Index of the desired time slice
topics = ldaseq_model.print_topics(time=time_slice_index)

# Print the topics for the selected time slice
for topic in topics:
    print(topic)
'''