import sys
from get_topic_files import *
from get_features import *
from summarize import *

def main():
    if len(sys.argv) < 3:
        print("python main.py input_file data_dir")

    input_file = sys.argv[1] # path to xml file with topics and file names
    data_dir = sys.argv[2] # path to documents

    # get list of paths to documents as well as a list of topic IDs.
    # ids should be a list of length n where n is the number of topics.
    # documents should be an n by m 2d list where m is the number of documents per topic.
    ids, documents = get_topic_files.get_topic_files(input_file)

    # get list of feature vectors (for now, just plain text).
    # feature_vectors should be an n by f 2d array where f is the number of features per topic.
    # For now, f will be the number of documents and each feature will be the full text of 1 document.
    feature_vectors = get_features.get_features(documents)

    # should create n files with names taken from list ids
    summarize.summarize(ids, feature_vectors)


main()
