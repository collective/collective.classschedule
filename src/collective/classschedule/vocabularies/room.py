from collective.classschedule import _
from zope.interface import provider
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary
from zope.interface import implementer
from plone.dexterity.content import DexterityContent
from plone import api
from zope.schema.vocabulary import SimpleTerm


@provider(IVocabularyFactory)
def FeaturesVocabularyFactory(context):
    """Vocabulary for indicate features."""

    return SimpleVocabulary([
        SimpleVocabulary.createTerm("chalk_board", "chalk_board", _("Chalk board")),
        SimpleVocabulary.createTerm("white_board", "white_board", _("White board")),
        SimpleVocabulary.createTerm("projector", "projector", _("Projector")),
    ])


@provider(IVocabularyFactory)
def RoomVocabularyFactory(context):
    """Vocabulary."""

    terms = []
    for brain in api.content.find(
        portal_type="Room", 
    ):
        terms.append(
            SimpleTerm(
                value=brain.getObject(),
                token=brain.UID,
                title=brain.Title,
            )
        )
    return SimpleVocabulary(terms)
