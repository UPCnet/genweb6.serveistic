# -*- coding: utf-8 -*-

from Products.Five import BrowserView

from plone import api

from genweb6.serveistic.data_access.problemes import ProblemesDataReporter
from genweb6.serveistic.utilities import get_ws_problemes_client


class Problemes(BrowserView):

    @property
    def problemes(self):
        reporter = ProblemesDataReporter(api.portal.get_tool("portal_catalog"), get_ws_problemes_client())

        product_id = self.context.product_id
        servei_path = '/'.join(self.context.getPhysicalPath())

        if product_id:
            return reporter.list_by_product_id(product_id)
        elif servei_path:
            return reporter.list_by_servei_path(servei_path)
        else:
            return None
