from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS
from wordcloud import WordCloud,STOPWORDS
from PIL import Image

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import mglearn
import sys
import re
import os

VECT = CountVectorizer(ngram_range=(1,1),stop_words='english')

def process_file(fpath: str):
    with open(fpath) as f:
        clean_cont = f.read().splitlines()

    clean_cont = [l.split(' -- ')[0] for l in clean_cont if l.strip() != '.']

    shear=[i.replace('\xe2\x80\x9c','') for i in clean_cont ]
    shear=[i.replace('\xe2\x80\x9d','') for i in shear ]
    shear=[i.replace('\xe2\x80\x99s','') for i in shear ]

    shears = [x for x in shear if x != ' ']
    shearss = [x for x in shears if x != '']

    dubby = [re.sub("[^a-zA-Z]+", " ", s) for s in shearss]

    return dubby

def analyze_contents(dubbed: list):
    global VECT
    dtm = VECT.fit_transform(dubbed)

    # pd.DataFrame(dtm.toarray(),columns=VECT.get_feature_names())

    lda=LatentDirichletAllocation(n_components=5)
    lda.fit_transform(dtm)

    lda_dtf = lda.fit_transform(dtm)
    # pd.DataFrame(lda_dtf.toarray(),columns=VECT.get_feature_names())

    sorting = np.argsort(lda.components_)[:,::-1]
    features = np.array(VECT.get_feature_names())

    # SHOW TOP 5 TOPICAL CATEGORIES AND THE TERMS IN FREQUENCY ORDER
    mglearn.tools.print_topics(topics=range(10), feature_names=features,
    sorting=sorting, topics_per_chunk=10, n_words=20)

    # GET RICHEST TOPIC 0/4 (0-4) instances
    # topic_0=np.argsort(lda_dtf[:,0])[::-1]
    # for i in topic_0[:4]:
    #     print(".".join(dubbed[i].split(".")[:2]) + ".\n")

    # GET RICHEST TOPIC 1/4 (0-4) instances
    # topic_1=np.argsort(lda_dtf[:,1])[::-1]
    # for i in topic_1[:4]:
    #     print(".".join(dubbed[i].split(".")[:2]) + ".\n")
    
    # # GET RICHEST TOPIC 2/4 (0-4) instances
    # topic_2=np.argsort(lda_dtf[:,2])[::-1]
    # for i in topic_2[:4]:
    #     print(".".join(dubbed[i].split(".")[:2]) + ".\n")

    # # GET RICHEST TOPIC 3/4 (0-4) instances
    # topic_3=np.argsort(lda_dtf[:,3])[::-1]
    # for i in topic_3[:4]:
    #     print(".".join(dubbed[i].split(".")[:2]) + ".\n")
    
    # # GET RICHEST TOPIC 4/4 (0-4) instances
    # topic_4=np.argsort(lda_dtf[:,4])[::-1]
    # for i in topic_4[:4]:
    #     print(".".join(dubbed[i].split(".")[:2]) + ".\n")

def gen_wordcloud(fpath: str):
    text = open(fpath).read()
    mask = np.array(Image.open("./mask.png"))
    stopwords = set(STOPWORDS)
    wc = WordCloud(background_color="black", max_words=2000, mask=mask, stopwords=stopwords)
    wc.generate(text)
    wc.to_file("./wordclouds/" + os.path.splitext(os.path.basename(fpath))[0] + ".wc.png")
    plt.figure(figsize=(16,13))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")
    # plt.figure()
    # plt.imshow(mask, cmap=plt.cm.gray, interpolation='bilinear')
    # plt.axis("off")
    plt.show()

def main(argv):
    analyze = True

    if len(argv) > 1:
        analyze = False

    directory = "./files-to-analyze"
    for file in os.listdir(directory):
        if file.endswith('.txt'):
            fpath = directory + "/" + file

            if analyze:
                # Analyze contents
                dubbed = process_file(fpath)
                analyze_contents(dubbed)
            else:
                # Generate WordCloud from document contents
                gen_wordcloud(fpath)
            

if __name__ == "__main__":
    main(sys.argv)