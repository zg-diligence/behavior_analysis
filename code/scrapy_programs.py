import os
import codecs
from bs4 import BeautifulSoup
from urllib.request import urlopen

DEBUG = True
SCRAPY_PATH = os.getcwd() + '/tmp_result/scrapy_programs'

class Scrapyer(object):
    def __init__(self):
        pass

    def scrapy_aiqiyi_program(self, category_num, des_file):
        programs = []
        for page in range(1, 31):
            url = 'http://list.iqiyi.com/www/%d/-----------2011_2015--' \
                  '11-%d-1-iqiyi--.html' % (category_num, page)
            if DEBUG: print('enter', url)

            try:
                html = urlopen(url)
                bsObj = BeautifulSoup(html, 'html.parser')
                ul = bsObj.find_all('ul', class_='site-piclist site-piclist-180236 site-piclist-auto')[0]
                programs += [item.div.a['title'] for item in ul.find_all('li')]
            except Exception as e:
                print('page', page, 'error', e)
                continue

        with codecs.open(des_file, 'w', encoding='utf8') as fw:
            fw.write('\n'.join(sorted(set(programs))))

    def scrapy_programs_from_aiqiyi(self):
        num_categories = {2:'电视剧', 1:'电影'}
        for num in num_categories.keys():
            des_file_path = SCRAPY_PATH + '/爱奇艺_' + num_categories[num] + '.txt'
            self.scrapy_aiqiyi_program(num, des_file_path)

    def scrapy_youku_program(self, category_num, des_file):
        programs = []
        years = list(range(2011, 2016))
        for year in years:
            url = 'http://list.youku.com/category/show/c_%d_r_%d_s_1_d_1_p_1.html?' \
                  'spm=a2h1n.8251845.0.0' % (category_num, year)

            try:
                html = urlopen(url)
                bsObj = BeautifulSoup(html, 'html.parser')
                tmp = bsObj.find_all('ul', class_='yk-pages')[0]
                max_page = int(tmp.find_all('li')[-2].a.get_text())
                if DEBUG: print('\n\rThe year', year, 'total', max_page, 'pages')
            except Exception as e:
                print('year', year, 'error', e)
                continue

            for page in range(1, max_page+1):
                url = 'http://list.youku.com/category/show/c_%d_r_%d_s_1_d_1_p_%d.html?' \
                      'spm=a2h1n.8251845.0.0' % (category_num, year, page)
                if DEBUG: print('enter', url)

                try:
                    html = urlopen(url)
                    bsObj = BeautifulSoup(html, 'html.parser')
                    items = bsObj.find_all('li', class_='yk-col4 mr1')
                    programs += [item.div.div.a['title'] for item in items]
                except Exception as e:
                    print('page', page, 'error', e)
                    continue

        with codecs.open(des_file, 'w', encoding='utf8') as fw:
            fw.write('\n'.join(sorted(set(programs))))

    def scrapy_programs_from_youku(self):
        num_categories = {96:'电影', 97:'电视剧', 100:'动漫'}
        for num in num_categories.keys():
            des_file_path = SCRAPY_PATH + '/优酷_' + num_categories[num] + '.txt'
            self.scrapy_youku_program(num, des_file_path)

    def scrapy_tencent_program(self, category_name, des_file):
        years = {'movie':[100063, 100034, 100035], 'tv':[860, 861, 862, 863, 864], 'cartoon':[2, 3, 4, 5, 6]}

        programs = []
        for year in years[category_name]:
            url = 'http://v.qq.com/x/list/%s?year=%d&offset=0' % (category_name, year)

            try:
                html = urlopen(url)
                bsObj = BeautifulSoup(html, 'html.parser')
                max_page = int(bsObj.find_all('a', class_='page_num')[-1].get_text())
                if DEBUG: print('\n\rThe year', year, 'total', max_page, 'pages')
            except Exception as e:
                print('year', year, 'error', e)
                continue

            for page in range(max_page):
                url = 'http://v.qq.com/x/list/%s?year=%d&offset=%d' % (category_name, year, 30 * page)
                if DEBUG: print('enter', url)

                try:
                    html = urlopen(url)
                    bsObj = BeautifulSoup(html, 'html.parser')
                    items = bsObj.find_all('li', class_='list_item')
                    programs += [item.a.img['alt'] for item in items]
                except Exception as e:
                    print('page', page, 'error', e)
                    continue

        with codecs.open(des_file, 'w', encoding='utf8') as fw:
            fw.write('\n'.join(sorted(set(programs))))

    def scrapy_programs_from_tencent(self):
        name_categories = {'tv': '电视剧', 'movie':'电影', 'cartoon':'动漫'}
        for name in name_categories.keys():
            des_file_path = SCRAPY_PATH + '/腾讯_' + name_categories[name] + '.txt'
            self.scrapy_tencent_program(name, des_file_path)


if __name__ == '__main__':
    handler = Scrapyer()

    if not os.path.exists(SCRAPY_PATH):
        os.mkdir(SCRAPY_PATH)

    # handler.scrapy_programs_from_aiqiyi()
    handler.scrapy_programs_from_youku()
    # handler.scrapy_programs_from_tencent()
