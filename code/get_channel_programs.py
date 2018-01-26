import os
import re
import time
import codecs
import psutil
import shutil
import multiprocessing
from string import punctuation as env_punc
from zhon.hanzi import punctuation as chs_punc
from classify_programs import Classify
from basic_category import sports_keywords

DEBUG = True
TMP_PATH = os.getcwd() + '/tmp_result'
ROOT_CATELOGUE = '/media/gzhang/Data'
SCRAPY_PATH = TMP_PATH + '/scrapy_programs'
EXTRACT_ITEM_ERR = TMP_PATH + '/extract_item_error'
EXTRACT_PROGRAM_ERR = TMP_PATH + '/extract_program_error'
EXTRACT_CHANNEL_PROGRAM = TMP_PATH + '/extract_channel_program'

class Preprocess(object):
    def __init__(self):
        self.events = ['21','5','96','97','6','7','13','14','17', '23']

    def extract_channel_program(self, err_fw, fr_path, line):
        """
        extract channel and program in one item
        :param err_fw: file writer for err log
        :param fr_path: path of file that current item belongs to
        :param line: current item
        :return: channel and program in current item
        """

        try:
            items = line.strip().split('|')
            if items[1] in ['21', '97', '6', '13', '14', '17', '23']:
                return items[9] + "|" + items[10]
            if items[1] == "5":
                return items[10] + "|" + items[11]
            elif items[1] == "7":
                return items[11] + "|" + items[12]
            elif items[1] == "96":
                return items[-2]
        except IndexError as e: # invalid data item
            err_fw.write(fr_path + '|'  + str(e) + '|' + line +'\n\r')
            return None

    def write_extract_buffer(self, src_folder, channel_program_res):
        """
        flush buffer content into file
        :param src_folder: folder that current buffer content belongs to
        :param channel_program_res: extracted channels and programs in the buffer
        """

        if DEBUG: print(psutil.virtual_memory().percent, src_folder)
        for i in range(len(channel_program_res)):
            path = EXTRACT_CHANNEL_PROGRAM + '/' + src_folder[-2:] + '_' + self.events[i] + '.txt'
            with codecs.open(path, 'a', encoding='utf8') as fw:
                fw.write('\n'.join(set(channel_program_res[i])) + '\n')
            channel_program_res[i] = []

    def extract_events(self, src_folder, des_folder):
        """
        extract events/channels/programs in one single folder
        :param src_folder: source folder
        :param des_folder: destination folder
        """

        extract_item_err_file = EXTRACT_ITEM_ERR + '/' + src_folder[-2:] + '_error.txt'
        extract_program_err_file = EXTRACT_PROGRAM_ERR + '/' + src_folder[-2:] + '_error.txt'
        err_fw = codecs.open(extract_program_err_file, 'w', encoding='utf8', errors='replace')

        src_files = sorted(os.listdir(src_folder))
        channel_program_res = [[] for _ in range(len(self.events))]
        with codecs.open(extract_item_err_file, 'w', encoding='utf8') as err:
            for file_name in src_files:
                if DEBUG: print("enter", src_folder[-2:], file_name)
                fr_path = src_folder + "/" + file_name
                fw_path = des_folder + "/" + file_name[:-3] + "txt"
                fr = codecs.open(fr_path, 'r', encoding='gb18030', errors='replace')
                fw = codecs.open(fw_path, 'w', encoding='utf8', errors='replace')
                for line in fr:
                    try:
                        event_num = line.strip().split('|')[1]
                        if event_num in self.events:
                            res = self.extract_channel_program(err_fw, fr_path, line)
                            if res is None: continue
                            channel_program_res[self.events.index(event_num)].append(res)
                        if event_num in ['21', '5']:
                            fw.write(line)
                    except IndexError as e: # invalid data item
                        err.write(fr_path + '|' + str(e) + '|' + line + '\n\r')
                fr.close()
                fw.close()

                # when usage of the memory reaches 80 percent, flush the buffer
                if psutil.virtual_memory().percent > 80:
                    self.write_extract_buffer(src_folder, channel_program_res)
        self.write_extract_buffer(src_folder, channel_program_res)

    def extract_all_events(self, process):
        """
        extract events/channels/programs in all folders
        :param process: number of the process
        """

        # src_catelogue = ROOT_CATELOGUE + "/origin_data"
        src_catelogue =  "/media/gzhang/Others/original_data"
        des_catelogue = ROOT_CATELOGUE + "/extract_data"

        if not os.path.exists(EXTRACT_ITEM_ERR):
            os.mkdir(EXTRACT_ITEM_ERR)
        if not os.path.exists(EXTRACT_PROGRAM_ERR):
            os.mkdir(EXTRACT_PROGRAM_ERR)
        if os.path.exists(EXTRACT_CHANNEL_PROGRAM):
            shutil.rmtree(EXTRACT_CHANNEL_PROGRAM)
        os.mkdir(EXTRACT_CHANNEL_PROGRAM)

        if DEBUG: print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

        pool = multiprocessing.Pool(process)
        src_folders = sorted(os.listdir(src_catelogue))
        for folder in src_folders:
            src_folder = src_catelogue + "/" + folder
            des_folder = des_catelogue + "/" + folder
            if DEBUG: print("enter", src_folder)
            if not os.path.exists(des_folder):
                os.mkdir(des_folder)
            pool.apply_async(self.extract_events, (src_folder, des_folder))
        pool.close()
        pool.join()

        if DEBUG: print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    def cat_sort_uniq_lines(self):
        """
        merge all channel_program files
        :return:
        """

        if DEBUG: print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

        os.chdir(TMP_PATH + '/extract_channel_program')
        for event in self.events:
            if DEBUG: print('start event', event)
            command = 'cat *_' + event + '.txt |sort|uniq > uniq_' + event + '.txt'
            os.system(command)

        if DEBUG: print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    def get_channels_programs(self, file_path):
        """
        extract all unique channels and programs in one file
        :param file_path:path of the source file
        :return:ordered list of the channels and programs
        """

        channels, programs = [], []
        with codecs.open(file_path, 'r', encoding='utf8') as fr:
            for line in fr:
                channel_program = line.strip().split('|')
                if len(channel_program) != 2:
                    continue
                if channel_program[0]:
                    channels.append(channel_program[0])
                if channel_program[1]:
                    programs.append(channel_program[1])
        return list(set(channels)), list(set(programs))

    def get_all_channels_programs(self):
        """
        extract all unique channels and programs
        :return all_unique_channels/programs.txt
        """

        channels, programs = [], []
        all_files = sorted(os.listdir(EXTRACT_CHANNEL_PROGRAM))
        for file_name in all_files:
            fr_path = EXTRACT_CHANNEL_PROGRAM + '/' + file_name
            with codecs.open(fr_path, 'r', encoding='utf8') as fr:
                if file_name == 'uniq_96.txt':
                    programs += [line.strip() for line in set(fr.readlines()) if line.strip()]
                else:
                    res = self.get_channels_programs(fr_path)
                    channels += res[0]
                    programs += res[1]

        with codecs.open(TMP_PATH + '/all_unique_channels.txt', 'w', encoding='utf8') as fw:
            fw.write('\n'.join(sorted(set(channels))))
        with codecs.open(TMP_PATH + '/all_unique_programs.txt', 'w', encoding='utf8') as fw:
            fw.write('\n'.join(sorted(set(programs))))

    def get_reclassify_programs(self):
        """
        extract programms need to be reclassify
        :return: reclassify_programs.txt, reclassify_channel_programs.txt
        """

        classifier = Classify()
        reclassify_programs = []
        reclassify_channel_programs = []
        all_files = sorted(os.listdir(EXTRACT_CHANNEL_PROGRAM))
        for file_name in all_files:
            if file_name == 'uniq_13.txt': continue
            fr_path = EXTRACT_CHANNEL_PROGRAM + '/' + file_name
            with codecs.open(fr_path, 'r', encoding='utf8') as fr:
                if file_name == 'uniq_96.txt':
                    programs = [line.strip() for line in set(fr.readlines()) if line.strip()]
                    for program in programs:
                        # 音乐、电视剧、体育
                        if re.match('^\d+-.*-.*$', program): continue
                        if re.search('^电视剧|剧场', program): continue
                        if re.search(sports_keywords, program): continue
                        res = classifier.preprocess_program(program)
                        if res: reclassify_programs.append(res)
                else:
                    for line in fr.readlines():
                        tmp = line.strip()
                        if not tmp: continue

                        res = tmp.split('|')
                        if len(res) != 2: continue
                        channel, program = res[0], res[1]

                        channel = classifier.preprocess_channel(channel)
                        program = classifier.preprocess_program(program)

                        if not program: continue
                        if re.search('^电视剧|剧场', program): continue
                        if re.search(sports_keywords, program): continue
                        if not channel:
                            reclassify_programs.append(program)
                            continue

                        category = classifier.classify_channel(channel, flag=False)
                        if category == '再分类':
                            reclassify_channel_programs.append(channel + '|' + program)
                        else:
                            reclassify_programs.append(program)

        with codecs.open(TMP_PATH + '/reclassify_programs.txt', 'w') as fw:
                fw.write('\n'.join(sorted(set(reclassify_programs))))
        with codecs.open(TMP_PATH + '/reclassify_channel_programs.txt', 'w') as fw:
                fw.write('\n'.join(sorted(set(reclassify_channel_programs))))

    def normalize_programs(self, src_path, des_path):
        """
        normalize program names
        :param src_path: path of source file
        :param des_path: path of target file
        :return normalized_prorgams.txt
        """

        programs, regexes = [], []
        chs_num = '一二三四五六七八九十'
        punctuations = env_punc + chs_punc
        unvisible_chars = ''.join([chr(i) for i in range(32)])
        regexes.append(re.compile('.*(报复|反复|回复|修复)$'))
        regexes.append(re.compile('(限免|中文版|英文版|回看|复播|重播|复|[上中下尾]|[ⅡⅢI]+)$'))
        regexes.append(re.compile('\s'))                            # remove space chars
        regexes.append(re.compile('[%s]' % punctuations))           # remove punctuations
        regexes.append(re.compile('[%s]' % unvisible_chars))        # remove control chars
        regexes.append(re.compile('^(HD|3D)|(HD|SD|3D|TV|杜比)$'))   # remove program marks
        regexes.append(re.compile('(\d{2,4}年)*\d{1,2}月\d{1,2}日'))       # remove date
        regexes.append(re.compile('(第([%s]+|\d+)[部季集]+)$' % chs_num))  # remove serial number
        regexes.append(re.compile('(\d+|[%s]+)$' % chs_num))        # remove serial number

        with codecs.open(src_path, 'r', encoding='utf8') as fr:
            for line in fr:
                tmp = line.strip()
                for regex in regexes[2:]:
                    tmp = re.sub(regex, '', tmp)
                if not re.match(regexes[0], tmp):
                    tmp = re.sub(regexes[1], '', tmp)

                # remove serial number at the middle of the program name
                res = re.search('第([%s]+|\d+)[部集季]+' % chs_num, tmp)
                if res and not re.match('^\d+', tmp):
                    tmp = tmp[:res.span()[0]]

                # remove serial number at the end of the program name again
                tmp = re.sub('(\d+|[%s]+)$' % chs_num, '', tmp)
                tmp = re.sub('(第([%s]+|\d+)[部季集]+)$' % chs_num, '', tmp)

                # remove chinese garbled
                if re.search('[^(\w+\-)]', tmp):continue
                if tmp: programs.append(tmp)

        with codecs.open(des_path, 'w', encoding='utf8') as fw:
            fw.write('\n'.join(sorted(set(programs))))

    def normalize_channels(self, src_path, des_path):
        """
        normalize channel names
        :param src_path: path of source file
        :param des_path: path of target file
        :return normalized_channels.txt
        """

        with codecs.open(src_path, 'r', encoding='utf8') as fr:
            # remove punctuations
            punctuations = env_punc + chs_punc
            channels = [re.sub('[%s]' % punctuations, '', line.strip()) for line in fr]

            # remove channels including chinese garbled
            channels = [channel for channel in channels if not re.search('[^(\w+\-)]', channel)]

            # remove channels whose name is purely made up with number
            channels = [channel for channel in channels if not re.match('^[0-9]+$', channel)]

            # remove Dolby、HD、高清 channels
            tmp_channels = []
            channels = sorted(list(set(channels)))
            for channel in channels:
                if len(channel) >= 5 and re.search('(高清|频道|HD)$', channel):
                    tmp_channels.append(channel[:-2])
                elif re.search('Dolby$', channel):
                    tmp_channels.append(channel[:-5])
                elif re.search('^NVOD', channel) and channel != 'NVOD4K':
                    tmp_channels.append(channel[4:])
                else:
                    tmp_channels.append(channel)

            with codecs.open(des_path, 'w', encoding='utf') as fw:
                fw.write('\n'.join(sorted(set(tmp_channels))))

    def normalize_scrapy_programs(self):
        """
        merge and normalize scrapy_programs by category
        :return:
        """

        os.chdir(SCRAPY_PATH)
        for category in ['电视剧', '电影', '动漫']:
            command = 'cat *_' + category + '.txt |sort|uniq > merge_scrapy_' + category + '.txt'
            os.system(command)

        for category in ['电视剧', '电影', '动漫']:
            src_path = SCRAPY_PATH + '/merge_scrapy_' + category + '.txt'
            des_path = SCRAPY_PATH + '/normalized_scrapy_' + category + '.txt'
            self.normalize_programs(src_path, des_path)


if __name__ == "__main__":
    handler = Preprocess()

    # handler.extract_all_events(3)
    # handler.cat_sort_uniq_lines()
    # handler.get_all_channels_programs()
    # handler.normalize_programs(TMP_PATH + '/all_unique_programs.txt', TMP_PATH + '/normalized_prorgams.txt')
    # handler.normalize_channels(TMP_PATH + '/all_unique_channels.txt', TMP_PATH + '/normalized_channels.txt')
    # handler.get_reclassify_programs()
    handler.normalize_scrapy_programs()
