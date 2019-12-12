from engines import FAQEngine


e = FAQEngine()
import os

with os.scandir(r'C:\Users\pramod\Desktop\CodeWeek\faq') as entries:
    for entry in entries:
        with open(entry.path) as fp:
            for faq in fp.read().split('\n\n\n')[1:]:
                faqsplit = faq.split('\n')
                q, a = faqsplit[0], '\n'.join(faqsplit[2:])
                e.store(q, a)
