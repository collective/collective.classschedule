from collective.classschedule import _
from collective.z3cform.datagridfield.datagridfield import DataGridFieldFactory
from collective.z3cform.datagridfield.row import DictRow
from plone import schema
from plone.autoform import directives
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from Products.CMFPlone.utils import safe_hasattr
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface
from zope.interface import provider
from z3c.form import validator
from zope.interface import Invalid
import zope.component

from z3c.form.browser.checkbox import CheckBoxFieldWidget
from z3c.relationfield.schema import RelationChoice
from plone.app.z3cform.widget import SelectFieldWidget
from zope.interface import invariant



class IRowProfessorSchema(Interface):
    fullname = schema.TextLine(
        title=_("label_fullname", default="Fullname"),
        required=False,
    )
    directives.widget(days=CheckBoxFieldWidget)
    days = schema.List(
        title=_("label_days", default="Days"),
        value_type=schema.Choice(
            vocabulary="collective.classschedule.DaysVocabulary",
        ),
        required=False,
    )

    start_time = schema.Time(
        title=_("label_start_time", default="Start Time"),
        required=False,
    )

    end_time = schema.Time(
        title=_("label_end_time", default="End Time"),
        required=False,
    )

    directives.widget(
        "location_room",
        SelectFieldWidget,
    )
    location_room = RelationChoice(
        title=_("label_location_room", default="Room"),
        vocabulary="collective.classschedule.RoomVocabulary",
        required=False,
        missing_value='',
    )


class IProfessorMarker(Interface):
    pass


@provider(IFormFieldProvider)
class IProfessor(model.Schema):
    """ """

    directives.widget(
        "professors",
        DataGridFieldFactory,
        auto_append=False,
        allow_reorder=True,
    )

    professors = schema.List(
        title=_("label_professors", default="Professors"),
        value_type=DictRow(title="Table", schema=IRowProfessorSchema),
        required=True,
    )


class ProfessorRowsValidator(validator.SimpleFieldValidator):
    """z3c.form validator class for datagrid professors
    """

    def validate(self, value):
        """Validate the Required and empty rows
        """
    
        if not(value):
            raise Invalid(_('At least one professor is required. Please correct it.'))
        
        for row in value:
            if not (row["fullname"]):
                raise Invalid(_('The fullname is required. Please correct it.'))
            
            if not (row["days"]):
                raise Invalid(_('At least one day is required. Please correct it.'))
            
            if not(row["start_time"]):
                raise Invalid(_('The start time is required. Please correct it.'))
            
            if not(row["end_time"]):
                raise Invalid(_('The end time is required. Please correct it.'))
            
            if row["start_time"] > row["end_time"]:
                raise Invalid(_('The end time must be greater tha start time. Please correct it.'))
            
            if not(row["location_room"]):
                raise Invalid(_('The room is required. Please correct it.'))

            

validator.WidgetValidatorDiscriminators(
    ProfessorRowsValidator,
    field=IProfessor['professors']
)
zope.component.provideAdapter(ProfessorRowsValidator)


@implementer(IProfessor)
@adapter(IProfessorMarker)
class Professor:
    def __init__(self, context):
        self.context = context
        

    @property
    def professors(self):
        if safe_hasattr(self.context, "professors"):
            return self.context.professors
        return None

    @professors.setter
    def professors(self, value):
        self.context.professors = value
