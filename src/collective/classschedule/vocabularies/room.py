from zope.interface import provider
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary


@provider(IVocabularyFactory)
def FeaturesVocabularyFactory(context):
    """Vocabulary for indicate features."""

    return SimpleVocabulary([
        SimpleVocabulary.createTerm("chalk_board", "chalk_board", "Chalk board"),
        SimpleVocabulary.createTerm("white_board", "white_board", "White board"),
        SimpleVocabulary.createTerm("projector", "projector", "Projector"),
    ])
