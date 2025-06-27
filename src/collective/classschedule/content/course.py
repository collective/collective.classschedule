from collective.classschedule import _
from plone.app.textfield import RichText
from plone.autoform import directives
from plone.dexterity.content import Item
from plone.portlets.interfaces import ILocalPortletAssignmentManager
from plone.portlets.interfaces import IPortletManager

# from plone.namedfile import field as namedfile
from plone.supermodel import model

# from plone.supermodel.directives import fieldset
# from z3c.form.browser.radio import RadioFieldWidget
from zope.component import getMultiAdapter
from zope.component import queryUtility
from zope.interface import implementer


class ICourse(model.Schema):
    """Marker interface and Dexterity Python Schema for Course"""

    presentation = RichText(
        title=_("label_presentation", default="Presentation"),
        required=False,
        default_mime_type="text/html",
        allowed_mime_types=(
            "text/html",
            "text/plain",
        ),
    )

    directives.order_after(presentation="*")


@implementer(ICourse)
class Course(Item):
    """Content-type class for ICourse"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Block all right column portlets by default
        manager = queryUtility(IPortletManager, name="plone.leftcolumn")
        if manager is not None:
            assignable = getMultiAdapter(
                (self, manager), ILocalPortletAssignmentManager
            )
            assignable.setBlacklistStatus("context", True)
