from zope.schema.vocabulary import SimpleVocabulary


import pytest

class TestVocab:
    name = "collective.classschedule.DaysVocabulary"

    @pytest.fixture(autouse=True)
    def _setup(self, portal, get_vocabulary):
        self.vocab = get_vocabulary(self.name, portal)

    def test_vocabulary_type(self):
        assert isinstance(self.vocab, SimpleVocabulary)

    @pytest.mark.parametrize(
        "token,title",
        [
            ('monday', 'Monday'),
            ('sunday', 'Sunday')
        ]
    )
    def test_vocab_terms(self, token: str, title: str):
        term = self.vocab.getTermByToken(token)
        assert term.title == title
