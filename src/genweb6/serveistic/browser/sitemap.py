# -*- coding: utf-8 -*-
"""Override del ``NavtreeQueryBuilder`` de CMFPlone: ampliar ``portal_type`` (línia 65)."""
from Acquisition import aq_inner
from plone.app.layout.navigation.interfaces import INavtreeStrategy
from plone.app.layout.navigation.navtree import buildFolderTree
from Products.CMFPlone.browser.navigation import CatalogSiteMap
from Products.CMFPlone.browser.navtree import SitemapQueryBuilder
from zope.component import getMultiAdapter


# Id del FTI (el producte usa ``serveitic``; si el teu és ``serveistic``, canvia'l aquí)
SERVEISTIC_PORTAL_TYPE = 'serveitic'


def _append_serveistic_portal_type(query):
    """El que s'afegiria a la línia 65 després de ``utils.typesToList(context)``."""
    portal_types = query.get('portal_type')
    if portal_types is None:
        return
    merged = list(portal_types)
    if SERVEISTIC_PORTAL_TYPE not in merged:
        merged.append(SERVEISTIC_PORTAL_TYPE)
    query['portal_type'] = merged


class ServeisticSitemapQueryBuilder(SitemapQueryBuilder):
    """``SitemapQueryBuilder`` crida ``NavtreeQueryBuilder.__init__``; re-apliquem l'extensió."""

    def __init__(self, context):
        super().__init__(context)
        _append_serveistic_portal_type(self.query)


class ServeisticCatalogSiteMap(CatalogSiteMap):

    def siteMap(self):
        context = aq_inner(self.context)
        query_builder = ServeisticSitemapQueryBuilder(context)
        query = query_builder()
        strategy = getMultiAdapter((context, self), INavtreeStrategy)
        return buildFolderTree(context, obj=context, query=query, strategy=strategy)
