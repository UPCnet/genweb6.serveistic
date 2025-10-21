# -*- coding: utf-8 -*-

from Products.Five import BrowserView
from Products.GenericSetup.context import SnapshotImportContext
from Products.GenericSetup.interfaces import IBody

from eea.facetednavigation.config import ANNO_FACETED_LAYOUT
from eea.facetednavigation.settings.interfaces import IDisableSmartFacets
from eea.facetednavigation.settings.interfaces import IHidePloneLeftColumn
from eea.facetednavigation.settings.interfaces import IHidePloneRightColumn
from eea.facetednavigation.subtypes.interfaces import IFacetedNavigable
from eea.facetednavigation.subtypes.interfaces import IPossibleFacetedNavigable
from plone import api
from plone.dexterity.utils import createContentInContainer
from zope.annotation.interfaces import IAnnotations
from zope.component import queryMultiAdapter
from zope.interface import alsoProvides

from genweb6.core import utils
from genweb6.core.interfaces import IProtectedContent

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
            alsoProvides(portal_ca, IPossibleFacetedNavigable)
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
            alsoProvides(portal_es, IPossibleFacetedNavigable)
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
            alsoProvides(portal_en, IPossibleFacetedNavigable)
            IAnnotations(portal_en)[ANNO_FACETED_LAYOUT] = "faceted-preview-items"
            environ = SnapshotImportContext(portal_en, "utf-8")
            importer = queryMultiAdapter((portal_en, environ), IBody)
            importer.body = open('{}/genweb6/serveistic/data/faceted_settings_en.xml'.format(egglocation), 'rb').read()

        return self.request.response.redirect(portal.absolute_url())


def create_content(container, portal_type, id, **kwargs):
    if not getattr(container, id, False):
        obj = createContentInContainer(
            container, portal_type, checkConstraints=False, **kwargs)
    return getattr(container, id)


class SetupServeisticInFolder(BrowserView):

    def __call__(self):
        context = self.context
        context.setLayout('facetednavigation_view')

        alsoProvides(context, IFacetedNavigable)
        alsoProvides(context, IHidePloneLeftColumn)
        alsoProvides(context, IHidePloneRightColumn)
        alsoProvides(context, IDisableSmartFacets)
        alsoProvides(context, IPossibleFacetedNavigable)
        alsoProvides(context, IProtectedContent)

        IAnnotations(context)[ANNO_FACETED_LAYOUT] = "faceted-preview-items"

        environ = SnapshotImportContext(context, "utf-8")
        importer = queryMultiAdapter((context, environ), IBody)
        egglocation = pkg_resources.get_distribution('genweb6.serveistic').location

        lang = utils.pref_lang()
        importer.body = open('{}/genweb6/serveistic/data/faceted_settings_{}.xml'.format(egglocation, lang), 'rb').read()

        banners = create_content(
            self.context, 'BannerContainer', 'banners', title='banners',
            description=u'Banners')

        banners.title = 'Banners'
        banners.exclude_from_nav = True
        banners.reindexObject()
        alsoProvides(banners, IProtectedContent)

        return self.request.response.redirect(self.context.absolute_url())


class CreateBannerFolder(BrowserView):

    def __call__(self):
        banners = create_content(
            self.context, 'BannerContainer', 'banners', title='banners',
            description=u'Banners')

        banners.title = 'Banners'
        banners.exclude_from_nav = True
        banners.reindexObject()
        alsoProvides(banners, IProtectedContent)

        return self.request.response.redirect(self.context.absolute_url())