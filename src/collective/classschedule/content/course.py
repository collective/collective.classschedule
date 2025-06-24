from collective.classschedule import _
from plone.app.textfield import RichText
from plone.app.z3cform.widget import SelectFieldWidget
from plone.autoform import directives
from plone.dexterity.content import Item

# from plone.namedfile import field as namedfile
from plone.supermodel import model
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from z3c.relationfield.schema import RelationChoice

# from plone.supermodel.directives import fieldset
# from z3c.form.browser.radio import RadioFieldWidget
from zope import schema
from zope.interface import implementer
from zope.interface import Invalid
from zope.interface import invariant


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

    group = schema.TextLine(
        title=_("label_group", default="Group"),
        required=True,
    )

    directives.widget(days=CheckBoxFieldWidget)
    days = schema.List(
        title=_("label_days", default="Days"),
        value_type=schema.Choice(
            vocabulary="collective.classschedule.DaysVocabulary",
        ),
        required=True,
    )

    start_time = schema.Time(
        title=_("label_start_time", default="Start Time"),
        required=True,
    )

    end_time = schema.Time(
        title=_("label_end_time", default="End Time"),
        required=False,
    )

    presentation = RichText(
        title=_("label_presentation", default="Presentation"),
        required=False,
        default_mime_type="text/html",
        allowed_mime_types=(
            "text/html",
            "text/plain",
        ),
    )

    directives.order_after(location_room="*")
    directives.order_after(group="location_room")
    directives.order_after(days="group")
    directives.order_after(start_time="days")
    directives.order_after(end_time="start_time")
    directives.order_after(presentation="end_time")

    @invariant
    def validate_time(data):
        if data.end_time and data.start_time > data.end_time:
            raise Invalid(_('The end time must be greater tha start time. Please correct it.'))
    

@implementer(ICourse)
class Course(Item):
    """Content-type class for ICourse"""
