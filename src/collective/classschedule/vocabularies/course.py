from collective.classschedule import _
from zope.interface import provider
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary


@provider(IVocabularyFactory)
def DaysVocabularyFactory(context):
    """Vocabulary for indicate features."""

    return SimpleVocabulary([
        SimpleVocabulary.createTerm("monday", "monday", _("Monday")),
        SimpleVocabulary.createTerm("tuesday", "tuesday", _("Tuesday")),
        SimpleVocabulary.createTerm("wednesday", "wednesday", _("Wednesday")),
        SimpleVocabulary.createTerm("thursday", "thursday", _("Thursday")),
        SimpleVocabulary.createTerm("friday", "friday", _("Friday")),
        SimpleVocabulary.createTerm("saturday", "saturday", _("Saturday")),
        SimpleVocabulary.createTerm("sunday", "sunday", _("Sunday")),
    ])
