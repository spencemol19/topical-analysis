import subprocess
import spacy
import re

def check_for_desired_type(token):
    for t_base in ['NN', 'VB']:
        if t_base in token.tag_:
            return True

    return False


def main():
    ta_output = subprocess.check_output(['python3', 'topical_analysis.bible.py']).decode('utf-8',errors='ignore')

    ta_list = list(filter(lambda l: not re.match(r'[0-9|-]', l) and bool(l.strip()), ta_output.splitlines()))

    words = []

    for line in ta_list:
        terms = line.split('\t')
        for t in terms:
            words.append(t)

    print(ta_list)

    # nlp = spacy.load('en_core_web_sm')

    # doc = nlp(' '.join(words))

    # crucial = []

    # for token in doc:
    #     if not token.is_stop and token.lemma_.length > 2 and check_for_desired_type(token):
    #         crucial.append(token.lemma_)

    # topic_map = {}

    # for item in crucial:
    #     if not topic_map.get(item):
    #         topic_map[item] = 1
    #     else:
    #         topic_map[item] += 1

    # items = [(v, k) for k, v in topic_map.items()]
    # items.sort()
    # items.reverse()
    # crucial = [k for v, k in items]

    # for c in crucial:
    #     print(c[0])

if __name__ == "__main__":
    main()
