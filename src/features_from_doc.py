from bs4 import BeautifulSoup

def get_features(docs):
    features = []

    #trivial system: just get first paragraph of first document
    file_name, file_id = docs[0]
    f = open(file_name)
    soup = BeautifulSoup(f.read(), "lxml")
    return soup.find("doc", id=file_id).find('p').text.split()


#    for file_name, file_id in docs:
#        f = open(file_name)
#        soup = BeautifulSoup(f.read(), "lxml")
#        doc = soup.findAll("doc", id=file_id)
#        if len(doc) > 0:
#            paragraphs = []
#            p_tags = doc[0].findAll("p")
#            for p in p_tags:
#                paragraphs.append(p.text)
#            features.append(paragraphs)
#    return features
