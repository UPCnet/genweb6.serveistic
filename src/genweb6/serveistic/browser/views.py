# -*- coding: utf-8 -*-

from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.browser.interfaces import ISitemapView
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from eea.facetednavigation.browser.app.view import FacetedContainerView
from eea.facetednavigation.views.preview import PreviewBrain
from plone.registry.interfaces import IRegistry
from zope.component import getMultiAdapter
from zope.component import queryMultiAdapter
from zope.component import queryUtility
from zope.component.hooks import getSite
from zope.interface import implementer

from genweb6.serveistic.controlpanels.serveistic import IServeisTICControlPanelSettings
from genweb6.serveistic.data_access.notificacio import NotificacioDataReporter
from genweb6.serveistic.utilities import default_serveistic_url_preview_image
from genweb6.serveistic.utilities import NotificacioViewHelper


@implementer(ISitemapView)
class SitemapView(BrowserView):

    item_template = ViewPageTemplateFile('views_templates/sitemap-item.pt')

    def createSiteMap(self):
        context = aq_inner(self.context)
        view = getMultiAdapter((context, self.request),
                               name='sitemap_builder_view')
        data = view.siteMap()
        return self._renderLevel(children=data.get('children', []))

    def _renderLevel(self, children=[]):
        output = ''
        for node in children:
            output += '<li class="navTreeItem visualNoMarker">\n'
            output += self.item_template(node=node)
            output += '</li>\n'

        return output


class FacetedContainerView(FacetedContainerView, NotificacioViewHelper):

    SHORT_SUMMARY_MAX_LENGTH = 115

    @property
    def notificacions(self):
        reporter = NotificacioDataReporter(
            getToolByName(self.context, 'portal_catalog'))
        return reporter.list_by_general()

    def page_content(self):
        try:
            lang = self.context.language
            if lang == 'ca':
                benvingut = self.context["benvingut"]
            elif lang == 'es':
                benvingut = self.context["bienvenido"]
            elif lang == 'en':
                benvingut = self.context["welcome"]
            else:
                benvingut = self.context["benvingut"]

            wf_tool = getToolByName(self.context, 'portal_workflow')
            tools = getMultiAdapter((self.context, self.request), name='plone_tools')
            workflows = tools.workflow().getWorkflowsFor(benvingut)[0]
            benvingut_workflow = wf_tool.getWorkflowsFor(benvingut)[0].id
            benvingut_status = wf_tool.getStatusOf(benvingut_workflow, benvingut)
            if workflows['states'][benvingut_status['review_state']].id == 'published':
                return benvingut.text.raw
            else:
                return None
        except KeyError:
            return None

    def get_populars(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        serveitics = catalog(portal_type='serveitic', sort_on='sortable_title', path='/'.join(self.context.getPhysicalPath()))
        populars = []
        for item in serveitics:
            serveitic = item.getObject()
            if serveitic.popular:
                populars.append(serveitic)
        return populars

    def showFilters(self):
        registry = queryUtility(IRegistry)
        serveistic_tool = registry.forInterface(IServeisTICControlPanelSettings)
        return serveistic_tool.show_filters

    def default_preview_url(self):
        return default_serveistic_url_preview_image()


class ServeisTICPreviewBrain(PreviewBrain):

    def preview_url(self):
        """Get Ad image"""
        site = getSite()
        image_scale = queryMultiAdapter((site, self.request), name="image_scale")
        if not image_scale:
            return None
        try:
            if self.brain.image_item:
                return image_scale.tag(self.brain, "image_item", scale="preview", css_class="card-img-top")
            elif self.brain.image:
                return image_scale.tag(self.brain, "image", scale="preview", css_class="card-img-top")
            else:
                return None
        except AttributeError:
            return None

    def default_preview_url(self):
        return default_serveistic_url_preview_image()
