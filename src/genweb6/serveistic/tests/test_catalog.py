# -*- coding: utf-8 -*-
import unittest
from unittest.mock import MagicMock
from unittest.mock import patch

from genweb6.serveistic.catalog import find_container_servei
from genweb6.serveistic.catalog import get_servei_facetas_for_content
from genweb6.serveistic.catalog import get_unified_faceta_values


class DummyServeiTIC(object):
    ca_faceta_1 = ('aplicacio-web',)
    ca_faceta_2 = ('recerca-i-transferencia', 'aplicacio-web')
    ca_faceta_3 = ()
    ca_faceta_4 = None
    ca_faceta_5 = []
    ca_faceta_6 = ()
    ca_faceta_7 = ()
    ca_faceta_8 = ()


class TestUnifiedFacetaValues(unittest.TestCase):

    def test_get_unified_faceta_values_deduplicates(self):
        values = get_unified_faceta_values(DummyServeiTIC())
        self.assertEqual(
            ('aplicacio-web', 'recerca-i-transferencia'),
            values,
        )

    @patch('genweb6.serveistic.catalog.find_container_servei')
    def test_child_inherits_parent_facetas(self, mock_find_servei):
        servei = DummyServeiTIC()
        mock_find_servei.return_value = servei
        child = MagicMock()
        self.assertEqual(
            get_servei_facetas_for_content(child),
            get_unified_faceta_values(servei),
        )

    @patch('genweb6.serveistic.catalog.IServeiTIC')
    def test_find_container_servei_by_path(self, mock_iface):
        mock_iface.providedBy.side_effect = lambda obj: isinstance(obj, DummyServeiTIC)

        servei = DummyServeiTIC()
        portal = MagicMock()
        portal.unrestrictedTraverse.return_value = servei

        child = MagicMock()
        child.getPhysicalPath.return_value = ('Plone', 'ca', 'servei-test', 'notificacio-1')
        child.getPortalObject.return_value = portal
        child.__parent__ = None

        with patch('genweb6.serveistic.catalog.aq_parent', return_value=None):
            result = find_container_servei(child)

        self.assertIs(servei, result)
        portal.unrestrictedTraverse.assert_called_with('Plone/ca/servei-test')

    def test_find_container_servei_returns_none_without_parent(self):
        self.assertIsNone(find_container_servei(object()))
