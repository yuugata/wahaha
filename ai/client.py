import json
import numpy as np
import torch
import torch.nn as nn
from .mjtypes import *
from .model import *
from mjlegal.mjai_player_loader import MjaiPlayerLoader
from mjlegal.mjai_possible_action import MjaiPossibleActionGenerator

class Client : 
    def setup(self) :
        self.models = {}
        self.model_paths = {}
        self.model_paths['dahai'] = 'model/dahai_model_cpu_state_dict.pth'
        # self.model_paths['reach'] = 'model/reach_model_cpu_state_dict.pth'
        # self.model_paths['chi'] = 'model/chi_model_cpu_state_dict.pth'
        # self.model_paths['pon'] = 'model/pon_model_cpu_state_dict.pth'
        # self.model_paths['kan'] = 'model/kan_model_cpu_state_dict.pth'
        # self.model_inchannels = {'reach': 560, 'chi': 564, 'pon': 564, 'ankan': 567, 'daiminkan': 567, 'kakan': 567}
        
        #self.models['dahai'] = DiscardNet(560, 256, 50)
        self.models['dahai'] = DiscardNet(560, 128, 15)
        self.models['dahai'].load_state_dict(torch.load(self.model_paths['dahai']))

        self.reset()

    def reset(self) :
        self.game_state = get_game_state_start_kyoku(json.loads(INITIAL_START_KYOKU))
        self.mjaiLoader = MjaiPlayerLoader()
        self.possibleActionGenerator = MjaiPossibleActionGenerator()

    def update_state(self, action) :
        self.mjaiLoader.action_receive(action)
        action_type = action["type"]

        # TODO: mjlegalがscoreをチェックしていないため、暫定的にclient.py側で取得する
        if "scores" in action :
            self.player_scores = action["scores"]

        if action_type == "start_game" :
            self.player_id = action["id"]
            self.player_scores = [35000, 35000, 35000]
        elif action_type == "start_kyoku":
            if "scores" not in action :
                action["scores"] = self.player_scores
            self.game_state = get_game_state_start_kyoku(action)
        else :
            self.game_state.go_next_state(action)
        self.last_action = action

    def get_feature(self, legal_actions) :
        dahai_legal_action = [legal_action for legal_action in legal_actions if (legal_action["type"] == "dahai") and legal_action["actor"] == self.player_id]
        dahai_feature = None
        if len(dahai_legal_action) > 0 :
            dahai_feature = self.game_state.to_numpy(self.player_id)

        return {
            "dahai" : dahai_feature
        }

    def get_legal_actions(self) :
        return self.possibleActionGenerator.possible_mjai_action(self.mjaiLoader.game,self.last_action)

    def can_dahai(self, legal_actions) :
        return any(legal_action["type"] == "dahai" for legal_action in legal_actions)

    def get_dahai_action(self, legal_actions, prob_discard) :
        dahai_actions = [legal_action for legal_action in legal_actions if legal_action["type"] == "dahai"]
        
        def action_prob(action) :
            hai34 = get_hai34(hai_str_to_int(action["pai"]))
            return prob_discard[hai34]
            
        return max(dahai_actions, key = action_prob)

    def forward_one(self, model, feature):
        model.eval()
        x = torch.from_numpy(feature.astype(np.float32)).clone()
        x = torch.unsqueeze(x, -1)
        x = torch.unsqueeze(x, 0)
        return nn.Softmax(dim=1)(model(x)).detach().numpy()[0]

    def choose_action_rule_base(self, legal_actions) :
        # 立直, 抜きドラ, 和了, 流局は必ず実施
        reach_action = None
        nukidora_action = None
        hora_action = None
        ryukyoku_action = None
        action = None
        for legal_action in legal_actions :
            action_type = legal_action["type"]
            if action_type == "hora" :
                hora_action = legal_action
            elif action_type == "reach" :
                reach_action = legal_action
            elif action_type == "nukidora" :
                nukidora_action = legal_action
            elif action_type == "ryukyoku" :
                ryukyoku_action = "ryukyoku"

        if hora_action is not None :
            action = hora_action
        elif reach_action is not None :
            action = reach_action
        elif ryukyoku_action is not None :
            action = ryukyoku_action
        elif nukidora_action is not None :
            action = nukidora_action

        return action

    def choose_action(self) :
        legal_actions = self.get_legal_actions()
        len_legal_actions = len(legal_actions)
        choosed_action = {"type" : "none"}

        action_rule_base = self.choose_action_rule_base(legal_actions)
        if action_rule_base is not None :
            choosed_action = action_rule_base
        elif len_legal_actions > 1 :
            if self.can_dahai(legal_actions) :
                feature = self.get_feature(legal_actions)
                prob_discard = self.forward_one(self.models['dahai'], feature["dahai"])
                choosed_action = self.get_dahai_action(legal_actions, prob_discard)
        elif len_legal_actions == 1 :
            choosed_action = legal_actions[0]

        return choosed_action

        

    