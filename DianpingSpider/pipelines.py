# -*- coding: utf-8 -*-


import json
import codecs

class DianpingspiderJsonWriterPipeline(object):

    def __init__(self):
        self.file = codecs.open('dianping.json',
                'w', encoding='utf-8')


    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line.decode('unicode_escape'))
        return item
