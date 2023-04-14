# -*- coding: utf-8 -*-
from Products.Five import BrowserView

from genweb6.core.indicators import RegistryException
from genweb6.core.indicators import ReporterException
from genweb6.serveistic.data_access.indicadors import IndicadorsDataReporter
from genweb6.serveistic.data_access.indicadors import IndicadorsDataReporterException
from genweb6.serveistic.indicators.updating import update_indicators
from genweb6.serveistic.utilities import get_servei
from genweb6.serveistic.utilities import get_ws_indicadors_client
from genweb6.serveistic.utilities import serveistic_config

import logging

logger = logging.getLogger(name='genweb6.serveistic')


class Indicadors(BrowserView):

    def parse_parameters(self):
        try:
            count_indicator = int(
                self.request.form.get('count_indicator', None))
        except (TypeError, ValueError):
            count_indicator = None

        try:
            count_category = int(self.request.form.get('count_category', None))
        except (TypeError, ValueError):
            count_category = None

        apply_order = True if self.request.form.get(
            'apply_order', 'no') in ('yes', 'true') else False

        return count_indicator, count_category, apply_order

    @property
    def count(self):
        return self.parse_parameters()[0]

    @property
    def indicadors_href(self):
        servei = get_servei(self)
        return servei.absolute_url() + "/indicadors_list"

    @property
    def indicadors(self):
        reporter = IndicadorsDataReporter(
            get_ws_indicadors_client(), self.context)

        count_indicator, count_category, apply_order = self.parse_parameters()
        service_id = self.context.service_id
        service_indicators_order = (
            self.context.service_indicators_order if apply_order else None)

        if not service_id:
            return None

        try:
            return reporter.list_by_service_id_and_indicators_order(
                service_id, service_indicators_order,
                count_indicator, count_category)
        except IndicadorsDataReporterException as e:
            logger.warning(
                "Error when listing indicators ({0})".format(e))
            return None


class UpdateIndicadors(BrowserView):

    def render(self):
        if not self._is_authorised():
            self._set_unauthorised_response()
            return
        try:
            for indicator in (
                    'visita-n-data_mes',
                    'visita-n-data_setmana',
                    'visita-n-data_ahir'):
                update_indicators(
                    self.context,
                    service=serveistic_config().ws_indicadors_service_id,
                    indicator=indicator)
            return "Indicators were successfully reported"
        except (RegistryException, ReporterException) as e:
            self.request.response.setStatus(500)
            logger.warning(
                "Error while reporting indicators ({0})".format(e))
            self.request.response.setBody("Error while reporting indicators")

    def _is_authorised(self):
        passphrase = serveistic_config().update_indicadors_passphrase
        return self._parse_passphrase() == passphrase

    def _parse_passphrase(self):
        return self.request.form.get('passphrase', None)

    def _set_unauthorised_response(self):
        self.request.response.setStatus(401)
        self.request.response.setBody(
            "Unauthorized")
