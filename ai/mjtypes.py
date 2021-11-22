from enum import IntEnum
from typing import List
import json
import copy
import random
import numpy as np

def is_valid_hai(hai):
    return 0 < hai and hai < 38

def haikind(hai):
	if hai % 10 == 0:
		return hai - 5
	else:
		return hai

def kaze_str_to_int(kaze_str):
    if kaze_str == "E":
        return 0
    elif kaze_str == "S":
        return 1
    elif kaze_str == "W":
        return 2
    elif kaze_str == "N":
        return 3
    else:
        assert False, "kaze_str_to_int_err"

def kaze_int_to_str(kaze):
    if kaze == 0:
        return "E"
    elif kaze == 1:
        return "S"
    elif kaze == 2:
        return "W"
    elif kaze == 3:
        return "N"
    else:
        assert False, "kaze_int_to_str_error"
        return ""

def hai_str_to_int(hai_str):
    if hai_str == "1m":
        return 1
    elif hai_str == "2m":
        return 2
    elif hai_str == "3m":
        return 3
    elif hai_str == "4m":
        return 4
    elif hai_str == "5m":
        return 5
    elif hai_str == "6m":
        return 6
    elif hai_str == "7m":
        return 7
    elif hai_str == "8m":
        return 8
    elif hai_str == "9m":
        return 9
    elif hai_str == "5mr":
        return 10
    elif hai_str == "1p":
        return 11
    elif hai_str == "2p":
        return 12
    elif hai_str == "3p":
        return 13
    elif hai_str == "4p":
        return 14
    elif hai_str == "5p":
        return 15
    elif hai_str == "6p":
        return 16
    elif hai_str == "7p":
        return 17
    elif hai_str == "8p":
        return 18
    elif hai_str == "9p":
        return 19
    elif hai_str == "5pr":
        return 20
    elif hai_str == "1s":
        return 21
    elif hai_str == "2s":
        return 22
    elif hai_str == "3s":
        return 23
    elif hai_str == "4s":
        return 24
    elif hai_str == "5s":
        return 25
    elif hai_str == "6s":
        return 26
    elif hai_str == "7s":
        return 27
    elif hai_str == "8s":
        return 28
    elif hai_str == "9s":
        return 29
    elif hai_str == "5sr":
        return 30
    elif hai_str == "E":
        return 31
    elif hai_str == "S":
        return 32
    elif hai_str == "W":
        return 33
    elif hai_str == "N":
        return 34
    elif hai_str == "P":
        return 35
    elif hai_str == "F":
        return 36
    elif hai_str == "C":
        return 37
    elif hai_str == "?":
        return -1
    else:
        assert False, "hai_str_to_int_err"

def hai_int_to_str(hai_int):
    if hai_int == 1:
        return "1m"
    elif hai_int == 2:
        return "2m"
    elif hai_int == 3:
        return "3m"
    elif hai_int == 4:
        return "4m"
    elif hai_int == 5:
        return "5m"
    elif hai_int == 6:
        return "6m"
    elif hai_int == 7:
        return "7m"
    elif hai_int == 8:
        return "8m"
    elif hai_int == 9:
        return "9m"
    elif hai_int == 10:
        return "5mr"
    elif hai_int == 11:
        return "1p"
    elif hai_int == 12:
        return "2p"
    elif hai_int == 13:
        return "3p"
    elif hai_int == 14:
        return "4p"
    elif hai_int == 15:
        return "5p"
    elif hai_int == 16:
        return "6p"
    elif hai_int == 17:
        return "7p"
    elif hai_int == 18:
        return "8p"
    elif hai_int == 19:
        return "9p"
    elif hai_int == 20:
        return "5pr"
    elif hai_int == 21:
        return "1s"
    elif hai_int == 22:
        return "2s"
    elif hai_int == 23:
        return "3s"
    elif hai_int == 24:
        return "4s"
    elif hai_int == 25:
        return "5s"
    elif hai_int == 26:
        return "6s"
    elif hai_int == 27:
        return "7s"
    elif hai_int == 28:
        return "8s"
    elif hai_int == 29:
        return "9s"
    elif hai_int == 30:
        return "5sr"
    elif hai_int == 31:
        return "E"
    elif hai_int == 32:
        return "S"
    elif hai_int == 33:
        return "W"
    elif hai_int == 34:
        return "N"
    elif hai_int == 35:
        return "P"
    elif hai_int == 36:
        return "F"
    elif hai_int == 37:
        return "C"
    else:
        assert False, "hai_int_to_str_error"
        return "?"

def get_hai38(hai136: int) -> int:
	if hai136 == 16:
		return 10
	elif hai136 == 52:
		return 20
	elif hai136 == 88:
		return 30
	else:
		haic = hai136//36
		hain = (hai136%36)//4 + 1
		return 10*haic + hain

def get_hai34(hai38: int) -> int:
    hai = haikind(hai38)
    return hai - (hai//10 + 1)

def get_hai34_array(hai_array: List[int]) -> List[int]:
    ret = [0 for i in range(34)]
    for hai in range(38):
        ret[get_hai34(hai)] += hai_array[hai]
    return ret

class Fuuro_Type(IntEnum):
	FT_CHI = 1
	FT_PON = 2
	FT_DAIMINKAN = 3
	FT_ANKAN = 4
	FT_KAKAN = 5

def fuuro_type_str(fuuro_type):
    if fuuro_type == Fuuro_Type.FT_CHI:
        return "chi"
    elif fuuro_type == Fuuro_Type.FT_PON:
        return "pon"
    elif fuuro_type == Fuuro_Type.FT_DAIMINKAN:
        return "daiminkan"
    elif fuuro_type == Fuuro_Type.FT_ANKAN:
        return "ankan"
    elif fuuro_type == Fuuro_Type.FT_KAKAN:
        return "kakan"

def get_sorted_tehai(tehai):
    tehai_list = []
    def append_tehai(hai):
        for _i in range(tehai[hai]):
            tehai_list.append(hai)
    for hai in range(38):
        if hai % 10 == 0:
            continue
        append_tehai(hai)
        if hai < 30 and hai % 10 == 5:
            append_tehai(hai + 5)
    return tehai_list

class Fuuro_Elem:
    def __init__(self, fuuro_type, hai, consumed, target_relative):
        self.fuuro_type = fuuro_type
        self.hai = hai
        self.consumed = consumed
        self.target_relative = target_relative
        # 1. 下家、2:対面、3:上家、相対位置で記憶させておくと画像表示する際に都合がよい。

    def to_json(self):
        d = {}
        d["type"] = fuuro_type_str(self.fuuro_type)
        d["consumed"] = [hai_int_to_str(h) for h in self.consumed]
        d["target_relative"] = self.target_relative
        if d["type"] != "ankan":
            d["pai"] = hai_int_to_str(self.hai)
        return d

    def to_numpy(self):
        tmp = [0 for i in range(34)]
        if self.fuuro_type != Fuuro_Type.FT_ANKAN:
            tmp[get_hai34(self.hai)] += 1
        for hai in self.consumed:
            tmp[get_hai34(hai)] += 1
        ret = np.zeros((4, 34), dtype=np.int)
        for hai in range(34):
            for i in range(tmp[hai]):
                ret[i][hai] = 1
        #print(ret)
        return ret

class Sutehai:
    def __init__(self, hai, tsumogiri, is_reach):
        self.hai = hai
        self.tsumogiri = tsumogiri
        self.is_reach = is_reach
        self.is_taken = False

    def to_json(self):
        return {
            "pai": hai_int_to_str(self.hai),
            "tsumogiri": self.tsumogiri,
            "is_reach": self.is_reach,
            "is_taken": self.is_taken
        }

class Player_State:
    def __init__(self, score, jikaze, tehai):
        self.score = score
        self.jikaze = jikaze
        self.tehai = tehai
        self.fuuro = []
        self.kawa = []
        self.reach_declared = False
        self.reach_accepted = False
        self.prev_tsumo = 0

    def set_name(self, name):
        self.name = name

    def replace_pon_to_kakan(self, fuuro_elem):
        assert fuuro_elem.fuuro_type == Fuuro_Type.FT_KAKAN, "replace_pon_to_kakan_error"
        for i in range(len(self.fuuro)):
            if self.fuuro[i].fuuro_type == Fuuro_Type.FT_PON and haikind(self.fuuro[i].hai) == haikind(fuuro_elem.hai):
                self.fuuro[i].fuuro_type = Fuuro_Type.FT_KAKAN
                self.fuuro[i].hai = fuuro_elem.hai
                self.fuuro[i].consumed = fuuro_elem.consumed

    def to_json(self, visible, name):
        ret = {
            "name": name,
            "score": self.score,
            "jikaze": kaze_int_to_str(self.jikaze),
            "tehai": [(hai_int_to_str(hai) if visible else '0') for hai in get_sorted_tehai(self.tehai)],
            "fuuro": [elem.to_json() for elem in self.fuuro],
            "kawa": [sutehai.to_json() for sutehai in self.kawa],
            "reach_declared": self.reach_declared,
            "reach_accepted": self.reach_accepted,
        }
        if 0 < self.prev_tsumo:
            ret["current_tsumo"] = hai_int_to_str(self.prev_tsumo) if visible else '0'
        return ret

    def to_numpy_fuuro(self):
        if len(self.fuuro) == 0:
            return np.zeros((4*4, 34), dtype=np.int)
        else:
            ret = np.concatenate([elem.to_numpy() for elem in self.fuuro])
            zeros = np.zeros((4*(4 - len(self.fuuro)), 34), dtype=np.int)
            return np.concatenate([ret, zeros])

    def to_numpy_kawa(self):
        length = 20
        ret = np.zeros((length*2, 34), dtype=np.int)
        for i in range(min(len(self.kawa),length)):
            hai = get_hai34(self.kawa[i].hai)
            ret[i*2][hai] = 1
            if self.kawa[i].is_reach:
                ret[i*2+1][hai] = 1
        return ret

    def to_numpy_tehai(self):
        tmp = get_hai34_array(self.tehai)
        if self.prev_tsumo != 0:
            tmp[get_hai34(self.prev_tsumo)] += 1
        ret = np.zeros((4, 34), dtype=np.int)
        for hai in range(34):
            for i in range(tmp[hai]):
                ret[i][hai] = 1
        return ret

    def to_numpy_jikaze(self):
	    ret = np.zeros((4,34), dtype=np.int)
	    for i in range(34):
	        ret[self.jikaze][i] = 1
	    return ret

    def to_numpy_score(self):
        ret = np.zeros((71,34), dtype=np.int)
        if self.score < 0:
            m = 0
        elif self.score < 70000:
            m = self.score // 1000
        else:
            m = 70
        for i in range(34):
            ret[m][i] = 1
        return ret

    def to_numpy(self, tehai_flag):
        visible = np.concatenate([self.to_numpy_fuuro(), self.to_numpy_jikaze(), self.to_numpy_kawa(), self.to_numpy_score()])
        if tehai_flag:
            return np.concatenate([self.to_numpy_tehai(), visible])
        else:
            return visible

class Game_State:
    def __init__(self, bakaze, kyoku, honba, kyotaku, scores, oya, dora_marker, tehai_array):
        self.bakaze = bakaze
        self.kyoku = kyoku
        self.honba = honba
        self.kyotaku = kyotaku
        self.dora_marker = []
        if is_valid_hai(dora_marker):
            self.dora_marker.append(dora_marker)
        self.player_state = [Player_State(scores[i], (i - oya + 4) % 4, tehai_array[i]) for i in range (4)]
        self.total_tsumo_num = 0

    def go_next_state(self, action_json):
        if action_json["type"] != "tsumo" and action_json["type"] != "reach" and action_json["type"] != "hora":
            for i in range(4):
                if 0 < self.player_state[i].prev_tsumo:
                    self.player_state[i].tehai[self.player_state[i].prev_tsumo] += 1
                    self.player_state[i].prev_tsumo = 0

        if action_json["type"] == "dora":
            self.dora_marker.append(hai_str_to_int(action_json["dora_marker"]))
        elif action_json["type"] == "tsumo":
            hai = hai_str_to_int(action_json["pai"])
            self.total_tsumo_num += 1
            if is_valid_hai(hai):
                actor = action_json["actor"]
                #self.player_state[actor].tehai[hai] += 1
                self.player_state[actor].prev_tsumo = hai
        elif action_json["type"] == "reach":
            actor = action_json["actor"]
            self.player_state[actor].reach_declared = True
        elif action_json["type"] == "reach_accepted":
            actor = action_json["actor"]
            self.player_state[actor].reach_accepted = True
            self.player_state[actor].score -= 1000
            self.kyotaku += 1
        elif action_json["type"] == "dahai":
            hai = hai_str_to_int(action_json["pai"])
            actor = action_json["actor"]
            hai = hai
            tsumogiri = action_json["tsumogiri"]
            is_reach = self.player_state[actor].reach_declared and not self.player_state[actor].reach_accepted
            self.player_state[actor].kawa.append(Sutehai(hai, tsumogiri, is_reach))
            self.player_state[actor].tehai[hai] -= 1
        elif action_json["type"] == "chi":
            actor = action_json["actor"]
            target = action_json["target"]
            self.player_state[actor].tehai[hai_str_to_int(action_json["consumed"][0])] -= 1
            self.player_state[actor].tehai[hai_str_to_int(action_json["consumed"][1])] -= 1
            hai = hai_str_to_int(action_json["pai"])
            consumed = []
            consumed.append(hai_str_to_int(action_json["consumed"][0]))
            consumed.append(hai_str_to_int(action_json["consumed"][1]))
            target_relative = (4 + target - actor) % 4
            self.player_state[actor].fuuro.append(Fuuro_Elem(Fuuro_Type.FT_CHI, hai, consumed, target_relative))
            assert self.player_state[target].kawa[-1].hai == hai, "pon_hai_error"
            self.player_state[target].kawa[-1].is_taken = True
        elif action_json["type"] == "pon":
            actor = action_json["actor"]
            target = action_json["target"]
            self.player_state[actor].tehai[hai_str_to_int(action_json["consumed"][0])] -= 1
            self.player_state[actor].tehai[hai_str_to_int(action_json["consumed"][1])] -= 1
            hai = hai_str_to_int(action_json["pai"])
            consumed = []
            consumed.append(hai_str_to_int(action_json["consumed"][0]))
            consumed.append(hai_str_to_int(action_json["consumed"][1]))
            target_relative = (4 + target - actor) % 4
            self.player_state[actor].fuuro.append(Fuuro_Elem(Fuuro_Type.FT_PON, hai, consumed, target_relative))
            assert self.player_state[target].kawa[-1].hai == hai, "pon_hai_error"
            self.player_state[target].kawa[-1].is_taken = True
        elif action_json["type"] == "daiminkan":
            actor = action_json["actor"]
            target = action_json["target"]
            self.player_state[actor].tehai[hai_str_to_int(action_json["consumed"][0])] -= 1
            self.player_state[actor].tehai[hai_str_to_int(action_json["consumed"][1])] -= 1
            self.player_state[actor].tehai[hai_str_to_int(action_json["consumed"][2])] -= 1
            hai = hai_str_to_int(action_json["pai"])
            consumed = []
            consumed.append(hai_str_to_int(action_json["consumed"][0]))
            consumed.append(hai_str_to_int(action_json["consumed"][1]))
            consumed.append(hai_str_to_int(action_json["consumed"][2]))
            target_relative = (4 + target - actor) % 4
            self.player_state[actor].fuuro.append(Fuuro_Elem(Fuuro_Type.FT_DAIMINKAN, hai, consumed, target_relative))
            assert self.player_state[target].kawa[-1].hai == hai, "pon_hai_error"
            self.player_state[target].kawa[-1].is_taken = True
        elif action_json["type"] == "ankan":
            actor = action_json["actor"]
            self.player_state[actor].tehai[hai_str_to_int(action_json["consumed"][0])] -= 1
            self.player_state[actor].tehai[hai_str_to_int(action_json["consumed"][1])] -= 1
            self.player_state[actor].tehai[hai_str_to_int(action_json["consumed"][2])] -= 1
            self.player_state[actor].tehai[hai_str_to_int(action_json["consumed"][3])] -= 1
            consumed = []
            consumed.append(hai_str_to_int(action_json["consumed"][0]))
            consumed.append(hai_str_to_int(action_json["consumed"][1]))
            consumed.append(hai_str_to_int(action_json["consumed"][2]))
            consumed.append(hai_str_to_int(action_json["consumed"][3]))
            self.player_state[actor].fuuro.append(Fuuro_Elem(Fuuro_Type.FT_ANKAN, -1, consumed, 0))
        elif action_json["type"] == "kakan":
            actor = action_json["actor"]
            self.player_state[actor].tehai[hai_str_to_int(action_json["pai"])] -= 1
            hai = hai_str_to_int(action_json["pai"])
            consumed = []
            consumed.append(hai_str_to_int(action_json["consumed"][0]))
            consumed.append(hai_str_to_int(action_json["consumed"][1]))
            consumed.append(hai_str_to_int(action_json["consumed"][2]))
            self.player_state[actor].replace_pon_to_kakan(Fuuro_Elem(Fuuro_Type.FT_KAKAN, hai, consumed, 0))
        elif action_json["type"] == "nukidora" :
            actor = action_json["actor"]
            self.player_state[actor].tehai[hai_str_to_int(action_json["pai"][0])] -= 1
            # TODO 抜いた牌をfuuroに追加

    def to_json(self, view_pid):
        # view_pid == -1 ならば全部の手牌が見える。
        return {
            "bakaze": kaze_int_to_str(self.bakaze),
            "kyoku": self.kyoku,
            "honba": self.honba,
            "kyotaku": self.kyotaku,
            "dora_marker": [hai_int_to_str(d) for d in self.dora_marker],
            "player_state": [self.player_state[pid].to_json(
                pid == view_pid or view_pid == -1,
                "Player" + str(pid)
            ) for pid in range(4)],
            "total_tsumo_num": self.total_tsumo_num
        }

    def to_numpy_bakaze(self):
	    ret = np.zeros((4,34), dtype=np.int)
	    for i in range(34):
	        ret[self.bakaze][i] = 1
	    return ret

    def to_numpy_kyoku(self):
	    ret = np.zeros((4,34), dtype=np.int)
	    for i in range(34):
	        ret[self.kyoku-1][i] = 1
	    return ret

    def to_numpy_honba(self):
	    ret = np.zeros((10,34), dtype=np.int)
	    if self.honba < 9:
	        for i in range(34):
		        ret[self.honba][i] = 1
	    else:
	        for i in range(34):
		        ret[9][i] = 1
	    return ret

    def to_numpy_kyotaku(self):
	    ret = np.zeros((10,34), dtype=np.int)
	    if self.kyotaku < 9:
	        for i in range(34):
		        ret[self.kyotaku][i] = 1
	    else:
	        for i in range(34):
		        ret[9][i] = 1
	    return ret

    def to_numpy_dora(self):
        tmp = [0 for i in range(38)]
        for d in self.dora_marker:
            tmp[get_hai34(d)] += 1
        ret = np.zeros((4, 34), dtype=np.int)
        for hai in range(34):
            for i in range(tmp[hai]):
                ret[i][hai] = 1
        return ret

    def to_numpy(self, my_pid):
        # my_pid is 0,1,2,3
        ps = np.concatenate([self.player_state[(my_pid + i)%4].to_numpy(i == 0) for i in range(4)])
        #ps = np.concatenate([self.player_state[(my_pid + i)%4].to_numpy(True) for i in range(4)])
        ps2 = np.concatenate([ps, self.to_numpy_bakaze(), self.to_numpy_kyoku(), self.to_numpy_honba(), self.to_numpy_kyotaku(), self.to_numpy_dora()])
        return ps2

    def to_numpy_fuuro(self, my_pid, target_hai, consumed_hai):
        # my_pid is 0,1,2,3
        ps = np.concatenate([self.player_state[(my_pid + i)%4].to_numpy(i == 0) for i in range(4)])
        #ps = np.concatenate([self.player_state[(my_pid + i)%4].to_numpy(True) for i in range(4)])
        ret = np.zeros((4,34), dtype=np.int)
        tmp = [0 for i in range(34)]
        for c in consumed_hai:
            tmp[get_hai34(hai_str_to_int(c))] += 1
        ret[0][get_hai34(hai_str_to_int(target_hai))] = 1
        for hai in range(34):
            for i in range(tmp[hai]):
                ret[i+1][hai] = 1
        #print(ret)
        ps = np.concatenate([ps, ret])
        ps2 = np.concatenate([ps, self.to_numpy_bakaze(), self.to_numpy_kyoku(), self.to_numpy_honba(), self.to_numpy_kyotaku(), self.to_numpy_dora()])
        return ps2

    def to_numpy_kan(self, action_type, my_pid, consumed_hai):
        def get_kan_type():
            if action_type == "daiminkan":
                return 0
            elif action_type == "kakan":
                return 1
            elif action_type == "ankan":
                return 2
            else:
                assert False, "to_numpy_kan error"
                return -1
        # my_pid is 0,1,2,3
        ps = np.concatenate([self.player_state[(my_pid + i)%4].to_numpy(i == 0) for i in range(4)])
        #ps = np.concatenate([self.player_state[(my_pid + i)%4].to_numpy(True) for i in range(4)])
        ret = np.zeros((4,34), dtype=np.int)
        for i in range(4):
            ret[i][get_hai34(hai_str_to_int(consumed_hai[0]))] = 1
        #print(ret)
        kan_t = np.zeros((3,34), dtype=np.int)
        kan_type = get_kan_type()
        for i in range(34):
            kan_t[kan_type][i] = 1
        ps = np.concatenate([ps, ret, kan_t])
        ps2 = np.concatenate([ps, self.to_numpy_bakaze(), self.to_numpy_kyoku(), self.to_numpy_honba(), self.to_numpy_kyotaku(), self.to_numpy_dora()])
        return ps2

def get_game_state_start_kyoku(action_json_dict):
    assert action_json_dict["type"] == "start_kyoku", "get_game_state_start_kyoku_error"

    tehai_array = [[0 for j in range(38)] for i in range(4)]

    for i in range(3):
        for hai_str in action_json_dict["tehais"][i]:
            tehai_array[i][hai_str_to_int(hai_str)] += 1
    scores = action_json_dict["scores"] + [0]

    return Game_State(bakaze = kaze_str_to_int(action_json_dict["bakaze"]),
                      kyoku = action_json_dict["kyoku"],
                      honba = action_json_dict["honba"],
                      kyotaku = action_json_dict["kyotaku"],
                      scores = scores,
                      oya = action_json_dict["oya"],
                      dora_marker = hai_str_to_int(action_json_dict["dora_marker"]),
                      tehai_array = tehai_array)

INITIAL_START_KYOKU = '{ "type": "start_kyoku", "bakaze": "E", "kyoku": 1, "honba": 0, "kyotaku": 0, "scores": [35000, 35000, 35000, 0], "oya": 0, "dora_marker": "?", "tehais": [[], [], [], []] }'


#-- for ui ---#

def make_none(actor):
    d = {}
    d["type"] = "none"
    d["actor"] = actor
    return d

def make_dahai(actor, hai, tsumogiri):
    d = {}
    d["type"] = "dahai"
    d["actor"] = actor
    d["pai"] = hai_int_to_str(hai)
    d["tsumogiri"] = tsumogiri
    return d

def make_reach(actor):
    d = {}
    d["type"] = "reach"
    d["actor"] = actor
    return d

def make_chi(actor, target, hai, consumed):
    d = {}
    d["type"] = "chi"
    d["actor"] = actor
    d["target"] = target
    d["pai"] = hai_int_to_str(hai)
    d["consumed"] = [hai_int_to_str(consumed[0]), hai_int_to_str(consumed[1])]
    return d

def make_pon(actor, target, hai, consumed):
    d = {}
    d["type"] = "pon"
    d["actor"] = actor
    d["target"] = target
    d["pai"] = hai_int_to_str(hai)
    d["consumed"] = [hai_int_to_str(consumed[0]), hai_int_to_str(consumed[1])]
    return d

def make_pon_default(actor, target, hai):
    return make_pon(actor, target, hai, [haikind(hai), haikind(hai)])

def make_pon_aka(actor, target, hai):
    return make_pon(actor, target, hai, [haikind(hai), haikind(hai)+5])

def make_daiminkan(actor, target, hai, consumed):
    d = {}
    d["type"] = "daiminkan"
    d["actor"] = actor
    d["target"] = target
    d["pai"] = hai_int_to_str(hai)
    d["consumed"] = [hai_int_to_str(consumed[0]), hai_int_to_str(consumed[1]), hai_int_to_str(consumed[2])]
    return d

def make_daiminkan_default(actor, target, hai):
    return make_daiminkan(actor, target, hai, [haikind(hai), haikind(hai), haikind(hai)])

def make_daiminkan_aka(actor, target, hai):
    assert hai % 10 == 5 and hai < 30, "make_daiminkan_aka error"
    return make_daiminkan(actor, target, hai, [haikind(hai), haikind(hai), haikind(hai) + 5])

def make_ankan(actor, consumed):
    d = {}
    d["type"] = "ankan"
    d["actor"] = actor
    d["consumed"] = [hai_int_to_str(consumed[0]), hai_int_to_str(consumed[1]), hai_int_to_str(consumed[2]), hai_int_to_str(consumed[3])]
    return d

def make_ankan_default(actor, hai):
    return make_ankan(actor, [haikind(hai), haikind(hai), haikind(hai), haikind(hai)])

def make_ankan_aka(actor, hai):
    assert hai % 10 == 5 and hai < 30, "make_ankan_aka error"
    return make_ankan(actor, [haikind(hai), haikind(hai), haikind(hai), haikind(hai) + 5])

def make_kakan(actor, hai, consumed):
    d = {}
    d["type"] = "kakan"
    d["actor"] = actor
    d["pai"] = hai_int_to_str(hai)
    d["consumed"] = [hai_int_to_str(consumed[0]), hai_int_to_str(consumed[1]), hai_int_to_str(consumed[2])]
    return d

def make_kakan_default(actor, hai):
    return make_kakan(actor, hai, [haikind(hai), haikind(hai), haikind(hai)])

def make_kakan_aka(actor, hai):
    assert hai % 10 == 5 and hai < 30, "make_kakan_aka error"
    return make_kakan(actor, hai, [haikind(hai), haikind(hai), haikind(hai) + 5])

def make_hora(actor, target, hai):
    d = {}
    d["type"] = "hora"
    d["actor"] = actor
    d["target"] = target
    d["pai"] = hai_int_to_str(hai)
    return d

def make_kyushukyuhai(actor):
    d = {}
    d["type"] = "ryukyoku"
    d["reason"] = "kyushukyuhai"
    d["actor"] = actor
    return d

def mask_action(action_json, view_pid):
    ret = copy.deepcopy(action_json)
    if ret["type"] == "tsumo":
        if ret["actor"] != view_pid:
            ret["pai"] = "?"
    elif ret["type"] == "start_kyoku":
        for pid in range(4):
            if pid != view_pid:
                ret["tehais"][pid] = ["?" for i in range(13)]
    return ret

def field_label_str(game_state):
    ret = "bakaze:" + kaze_int_to_str(game_state.bakaze) + "  kyoku:" + str(game_state.kyoku) + "  honba:" + str(game_state.honba) + "\n"
    ret += "kyotaku:" + str(game_state.kyotaku) + "  remain:" + str(70-game_state.total_tsumo_num)
    return ret

def player_label_str(name, player_state):
    ret = name + "\n"
    ret += kaze_int_to_str(player_state.jikaze) + " "
    ret += str(player_state.score) + " "
    if player_state.reach_accepted:
        ret += "R"
    elif player_state.reach_declared:
        ret += "r"
    else:
        ret += " "
    return ret

def create_haiyama():
    haiyama = [i for i in range(136)]
    random.shuffle(haiyama)
    ret = [hai_int_to_str(get_hai38(i)) for i in haiyama]
    return ret