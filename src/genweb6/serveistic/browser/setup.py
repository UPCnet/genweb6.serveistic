# -*- coding: utf-8 -*-

from Products.Five import BrowserView
from Products.GenericSetup.context import SnapshotImportContext
from Products.GenericSetup.interfaces import IBody

from eea.facetednavigation.config import ANNO_FACETED_LAYOUT
from eea.facetednavigation.settings.interfaces import IDisableSmartFacets
from eea.facetednavigation.settings.interfaces import IHidePloneLeftColumn
from eea.facetednavigation.settings.interfaces import IHidePloneRightColumn
from eea.facetednavigation.subtypes.interfaces import IFacetedNavigable
from plone import api
from zope.annotation.interfaces import IAnnotations
from zope.component import queryMultiAdapter
from zope.interface import alsoProvides

import pkg_resources


class SetupServeistic(BrowserView):

    def __call__(self):
        portal = api.portal.get()
        egglocation = pkg_resources.get_distribution('genweb6.serveistic').location

        if 'ca' in portal:
            portal_ca = portal['ca']
            portal_ca.setLayout('facetednavigation_view')
            alsoProvides(portal_ca, IFacetedNavigable)
            alsoProvides(portal_ca, IHidePloneLeftColumn)
            alsoProvides(portal_ca, IHidePloneRightColumn)
            alsoProvides(portal_ca, IDisableSmartFacets)
            IAnnotations(portal_ca)[ANNO_FACETED_LAYOUT] = "faceted-preview-items"
            environ = SnapshotImportContext(portal_ca, "utf-8")
            importer = queryMultiAdapter((portal_ca, environ), IBody)
            importer.body = open('{}/genweb6/serveistic/data/faceted_settings_ca.xml'.format(egglocation), 'rb').read()

        if 'es' in portal:
            portal_es = portal['es']
            portal_es.setLayout('facetednavigation_view')
            alsoProvides(portal_es, IFacetedNavigable)
            alsoProvides(portal_es, IHidePloneLeftColumn)
            alsoProvides(portal_es, IHidePloneRightColumn)
            alsoProvides(portal_es, IDisableSmartFacets)
            IAnnotations(portal_es)[ANNO_FACETED_LAYOUT] = "faceted-preview-items"
            environ = SnapshotImportContext(portal_es, "utf-8")
            importer = queryMultiAdapter((portal_es, environ), IBody)
            importer.body = open('{}/genweb6/serveistic/data/faceted_settings_es.xml'.format(egglocation), 'rb').read()

        if 'en' in portal:
            portal_en = portal['en']
            portal_en.setLayout('facetednavigation_view')
            alsoProvides(portal_en, IFacetedNavigable)
            alsoProvides(portal_en, IHidePloneLeftColumn)
            alsoProvides(portal_en, IHidePloneRightColumn)
            alsoProvides(portal_en, IDisableSmartFacets)
            IAnnotations(portal_en)[ANNO_FACETED_LAYOUT] = "faceted-preview-items"
            environ = SnapshotImportContext(portal_en, "utf-8")
            importer = queryMultiAdapter((portal_en, environ), IBody)
            importer.body = open('{}/genweb6/serveistic/data/faceted_settings_en.xml'.format(egglocation), 'rb').read()

        return self.request.response.redirect(portal.absolute_url())
