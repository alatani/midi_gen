import tensorflow as tf
import time

from deepdazai_old.language_model import LanguageModel
from deepdazai_old.util import TextLoader

from utils.training_saver import TrainingSaver

def run():

    import argparse

    parser = argparse.ArgumentParser()
    replace_args = False
    args = parser.parse_args()
    args.prime = " "
    args.batch_size = 50
    args.seq_length = 20
    args.rnn_state_size = 300
    args.stacked_rnn_layers = 2
    args.grad_clip = 5.0
    args.n = 300

    ## args
    args.num_epochs = 40
    learning_rate = 0.0007
    decay_rate = 0.97
    save_every = 100


    data_dir = "/Users/a14139/workspace/mml/lstm/dataset/dazai"
    data_dir = "/Users/a14139/workspace/mml/lstm/dataset/dazai_tiny"
    data_loader = TextLoader(data_dir, args.batch_size, args.seq_length)
    args.vocab_size = data_loader.vocab_size

    saver = TrainingSaver("deepdazai_tiny", "2016-12-27")


    restore_model = False
    if restore_model:
        new_args = saver.restore_args(args)
        if not replace_args:
           args = new_args
        else:
           print("replaced old args with new setting")
        data_loader = saver.restore_data(data_loader)

    model = LanguageModel(args, False)


    with tf.Session() as sess:
        tf.global_variables_initializer().run()

        #saver.restore_model(sess)
        first_global_step = sess.run(model.global_step)


        #tensorboard
        merged = tf.summary.merge_all()
        writer = tf.summary.FileWriter("/tmp/tensorflow_log", sess.graph)

        #restore model
        for e in range(args.num_epochs):
            sess.run(tf.assign(model.lr, learning_rate * (decay_rate ** e)))
            data_loader.reset_batch_pointer()
            print(model.initial_state)
            state = sess.run(model.initial_state)
            print("state",state)

            for b in range(data_loader.num_batches):
                start = time.time()
                x, y = data_loader.next_batch()
                feed = {model.input_data: x, model.targets: y, model.initial_state: state}
                merged_result, train_loss, state, _ = sess.run([merged, model.cost, model.final_state, model.train_op], feed)
                writer.add_summary(merged_result[0], e)

                end = time.time()

                global_step = sess.run(model.global_step)
                print("{}/{} (epoch {}), train_loss = {:.3f}, time/batch = {:.3f}" \
                      .format(global_step,
                              args.num_epochs * data_loader.num_batches + first_global_step,
                              e, train_loss, end - start))

                if global_step % save_every == 0 or (e==args.num_epochs-1 and b==data_loader.num_batches-1): # save for the last result
                    saver.save(sess, global_step = global_step)


if __name__ == "__main__":
    run()
