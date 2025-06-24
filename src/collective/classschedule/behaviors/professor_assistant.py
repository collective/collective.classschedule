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



class IRowProfessorAssistantSchema(Interface):
    fullname = schema.TextLine(
        title=_("label_fullname", default="Fullname"),
        required=False,
    )


class IProfessorAssistantMarker(Interface):
    pass


@provider(IFormFieldProvider)
class IProfessorAssistant(model.Schema):
    """ """

    directives.widget(
        "professor_assistants",
        DataGridFieldFactory,
        auto_append=False,
        allow_reorder=True,
    )

    professor_assistants = schema.List(
        title=_("label_professor_assistants", default="Professor Assistants"),
        value_type=DictRow(title="Table", schema=IRowProfessorAssistantSchema),
        required=False,
    )

class ProfessorAssitantsRowsValidator(validator.SimpleFieldValidator):
    """z3c.form validator class for datagrid professors assitants
    """

    def validate(self, value):
        """Validate empty rows
        """
        super(ProfessorAssitantsRowsValidator, self).validate(value)
        
        if value != [{'fullname': None}]:
            for row in value:
                if not (row["fullname"]):
                    raise Invalid(_('The fullname is required. Please correct it.'))

validator.WidgetValidatorDiscriminators(
    ProfessorAssitantsRowsValidator,
    field=IProfessorAssistant['professor_assistants']
)
zope.component.provideAdapter(ProfessorAssitantsRowsValidator)


@implementer(IProfessorAssistant)
@adapter(IProfessorAssistantMarker)
class ProfessorAssistant:
    def __init__(self, context):
        self.context = context

    @property
    def professor_assistants(self):
        if safe_hasattr(self.context, "professor_assistants"):
            return self.context.professor_assistants
        return None

    @professor_assistants.setter
    def professor_assistants(self, value):
        self.context.professor_assistants = value
