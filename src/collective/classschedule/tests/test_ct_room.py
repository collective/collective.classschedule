from collective.classschedule.content.room import IRoom
from collective.classschedule.testing import (
    COLLECTIVE_CLASSSCHEDULE_INTEGRATION_TESTING,
)
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest


class RoomIntegrationTest(unittest.TestCase):
    layer = COLLECTIVE_CLASSSCHEDULE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            "Building",
            self.portal,
            "parent_container",
            title="Parent container",
        )
        self.parent = self.portal[parent_id]

    def test_ct_room_schema(self):
        fti = queryUtility(IDexterityFTI, name="Room")
        schema = fti.lookupSchema()
        self.assertEqual(IRoom, schema)

    def test_ct_room_fti(self):
        fti = queryUtility(IDexterityFTI, name="Room")
        self.assertTrue(fti)

    def test_ct_room_factory(self):
        fti = queryUtility(IDexterityFTI, name="Room")
        factory = fti.factory
        obj = createObject(factory)

        self.assertTrue(
            IRoom.providedBy(obj),
            f"IRoom not provided by {obj}!",
        )

    def test_ct_room_adding(self):
        setRoles(self.portal, TEST_USER_ID, ["Contributor"])
        obj = api.content.create(
            container=self.parent,
            type="Room",
            id="room",
        )

        self.assertTrue(
            IRoom.providedBy(obj),
            f"IRoom not provided by {obj.id}!",
        )

        parent = obj.__parent__
        self.assertIn("room", parent.objectIds())

        # check that deleting the object works too
        api.content.delete(obj=obj)
        self.assertNotIn("room", parent.objectIds())

    def test_ct_room_globally_not_addable(self):
        setRoles(self.portal, TEST_USER_ID, ["Contributor"])
        fti = queryUtility(IDexterityFTI, name="Room")
        self.assertFalse(fti.global_allow, f"{fti.id} is globally addable!")
