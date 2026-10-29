from plone.registry.interfaces import IRegistry
from plone.restapi.bbb import INavigationSchema
from Products.CMFPlone.interfaces import INonInstallable
from zope.component import getUtility
from zope.interface import implementer


@implementer(INonInstallable)
class HiddenProfiles:
    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return [
            "collective.classschedule:uninstall",
        ]


def post_install(context):
    """Post install script"""
    # Do something at the end of the installation of this package.

    registry = getUtility(IRegistry)
    settings = registry.forInterface(INavigationSchema, prefix="plone")
    displayed_types = settings.displayed_types
    display_contents = [
        *list(displayed_types),
        "AcademicCalendar",
    ]
    settings.displayed_types = tuple(display_contents)
