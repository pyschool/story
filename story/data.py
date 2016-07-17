import codecs
import json
import os
import gettext


domain = 'story'
localedir = os.path.join(os.path.dirname(__file__), 'locale/')
gettext.bindtextdomain(domain, localedir)
translation = gettext.translation(domain, localedir, fallback=True)
_ = lambda msg: gettext.dgettext(domain, msg)


def set_language(language):
    os.environ['LANG'] = str(language)


class DataManager(object):

    filename = os.path.expanduser('~/.pyschool')
    _data = None

    def __init__(self, *args, **kwargs):
        set_language(self.language)
        super().__init__(*args, **kwargs)

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
        set_language(self.language)

    def get_language(self):
        return self.data.get('language', self.default_language)

    language = property(get_language, set_language)

    def set_current(self, language):
        set_language(language)
        self.data['current'] = language
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
