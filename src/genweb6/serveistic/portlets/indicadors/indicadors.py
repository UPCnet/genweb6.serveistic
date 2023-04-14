# -*- coding: utf-8 -*-

from Products.CMFPlone import PloneMessageFactory as _
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from zope import schema
from zope.formlib import form
from zope.interface import implementer

from genweb6.serveistic.data_access.indicadors import IndicadorsDataReporter
from genweb6.serveistic.data_access.indicadors import IndicadorsDataReporterException
from genweb6.serveistic.utilities import get_servei
from genweb6.serveistic.utilities import get_ws_indicadors_client

import logging

logger = logging.getLogger(name='genweb.serveistic')


class IIndicadorsPortlet(IPortletDataProvider):
    count_indicator = schema.Int(
        title=_(u"Nombre màxim d'indicadors"),
        required=True,
        default=5)

    count_category = schema.Int(
        title=_(u"Nombre màxim de categories"),
        required=False)


@implementer(IIndicadorsPortlet)
class Assignment(base.Assignment):

    def __init__(self, count_indicator=5, count_category=None, showdata=True):
        self.count_indicator = count_indicator
        self.count_category = count_category
        self.showdata = showdata

    @property
    def title(self):
        return _(u"Indicadors")


class Renderer(base.Renderer):
    render = ViewPageTemplateFile('indicadors.pt')

    @property
    def indicadors_href(self):
        servei = get_servei(self)
        return servei.absolute_url() + "/indicadors_list"

    @property
    def indicadors(self):
        reporter = IndicadorsDataReporter(get_ws_indicadors_client(), self.context)

        service_id = self.context.service_id
        if not service_id:
            return None

        try:
            return reporter.list_by_service_id_and_indicators_order(
                service_id, self.context.service_indicators_order, self.data.count_indicator, self.data.count_category)
        except IndicadorsDataReporterException as e:
            logger.warning(
                "Error when listing indicators ({0})".format(e))
            return None


class AddForm(base.AddForm):
    schema = IIndicadorsPortlet
    label = _(u"Afegeix portlet d'indicadors")
    description = _(u"Llistat d'indicadors associats a un Servei TIC")

    def create(self, data):
        return Assignment(
            count_indicator=data.get('count_indicator', 5),
            count_category=data.get('count_category', None),
            showdata=data.get('showdata', True))


class EditForm(base.EditForm):
    schema = IIndicadorsPortlet
    label = _(u"Edita el portlet d'indicadors")
    description = _(u"Llistat d'indicadors associats amb un Servei TIC")
