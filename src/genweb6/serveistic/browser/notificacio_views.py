# -*- coding: utf-8 -*-

from Products.Five import BrowserView

from plone import api

from genweb6.serveistic.data_access.notificacio import NotificacioDataReporter
from genweb6.serveistic.utilities import get_servei
from genweb6.serveistic.utilities import NotificacioViewHelper


class Notificacions(BrowserView, NotificacioViewHelper):

    @property
    def notificacions(self):
        reporter = NotificacioDataReporter(api.portal.get_tool('portal_catalog'))
        return reporter.list_by_servei(get_servei(self))
