import regex as re
from collections import Counter

docs=[]
n_doc=input()
for i in range(int(n_doc)):
    docs.append(input())
query = input()
# ranking = input()
# ranking=[int(x) for x in ranking if x !=" "]

def preprocess_doc(text):
    text = "".join(re.findall(r"[\w\s]",text))
    text = re.sub(r"\s",' ',text).strip()
    text = re.sub(r"\s+",' ',text).lower().split()
    return text
docs = [preprocess_doc(doc) for doc in docs]
query = preprocess_doc(query)


def compute_query_likelihood(doc_tokens, query_tokens, lambda_smooth, corpus_tokens):
    doc_counter = Counter(doc_tokens)
    corpus_counter = Counter(corpus_tokens)
    doc_len = len(doc_tokens)
    corpus_len = len(corpus_tokens)

    likelihood = 1.0
    for token in query_tokens:
        pw_d = doc_counter[token] / doc_len if doc_len > 0 else 0
        pw_c = corpus_counter[token] / corpus_len if corpus_len > 0 else 0
        smoothed = lambda_smooth * pw_d + (1 - lambda_smooth) * pw_c
        likelihood *= smoothed
    return likelihood


# Tworzenie korpusu
total_corpus_tokens = [token for doc in docs for token in doc]

# Obliczanie prawdopodobieństw dla każdego dokumentu
lambda_smooth = 0.5
scores = []
for i, doc_tokens in enumerate(docs):
    score = compute_query_likelihood(doc_tokens, query, lambda_smooth, total_corpus_tokens)
    scores.append((i, score))

# Sortowanie wyników na podstawie rankingu i wartości prawdopodobieństwa
sorted_scores = sorted(scores, key=lambda x: (-x[1]))

# Wyświetlenie wyników
wynik = []
for result in sorted_scores:
    wynik.append(result[0])

print([int(x) for x in wynik])
