import tensorflow as tf
import os.path
import pickle as cPickle

class TrainingSaver:
    def __init__(self, model_name, version = "01"):
        import datetime

        self.model_name  = model_name

        if version is None:
            version = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
        assert(isinstance(version, str))

        util_dir = os.path.abspath(os.path.dirname(__file__))
        base_dir = os.path.dirname(util_dir)
        self.model_dir = os.path.join(base_dir, "models", model_name, version)

        if os.path.exists(self.model_dir):
            self.new_model = False
            pass
        else:
            os.makedirs(self.model_dir)
            self.new_model = True
        self.ckpt = tf.train.get_checkpoint_state(self.model_dir)
        self.saver = None

    def restore_data(self, data=None):
        if self.new_model:
            with open(os.path.join(self.model_dir, 'chars_vocab.pkl'), 'wb') as f:
                cPickle.dump(data, f)
            return data
        else:
            with open(os.path.join(self.model_dir, 'chars_vocab.pkl'), 'rb') as f:
                data = cPickle.load(f)
                return data

    def restore_args(self, args=None):
        if self.new_model:
            with open(os.path.join(self.model_dir, 'config.pkl'), 'wb') as f:
                cPickle.dump(args, f)
            return args
        else:
            with open(os.path.join(self.model_dir, 'config.pkl'), 'rb') as f:
                args = cPickle.load(f)
                return args


    def save(self, sess, **args):
        if not self.saver:
            self.saver = tf.train.Saver(tf.all_variables())
        checkpoint_path = os.path.join(self.model_dir, "model.ckpt")
        self.saver.save(sess, checkpoint_path, **args)
        print("model saved to {}".format(checkpoint_path))

    def restore_model(self, sess):
        if not self.saver:
            self.saver = tf.train.Saver(tf.all_variables())
        if not self.new_model:
            self.saver.restore(sess, self.ckpt.model_checkpoint_path)

            #return args, data
        else:
            pass #new model. do nothing.

if __name__ == "__main__":
    # model_name = "deep_dazai"
    # utildir = os.path.abspath(os.path.dirname(__file__))
    # basedir = os.path.dirname(utildir)
    # path = os.path.join(basedir, "models", model_name)
    # print(path)
    pass