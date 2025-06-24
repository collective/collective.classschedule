from collective.classschedule.content.course import ICourse
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


class CourseIntegrationTest(unittest.TestCase):
    layer = COLLECTIVE_CLASSSCHEDULE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.parent = self.portal

    def test_ct_course_schema(self):
        fti = queryUtility(IDexterityFTI, name="Course")
        schema = fti.lookupSchema()
        self.assertEqual(ICourse, schema)

    def test_ct_course_fti(self):
        fti = queryUtility(IDexterityFTI, name="Course")
        self.assertTrue(fti)

    def test_ct_course_factory(self):
        fti = queryUtility(IDexterityFTI, name="Course")
        factory = fti.factory
        obj = createObject(factory)

        self.assertTrue(
            ICourse.providedBy(obj),
            f"ICourse not provided by {obj}!",
        )

    def test_ct_course_adding(self):
        setRoles(self.portal, TEST_USER_ID, ["Contributor"])
        obj = api.content.create(
            container=self.portal,
            type="Course",
            id="course",
        )

        self.assertTrue(
            ICourse.providedBy(obj),
            f"ICourse not provided by {obj.id}!",
        )

        parent = obj.__parent__
        self.assertIn("course", parent.objectIds())

        # check that deleting the object works too
        api.content.delete(obj=obj)
        self.assertNotIn("course", parent.objectIds())

    def test_ct_course_globally_addable(self):
        setRoles(self.portal, TEST_USER_ID, ["Contributor"])
        fti = queryUtility(IDexterityFTI, name="Course")
        self.assertTrue(fti.global_allow, f"{fti.id} is not globally addable!")
