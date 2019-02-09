# -*- coding: utf-8 -*-
import json
import logging
import os

logger = logging.getLogger(__name__)


class JSONStorage:
    def __init__(self, data_file):
        self.data_file = data_file
        self._data = {}
        self.__load(data_file)

    def __load(self, directory):
        """
        loads messages into memory from slack exported data
        """
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                self._data = json.loads(f.read())
        else:
            self._data = {}

    def get(self, cached=False):
        if not cached:
            self.__load(self.data_file)
        return self._data

    def save(self, data):
        self._data = data
        with open(self.data_file, 'w') as f:
            f.write(json.dumps(self._data))

    def get_messages(self):
        # todo remove
        return self._data

    def save_messages(self, messages):
        self._data += messages
        self.save(self._data)

