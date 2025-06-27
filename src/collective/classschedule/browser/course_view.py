from collective.classschedule import _
from plone import api
from plone.autoform.view import WidgetsView
from plone.dexterity.interfaces import IDexterityFTI
from plone.dexterity.utils import getAdditionalSchemata
from zope.component import getUtility


class CourseView(WidgetsView):
    """This class is the same in plone.dexterity.browser.view.DefaultView
    The default view for Dexterity content. This uses a WidgetsView and
    renders all widgets in display mode.
    """

    @property
    def schema(self):
        fti = getUtility(IDexterityFTI, name=self.context.portal_type)
        return fti.lookupSchema()

    @property
    def additionalSchemata(self):
        return getAdditionalSchemata(context=self.context)

    def get_professors(self):
        results = []
        language = api.portal.get_current_language()
        connector1 = _("to")
        connector2 = _("in the building")
        for professor in self.context.professors:
            days = professor["days"]
            days = sorted(
                days,
                key=[
                    "monday",
                    "tuesday",
                    "wednesday",
                    "thursday",
                    "friday",
                    "saturday",
                    "sunday",
                ].index,
            )
            days = [
                api.portal.translate(
                    day.capitalize(), domain="collective.classschedule", lang=language
                )[0:3]
                for day in days
            ]
            days_str = ", ".join(day for day in days)
            professor_name = professor["fullname"]
            room_uid = professor["location_room"]
            room = api.content.get(UID=room_uid)
            room_name = room.Title()
            building = room.aq_parent.Title()
            start_time = professor["start_time"].strftime("%I:%M %p")
            end_time = professor["end_time"].strftime("%I:%M %p")
            place = (
                f"{room_name} "
                + api.portal.translate(
                    connector2, domain="collective.classschedule", lang=language
                )
                + f" {building}"
            )
            url = room.absolute_url_path()
            schedule = (
                f"{start_time} "
                + api.portal.translate(
                    connector1, domain="collective.classschedule", lang=language
                )
                + f" {end_time}"
            )
            results.append({
                "name": professor_name,
                "place": place,
                "schedule": schedule,
                "url": url,
                "days": days_str,
            })
        return results

    def get_assistant(self):
        results = []
        for assistant in self.context.professor_assistants:
            professor_name = assistant["fullname"]
            results.append({"name": professor_name})
        return results

    def get_summary(self):
        return self.context.description

    def get_titular_title(self):
        if len(self.context.professors) == 1:
            return _("Professor")
        return _("Professors")

    def get_assistant_title(self):
        if len(self.context.professor_assistants) == 1:
            return _("Assistant")
        return _("Assistants")
