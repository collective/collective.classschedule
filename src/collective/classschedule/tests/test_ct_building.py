from collective.classschedule.content.building import IBuilding
from collective.classschedule.testing import (
    COLLECTIVE_CLASSSCHEDULE_INTEGRATION_TESTING,
)
from plone import api
from plone.api.exc import InvalidParameterError
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest


class BuildingIntegrationTest(unittest.TestCase):
    layer = COLLECTIVE_CLASSSCHEDULE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.parent = self.portal

    def test_ct_building_schema(self):
        fti = queryUtility(IDexterityFTI, name="Building")
        schema = fti.lookupSchema()
        self.assertEqual(IBuilding, schema)

    def test_ct_building_fti(self):
        fti = queryUtility(IDexterityFTI, name="Building")
        self.assertTrue(fti)

    def test_ct_building_factory(self):
        fti = queryUtility(IDexterityFTI, name="Building")
        factory = fti.factory
        obj = createObject(factory)

        self.assertTrue(
            IBuilding.providedBy(obj),
            f"IBuilding not provided by {obj}!",
        )

    def test_ct_building_adding(self):
        setRoles(self.portal, TEST_USER_ID, ["Contributor"])
        obj = api.content.create(
            container=self.portal,
            type="Building",
            id="building",
        )

        self.assertTrue(
            IBuilding.providedBy(obj),
            f"IBuilding not provided by {obj.id}!",
        )

        parent = obj.__parent__
        self.assertIn("building", parent.objectIds())

        # check that deleting the object works too
        api.content.delete(obj=obj)
        self.assertNotIn("building", parent.objectIds())

    def test_ct_building_globally_addable(self):
        setRoles(self.portal, TEST_USER_ID, ["Contributor"])
        fti = queryUtility(IDexterityFTI, name="Building")
        self.assertTrue(fti.global_allow, f"{fti.id} is not globally addable!")

    def test_ct_building_filter_content_type_true(self):
        setRoles(self.portal, TEST_USER_ID, ["Contributor"])
        fti = queryUtility(IDexterityFTI, name="Building")
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            fti.id,
            self.portal,
            "building_id",
            title="Building container",
        )
        self.parent = self.portal[parent_id]
        with self.assertRaises(InvalidParameterError):
            api.content.create(
                container=self.parent,
                type="Document",
                title="My Content",
            )
