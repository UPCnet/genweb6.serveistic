# -*- coding: utf-8 -*-

from eea.facetednavigation import _
from plone.protect.utils import addTokenToUrl


def getMenuItems(self, context, request):
    url = context.absolute_url()

    action = url + "/@@faceted_settings/{0}"
    action = addTokenToUrl(action, request)

    configure = url + "/configure_faceted.html"

    menu = [
        {
            "title": _("Configure"),
            "description": "Configure faceted navigation",
            "action": addTokenToUrl(configure, request),
            "selected": "configure_faceted" in request.URL,
            "icon": "",
            "extra": {
                "id": "configure_faceted_navigation",
                "separator": None,
                "class": "",
            },
            "submenu": None,
        },
    ]

    return menu

