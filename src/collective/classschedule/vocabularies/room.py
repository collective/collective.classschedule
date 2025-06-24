from collective.classschedule import _
from plone import api
from zope.interface import provider
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


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
        obj = brain.getObject()
        titleroom = f"{brain.Title} ({obj.aq_parent.title})"        
        terms.append(
            SimpleTerm(
                value=obj,
                token=brain.UID,
                title=titleroom,
            )
        )
    return SimpleVocabulary(terms)
