# -*- coding: utf-8 -*-

from plone import api

from genweb6.core.indicators import ReporterException
from genweb6.core.indicators import WebServiceReporter
from genweb6.serveistic.indicators.registry import get_registry
from genweb6.serveistic.utilities import serveistic_config

import transaction


def update_indicators_if_state(content, state, service=None, indicator=None, after_commit=False):
    workflow_tool = api.portal.get_tool("portal_workflow")
    if workflow_tool.getInfoFor(content, 'review_state') in state:
        update_indicators(content, service, indicator, after_commit)


def update_indicators(context, service=None, indicator=None, after_commit=False):
    if after_commit:
        transaction.get().addAfterCommitHook(
            update_after_commit_hook,
            kws=dict(context=context, service=service, indicator=indicator))
    else:
        update(context, service, indicator)


def update_after_commit_hook(is_commit_successful, context, service, indicator):
    if not is_commit_successful:
        return
    update(context, service, indicator)


def update(context, service, indicator):
    st_tools = serveistic_config()
    ws_url = st_tools.get('ws_indicadors_endpoint', '')
    ws_key = st_tools.get('ws_indicadors_key', '')
    registry = get_registry(context)

    reporter = WebServiceReporter(ws_url, ws_key)
    reporter.report(get_data_to_report(registry, service, indicator))


def get_data_to_report(registry, service, indicator):
    if not service:
        return registry

    if not indicator:
        if service not in registry:
            raise ReporterException(
                "Service '{0}' was not found in registry".format(service))
        return registry[service]

    if service not in registry or indicator not in registry[service]:
        raise ReporterException(
            "Indicator '{0}' of service '{1}' was not found in "
            "registry".format(indicator, service))
    return registry[service][indicator]
