import tensorflow as tf
from deepdazai_old.language_model import LanguageModel
from utils.training_saver import TrainingSaver

def run():
    import pickle as cPickle
    import argparse
    import os,os.path

    saver = TrainingSaver("deepdazai_full", "2016-06-08_20-07")

    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    args.prime = "メロスは激怒した。"
    args.sample = 1
    args.n = 5000


    saved_args = saver.restore_args()
    data_loader = saver.restore_data()
    chars,vocab = data_loader.chars, data_loader.vocab

    model = LanguageModel(saved_args, True)
    with tf.Session() as sess:
        tf.initialize_all_variables().run()
        saver.restore_model(sess)
        print(model.sample(sess, chars, vocab, args.n, args.prime, args.sample))
