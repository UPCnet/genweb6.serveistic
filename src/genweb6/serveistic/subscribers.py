# -*- coding: utf-8 -*-

from Acquisition import aq_chain
from Products.CMFPlone.interfaces.constrains import ISelectableConstrainTypes

from plone import api
from plone.app.contenttypes.behaviors.richtext import IRichTextBehavior
from plone.dexterity.utils import createContentInContainer
from plone.i18n.normalizer.interfaces import IIDNormalizer
from plone.portlets.interfaces import IPortletAssignmentMapping
from plone.portlets.interfaces import IPortletManager
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.component import queryUtility
from zope.interface import alsoProvides

from genweb6.core.indicators import RegistryException
from genweb6.core.indicators import ReporterException
from genweb6.serveistic.content.serveitic.serveitic import IInitializedServeiTIC
from genweb6.serveistic.content.serveitic.serveitic import IServeiTIC
from genweb6.serveistic.data.folder_structure import folder_structure
from genweb6.serveistic.indicators.updating import update_indicators
from genweb6.serveistic.indicators.updating import update_indicators_if_state
from genweb6.serveistic.portlets.bannersportlet.bannersportlet import Assignment as BannersAssignment
from genweb6.serveistic.portlets.indicadors.indicadors import Assignment as IndicadorsAssignment
from genweb6.serveistic.portlets.notificacions.notificacions import Assignment as NotificacionsAssignment
from genweb6.serveistic.utilities import serveistic_config

import logging
import unicodedata

logger = logging.getLogger(name='genweb6.serveistic.indicators')


def Added(content, event):
    """ MAX hooks main handler """

    servei = findContainerServei(content)
    if not servei:
        # If file we are creating is not inside a servei folder
        return

    servei_tags = servei.subject
    addTagsToObject(servei_tags, content)


def initialize_servei(serveitic, event):
    # If it is a copy do not execute
    if 'copy_of_' in event.newName:
        return

    # Configure portlets
    assignments = get_portlet_assignments(serveitic, 'plone.leftcolumn')
    if 'banners_global' not in assignments:
        assignments['banners_global'] = BannersAssignment(banner_type=u"Global")
    if 'banners_local' not in assignments:
        assignments['banners_local'] = BannersAssignment(banner_type=u"Local")

    assignments = get_portlet_assignments(serveitic, 'genweb.portlets.HomePortletManager3')
    if 'notificacions' not in assignments:
        assignments['notificacions'] = NotificacionsAssignment()

    assignments = get_portlet_assignments(serveitic, 'genweb.portlets.HomePortletManager4')
    if 'indicadors' not in assignments:
        assignments['indicadors'] = IndicadorsAssignment()

    # Create folder structure
    normalizer = getUtility(IIDNormalizer)
    for folder_data in folder_structure:
        try:
            if isinstance(folder_data[0], str):
                flattened = unicodedata.normalize('NFKD', folder_data[0].decode('utf-8')).encode('ascii', errors='ignore')
            else:
                flattened = unicodedata.normalize('NFKD', folder_data[0]).encode('ascii', errors='ignore')

            if normalizer.normalize(flattened) not in serveitic:
                createFolderAndContents(serveitic, folder_data)
        except:
            createFolderAndContents(serveitic, folder_data)

    # Mark ServeiTIC as initialized to prevent previous folder creations from
    # triggering the modify event
    alsoProvides(serveitic, IInitializedServeiTIC)

    # Facetas
    serveitic.es_faceta_1 = serveitic.ca_faceta_1
    serveitic.en_faceta_1 = serveitic.ca_faceta_1

    serveitic.es_faceta_2 = serveitic.ca_faceta_2
    serveitic.en_faceta_2 = serveitic.ca_faceta_2

    serveitic.es_faceta_3 = serveitic.ca_faceta_3
    serveitic.en_faceta_3 = serveitic.ca_faceta_3

    serveitic.es_faceta_4 = serveitic.ca_faceta_4
    serveitic.en_faceta_4 = serveitic.ca_faceta_4

    serveitic.es_faceta_5 = serveitic.ca_faceta_5
    serveitic.en_faceta_5 = serveitic.ca_faceta_5

    serveitic.es_faceta_6 = serveitic.ca_faceta_6
    serveitic.en_faceta_6 = serveitic.ca_faceta_6

    serveitic.es_faceta_7 = serveitic.ca_faceta_7
    serveitic.en_faceta_7 = serveitic.ca_faceta_7

    serveitic.es_faceta_8 = serveitic.ca_faceta_8
    serveitic.en_faceta_8 = serveitic.ca_faceta_8

    serveitic.reindexObject()


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


def createFolderAndContents(folder_directori, folder_data):
    # Create folder
    folder_props = {
        'title': folder_data[0],
        'checkConstraints': False,
        'exclude_from_nav': folder_data[2],
        'allow_discussion': folder_data[3]}
    if folder_data[5] is not None:
        folder_props['layout'] = folder_data[5]
    folder = createContentInContainer(folder_directori, folder_data[1], **folder_props)

    behavior = ISelectableConstrainTypes(folder)
    behavior.setConstrainTypesMode(1)
    behavior.setLocallyAllowedTypes(folder_data[4])
    behavior.setImmediatelyAddableTypes(folder_data[4])
    folder.reindexObject()

    # Create a contents
    for folder_content in folder_data[7]:
        createContentInFolder(folder, folder_content)

    if folder_data[6] is not None:
        folder.setDefaultPage(folder_data[6])


def createContentInFolder(folder_directori, folder_content):
    # Create content
    if folder_content[1] != "Folder":
        content_props = {
            'title': folder_content[0],
            'checkConstraints': False,
            'exclude_from_nav': folder_content[2],
            'allow_discussion': folder_content[3]}

        if folder_content[6] is not None:
            content_props['description'] = folder_content[6]

        if folder_content[7] is not None:
            content_props['text'] = IRichTextBehavior['text'].fromUnicode(folder_content[7])

        if folder_content[5] is not None:
            content_props['layout'] = folder_content[5]

        content = createContentInContainer(folder_directori, folder_content[1], **content_props)
        if folder_content[4] is not None:
            behavior = ISelectableConstrainTypes(content)
            behavior.setConstrainTypesMode(1)
            behavior.setLocallyAllowedTypes(folder_content[4])
            behavior.setImmediatelyAddableTypes(folder_content[4])
    else:
        createFolderAndContents(folder_directori, folder_content)


def get_portlet_assignments(context, name):
    portlet_manager = queryUtility(IPortletManager, name=name, context=context)
    return getMultiAdapter((context, portlet_manager), IPortletAssignmentMapping)
