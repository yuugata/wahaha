import unittest
import json

# from mjlegal.mjai import MjaiLoader
from mjlegal.mjai_player_loader import MjaiPlayerLoader
# from mjlegal.possible_action import PossibleActionGenerator
from mjlegal.mjai_possible_action import MjaiPossibleActionGenerator

from ai.client import *

SERVER_TO_CLIENT = 0
CLIENT_TO_SERVER = 1
DIRECT_DICT = {'<-' : SERVER_TO_CLIENT, '->' : CLIENT_TO_SERVER}

def load_mjai_records(filename) :
    records = []
    log_input_file = open(filename, 'r', encoding="utf-8")
    for line in log_input_file :
        mjai_ev = json.loads(line)
        records.append(mjai_ev)
    log_input_file.close()
    return records

def load_mjai_player_records(filename) :
    records = []
    log_input_file = open(filename, 'r', encoding="utf-8")
    for line in log_input_file :
        tokens = line.split('\t')
        direction_str = tokens[0]
        if direction_str in DIRECT_DICT :
            mjai_str = tokens[1]
            mjai_ev = json.loads(mjai_str)
            record = {'direction' : DIRECT_DICT[direction_str], 'record' : mjai_ev}
            records.append(record)
    log_input_file.close()
    return records

def equal_mjai_action(action1, action2) :
    return all(action1[key] == action2[key] for key in action1)

def test_mjai_load(log_filename) :
    records = load_mjai_records(log_filename)
    for i in range(len(records)) :
        pass

def test_mjai_player_records(filename) :
    records = load_mjai_player_records(filename)
    # mjaiPlayerLoader = MjaiPlayerLoader()
    # mjaiPossibleActionGenerator = MjaiPossibleActionGenerator()
    # mjaiPossibleActionGenerator.name = 'Manue1'
    # possible_actions = None
    # previous_receive_action = None
    
    client = Client()
    client.setup()
    client.reset()
    
    for record in records :
        direction = record['direction']
        ev = record['record']
        if direction == SERVER_TO_CLIENT :
            client.update_state(ev)
        elif direction == CLIENT_TO_SERVER :
            client.choose_action()
        else :
            self.fail('Invalid mjai player record..')

class TestMjaiLoader(unittest.TestCase) :
    def test_mjai_load_0(self) :
        test_mjai_load('./test/test_data/test_mjson_0.mjson')
        # pdb.run("test_mjai_load('./test/test_data/test_mjson_0.mjson')")

    def test_player_mjai_log_load_0(self) :
        test_mjai_player_records('./test/test_data/test_mjai_player_log_01.txt')
