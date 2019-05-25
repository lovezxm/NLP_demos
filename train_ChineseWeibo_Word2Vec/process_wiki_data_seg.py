# process_wiki_data.py 用于解析XML，将XML的wiki数据转换为text格式

import logging
import os.path
import sys
import io
import jieba

import warnings

warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')

from gensim.corpora import WikiCorpus

if __name__ == '__main__':
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)

    logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
    logging.root.setLevel(level=logging.INFO)
    logger.info("running %s" % ' '.join(sys.argv))

    # check and process input arguments
    if len(sys.argv) < 3:
        print(globals())
        print(locals())
        sys.exit(1)
    inp, outp = sys.argv[1:3]
    space = " "
    i = 0

    output = open(outp, 'w', encoding='utf-8')
    wiki = WikiCorpus(inp, lemmatize=False, dictionary={})
    for text in wiki.get_texts():  # 一篇文章一篇文章的获取
        jieba.enable_parallel(6)
        word_cut = jieba.cut(space.join(text), cut_all=False)  # 精确模式，返回的结构是一个可迭代的genertor
        word_list = list(word_cut)  # genertor转化为list，每个词unicode格式
        jieba.disable_parallel() # 关闭并行分词模式
        for text in word_list:
            output.write(text + " ")

        output.write("\n")
        i = i + 1
        if (i % 10000 == 0):
            logger.info("Saved " + str(i) + " articles")

    output.close()
    logger.info("Finished Saved " + str(i) + " articles")
