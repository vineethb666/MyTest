from engines import ElasticEngine


e = ElasticEngine()
import os

with os.scandir(r'C:\Users\pramod\Desktop\CodeWeek\python-3.7.5-docs-text') as entries:
    for entry in entries:
        if entry.path.endswith('.txt'):
            with open(entry.path,  encoding="utf8") as fp:
                e.store(fp.read(), entry.path)
        else:
            with os.scandir(entry.path) as folder:
                for file in folder:
                    with open(file.path,  encoding="utf8") as fp:
                         e.store(fp.read(), entry.path)
