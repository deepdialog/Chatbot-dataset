import sys
sys.path.append('/home/jovyan/work/translation')
from translate import translate
from joblib import Parallel, delayed

import yaml
from tqdm import tqdm

def translate_intent(path):
    print(path)
    with open(path) as fp:
        data = yaml.load(fp.read(), Loader=yaml.Loader)

    sentence = []
    for intent, lines in data.items():
        for l in lines:
            sentence.append(l)

    translated = Parallel(n_jobs=100)(
        delayed(translate)(x)
        for x in tqdm(sentence)
    )
    translated = {
        k: v
        for k, v in zip(sentence, translated)
    }

    ret = {}
    for intent, lines in data.items():
        ret[intent] = [translated[l] for l in lines]

    with open(path + '_zh.yaml', 'w') as fp:
        fp.write(yaml.dump(ret, allow_unicode=True))
    with open(path + '_zh_map.yaml', 'w') as fp:
        fp.write(yaml.dump(translated, allow_unicode=True))

 
if __name__ == '__main__':
    # tl = TransformersTrans()
    # print(tl.translate('hello, my friend'))
    translate_intent('intent.yaml')
    translate_intent('intent2.yaml')
    translate_intent('intent3.yaml')


