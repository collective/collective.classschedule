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


class IRowProfessorSchema(Interface):
    fullname = schema.TextLine(
        title=_("label_fullname", default="Fullname"),
        required=False,
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
