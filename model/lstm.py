import tensorflow as tf

class Model:
    #
    def train(self, piano_rolls):

        pass

    def test(self):
        pass

class MusicModel(Model):
    def __init__(self, args, infer=False):
        import tensorflow as tf
        from tensorflow.models.rnn import seq2seq, rnn_cell

        if infer:
            args.batch_size = 1
            args.seq_length = 1

        gru = rnn_cell.GRUCell(args.rnn_state_size)
        self.cell = rnn_cell.MultiRNNCell([gru] * args.stacked_rnn_layers)

        self.input_data = tf.placeholder(tf.int32, [args.batch_size, args.seq_length])         # [batch_size, seq_length]
        self.targets = tf.placeholder(tf.int32, [args.batch_size, args.seq_length])            # [batch_size, seq_length]
        self.initial_state = self.cell.zero_state(args.batch_size, tf.float32)                 # [batch_size]

    pass

