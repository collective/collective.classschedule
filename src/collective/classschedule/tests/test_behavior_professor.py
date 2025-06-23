from collective.classschedule.behaviors.professor import IProfessorMarker
from collective.classschedule.testing import (
    COLLECTIVE_CLASSSCHEDULE_INTEGRATION_TESTING,
)
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.behavior.interfaces import IBehavior
from zope.component import getUtility

import unittest


class ProfessorIntegrationTest(unittest.TestCase):
    layer = COLLECTIVE_CLASSSCHEDULE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_behavior_professor(self):
        behavior = getUtility(IBehavior, "collective.classschedule.professor")
        self.assertEqual(
            behavior.marker,
            IProfessorMarker,
        )
