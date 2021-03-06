import tensorflow as tf
import numpy as np

class LanguageModel:
    def __init__(self, args, infer=False):

        import tensorflow as tf
        from tensorflow.python.ops import seq2seq, rnn_cell

        if infer:
            args.batch_size = 1
            args.seq_length = 1

        gru = rnn_cell.GRUCell(args.rnn_state_size)
        self.cell = rnn_cell.MultiRNNCell([gru] * args.stacked_rnn_layers)

        self.input_data = tf.placeholder(tf.int32, [args.batch_size, args.seq_length])         # [batch_size, seq_length]
        self.targets = tf.placeholder(tf.int32, [args.batch_size, args.seq_length])            # [batch_size, seq_length]
        self.initial_state = self.cell.zero_state(args.batch_size, tf.float32)                 # [batch_size]

        with tf.variable_scope('rnnlm'):
            softmax_w = tf.get_variable("softmax_w", [args.rnn_state_size, args.vocab_size])       # [rnn_state_size, vocab_size]
            softmax_b = tf.get_variable("softmax_b", [args.vocab_size])                       # [vocab_size]

            word_embedding = tf.get_variable("embedding", [args.vocab_size, args.rnn_state_size])  # [vocab_size, rnn_state_size]
            inputs = tf.split(1, args.seq_length, tf.nn.embedding_lookup(word_embedding, self.input_data))
            inputs = [tf.squeeze(input_, [1]) for input_ in inputs]

        def loop(prev, _):  # [batch_size, rnn_state_size]
            prev = tf.matmul(prev, softmax_w) + softmax_b      # [batch_size, vocab_size]
            prev_symbol = tf.stop_gradient(tf.argmax(prev, 1)) # [batch_size]
            return tf.nn.embedding_lookup(word_embedding, prev_symbol)

        outputs, last_state = seq2seq.rnn_decoder(inputs, self.initial_state, self.cell, loop_function=loop if infer else None, scope='rnnlm')
        # outputs: [batch_size, rnn_state_size] * seq_length

        output = tf.reshape(tf.concat(1, outputs), [-1, args.rnn_state_size])

        self.logits = tf.matmul(output, softmax_w) + softmax_b  # [batch_size * seq_length, vocab_size]
        self.probs = tf.nn.softmax(self.logits)



        loss = seq2seq.sequence_loss_by_example([self.logits],
                                                [tf.reshape(self.targets, [-1])], # [batch_size * seq_length]
                                                [tf.ones([args.batch_size * args.seq_length])],
                                                args.vocab_size)

        self.global_step = tf.Variable(0, name='global_step', trainable=False)
        self.cost = tf.reduce_sum(loss) / args.batch_size / args.seq_length

        tf.summary.scalar("cost", self.cost)

        self.final_state = last_state
        self.lr = tf.Variable(0.0, trainable=False)
        tvars = tf.trainable_variables()
        grads, _ = tf.clip_by_global_norm(tf.gradients(self.cost, tvars), args.grad_clip)
        optimizer = tf.train.AdamOptimizer(self.lr)
        self.train_op = optimizer.apply_gradients(zip(grads, tvars), global_step=self.global_step)



    def sample(self, sess, chars, vocab, num=200, prime='私は', sampling_type=1) -> str:
        state = self.cell.zero_state(1, tf.float32).eval()
        for char in prime[:-1]:
            x = np.zeros((1, 1))
            x[0, 0] = vocab[char]
            feed = {self.input_data: x, self.initial_state:state}
            [state] = sess.run([self.final_state], feed)

        def weighted_pick(weights):
            t = np.cumsum(weights)
            s = np.sum(weights)
            return(int(np.searchsorted(t, np.random.rand(1)*s)))

        ret = prime
        char = prime[-1]
        for n in range(num):
            x = np.zeros((1, 1))
            x[0, 0] = vocab.get(char)
            feed = {self.input_data: x, self.initial_state:state}
            [probs, state] = sess.run([self.probs, self.final_state], feed)
            p = probs[0]

            if sampling_type == 0:
                sample = np.argmax(p)
            elif sampling_type == 2:
                if char == ' ':
                    sample = weighted_pick(p)
                else:
                    sample = np.argmax(p)
            else: # sampling_type == 1 default:
                sample = weighted_pick(p)

            pred = chars[sample]
            ret += pred
            char = pred

        return ret




def run():
    #train()
    sample()

