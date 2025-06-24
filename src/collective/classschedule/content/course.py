# from plone.app.textfield import RichText
from collective.classschedule import _
from plone.app.z3cform.widget import SelectFieldWidget
from plone.autoform import directives
from plone.dexterity.content import Item

# from plone.namedfile import field as namedfile
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice

# from plone.supermodel.directives import fieldset
# from z3c.form.browser.radio import RadioFieldWidget
# from zope import schema
from zope.interface import implementer


class ICourse(model.Schema):
    """Marker interface and Dexterity Python Schema for Course"""

    directives.widget(
        "location_room",
        SelectFieldWidget,
    )
    location_room = RelationChoice(
        title=_("label_location_room", default="Room"),
        vocabulary="collective.classschedule.RoomVocabulary",
        required=True,
    )


@implementer(ICourse)
class Course(Item):
    """Content-type class for ICourse"""
