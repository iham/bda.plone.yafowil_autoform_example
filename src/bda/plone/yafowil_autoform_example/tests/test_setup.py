# -*- coding: utf-8 -*-
"""Setup tests for this package."""
import unittest

from plone import api
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone.browserlayer import utils

from bda.plone.yafowil_autoform_example.interfaces import \
    IYafowilAutoformExampleLayer
from bda.plone.yafowil_autoform_example.testing import \
    YAFOWIL_AUTOFORM_EXAMPLE_FUNCTIONAL_TESTING


try:
    from Products.CMFPlone.utils import get_installer
except ImportError:
    get_installer = None


INSTALLED_ADDONS = [
    'plone.app.contenttypes',
    'plone.app.multilingual',
    # 'plone.app.multilingualindexes',
    'yafowil.plone',
]


class TestSetup(unittest.TestCase):
    """Test that yafowil.autoform_example is properly installed."""

    layer = YAFOWIL_AUTOFORM_EXAMPLE_FUNCTIONAL_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        if get_installer:
            self.installer = get_installer(self.portal, self.layer['request'])
        else:
            self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if bda.plone.yafowil_autoform_example is installed."""
        self.assertTrue(
            self.installer.isProductInstalled(
                'bda.plone.yafowil_autoform_example',
            ),
        )

    def test_browserlayer(self):
        """Test that IYafowilAutoformExampleLayer is registered."""
        self.assertIn(
            IYafowilAutoformExampleLayer,
            utils.registered_layers(),
        )

    def test_addons_installed(self):
        """Test if addons are installed."""
        for addon in INSTALLED_ADDONS:
            self.assertTrue(
                self.installer.isProductInstalled(addon),
            )

    # def test_contenttypes(self):
    #     """Test if all contenttypes are installed properly."""
    #     import pdb; pdb.set_trace()
    #     types = api.portal.get_tool('portal_types')
    #     types_list = types.listContentTypes()
    #     for installed_type in INSTALLED_TYPES:
    #         self.assertTrue(installed_type['type_name'] in types_list)
    #         behaviors = types.get(
    #             installed_type['type_name'],
    #         ).behaviors

    #         for behavior in installed_type['behaviors']:
    #             self.assertTrue(behavior in behaviors)


class TestUninstall(unittest.TestCase):

    layer = YAFOWIL_AUTOFORM_EXAMPLE_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        if get_installer:
            self.installer = get_installer(self.portal, self.layer['request'])
        else:
            self.installer = api.portal.get_tool('portal_quickinstaller')
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer.uninstallProducts(
            ['bda.plone.yafowil_autoform_example'],
        )
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if bda.plone.yafowil_autoform_example is cleanly uninstalled."""
        self.assertFalse(
            self.installer.isProductInstalled(
                'bda.plone.yafowil_autoform_example',
            ),
        )

    def test_browserlayer_removed(self):
        """Test that IYafowilAutoformExampleLayer is removed."""
        self.assertNotIn(
            IYafowilAutoformExampleLayer,
            utils.registered_layers(),
        )
