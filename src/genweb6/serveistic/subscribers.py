# -*- coding: utf-8 -*-

from Acquisition import aq_chain

from plone import api

from genweb6.core.indicators import RegistryException
from genweb6.core.indicators import ReporterException
from genweb6.serveistic.content.serveitic.serveitic import IServeiTIC
from genweb6.serveistic.indicators.updating import update_indicators
from genweb6.serveistic.indicators.updating import update_indicators_if_state
from genweb6.serveistic.utilities import serveistic_config

import logging

logger = logging.getLogger(name='genweb6.serveistic.indicators')


def Added(content, event):
    """ MAX hooks main handler """

    servei = findContainerServei(content)
    if not servei:
        # If file we are creating is not inside a servei folder
        return

    servei_tags = servei.subject
    addTagsToObject(servei_tags, content)


def serveiModifyAddSubjects(content, event):
    """ Servei modified handler """

    pc = api.portal.get_tool("portal_catalog")
    servei_tags = content.subject
    path = "/".join(content.getPhysicalPath())
    r_results = pc.searchResults(portal_type=('Document', 'Link', 'File'),
                                 path=path)

    for brain in r_results:
        obj = brain.getObject()
        addTagsToObject(servei_tags, obj)

    content.es_faceta_1 = content.ca_faceta_1
    content.en_faceta_1 = content.ca_faceta_1

    content.es_faceta_2 = content.ca_faceta_2
    content.en_faceta_2 = content.ca_faceta_2

    content.es_faceta_3 = content.ca_faceta_3
    content.en_faceta_3 = content.ca_faceta_3

    content.es_faceta_4 = content.ca_faceta_4
    content.en_faceta_4 = content.ca_faceta_4

    content.es_faceta_5 = content.ca_faceta_5
    content.en_faceta_5 = content.ca_faceta_5

    content.es_faceta_6 = content.ca_faceta_6
    content.en_faceta_6 = content.ca_faceta_6

    content.es_faceta_7 = content.ca_faceta_7
    content.en_faceta_7 = content.ca_faceta_7

    content.es_faceta_8 = content.ca_faceta_8
    content.en_faceta_8 = content.ca_faceta_8

    content.reindexObject()


def update_indicators_on_serveitic_deletion(obj, event):
    try:
        update_indicators_if_state(
            obj, ('published',),
            service=serveistic_config().ws_indicadors_service_id,
            indicator='servei-n')
        logger.info("Indicators were successfully reported")
    except RegistryException as e:
        logger.warning(
            "Error while loading indicator registry ({0})".format(e))
    except ReporterException as e:
        logger.warning("Error while reporting indicators ({0})".format(e))


def update_indicators_on_serveitic_review_state_change(obj, event):
    try:
        update_indicators(
            obj,
            service=serveistic_config().ws_indicadors_service_id,
            indicator='servei-n', after_commit=True)
        logger.info("Indicators were successfully reported")
    except RegistryException as e:
        logger.warning(
            "Error while loading indicator registry ({0})".format(e))
    except ReporterException as e:
        logger.warning("Error while reporting indicators ({0})".format(e))


# --------------- helpers ---------------

def addTagsToObject(servei_tags, obj):
    tags = []
    object_tags = list(obj.subject)
    [tags.append(tag) for tag in servei_tags if tag not in object_tags]
    obj.subject = tuple(sum([object_tags, tags], []))
    obj.reindexObject()


def findContainerServei(content):
    for parent in aq_chain(content):
        if IServeiTIC.providedBy(parent):
            return parent

    return None
