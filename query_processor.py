
import math
import json
from preprocessor import preprocess

#calculate term frequency (TF)
def calculate_tf(term, document):
    words = document.split(" ")
    N = len(words)
    term_count = len([token for token in words if token == term])
    return term_count / N

#calculate inverse document frequency (IDF)
def calculate_idf(term, index, total_documents):
    term_count = len(index.get(term, []))
    return math.log(total_documents / (term_count + 1))

#calculate TF-IDF score for a term in a document
def calculate_tf_idf(term, document, total_documents, index):
    tf = calculate_tf(term, document)
    idf = calculate_idf(term, index, total_documents)
    return tf * idf

#retrieve relevant publication for a query
def search_publications(query, processed_tokens, index, publications):
    #preprocess query
    query_terms = preprocess(query)
    document_scores = {}

    for term in query_terms.split(" "):
        if term in index:
            for document_id in index[term]:
                score = calculate_tf_idf(term, processed_tokens[document_id], len(publications), index)
                if document_id in document_scores:
                    document_scores[document_id] += score
                else:
                    document_scores[document_id] = score
    
    #sort the calculated score
    relevant_documents = [publications[doc_id] for doc_id in sorted(document_scores, key=document_scores.get, reverse=True)]
    
    return relevant_documents