# -*- coding: utf-8 -*-

from Acquisition import aq_inner, aq_chain
from Products.CMFPlone import PloneMessageFactory as _
from Products.CMFPlone.browser.navtree import getNavigationRoot

from plone import api
from plone.i18n.normalizer.interfaces import IIDNormalizer
from plone.memoize import ram
from plone.registry.interfaces import IRegistry
from time import time
from zope.component import getUtility
from zope.component import queryUtility
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

from genweb6.core.indicators.client import Client as IndicadorsClient
from genweb6.serveistic.config_helper import facets_vocabulary
from genweb6.serveistic.content.serveitic.serveitic import IServeiTIC
from genweb6.serveistic.controlpanels.serveistic import IServeisTICControlPanelSettings
from genweb6.serveistic.controlpanels.facetes import IServeisTICFacetesControlPanelSettings
from genweb6.serveistic.ws_client.problems import Client as ProblemesClient


class NotificacioViewHelper(object):

    def get_bootstrap_icon_class(self, notificacio):
        if notificacio["tipus"] == u"Avís":
            return "bi bi-exclamation-triangle-fill"
        elif notificacio["tipus"] == u"Notificació":
            return "bi bi-info-circle-fill"
        elif notificacio["tipus"] == u"Novetat":
            return "bi bi-exclamation-circle-fill"
        else:
            return ""


def build_vocabulary(values):
    return SimpleVocabulary([
        SimpleTerm(title=_(value), value=value, token=token)
        for token, value in enumerate(values)])


@ram.cache(lambda *args: time() // (24 * 60 * 60))
def serveistic_config():
    """ Funcio que retorna les configuracions del controlpanel """
    registry = queryUtility(IRegistry)
    return registry.forInterface(IServeisTICControlPanelSettings)


@ram.cache(lambda *args: time() // (24 * 60 * 60))
def serveistic_facetes_config():
    """ Funcio que retorna les configuracions del controlpanel """
    registry = queryUtility(IRegistry)
    return registry.forInterface(IServeisTICFacetesControlPanelSettings)


def get_servei(self):
    context = aq_inner(self.context)
    for obj in aq_chain(context):
        if IServeiTIC.providedBy(obj):
            return obj
    return None


def get_ws_problemes_client():
    endpoint = serveistic_config().ws_problemes_endpoint
    login_username = serveistic_config().ws_problemes_login_username
    login_password = serveistic_config().ws_problemes_login_password
    return ProblemesClient(endpoint, login_username, login_password)


def get_ws_indicadors_client():
    endpoint = serveistic_config().ws_indicadors_endpoint
    return IndicadorsClient(endpoint)


def get_referer_path(context, request):
    if referer_is_current(request):
        return getNavigationRoot(context)
    try:
        return request.getHeader('referer').replace(
            get_site_url(context), get_site_path(context))
    except (AttributeError, TypeError):
        return None


def referer_is_current(request):
    if request.getHeader('referer'):
        return (get_clean_url(request.getHeader('referer')) ==
                get_clean_url(request.getURL()))
    return True


def get_clean_url(url):
    return url.split('?')[0].split('@')[0]


def get_site_url(context):
    portal_url = api.portal.get_tool("portal_url")
    return portal_url.getPortalObject().absolute_url()


def get_site_path(context):
    portal_url = api.portal.get_tool("portal_url")
    return '/'.join(portal_url.getPortalObject().getPhysicalPath())


def default_serveistic_url_preview_image():
    return api.portal.get().absolute_url() + '/++theme++genweb6.serveistic/img/capcalera_mini.jpg'


@implementer(IVocabularyFactory)
class FacetsVocabulary(object):

    def __call__(self, context):
        return facets_vocabulary


@implementer(IVocabularyFactory)
class FacetValuesVocabularyBase(object):
    """
    Base class that represents a vocabulary containing the defined values for
    a facet taken from the 'facetes_tables' property of the Serveis TIC plugin
    settings. The name of the facet the values of which are retrieved is
    specified in self.facet_id.
    """

    def __init__(self):
        self.facet_id = ""
        self.lang = ""

    def __call__(self, context):
        facets = serveistic_facetes_config().facetes_table
        facets = [] if facets is None else facets

        vocabulary = []
        for facet in facets:
            if facet['faceta'] == self.facet_id and facet['valor']:
                vocabulary.append(SimpleTerm(
                    value=getUtility(IIDNormalizer).normalize(facet['valor']),
                    title=facet['valor' + self.lang] if facet['valor' + self.lang] else '-'
                ))

        return SimpleVocabulary(vocabulary)


class CAFaceta1Vocabulary(FacetValuesVocabularyBase):
    def __init__(self):
        self.facet_id = u"Faceta 1"
        self.lang = u""


class CAFaceta2Vocabulary(FacetValuesVocabularyBase):
    def __init__(self):
        self.facet_id = u"Faceta 2"
        self.lang = u""


class CAFaceta3Vocabulary(FacetValuesVocabularyBase):
    def __init__(self):
        self.facet_id = u"Faceta 3"
        self.lang = u""


class CAFaceta4Vocabulary(FacetValuesVocabularyBase):
    def __init__(self):
        self.facet_id = u"Faceta 4"
        self.lang = u""


class CAFaceta5Vocabulary(FacetValuesVocabularyBase):
    def __init__(self):
        self.facet_id = u"Faceta 5"
        self.lang = u""


class CAFaceta6Vocabulary(FacetValuesVocabularyBase):
    def __init__(self):
        self.facet_id = u"Faceta 6"
        self.lang = u""


class CAFaceta7Vocabulary(FacetValuesVocabularyBase):
    def __init__(self):
        self.facet_id = u"Faceta 7"
        self.lang = u""


class CAFaceta8Vocabulary(FacetValuesVocabularyBase):
    def __init__(self):
        self.facet_id = u"Faceta 8"
        self.lang = u""


class ESFaceta1Vocabulary(FacetValuesVocabularyBase):
    def __init__(self):
        self.facet_id = u"Faceta 1"
        self.lang = u"_es"


class ESFaceta2Vocabulary(FacetValuesVocabularyBase):
    def __init__(self):
        self.facet_id = u"Faceta 2"
        self.lang = u"_es"


class ESFaceta3Vocabulary(FacetValuesVocabularyBase):
    def __init__(self):
        self.facet_id = u"Faceta 3"
        self.lang = u"_es"


class ESFaceta4Vocabulary(FacetValuesVocabularyBase):
    def __init__(self):
        self.facet_id = u"Faceta 4"
        self.lang = u"_es"


class ESFaceta5Vocabulary(FacetValuesVocabularyBase):
    def __init__(self):
        self.facet_id = u"Faceta 5"
        self.lang = u"_es"


class ESFaceta6Vocabulary(FacetValuesVocabularyBase):
    def __init__(self):
        self.facet_id = u"Faceta 6"
        self.lang = u"_es"


class ESFaceta7Vocabulary(FacetValuesVocabularyBase):
    def __init__(self):
        self.facet_id = u"Faceta 7"
        self.lang = u"_es"


class ESFaceta8Vocabulary(FacetValuesVocabularyBase):
    def __init__(self):
        self.facet_id = u"Faceta 8"
        self.lang = u"_es"


class ENFaceta1Vocabulary(FacetValuesVocabularyBase):
    def __init__(self):
        self.facet_id = u"Faceta 1"
        self.lang = u"_en"


class ENFaceta2Vocabulary(FacetValuesVocabularyBase):
    def __init__(self):
        self.facet_id = u"Faceta 2"
        self.lang = u"_en"


class ENFaceta3Vocabulary(FacetValuesVocabularyBase):
    def __init__(self):
        self.facet_id = u"Faceta 3"
        self.lang = u"_en"


class ENFaceta4Vocabulary(FacetValuesVocabularyBase):
    def __init__(self):
        self.facet_id = u"Faceta 4"
        self.lang = u"_en"


class ENFaceta5Vocabulary(FacetValuesVocabularyBase):
    def __init__(self):
        self.facet_id = u"Faceta 5"
        self.lang = u"_en"


class ENFaceta6Vocabulary(FacetValuesVocabularyBase):
    def __init__(self):
        self.facet_id = u"Faceta 6"
        self.lang = u"_en"


class ENFaceta7Vocabulary(FacetValuesVocabularyBase):
    def __init__(self):
        self.facet_id = u"Faceta 7"
        self.lang = u"_en"


class ENFaceta8Vocabulary(FacetValuesVocabularyBase):
    def __init__(self):
        self.facet_id = u"Faceta 8"
        self.lang = u"_en"
