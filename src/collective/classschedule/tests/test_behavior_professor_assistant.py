from collective.classschedule.behaviors.professor_assistant import (
    IProfessorAssistantMarker,
)
from collective.classschedule.testing import (
    COLLECTIVE_CLASSSCHEDULE_INTEGRATION_TESTING,
)
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.behavior.interfaces import IBehavior
from zope.component import getUtility

import unittest


class ProfessorAssistantIntegrationTest(unittest.TestCase):
    layer = COLLECTIVE_CLASSSCHEDULE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_behavior_professor_assistant(self):
        behavior = getUtility(IBehavior, "collective.classschedule.professor_assistant")
        self.assertEqual(
            behavior.marker,
            IProfessorAssistantMarker,
        )
