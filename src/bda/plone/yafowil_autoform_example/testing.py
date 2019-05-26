# -*- coding: utf-8 -*-
from Products.CMFCore.indexing import processQueue
from zope.configuration import xmlconfig
from zope.interface import alsoProvides

import plone.app.multilingual
# import plone.app.multilingualindexes
from plone import api
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.multilingual.dx.interfaces import ILanguageIndependentField
from plone.app.relationfield.behavior import IRelatedItems
from plone.app.testing import TEST_USER_ID
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PloneWithPackageLayer
from plone.app.testing import applyProfile
from plone.app.testing import setRoles
from plone.testing import zope

import yafowil.plone

import bda.plone.yafowil_autoform_example



class YafowilAutoformExampleLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)  # NOQA N815

    def setUpZope(self, app, configurationContext):  # NOQA N802, N803
        # add plone.app.multilingual
        xmlconfig.file('testing.zcml', plone.app.multilingual,
                       context=configurationContext)

        xmlconfig.file('overrides.zcml', plone.app.multilingual,
                       context=configurationContext)

        # Enable languageindependent-field on IRelatedItems-behavior
        alsoProvides(IRelatedItems['relatedItems'], ILanguageIndependentField)

        # self.loadZCML(package=plone.app.multilingualindexes)
        # zope.installProduct(app, 'plone.app.multilingualindexes')

        self.loadZCML(package=yafowil.plone)
        self.loadZCML(package=bda.plone.yafowil_autoform_example)

    def setUpPloneSite(self, portal):  # NOQA N802
        applyProfile(portal, 'bda.plone.yafowil_autoform_example:default')

        setRoles(portal, TEST_USER_ID, ['Manager'])
        self.language = api.portal.get_default_language()
        self.root = portal.get(self.language) or portal

        self.prepare_test_content(portal)

    def prepare_test_content(self, portal):
        processQueue()


YAFOWIL_AUTOFORM_EXAMPLE_FIXTURE = YafowilAutoformExampleLayer()


YAFOWIL_AUTOFORM_EXAMPLE_INTEGRATION_TESTING = IntegrationTesting(
    bases=(YAFOWIL_AUTOFORM_EXAMPLE_FIXTURE,),
    name='YafowilAutoformExampleLayer:IntegrationTesting',
)


YAFOWIL_AUTOFORM_EXAMPLE_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(YAFOWIL_AUTOFORM_EXAMPLE_FIXTURE,),
    name='YafowilAutoformExampleLayer:FunctionalTesting',
)
