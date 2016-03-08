"""Calc Rating of Each Strategy

usage: calc_rating_of_each_strategy.py -h | --help
       calc_rating_of_each_strategy.py <csv_path>

options:
    -h, --help  show this help message and exit
"""

#TODO
#勝敗/引をクラス化
#

import csv
from docopt import docopt
from enum import Enum
import sys

def calc_diff_rate(m, o, result):
    if result == Result.win:
        s = (o - m) / 25.0 + 16.0
        s = max(1.0, s)
        s = min(31.0, s)
        return s
    elif result == Result.lose:
        return -calc_diff_rate(o, m, Result.win)
    else:
        return 0.0

class Result(Enum):
    win = 1
    draw = 0
    lose = -1

class RatingManager:
    def load_csv(self, csv_path):
        with open(csv_path, 'r') as f:
            reader = csv.reader(f)
            header = next(reader) #1行目は列に関するヘッダ

            for csv_line_obj in reader:
                id_i = int(csv_line_obj[0])
                date_str = csv_line_obj[1]
                my_R = float(csv_line_obj[2])
                opp_R = float(csv_line_obj[3])
                fs = csv_line_obj[4]
                strategy = csv_line_obj[5]

                if csv_line_obj[6] == "●":
                    result = Result.lose
                elif csv_line_obj[6] == "○":
                    result = Result.win
                elif csv_line_obj[6] == "引":
                    result = Result.draw
                else:
                    raise Exception('Error in csv')

                tpl = (id_i, date_str, my_R, opp_R, fs, strategy, result)
                self.all_stats.append(tpl)


    def __init__(self, csv_path):
        self.all_stats = []
        self.load_csv(csv_path)

        self.rating_turn_dic = {}

        self.real_rate_list = [] #総合レートの推移。ただし、NR戦でもレートが上昇することと15-60の場合の倍率を考慮していないので実際のレートとは異なる
        for id_i, date_str, my_R, opp_R, fs, strategy, result in self.all_stats:
            key = (strategy, fs)
            if not (key in self.rating_turn_dic):
                    init_rate = 1080.0
                    self.rating_turn_dic[key] = [init_rate]
            old_rate = self.rating_turn_dic[key][-1]
            new_rate = old_rate + calc_diff_rate(old_rate, opp_R, result)

            self.real_rate_list.append(my_R + calc_diff_rate(my_R, opp_R, result))
            self.rating_turn_dic[key].append(new_rate)

        # for key, val in self.rating_turn_dic.items():
            # print("%s : %s" % (key, val))

        # a = [val[-1] for key, val in self.rating_turn_dic.items()]
        # l = len(a)
        # average = sum(a) / l


        last_rates = [(key, val[-1])for key, val in self.rating_turn_dic.items()]

        filter_num = 10 #この数以上対局した戦型しかカウントしない
        lst = [(key, last_rate) for key, last_rate in last_rates if len(self.rating_turn_dic[key]) - 1 >= filter_num]
        all_battle_num = sum([len(self.rating_turn_dic[key]) - 1  for key, last_rate in lst])


        weighed_avg = sum([last_rate * (len(self.rating_turn_dic[key]) - 1) / all_battle_num for key, last_rate in lst]) #リストの先頭はinit_rateなので、対局数はlen() - 1

        print("過去10戦の平均レート: %.0f" % (sum(self.real_rate_list[-10:]) / 10.0))

        for key, last_rate in sorted([tpl for tpl in lst if tpl[1] >= weighed_avg], key=lambda tpl:tpl[1], reverse=True):
            print("%s : %.0f (%d/%d = %.1f%%)" % (key, last_rate, len(self.rating_turn_dic[key])-1, all_battle_num, (len(self.rating_turn_dic[key])-1)/ all_battle_num * 100))

        print("----------")
        print("重み付き平均 : %.0f" % weighed_avg)
        print("----------")

        for key, last_rate in sorted([tpl for tpl in lst if tpl[1] < weighed_avg], key=lambda tpl:tpl[1], reverse=True):
            print("%s : %.0f (%d/%d = %.1f%%)" % (key, last_rate, len(self.rating_turn_dic[key])-1, all_battle_num, (len(self.rating_turn_dic[key])-1)/ all_battle_num * 100))



def main():
    args = docopt(__doc__)
    csv_path = args["<csv_path>"]

    rate_manager = RatingManager(csv_path)


    return

if __name__ == '__main__':
    main()
