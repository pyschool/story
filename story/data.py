import codecs
import json
import os
import getpass


class DataManager(object):

    filename = '.pyschool'
    _data = None

    def get_filename(self):
        return os.path.join('/home/', getpass.getuser(), self.filename)

    def load(self):
        if self._data is None:
            filename = self.get_filename()
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
        with codecs.open(self.get_filename(), 'w+', encoding='utf8') as f:
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

    def set_language(self, value):
        self.data['language'] = value
        self.save()

    def get_language(self):
        return self.data.get('language', self.default_language)

    language = property(get_language, set_language)

    def set_current(self, value):
        self.data['current'] = value
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
