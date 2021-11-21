""" 
 stat_mjai_score.py

"""

import json
import argparse
import os
import glob
import dataclasses

NUM_PLAYERS = 3

@dataclasses.dataclass
class PlayerResult :
    count_kyoku : int   = 0
    count_game  : int   = 0 
    count_reach : int   = 0
    count_furo  : int   = 0
    count_hora  : int   = 0
    count_baojia: int   = 0 # 放銃
    count_tsumo : int   = 0
    total_score : int   = 0
    total_hora_score : int  = 0
    total_baojia_score : int = 0
    count_ranks : list = None

    def __post_init__(self) :
        self.count_ranks = [0] * NUM_PLAYERS
        
    def calc_stat(self) :
        pass

    def __add__(self, other) :
        result = PlayerResult(
            count_kyoku = self.count_kyoku + other.count_kyoku,
            count_game = self.count_game + other.count_game,
            count_reach = self.count_reach + other.count_reach,
            count_furo = self.count_furo + other.count_furo,
            count_hora = self.count_hora + other.count_hora,
            count_baojia = self.count_baojia + other.count_baojia,
            count_tsumo = self.count_tsumo + other.count_tsumo,
            total_score = self.total_score + other.total_score,
            total_hora_score = self.total_hora_score + other.total_hora_score,
            total_baojia_score = self.total_baojia_score + other.total_baojia_score,
        )
        result.count_ranks = [rank1 + rank2 for rank1, rank2 in zip(self.count_ranks, other.count_ranks)]
        return result

def merge_game_result(result1, result2) :
    game_result = {}
    names = result1.keys() | result2.keys()
    for name in names :
        res1 = result1[name] if (name in result1) else PlayerResult()
        res2 = result2[name] if (name in result2) else PlayerResult()
        game_result[name] = res1 + res2
    return game_result

def get_result_from_mjson(log_file) :
    result = {}
    for line in log_file :
        action = json.loads(line)
        action_type = action["type"]
        if action_type == "start_game" :
            names = action["names"]
            for name in names :
                result[name] = PlayerResult()
                result[name].count_game += 1
        elif action_type == "start_kyoku" :
            for name in names :
                result[name].count_kyoku += 1
        elif action_type == "reach" :
            actor = action["actor"]
            result[names[actor]].count_reach += 1
        elif action_type in ("pon", "chi") :
            actor = action["actor"]
            result[names[actor]].count_furo += 1
        elif action_type == "hora" :
            actor = action["actor"]
            target = action["target"]
            delta_scores = action["deltas"]
            result[names[actor]].count_hora += 1
            result[names[actor]].total_hora_score += delta_scores[actor]
            if actor != target :
                result[names[target]].count_baojia += 1
                result[names[target]].total_baojia_score += delta_scores[target]
            else :
                result[names[actor]].count_tsumo += 1
        elif action_type == "end_game" :
            scores = action["scores"]

            # Calculate ranking by Mahjong rule
            range_indices = range(len(scores))
            sorted_indices = sorted(range_indices, key = scores.__getitem__, reverse = True)
            ranks = sorted(range_indices, key = sorted_indices.__getitem__)

            for name, rank in zip(names, ranks) :
                result[name].count_ranks[rank] += 1
    return result

def print_player_result(name, player_result : PlayerResult) :
    count_ranks = player_result.count_ranks
    format_ranks = '\n'.join([ "  {}位       | {}".format(i + 1, count_rank ) for i, count_rank in enumerate(count_ranks)])

    format_str = """\
name        : {name}
---------------------------------------
局数        : {count_kyoku}局
和了率      : {rate_hora}%
自摸率      : {rate_tsumo}%
平均得点    : {average_win_score}
平均失点    : {average_loss_score}
放銃率      : {rate_dealin}%
立直率      : {rate_reach}%
副露率      : {rate_furo}%
  順位      | 回数 
{format_ranks}
平均順位    : {average_rank}
流局率      : {rate_draw}%
流局時聴牌率: {rate_draw_tenpai}%
    """
    score_message = format_str.format(
        name = name,
        count_kyoku = player_result.count_kyoku,
        rate_hora   = 0.0 * 100,
        rate_tsumo  = 0.0 * 100,
        average_win_score = 0,
        average_loss_score = 0,
        rate_dealin  = 0.0 * 100,
        rate_reach  = 0.0 * 100,
        rate_furo   = 0.0 * 100,
        format_ranks = format_ranks,
        average_rank = 0,
        rate_draw   = 0.0 * 100,
        rate_draw_tenpai = 0.0 * 100,
    )
    print(score_message)
"""
    count_kyoku : int   = 0
    count_game  : int   = 0 
    count_reach : int   = 0
    count_furo  : int   = 0
    count_hora  : int   = 0
    count_baojia: int   = 0 # 放銃
    count_tsumo : int   = 0
    total_score : int   = 0
    total_hora_score : int  = 0
    total_baojia_score : int = 0
    count_ranks : list = None
"""

def main(args) :
    log_dir = args.log_directory
    log_file_prefix = os.path.join(log_dir, '*.mjson')
    log_file_list = glob.glob(log_file_prefix)

    results = {}
    for log_file_name in log_file_list :
        log_file = open(log_file_name, 'r', encoding="utf-8")
        game_result = get_result_from_mjson(log_file)
        results = merge_game_result(game_result, results)
        log_file.close()
    
    for name, res in results.items() :
        print_player_result(name, res)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = "Statistics mjai records.")
    parser.add_argument('log_directory', help = "mjai log directory")
    args = parser.parse_args()
    main(args)