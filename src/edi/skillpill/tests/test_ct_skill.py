# -*- coding: utf-8 -*-
from edi.skillpill.content.skill import ISkill  # NOQA E501
from edi.skillpill.testing import EDI_SKILLPILL_INTEGRATION_TESTING  # noqa
from plone import api
from plone.api.exc import InvalidParameterError
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest




class SkillIntegrationTest(unittest.TestCase):

    layer = EDI_SKILLPILL_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.parent = self.portal

    def test_ct_skill_schema(self):
        fti = queryUtility(IDexterityFTI, name='Skill')
        schema = fti.lookupSchema()
        self.assertEqual(ISkill, schema)

    def test_ct_skill_fti(self):
        fti = queryUtility(IDexterityFTI, name='Skill')
        self.assertTrue(fti)

    def test_ct_skill_factory(self):
        fti = queryUtility(IDexterityFTI, name='Skill')
        factory = fti.factory
        obj = createObject(factory)

        self.assertTrue(
            ISkill.providedBy(obj),
            u'ISkill not provided by {0}!'.format(
                obj,
            ),
        )

    def test_ct_skill_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.portal,
            type='Skill',
            id='skill',
        )

        self.assertTrue(
            ISkill.providedBy(obj),
            u'ISkill not provided by {0}!'.format(
                obj.id,
            ),
        )

        parent = obj.__parent__
        self.assertIn('skill', parent.objectIds())

        # check that deleting the object works too
        api.content.delete(obj=obj)
        self.assertNotIn('skill', parent.objectIds())

    def test_ct_skill_globally_addable(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='Skill')
        self.assertTrue(
            fti.global_allow,
            u'{0} is not globally addable!'.format(fti.id)
        )

    def test_ct_skill_filter_content_type_true(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='Skill')
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            fti.id,
            self.portal,
            'skill_id',
            title='Skill container',
         )
        self.parent = self.portal[parent_id]
        with self.assertRaises(InvalidParameterError):
            api.content.create(
                container=self.parent,
                type='Document',
                title='My Content',
            )
