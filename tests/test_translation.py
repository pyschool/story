"""
Simple Test for translations

Author: Ignacio Avas <iavas@sophilabs.com>
"""
from story.translation import gettext, activate


class TestStory(object):

    def test_english_translation(self):
        activate('en')
        translation = gettext("Choose language")
        assert translation == "Choose language"

    def test_spanish_translation(self):
        activate('es')
        translation = gettext("Choose language")
        assert translation == "Elige un idioma"
