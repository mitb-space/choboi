# -*- coding: utf-8 -*-
import json
import logging

logger = logging.getLogger(__name__)


class JSONStorage:
    def __init__(self, data_file):
        self.data_file = data_file
        self._messages = []
        self.__load(data_file)

    def __load(self, directory):
        """
        loads messages into memory from slack exported data
        """
        with open(self.data_file, 'r') as f:
            self._messages = json.loads(f.read())

    def get_messages(self):
        return self._messages

    def save_messages(self, messages):
        self._messages += messages
        with open(self.data_file, 'w') as f:
            f.write(json.dumps(self._messages))
