import sys
import re
import os
from jpype import getDefaultJVMPath, startJVM, JClass
# import yaml
# sys.path.append(os.path.abspath(os.path.dirname(__file__)))


def chcwd(origin_func):
    def wrapper(self, *args, **kwargs):
        cwd = os.getcwd()
        os.chdir(self.module_path)
        u = origin_func(self, *args, **kwargs)
        os.chdir(cwd)
        return u
    return wrapper


class HanLP(object):
    module_path = os.path.abspath(os.path.dirname(__file__))
    java_class_path = os.path.join(module_path, 'hanlp.jar') + ':' + module_path

    @chcwd
    def __init__(self):
        try:
            startJVM(
                getDefaultJVMPath(),
                '-Djava.class.path=' + self.java_class_path,
                '-Xms1g', '-Xmx1g')
        except:
            pass
        self._hanlp = JClass('com.hankcs.hanlp.HanLP')

    @chcwd
    def tokenize(self, content, no_pos=True, engine='NLPTokenizer'):
        """分词
        """
        if isinstance(content, str) and len(content)>0:
            segments = []
            if engine == 'StandardTokenizer':
                tokenizer = JClass('com.hankcs.hanlp.tokenizer.StandardTokenizer')
            elif engine == 'IndexTokenizer':
                tokenizer = JClass('com.hankcs.hanlp.tokenizer.IndexTokenizer')
            elif engine == 'SpeedTokenizer':
                tokenizer = JClass('com.hankcs.hanlp.tokenizer.SpeedTokenizer')
            else:
                # NLPTokenizer
                tokenizer = JClass('com.hankcs.hanlp.tokenizer.NLPTokenizer')
            ret = tokenizer.segment(content)
            # print(content, ret)
            for v in ret:
                if no_pos:
                    segments.append(re.sub(r'/[a-zA-Z0-9]+$', '', str(v)))
                else:
                    segments.append(str(v))
            return segments

    @chcwd
    def extract_keywords(self, content, number=5):
        """提取关键字
        """
        hanlp = JClass('com.hankcs.hanlp.summary.TextRankKeyword')
        ret = hanlp.getKeywordList(content, number)
        segments = []
        for v in ret:
            segments.append(str(v))
        return segments

    @chcwd
    def extract_summary(self, content, number=5):
        """提取关键句子，即摘要
        """
        hanlp = JClass('com.hankcs.hanlp.summary.TextRankSentence')
        ret = hanlp.getTopSentenceList(content, number)
        segments = []
        for v in ret:
            segments.append(str(v))
        return segments

    @chcwd
    def extract_phrase(self, content, number=5):
        """提取互信息短句
        """
        hanlp = JClass('com.hankcs.hanlp.mining.phrase.MutualInformationEntropyPhraseExtractor')
        ret = hanlp.extract(content, number)
        segments = []
        for v in ret:
            segments.append(str(v))
        return segments

    @chcwd
    def add(self, word):
        hanlp = JClass('com.hankcs.hanlp.dictionary.CustomDictionary')
        hanlp.add(word)

    @chcwd
    def insert(self, word, info):
        hanlp = JClass('com.hankcs.hanlp.dictionary.CustomDictionary')
        hanlp.insert(word, info)


def test():
    nlp = HanLP()
    r = nlp.tokenize('我爱北京天安门')
    print(r)
    print(nlp.extract_keywords('我爱北京天安门'))


if __name__ == '__main__':
    test()

