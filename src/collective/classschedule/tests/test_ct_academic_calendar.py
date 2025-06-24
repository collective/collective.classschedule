# -*- coding: utf-8 -*-
from collective.classschedule.content.academic_calendar import IAcademicCalendar  # NOQA E501
from collective.classschedule.testing import COLLECTIVE_CLASSSCHEDULE_INTEGRATION_TESTING  # noqa
from plone import api
from plone.api.exc import InvalidParameterError
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest




class AcademicCalendarIntegrationTest(unittest.TestCase):

    layer = COLLECTIVE_CLASSSCHEDULE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.parent = self.portal

    def test_ct_academic_calendar_schema(self):
        fti = queryUtility(IDexterityFTI, name='AcademicCalendar')
        schema = fti.lookupSchema()
        self.assertEqual(IAcademicCalendar, schema)

    def test_ct_academic_calendar_fti(self):
        fti = queryUtility(IDexterityFTI, name='AcademicCalendar')
        self.assertTrue(fti)

    def test_ct_academic_calendar_factory(self):
        fti = queryUtility(IDexterityFTI, name='AcademicCalendar')
        factory = fti.factory
        obj = createObject(factory)

        self.assertTrue(
            IAcademicCalendar.providedBy(obj),
            u'IAcademicCalendar not provided by {0}!'.format(
                obj,
            ),
        )

    def test_ct_academic_calendar_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.portal,
            type='AcademicCalendar',
            id='academic_calendar',
        )

        self.assertTrue(
            IAcademicCalendar.providedBy(obj),
            u'IAcademicCalendar not provided by {0}!'.format(
                obj.id,
            ),
        )

        parent = obj.__parent__
        self.assertIn('academic_calendar', parent.objectIds())

        # check that deleting the object works too
        api.content.delete(obj=obj)
        self.assertNotIn('academic_calendar', parent.objectIds())

    def test_ct_academic_calendar_globally_addable(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='AcademicCalendar')
        self.assertTrue(
            fti.global_allow,
            u'{0} is not globally addable!'.format(fti.id)
        )

    def test_ct_academic_calendar_filter_content_type_true(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='AcademicCalendar')
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            fti.id,
            self.portal,
            'academic_calendar_id',
            title='AcademicCalendar container',
        )
        self.parent = self.portal[parent_id]
        with self.assertRaises(InvalidParameterError):
            api.content.create(
                container=self.parent,
                type='Document',
                title='My Content',
            )
