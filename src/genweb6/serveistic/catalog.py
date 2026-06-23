# -*- coding: utf-8 -*-
"""Catalog helpers for Servei TIC faceta search in collections."""

from Acquisition import aq_inner
from Acquisition import aq_parent

from plone.indexer.delegate import DelegatingIndexerFactory

from genweb6.serveistic.content.serveitic.serveitic import IServeiTIC


FACETA_FIELD_NAMES = tuple('ca_faceta_{0}'.format(i) for i in range(1, 9))

SERVEI_CHILD_PORTAL_TYPES = ('Document', 'Link', 'File', 'notificaciotic')

SERVEI_FACETAS_PORTAL_TYPE = 'notificaciotic'


def find_container_servei(content):
    """Return the Servei TIC ancestor of a content item, if any."""
    obj = aq_inner(content)
    while obj is not None:
        if IServeiTIC.providedBy(obj):
            return obj
        parent = aq_parent(obj)
        if parent is None or aq_inner(parent) is obj:
            break
        obj = aq_inner(parent)

    try:
        parts = content.getPhysicalPath()
        portal = content.getPortalObject()
    except AttributeError:
        return None
    for depth in range(len(parts) - 1, 0, -1):
        try:
            candidate = portal.unrestrictedTraverse('/'.join(parts[:depth]))
        except Exception:
            continue
        if IServeiTIC.providedBy(candidate):
            return candidate
    return None


def get_unified_faceta_values(obj):
    """Return all ca_faceta values from a Servei TIC, without duplicates."""
    values = []
    seen = set()
    for name in FACETA_FIELD_NAMES:
        field_values = getattr(obj, name, None) or ()
        for value in field_values:
            if value and value not in seen:
                seen.add(value)
                values.append(value)
    return tuple(values)


def get_servei_facetas_for_content(obj):
    """Return unified faceta values inherited from the parent Servei TIC."""
    servei = find_container_servei(obj)
    if servei is None:
        return ()
    return get_unified_faceta_values(servei)


def _servei_facetas_index(obj):
    return get_servei_facetas_for_content(obj)


servei_facetas = DelegatingIndexerFactory(_servei_facetas_index)
