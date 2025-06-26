from collective.classschedule import _
from plone.autoform import directives
from plone.dexterity.content import Item
from plone.portlets.interfaces import ILocalPortletAssignmentManager
from plone.portlets.interfaces import IPortletManager
from plone.supermodel import model
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from zope import schema
from zope.component import getMultiAdapter
from zope.component import queryUtility
from zope.interface import implementer


class IRoom(model.Schema):
    """Marker interface and Dexterity Python Schema for Room"""

    floor = schema.TextLine(
        title=_("label_floor", default="Floor Name"),
        required=False,
    )

    nplaces = schema.Int(
        title=_("label_nplaces", default="Number of places"),
        # description=_("help_nplaces", default="",),
        required=True,
        min=3,
        max=300,
    )

    directives.widget(features=CheckBoxFieldWidget)
    features = schema.List(
        title=_("label_features", default="Features"),
        value_type=schema.Choice(
            vocabulary="collective.classschedule.FeaturesVocabulary",
        ),
        required=False,
    )


@implementer(IRoom)
class Room(Item):
    """Content-type class for IRoom"""

    def __init__(self, id=None, **kwargs):
        super().__init__(id, **kwargs)

        # Block all right column portlets by default
        manager = queryUtility(IPortletManager, name="plone.leftcolumn")
        if manager is not None:
            assignable = getMultiAdapter(
                (self, manager), ILocalPortletAssignmentManager
            )
            assignable.setBlacklistStatus("context", True)
