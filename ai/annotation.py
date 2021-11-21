import os
import pathlib
import glob
import subprocess
import json
import joblib

import numpy as np

from .mjtypes import *

from mjlegal.mjai import MjaiLoader
from mjlegal.possible_action import PossibleActionGenerator


def read_log_json(file_path):
    ret = []
    try:
        with open(file_path, encoding='utf-8') as f:
            l = f.readlines()
            for i in range(len(l)):
                ret.append(json.loads(l[i]))
    except UnicodeDecodeError as e:
        print('read_log_json: UnicodeDecodeError exception')
        with open(file_path, encoding='utf-8') as f:
            l = f.readlines()
            for i in range(len(l)):
                ret.append(json.loads(l[i]))
        
    return ret

def get_output_pathstr(input_logdir, file_name, output_npzdir, action_type):
    tmp_path = os.path.join(output_npzdir, action_type, file_name[len(input_logdir):].lstrip(os.sep))
    tmp_dir = os.path.dirname(tmp_path)
    tmp_name = os.path.splitext(os.path.basename(tmp_path))[0]
    return os.path.join(tmp_dir, action_type + '_' + tmp_name + '.npz')

class Data_Processor:
    def __init__(self):
        self.x_discard = []
        self.y_discard = []

        self.x_chi = []
        self.y_chi = []

        self.x_pon = []
        self.y_pon = []

        """
        self.x_daiminkan = []
        self.y_daiminkan = []

        self.x_kakan = []
        self.y_kakan = []

        self.x_ankan = []
        self.y_ankan = []
        """

        self.x_kan = []
        self.y_kan = []

        self.x_reach = []
        self.y_reach = []

    def get_legal_moves(self, current_record):
        cmd = "./system.exe legal_action "
        input_json = {}
        input_json["record"] = current_record
        cmd += json.dumps(input_json, separators=(',', ':'))
        c = subprocess.check_output(cmd.split()).decode('utf-8').rstrip()
        return json.loads(c)

    def process_record(self, game_record, legal_actions_all):
        game_state = get_game_state_start_kyoku(json.loads(INITIAL_START_KYOKU))
        for i, action in enumerate(game_record):
            if action["type"] == "start_kyoku":
                game_state = get_game_state_start_kyoku(action)
            else:
                game_state.go_next_state(action)
            if action["type"] == "tsumo" or action["type"] == "chi" or action["type"] == "pon":
                if game_record[i+1]["type"] == "dahai" or game_record[i+1]["type"] == "reach":
                    x = game_state.to_numpy(action["actor"])
                    self.x_discard.append(x)

                    y = np.zeros(34, dtype=np.int)
                    i_dahai = i+1 if game_record[i+1]["type"] == "dahai" else i+2
                    hai = hai_str_to_int(game_record[i_dahai]["pai"])
                    y[get_hai34(hai)] = 1
                    self.y_discard.append(y)
            
            if action["type"] == "tsumo" or action["type"] == "dahai":
                for legal_action in legal_actions_all[i]:
                    if legal_action["type"] == "chi":
                        if ((game_record[i+1]["type"] == "hora" and game_record[i+1]["actor"] != legal_action["actor"]) or
                            (game_record[i+1]["type"] == "pon" and game_record[i+1]["actor"] != legal_action["actor"]) or
                            (game_record[i+1]["type"] == "daiminkan" and game_record[i+1]["actor"] != legal_action["actor"])):
                            continue
                        #x = game_state.to_numpy(legal_action["actor"])
                        x = game_state.to_numpy_fuuro(legal_action["actor"], legal_action["pai"], legal_action["consumed"])
                        self.x_chi.append(x)
                        self.y_chi.append(np.array([1,0]) if legal_action == game_record[i+1] else np.array([0,1]))
                    if legal_action["type"] == "pon":
                        if game_record[i+1]["type"] == "hora" and game_record[i+1]["actor"] != legal_action["actor"]:
                            continue
                        #x = game_state.to_numpy(legal_action["actor"])
                        x = game_state.to_numpy_fuuro(legal_action["actor"], legal_action["pai"], legal_action["consumed"])
                        self.x_pon.append(x)
                        self.y_pon.append(np.array([1,0]) if legal_action == game_record[i+1] else np.array([0,1]))
                    """
                    if legal_action["type"] == "daiminkan":
                        if game_record[i+1]["type"] == "hora" and game_record[i+1]["actor"] != legal_action["actor"]:
                            continue
                        #x = game_state.to_numpy(legal_action["actor"])
                        x = game_state.to_numpy_fuuro(legal_action["actor"], legal_action["pai"], legal_action["consumed"])
                        self.x_daiminkan.append(x)
                        self.y_daiminkan.append(np.array([1,0]) if legal_action == game_record[i+1] else np.array([0,1]))
                    if legal_action["type"] == "kakan":
                        #x = game_state.to_numpy(legal_action["actor"])
                        x = game_state.to_numpy_fuuro(legal_action["actor"], legal_action["pai"], legal_action["consumed"])
                        self.x_kakan.append(x)
                        self.y_kakan.append(np.array([1,0]) if legal_action == game_record[i+1] else np.array([0,1]))
                    if legal_action["type"] == "ankan":
                        #x = game_state.to_numpy(legal_action["actor"])
                        x = game_state.to_numpy_kan(legal_action["actor"], legal_action["consumed"])
                        self.x_ankan.append(x)
                        self.y_ankan.append(np.array([1,0]) if legal_action == game_record[i+1] else np.array([0,1]))
                    """
                    if legal_action["type"] == "reach":
                        x = game_state.to_numpy(legal_action["actor"])
                        self.x_reach.append(x)
                        self.y_reach.append(np.array([1,0]) if legal_action == game_record[i+1] else np.array([0,1]))
                    if  legal_action["type"] == "kakan" or legal_action["type"] == "ankan" or legal_action["type"] == "daiminkan":
                        x = game_state.to_numpy_kan(legal_action["type"], legal_action["actor"], legal_action["consumed"])
                        self.x_kan.append(x)
                        self.y_kan.append(np.array([1,0]) if legal_action == game_record[i+1] else np.array([0,1]))

    def dump_child(self, input_logdir, file_name, output_npzdir, action_type, X, Y):
        if 0 < len(Y):
            output_pathstr = get_output_pathstr(input_logdir, file_name, output_npzdir, action_type)
            # try_mkdir(os.path.dirname(output_pathstr))
            np.savez_compressed(output_pathstr, X, Y)
            X.clear()
            Y.clear()

    def dump(self, input_logdir, file_name, output_npzdir):
        self.dump_child(input_logdir, file_name, output_npzdir, "discard", self.x_discard, self.y_discard)
        self.dump_child(input_logdir, file_name, output_npzdir, "chi", self.x_chi, self.y_chi)
        self.dump_child(input_logdir, file_name, output_npzdir, "pon", self.x_pon, self.y_pon)
        self.dump_child(input_logdir, file_name, output_npzdir, "kan", self.x_kan, self.y_kan)
        self.dump_child(input_logdir, file_name, output_npzdir, "reach", self.x_reach, self.y_reach)

def legal_action_log_all(records) :
    legal_actions = []
    mjaiLoader = MjaiLoader()
    possibleActionGenerator = PossibleActionGenerator()
    for record in records :
        if record["type"] in ("end_game") : # なんかエラーが出る対策。将来的にはmjlegalを修正したい.
            continue

        mjaiLoader.action(record)

        # vvv for debug vvv
        # print("action:", record)
        # for i, player_state in enumerate(mjaiLoader.game.player_states) :
        #      print(i, player_state.dump())
        # ^^^ for debug ^^^
        
        actions = possibleActionGenerator.possible_game_actions(mjaiLoader.game)
        mjai_actions = [action.to_mjai_json() for action in actions]
        legal_actions.append(mjai_actions)
    return legal_actions

# def proc_mjailog(input_logdir, file_name, output_npzdir):
#     dp = Data_Processor()
#     game_record = read_log_json(file_name)
#     cmd = "./system.exe legal_action_log_all " + file_name
#     c = subprocess.check_output(cmd.split()).decode('utf-8').rstrip()
#     legal_actions_all = json.loads(c)
#     try:
#         dp.process_record(game_record, legal_actions_all)
#         dp.dump(input_logdir, file_name, output_npzdir)
#     except AssertionError as e:
#         print('proc_mjailog AssertionError:', e)

# def proc_batch_mjailog(input_logdir, input_regex, output_npzdir, update):
#     file_list = sorted(glob.glob(os.path.join(input_logdir, input_regex)))

#     def loop_func(file_name):
#         if not update:
#             discard_path = get_output_pathstr(input_logdir, file_name, output_npzdir, 'discard')
#             if pathlib.Path(discard_path).is_file():
#                 return
            
#         print("process:", file_name)
#         proc_mjailog(input_logdir, file_name, output_npzdir)

#     joblib.Parallel(n_jobs=6)(joblib.delayed(loop_func)(file_name) for file_name in file_list)

def get_current_feature(current_record, legal_actions):
    print("current_record",current_record)
    if len(current_record) == 0:
        return None

    print(legal_actions)
    if legal_actions is None:
        # cmd = "./system.exe legal_action " + json.dumps({'record': current_record}, separators=(',', ':'))
        # legal_actions = subprocess.check_output(cmd.split()).decode('utf-8').rstrip()
        # legal_actions = json.loads(legal_actions)
        legal_actions = legal_action_log_all(current_record)
        print("legal action num", len(legal_actions))

    features = [{"others": []} for i in range(4)]
    game_state = get_game_state_start_kyoku(json.loads(INITIAL_START_KYOKU))
    for action in current_record:
        if action["type"] == "start_kyoku":
            game_state = get_game_state_start_kyoku(action)
        else:
            game_state.go_next_state(action)

    last_action = current_record[-1]
    if last_action["type"] in ["tsumo", "chi", "pon", "reach"]:
        features[last_action["actor"]]["dahai"] = game_state.to_numpy(action["actor"])

    for legal_action in legal_actions:
        if legal_action["type"] in ["chi", "pon"]:
            x = game_state.to_numpy_fuuro(legal_action["actor"], legal_action["pai"], legal_action["consumed"])
            features[legal_action["actor"]]["others"].append((legal_action, x))
        elif legal_action["type"] == "reach":
            features[legal_action["actor"]]["reach"] = game_state.to_numpy(legal_action["actor"])
        elif legal_action["type"] in ["kakan", "ankan", "daiminkan"]:
            x = game_state.to_numpy_kan(legal_action["type"], legal_action["actor"], legal_action["consumed"])
            features[legal_action["actor"]]["others"].append((legal_action, x))
    return legal_actions, features
    