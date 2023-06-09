import math


def load_vocab():
    vocab = {}
    with open("./tf-idf/vocab.txt", 'r', encoding="utf-8") as f:
        vocab_terms = f.readlines()

    with open("./tf-idf/idf-values.txt", 'r', encoding="utf-8") as f:
        idf_terms = f.readlines()

    for (i, v) in zip(vocab_terms, idf_terms):
        vocab[i.strip()] = int(v.strip())
        
    return vocab


vocab_idf_values = load_vocab()
documents_text = []


def load_documents():
    with open("./tf-idf/documents.txt", 'r') as f:
        documents = f.readlines()
    documents = [document.strip().split() for document in documents]

    for index, document in enumerate(documents):
        with open(f"./tf-idf/Documents/{index+1}/{index+1}.txt", 'r', encoding="utf-8") as f:
            data_array = []
            for l in f:
                data_values = [term.lower() for term in l.strip().split(" ")]
                for v in data_values:
                    data_array.append(v)
            documents_text.append(data_array)

    return documents


documents = load_documents()


def load_inverted_index():
    inverted_index_head = {}
    inverted_index_data = {}
    with open("./tf-idf/inverted-index.txt", 'r', encoding="utf-8") as f:
        inverted_index_terms = f.readlines()

    for row_num in range(0, len(inverted_index_terms), 3):
        term = inverted_index_terms[row_num].strip()
        doucuments = inverted_index_terms[row_num+1].strip().split()
        doucuments_data = inverted_index_terms[row_num+2].strip().split()
        inverted_index_head[term] = doucuments
        inverted_index_data[term] = doucuments_data

    return [inverted_index_head, inverted_index_data]


inverted_index = load_inverted_index()


def get_tf_dict(term):
    tf_values = {}

    if term in inverted_index[0]:
        for document in inverted_index[0][term]:
            if document not in tf_values:
                tf_values[document] = 1
            else:
                tf_values[document] += 1
    
    if term in inverted_index[1]:
        for document in inverted_index[1][term]:
            if document not in tf_values:
                tf_values[document] = 1
            else:
                tf_values[document] += 1
    
    for document in tf_values:
        tf_values[document] /= len(documents[int(document)] +
                                   documents_text[int(document)])
    
    return tf_values


def get_idf_value(term):
    return math.log((len(documents)+len(documents_text))/vocab_idf_values[term])

def calculate_sorted_order_of_documents(query_terms):
    potential_documents = {}
    tf_values_by_document = {}

    for term in query_terms:
        if term not in vocab_idf_values:
            continue
        tf_values_by_document = get_tf_dict(term)
        idf_value = get_idf_value(term)
        for document in tf_values_by_document:
            if document not in potential_documents:
                potential_documents[document] = tf_values_by_document[document]*idf_value
            else:
                potential_documents[document] += tf_values_by_document[document]*idf_value
    
    for document in potential_documents:
        potential_documents[document] /= len(query_terms)
    
    potential_documents = dict(
        sorted(potential_documents.items(), key=lambda item: item[1], reverse=True))
    
    for document_index in potential_documents:
        print(" ".join(documents[int(document_index)]), "---->",
              "Score=", potential_documents[document_index])
        print(" ".join(documents_text[int(document_index)])+"\n\n")


query_string = input("Enter the query\n")
query_terms = [term.lower() for term in query_string.strip().split(" ")]

calculate_sorted_order_of_documents(query_terms)
