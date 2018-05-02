import numpy as np
import keras
import argparse
import codecs
import pickle
import keras.backend as K
import matplotlib.pyplot as plot
from keras.preprocessing.text import Tokenizer
from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers import Dense, SimpleRNN, Embedding, Bidirectional, LSTM

parser = argparse.ArgumentParser(description='Train unidirectional RNN')

parser.add_argument('--train-file', default='../datacleaning/train-data2',
                    help='File with sentence separated training data')
parser.add_argument('--dev-file', default='../datacleaning/devel-data2',
                    help='File with sentence separated development data')
parser.add_argument('--max-length', default=40, type=int,
                    help='Maximum sequence length in tokens (Default: 40)')
parser.add_argument('--epochs', default=10, type=int,
                    help='Number of training epochs (Default: 10)')
parser.add_argument('--vocab-size', default=29, type=int,
                    help='Vocabulary size (Default: 29)')
parser.add_argument('--chart',default=False, type=bool,
                    help="Chart the perplexity over epoches or not")
"""
def fScoreLoss(yTrue, yPred):
    obj = K.sum(int(yTrue!=0))
    pre = K.sum(int(yPred!=0))
    hit = K.sum(int(yTrue==yPred and yTrue!=0))
    precision = hit/pre
    recall = hit/obj
    return 2*precision*recall/(precision+recall)
"""

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
    with open('../tokenizer.pickle','wb') as handle:
        pickle.dump(tokenizer,handle,protocol=pickle.HIGHEST_PROTOCOL)


    train_in = [seq_start + " " + " ".join(list(x[0])) + " " + seq_end for x in trainpairs]
    train_out = [[5] + [int(c)+1 for c in p[1]] + [6] for p in trainpairs] # For output, 1-> 0, 2-> 1, 3-> start, 4-> ent
    train_in_seq = sequence.pad_sequences(tokenizer.texts_to_sequences(train_in),maxlen=max_tokens,padding='post',truncating='post')
    train_out_seq = sequence.pad_sequences(train_out, maxlen=max_tokens,padding='post',truncating='post')
    train_out_seq = np.expand_dims(train_out_seq,-1)

    print(train_in_seq)
    print(train_out_seq)

    dev_in = [seq_start + " " + " ".join(list(x[0])) + " " + seq_end for x in devpairs]
    dev_out = [[5] + [int(c)+1 for c in p[1]] + [6] for p in devpairs]
    dev_in_seq = sequence.pad_sequences(tokenizer.texts_to_sequences(dev_in),maxlen=max_tokens,padding='post',truncating='post')
    dev_out_seq = sequence.pad_sequences(dev_out, maxlen=max_tokens,padding='post',truncating='post')
    # https://github.com/keras-team/keras/issues/7303
    dev_out_seq_fixed = np.expand_dims(dev_out_seq,-1)
    vocab_size=len(tokenizer.word_counts)+1

    print(vocab_size)

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
    model.add(Dense(7, input_shape=(rnn_dim,), activation='softmax'))
    model.compile(optimizer='adam',loss='sparse_categorical_crossentropy', metrics=['acc'])

    model.summary()
    history = model.fit(train_in_seq,#+dev_in_seq,
                        train_out_seq,#+dev_out_seq_fixed,
                        epochs = args.epochs,
                        batch_size = batch_size,
                        # validation_data = (dev_in_seq,dev_out_seq_fixed),
                        validation_split=0.0)
    model.save("../hdf5")
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
            return "2"
        elif num==4:
            return "3"
        elif num==5:
            return "b"
        elif num==6:
            return "e"

    predict = model.predict(dev_in_seq, batch_size=batch_size)


    obj = 0
    pred = 0
    hit = 0

    words = [pair[0] for pair in devpairs]
    for pre,gold,word in zip(predict, dev_out_seq, words):
        pre = [map(np.argmax(p_group,axis=0)) for p_group in pre]
        result = pre[1:pre.index('e')]
        gold = [map(label) for label in gold]
        gold = gold[1:gold.index('e')]
        print("".join(gold))
        try:
            print(word)
            print("".join(result))
        except:
            print(word + "  $$\n" + "".join(pre[1:]) + "\n")
        print()
        # Calculate precision and recall:
        for r,g in zip(result,gold):
            # print(r,g, not r==0, not g==0)
            if not r=='0':
                pred+=1
                if r==g:
                    hit+=1
            if not g=='0':
                obj+=1
    # print(hit, pred, obj)
    precision = hit/pred
    recall = hit/obj
    f_measure = 2*precision*recall/(precision+recall)
    print("precision:",precision,"recall:",recall,"f-measure:",f_measure)

    for name, value in zip(model.metrics_names,model.evaluate(dev_in_seq, dev_out_seq_fixed, batch_size=batch_size)):
        print(name,value)
