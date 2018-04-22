import numpy as np
import keras
import argparse
import codecs
import matplotlib.pyplot as plot
from keras.preprocessing.text import Tokenizer
from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers import Dense, SimpleRNN, Embedding, Bidirectional, LSTM

parser = argparse.ArgumentParser(description='Train unidirectional RNN')

parser.add_argument('--train-file', default='train-pre2',
                    help='File with sentence separated training data')
parser.add_argument('--dev-file', default='pre2',
                    help='File with sentence separated development data')
parser.add_argument('--max-length', default=25, type=int,
                    help='Maximum sequence length in tokens (Default: 25)')
parser.add_argument('--epochs', default=10, type=int,
                    help='Number of training epochs (Default: 10)')
parser.add_argument('--vocab-size', default=28, type=int,
                    help='Vocabulary size (Default: None)')
parser.add_argument('--chart',default=False, type=bool,
                    help="Chart the perplexity over epoches or not")

if __name__ == "__main__":
    # Dashes in argument names get replaced with underscores to create variable names
    args = parser.parse_args()
    seq_start = "^"
    seq_end = "$"
    max_tokens = args.max_length

    # Converting training and validation data into sequences
    trainf = codecs.open(args.train_file,'r','utf-8')
    trainpairs = [pair.split('\t') for pair in trainf.read().splitlines()]
    devf = codecs.open(args.dev_file,'r','utf-8')
    devpairs = [pair.split('\t') for pair in devf.read().splitlines()]
    corpusin = []
    for trainpair in trainpairs:
        corpusin.append(seq_start + " " + " ".join(list(trainpair[0])) + " " + seq_end)
    for devpair in devpairs:
        corpusin.append(seq_start + " " + " ".join(list(devpair[0])) + " " + seq_end)
    tokenizer = Tokenizer(num_words=args.vocab_size,filters='!"#%&()*+,-./:;<=>?[\\]_`{|}~\t\n')
    tokenizer.fit_on_texts(corpusin)
    print(tokenizer.word_index)
    print(tokenizer.word_counts)

    train_in = [seq_start + " " + " ".join(list(x[0])) + " " + seq_end for x in trainpairs]
    train_out = [[3] + [int(c)+1 for c in p[1]] + [4] for p in trainpairs] # For output, 1-> 0, 2-> 1, 3-> start, 4-> ent
    train_in_seq = sequence.pad_sequences(tokenizer.texts_to_sequences(train_in),maxlen=max_tokens,padding='post',truncating='post')
    train_out_seq = sequence.pad_sequences(train_out, maxlen=max_tokens,padding='post',truncating='post')
    train_out_seq = np.expand_dims(train_out_seq,-1)

    print(train_in_seq)
    print(train_out_seq)

    dev_in = [seq_start + " " + " ".join(list(x[0])) + " " + seq_end for x in devpairs]
    dev_out = [[3] + [int(c)+1 for c in p[1]] + [4] for p in devpairs]
    dev_in_seq = sequence.pad_sequences(tokenizer.texts_to_sequences(dev_in),maxlen=max_tokens,padding='post',truncating='post')
    dev_out_seq = sequence.pad_sequences(dev_out, maxlen=max_tokens,padding='post',truncating='post')
    # https://github.com/keras-team/keras/issues/7303
    dev_out_seq_fixed = np.expand_dims(dev_out_seq,-1)
    vocab_size=len(tokenizer.word_counts)+1

    # Training the model
    embedding_dim = 32
    rnn_dim = 16
    batch_size = 48

    model=Sequential()
    # TBD: Add model definition and compilation here
    # TBD: Add model definition and compilation here
    model.add(Embedding(vocab_size, embedding_dim, input_length=max_tokens))
    model.add(Bidirectional(LSTM(rnn_dim, return_sequences=True),input_shape=(32,)))
    # model.add(LSTM(rnn_dim, return_sequences=True))
    # model.add(SimpleRNN(rnn_dim, return_sequences=True))
    # model.add(SimpleRNN(rnn_dim, return_sequences=True))
    model.add(Dense(5, input_shape=(16,), activation='softmax'))
    model.compile(optimizer='adam',loss='sparse_categorical_crossentropy', metrics=['acc'])

    model.summary()
    history = model.fit(train_in_seq,train_out_seq,
                        epochs = args.epochs,
                        batch_size = batch_size,
                        validation_data = (dev_in_seq,dev_out_seq_fixed),
                        validation_split=0.0)

    # Charting perplexity over the training epochs

    if args.chart:
        loss_values = history.history['loss']
        val_loss_values = history.history['val_loss']
        perp = np.exp2(history.history['loss'])
        val_perp = np.exp2(history.history['val_loss'])
        epochs = range(1, len(loss_values) + 1)

        plot.plot(epochs, loss_values, 'bo', label='Training loss')
        plot.plot(epochs, val_loss_values, 'b', label='Validation loss')
        plot.title('Training and validation loss')
        plot.xlabel('Epochs')
        plot.ylabel('Loss')
        plot.legend()
        plot.figure()

        plot.plot(epochs, perp, 'bo', label='Training perplexity')
        plot.plot(epochs, val_perp, 'b', label='Validation perplexity')
        plot.title('Training and validation perplexity')
        plot.xlabel('Epochs')
        plot.ylabel('Perplexity')
        plot.legend()
        plot.show()

    # predict
    def map(num):
        if num==0:
            return ""
        elif num==1:
            return "0"
        elif num==2:
            return "1"
        elif num==3:
            return "b"
        elif num==4:
            return "e"

    predict = model.predict(dev_in_seq, batch_size=batch_size)
    for pre,gold in zip(predict, dev_out_seq):
        print(" ".join([map(np.argmax(p_group,axis=0)) for p_group in pre]))
        print(" ".join([map(label) for label in gold]))
        print()

    for name, value in zip(model.metrics_names,model.evaluate(dev_in_seq, dev_out_seq_fixed, batch_size=batch_size)):
        print(name,value)
