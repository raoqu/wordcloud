from collections import Counter
from os import path

from wordcloud import WordCloud, STOPWORDS
from PIL import Image
import numpy as np
import jieba

TEXT_FILE = 'input.txt'
MASK_IMAGE = 'mask.png'
FONT = 'SimHei.ttf'
OUTPUT_IMAGE = 'output.png'
WORD_COUNT = 200

def filter_words(words):
    with open('stopwords.txt', 'r', encoding='utf-8') as file:
        exclude_words = [line.strip() for line in file.readlines()]
    exclude_words = exclude_words + [' ', '\n', '\t']
    return [item for item in words if item not in exclude_words]

# 分词
def word_segment(text):
    jieba_word=jieba.   cut(text,cut_all=False) # cut_all是分词模式，True是全模式，False是精准模式，默认False
    data=[]
    for word in jieba_word:
        data.append(word)

    data = filter_words(data)

    data_dict = Counter(data)
    return data_dict

def print_data(data_dict, limit):
    i = 0
    data_list = data_dict.most_common()
    for data in data_list:
        print(data)

        i = i + 1
        if i > limit:
            break

# 生成词云图片
def generate_wordcloud(word_freqs, mask_image):
    d=path.dirname(__file__)
    the_mask = np.array(Image.open(path.join(d, mask_image)))
    font_path=path.join(d, FONT)
    stopwords = set(STOPWORDS)
    wcloud = WordCloud(
        width = 1000,
        height = 800,
        background_color="white",
        colormap='viridis', # 'viridis', 'plasma', 'inferno', 'magma', 'cividis', 'jet', 'gray', 'autumn'
        max_words=WORD_COUNT,
        mask=the_mask,
        stopwords=stopwords,
        font_path=font_path, 
                  )
    wcloud.generate_from_frequencies(word_freqs)
    wcloud.to_file(OUTPUT_IMAGE)

if __name__=='__main__':
    jieba.load_userdict(path.join(path.dirname(__file__),'userdict.txt')) # 用户自定义词典

    d = path.dirname(__file__)
    text = open(path.join(d, TEXT_FILE), 'r', encoding='utf-8').read()
    data_dict = word_segment(text)
    print_data(data_dict, WORD_COUNT)
    generate_wordcloud(data_dict, MASK_IMAGE)
    
