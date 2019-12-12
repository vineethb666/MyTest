import elasticsearch
import hashlib

class BaseEngine(object):

    def get(self, question):
        raise NotImplementedError("All child classes need to implement this method")

    def store(self, data):
        raise NotImplementedError("All child classes need to implement this method")


class FAQEngine(BaseEngine):

    def __init__(self, index_name='faqengine', doc_type='faq3.7.5', settings={}):
        self.es = elasticsearch.Elasticsearch(['http://localhost:9200'])
        self.index_name = index_name
        self.doc_type = doc_type
        settings = {
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 2
            },
            "mappings": {
                "urls": {
                    "properties": {
                        "question": {
                            "type": "string"
                        },
                        "answer":{
                            "type": "string"
                        }
                    }
                }
            }
        }
        if not self.es.indices.exists(index_name):
            # Ignore 400 means to ignore "Index Already Exist" error.
            self.es.indices.create(index=index_name, ignore=400, body=settings)

    def get(self, question):
        from nltk.tokenize import sent_tokenize, word_tokenize
        from nltk.corpus import stopwords
        words = word_tokenize(question)
        stopWords = set(stopwords.words('english'))
        wordsFiltered = []
        for w in words:
            if w not in stopWords:
                wordsFiltered.append(w)
        return self.es.search(
            index=self.index_name,
            body={"query" : {
                "query_string" : {
                    "query": ' '.join(wordsFiltered), "default_operator": "AND", 'fields':['question']}
            }})['hits']

    def store(self, question, answer):
        data = {
            'question': question,
            'answer': answer,
        }
        self.es.index(
            index=self.index_name,
            doc_type=self.doc_type,
            id=hashlib.md5(question.encode('utf-8')).hexdigest(),
            body=data)


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

def tfidf(q, results):
    data = {'query': q}
    for result in results:
        root = result['_source']['path']
        pgraphs = result['_source']['content'].split('\n\n\n')
        data.update(zip([root+':'+str(count) for count in range(len(pgraphs))], pgraphs))
    vectorizer = TfidfVectorizer(tokenizer=LemmaTokenizer(), ngram_range=(1, 1))
    X = vectorizer.fit_transform(list(data.values()))
    newdata = sklearn.metrics.pairwise.cosine_similarity(X, X[0])
    tfidfdata = dict(zip(list(data.keys()), newdata.tolist()))
    sortedtfidf = sorted(tfidfdata.items(), key=operator.itemgetter(1), reverse=True)
    return  data[sortedtfidf[1][0]]


class ElasticEngine(BaseEngine):

    def __init__(self, index_name='docs', doc_type='python3.7.5'):
        self.es = elasticsearch.Elasticsearch(['http://localhost:9200'])
        self.index_name = index_name
        self.doc_type = doc_type
        settings = {
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 2
            },
            "mappings": {
                "urls": {
                    "properties": {
                        "content": {
                            "type": "string"
                        },
                        "path": {
                            "type": "string"
                        },
                    }
                }
            }
        }
        if not self.es.indices.exists(index_name):
            # Ignore 400 means to ignore "Index Already Exist" error.
            self.es.indices.create(index=index_name, ignore=400, body=settings)

    def store(self, text, path=None):
        data = {
            'path': path,
            'content': text,
        }
        self.es.index(
            index=self.index_name,
            doc_type=self.doc_type,
            id=hashlib.md5(text.encode('utf-8')).hexdigest(),
            body=data)

    def get(self, question):
        from nltk.tokenize import sent_tokenize, word_tokenize
        from nltk.corpus import stopwords
        words = word_tokenize(question)
        stopWords = set(stopwords.words('english'))
        wordsFiltered = []
        for w in words:
            if w not in stopWords:
                wordsFiltered.append(w)
        results = self.es.search(
            index=self.index_name,
            body={"query": {
                "query_string": {
                    "query": ' '.join(wordsFiltered), 'fields': ['content']}
            }})['hits']['hits']
        return tfidf(question, results)

def createQuery(question):
    import os
    from nltk.parse.stanford import StanfordDependencyParser
    os.environ['STANFORD_PARSER'] = r'C:\Users\pramod\Desktop\CodeWeek\nlp\stanford-parser-full-2018-10-17'
    os.environ['STANFORD_MODELS'] = r'C:\Users\pramod\Desktop\CodeWeek\nlp\stanford-parser-full-2018-10-17'
    os.environ['JAVAHOME'] = r'C:\Program Files\Java\jdk1.8.0_151\bin'
    dep_parser = StanfordDependencyParser(
        model_path=r"C:\Users\pramod\Desktop\CodeWeek\nlp\en_ewt_models\edu\stanford\nlp\models\lexparser\englishPCFG.ser.gz")
    parsedata = list(dep_parser.raw_parse(question))
    strees  = list(parsedata[0].tree())
    string =  '\"%s\"' % strees[0].flatten().label()
    for t in strees[1:]:
        string = string + '\"%s\"' % (' '.join(t.flatten().leaves()) + ' ' + t.flatten().label() )
        print('\"%s\"' % t.flatten().label(), '\"%s\"' % ' '.join(t.flatten().leaves()))
    print(string)
    return string
