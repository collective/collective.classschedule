from collective.classschedule import _
from plone import api
from plone.dexterity.content import Container
from plone.supermodel import model
from zope.globalrequest import getRequest
from zope.interface import implementer
from zope.interface import Invalid
from zope.interface import invariant
from zope.schema import Date


class IAcademicCalendar(model.Schema):
    """Marker interface and Dexterity Python Schema for AcademicCalendar"""

    start = Date(title=_("label_period_start", default="Start"))
    end = Date(title=_("label_period_end", default="End"))

    @invariant
    def validate_start_end(data):
        if (data.start is not None and data.end is not None) and (
            data.start > data.end
        ):
            raise Invalid(
                _("The end time must be greater tha start time. Please correct it.")
            )

    @invariant
    def validate_name(data):
        request = getRequest()
        current_period_name = request.form["form.widgets.IBasic.title"]
        if data.__context__:  # The object alredy exists
            current_period_uid = api.content.get_uuid(data.__context__)
            for brain in api.content.find(portal_type="AcademicCalendar"):
                academic_period = brain.getObject()
                if (
                    current_period_uid != api.content.get_uuid(academic_period)
                    and current_period_name == academic_period.Title()
                ):
                    raise Invalid(_("The name of the period have been alredy used"))
        else:
            for brain in api.content.find(portal_type="AcademicCalendar"):
                academic_period = brain.getObject()
                if current_period_name == academic_period.Title():
                    raise Invalid(_("The name of the period have been alredy used"))


@implementer(IAcademicCalendar)
class AcademicCalendar(Container):
    """Content-type class for IAcademicCalendar"""
