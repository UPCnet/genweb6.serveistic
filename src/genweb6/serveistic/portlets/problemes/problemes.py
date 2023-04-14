# -*- coding: utf-8 -*-

from Products.CMFPlone import PloneMessageFactory as _
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone import api
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from zope import schema
from zope.formlib import form
from zope.interface import implementer

from genweb6.serveistic.data_access.problemes import ProblemesDataReporter
from genweb6.serveistic.utilities import get_servei
from genweb6.serveistic.utilities import get_ws_problemes_client


class IProblemesPortlet(IPortletDataProvider):

    count = schema.Int(
        title=_(u'Nombre màxim de problemes'),
        required=True,
        default=5)


@implementer(IProblemesPortlet)
class Assignment(base.Assignment):

    def __init__(self, count=5, showdata=True):
        self.count = count
        self.showdata = showdata

    @property
    def title(self):
        return _(u"Problemes")


class Renderer(base.Renderer):
    render = ViewPageTemplateFile('problemes.pt')

    @property
    def problemes(self):
        reporter = ProblemesDataReporter(api.portal.get_tool("portal_catalog"), get_ws_problemes_client())

        product_id = self.context.product_id
        servei_path = '/'.join(self.context.getPhysicalPath())

        if product_id:
            return reporter.list_by_product_id(product_id, self.data.count)
        elif servei_path:
            return reporter.list_by_servei_path(servei_path, self.data.count)
        else:
            return None

    @property
    def problemes_href(self):
        servei = get_servei(self)
        return servei.absolute_url() + "/problemes_list"


class AddForm(base.AddForm):
    schema = IProblemesPortlet
    label = _(u"Afegeix portlet de problemes")
    description = _(u"Llistat de problemes associats a un Servei TIC")

    def create(self, data):
        return Assignment(
            count=data.get('count', 5),
            showdata=data.get('showdata', True))


class EditForm(base.EditForm):
    schema = IProblemesPortlet
    label = _(u"Edita el portlet de problemes")
    description = _(u"Llistat de problemes associats amb un Servei TIC")
