import os
import re
import hashlib
import elasticsearch
import elasticsearch.helpers
import textract
import sklearn


def getPagesTextDoc(filepath, splitBy='|'):
    '''Read text file and return pages using splitBy
    :param filepath:
    :param splitBy:
    :return: pages
    '''
    # Open document
    # doc = open(filepath, 'r')
    # Read pages from document using splitBy provided
    # pages = doc.read().split(splitBy)
    # return pages
    text = textract.process(r'C:\Users\pramod\Desktop\CodeWeek\Learning Python.pdf', encode='Ascii')
    pages = re.split(b'\r\n\r\n\x0c', text)
    return pages

def createIndex(docPath, esUrl='http://localhost:9200', index='docs', type='page'):
    es = elasticsearch.Elasticsearch([esUrl])
    to_index = []
    count = 1
    pages = getPagesTextDoc(docPath)
    for page in pages:
        pagePath = docPath+':'+str(count)
        count = count + 1
        page_id = hashlib.md5(pagePath.encode('utf-8')).hexdigest()
        doc = {
            'id': page_id,
            'project': os.path.basename(docPath),
            'path': pagePath,
            'title': os.path.basename(docPath),
            'headers': '',
            'content': page.decode(),
        }
        to_index.append({
            '_index': index,
            '_type': type,
            '_id': page_id,
            '_source': doc,
        })
    elasticsearch.helpers.bulk(es, to_index)
    es.indices.flush(wait_if_ongoing=True)

    es.delete_by_query(body={'query': {'bool': {
        'must': [{'term': {'project': os.path.basename(docPath)}}],
        'must_not': [{'term': {'commit': True}}],
    }}}, index=index)


def addDocIndex():
    createIndex(r'C:\Users\pramod\Desktop\CodeWeek\Learning Python.txt')

import requests

def queryes(q):
    resp = requests.get('http://localhost:9200/docs/_search?q=%s;size=50' %q)
    results = resp.json()['hits']['hits']
    return results
    # resp[48]['_source']['content'].split('\n\n')

from sklearn.feature_extraction.text import TfidfVectorizer
import sklearn.metrics.pairwise
import operator

from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
class LemmaTokenizer(object):
    def __init__(self):
        self.wnl = WordNetLemmatizer()
    def __call__(self, articles):
        return [self.wnl.lemmatize(t) for t in word_tokenize(articles)]

def tfidf(q):
    data = {'query': q}
    results = queryes(q)
    for result in results:
        root = result['_source']['path']
        pgraphs = result['_source']['content'].split('.\r\n')
        data.update(zip([root+':'+str(count) for count in range(len(pgraphs))], pgraphs))
    vectorizer = TfidfVectorizer(tokenizer=LemmaTokenizer(), ngram_range=(1, 3))
    X = vectorizer.fit_transform(list(data.values()))
    newdata = sklearn.metrics.pairwise.cosine_similarity(X, X[0])
    tfidfdata = dict(zip(list(data.keys()), newdata.tolist()))
    sortedtfidf = sorted(tfidfdata.items(), key=operator.itemgetter(1), reverse=True)
    return  data[sortedtfidf[1][0]]
