import os
from threading import local
import gettext as gettext_module

from .utils import lazy


_localedirs = []
_translations = {}
_active = local()
_default = None

DEFAULT_LANGUAGE = 'en'


class Translations(gettext_module.GNUTranslations):
    """
    GNUTranslations using many locale directories

    This translation object will be constructed out of multiple GNUTranslations
    objects by merging their catalogs. It will construct an object for the
    requested language and add a fallback to the default language, if it's
    different from the requested language.
    """

    domain = 'pyschool'

    def __init__(self, language):
        super().__init__()

        self.language = language
        self._catalog = None
        # If a language doesn't have a catalog, use the Germanic default for
        # pluralization: anything except one is pluralized.
        self.plural = lambda n: int(n != 1)

        self._init_translation_catalog()

        for localedir in _localedirs:
            translation = self._new_gnu_trans(localedir)
            self.merge(translation)

    def __repr__(self):
        return '<Translations lang:%s>' % self.language

    def _new_gnu_trans(self, localedir, use_null_fallback=True):
        """
        Return a mergeable gettext.GNUTranslations instance.

        A convenience wrapper. By default gettext uses 'fallback=False'.
        Using param `use_null_fallback` to avoid confusion with any other
        references to 'fallback'.
        """
        use_null_fallback = False
        return gettext_module.translation(
            domain=self.domain,
            localedir=localedir,
            languages=[self.language],
            codeset='utf-8',
            fallback=use_null_fallback)

    def _init_translation_catalog(self):
        """Create a base catalog using global translations."""
        localedir = os.path.join(os.path.dirname(__file__), 'locale')
        translation = self._new_gnu_trans(localedir)
        self.merge(translation)

    def add_localedir_translations(self, localedir):
        """Merge translations from localedir."""
        if os.path.exists(localedir):
            translation = self._new_gnu_trans(localedir)
            self.merge(translation)

    def merge(self, other):
        """Merge another translation into this catalog."""
        if not getattr(other, '_catalog', None):
            return  # NullTranslations() has no _catalog
        if self._catalog is None:
            # Take plural and _info from first catalog found
            self.plural = other.plural
            self._info = other._info.copy()
            self._catalog = other._catalog.copy()
        else:
            self._catalog.update(other._catalog)


def translation(language):
    """
    Return a translation object in the default 'django' domain.
    """
    global _translations
    if language not in _translations:
        _translations[language] = Translations(language)
    return _translations[language]


def activate(language):
    """
    Fetch the translation object for a given language and install it as the
    current translation object for the current thread.
    """
    if not language:
        return
    _active.value = translation(language)


def deactivate():
    """
    Uninstall the active translation object so that further _() calls resolve
    to the default translation object.
    """
    if hasattr(_active, 'value'):
        del _active.value


def get_language():
    """Return the currently selected language."""
    t = getattr(_active, 'value', None)
    if t is not None:
        try:
            return t.language
        except AttributeError:
            pass
    return DEFAULT_LANGUAGE


def add_localedir(localedir):
    global _translations
    global _localedirs
    if localedir not in _localedirs:
        _localedirs.append(localedir)
        for translation in _translations.values():
            translation.add_localedir_translations(localedir)


def gettext(message):
    """
    Translate the 'message' string. It uses the current thread to find the
    translation object to use. If no current translation is activated, the
    message will be run through the default translation object.
    """
    global _default
    _default = _default or translation(DEFAULT_LANGUAGE)
    translation_object = getattr(_active, 'value', _default)
    result = translation_object.gettext(message)
    return result


gettext = lazy(gettext, str)


LANGUAGES = [
    ('en', gettext('English')),
    ('es', gettext('Spanish'))
]
