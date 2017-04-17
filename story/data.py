import codecs
import json
import os
import sys

from .translation import DEFAULT_LANGUAGE, activate, add_localedir


class DataManager(object):

    filename = os.path.expanduser('~/.pyschool')
    _data = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.activate_language()
        # Load story translations
        module = sys.modules[self.__class__.__module__.split('.')[0]]
        for path in module.__path__:
            add_localedir(path)

    def load(self):
        if self._data is None:
            filename = self.filename
            if not os.path.exists(filename):
                self._data = {}
            else:
                try:
                    with codecs.open(filename, encoding='utf8') as f:
                        self._data = json.loads(f.read())
                except:
                    # TODO: Add error handling
                    self._data = {}
        return self._data

    def save(self):
        with codecs.open(self.filename, 'w+', encoding='utf8') as f:
            f.write(json.dumps(self._data))

    def set_data(self, value):
        data = self.load()
        data[self.name] = value
        self.save()

    def get_data(self):
        data = self.load()
        if self.name not in data:
            data[self.name] = {}
        return data[self.name]

    data = property(get_data, set_data)

    def set_language(self, language):
        self.data['language'] = language
        self.save()
        self.activate_language()

    def get_language(self):
        return self.data.get('language', DEFAULT_LANGUAGE)

    language = property(get_language, set_language)

    def activate_language(self):
        activate(self.language)

    def set_current(self, current):
        self.data['current'] = current
        self.save()

    def get_current(self):
        return self.data.get('current', None)

    current = property(get_current, set_current)

    def set_completed(self, value):
        if isinstance(value, str):
            completed = self.completed
            if value not in completed:
                completed.append(value)
        else:
            completed = value
        self.data['completed'] = completed
        self.save()

    def get_completed(self):
        return self.data.get('completed', [])

    completed = property(get_completed, set_completed)
