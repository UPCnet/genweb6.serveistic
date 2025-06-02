# -*- coding: utf-8 -*-

from Products.Five import BrowserView

from eea.facetednavigation.browser.app.view import FacetedContainerView
from eea.facetednavigation.views.preview import PreviewBrain
from plone import api
from plone.registry.interfaces import IRegistry
from zope.component import getMultiAdapter
from zope.component import queryMultiAdapter
from zope.component import queryUtility
from zope.component.hooks import getSite

from genweb6.serveistic.controlpanels.serveistic import IServeisTICControlPanelSettings
from genweb6.serveistic.data_access.notificacio import NotificacioDataReporter
from genweb6.serveistic.utilities import default_serveistic_url_preview_image
from genweb6.serveistic.utilities import serveistic_config


class FacetedContainerView(FacetedContainerView):

    SHORT_SUMMARY_MAX_LENGTH = 115

    @property
    def notificacions(self):
        reporter = NotificacioDataReporter(api.portal.get_tool('portal_catalog'))
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
                if "benvingut" in self.context:
                    benvingut = self.context["benvingut"]
                else:
                    return None

            wf_tool = api.portal.get_tool("portal_workflow")
            tools = getMultiAdapter((self.context, self.request), name='plone_tools')
            workflows = tools.workflow().getWorkflowsFor(benvingut)[0]
            benvingut_workflow = wf_tool.getWorkflowsFor(benvingut)[0].id
            benvingut_status = wf_tool.getStatusOf(benvingut_workflow, benvingut)
            if workflows['states'][benvingut_status['review_state']].id == 'published' and benvingut.text:
                return benvingut.text.output
            else:
                return None
        except KeyError:
            return None

    def get_populars(self):
        catalog = api.portal.get_tool('portal_catalog')
        serveitics = catalog(portal_type='serveitic', sort_on='sortable_title', path='/'.join(self.context.getPhysicalPath()))
        populars = []
        for item in serveitics:
            serveitic = item.getObject()
            if serveitic.popular:
                populars.append(serveitic)
        return populars

    def showFilters(self):
        request = getattr(self.context, 'REQUEST', None)
        return serveistic_config(request).get('show_filters', False)

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
            servei = self.brain.getObject()
            if servei.image_item:
                return image_scale.tag(self.brain, "image_item", scale="preview", css_class="card-img-top object-fit-cover")
            elif servei.image:
                return image_scale.tag(self.brain, "image", scale="preview", css_class="card-img-top object-fit-cover")
            else:
                return None
        except AttributeError:
            return None

    def default_preview_url(self):
        return default_serveistic_url_preview_image()


class PortletIndicadorsReinstallAll(BrowserView):

    def __call__(self):
        from plone.protect.interfaces import IDisableCSRFProtection
        alsoProvides(self.request, IDisableCSRFProtection)

        service_id_updated = []
        catalog = api.portal.get_tool("portal_catalog")
        for servei in catalog.searchResults(portal_type='serveitic'):
            assignments = self._get_portlet_assignments(
                servei.getObject(), 'genweb.portlets.HomePortletManager5')
            if 'indicadors' in assignments:
                del assignments['indicadors']
            assignments['indicadors'] = IndicadorsAssignment(
                count_indicator=5, count_category=4)
            service_id_updated.append(servei.id)

        report = "{0} serveis have been updated:\n\n".format(
            len(service_id_updated))
        report += '\n'.join(sorted(service_id_updated))
        return report

    def _get_portlet_assignments(self, context, name):
        portlet_manager = queryUtility(
            IPortletManager,
            name=name,
            context=context)
        return getMultiAdapter(
            (context, portlet_manager), IPortletAssignmentMapping)
