import pickle,codecs
import numpy as np
from keras.models import load_model
from keras.preprocessing import sequence

with open('../tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

predictwords = codecs.open('inflections_de','r','utf-8').read().splitlines()
predict_in = ["^ "+" ".join(list(w))+" $" for w in predictwords]
train_in_seq = sequence.pad_sequences(tokenizer.texts_to_sequences(predict_in),maxlen=40,padding='post',truncating='post')

model = load_model('../hdf5')

pre = model.predict(train_in_seq,batch_size=48)


def map(num):
    if num == 0:
        return ""
    elif num == 1:
        return "0"
    elif num == 2:
        return "1"
    elif num == 3:
        return "2"
    elif num == 4:
        return "3"
    elif num == 5:
        return "b"
    elif num == 6:
        return "e"

for p_word, word in zip(pre,predictwords):
    result = [map(np.argmax(p_char,axis=0)) for p_char in p_word]
    #try:
    result = result[1:result.index('e')]
    positions = [(i,x) for i,x in enumerate(result) if x!='0']
    print(word)
    print("".join(result))
    for i, (pos, type) in enumerate(positions[:-1]):
        print(word[pos:positions[i+1][0]]+"_"+type, end=" ")
    if len(positions)>0:
        print(word[positions[-1][0]:]+"_"+positions[-1][1]+"\n")
    else:
        print(word+"_2")
    #except:
    #    print(word+"  $$\n"+"".join(result)+"\n")
