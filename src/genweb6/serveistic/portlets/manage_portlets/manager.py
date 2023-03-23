# -*- coding: utf-8 -*-

from AccessControl import getSecurityManager
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.app.layout.viewlets.common import ManagePortletsFallbackViewlet

from genweb6.core.browser.viewlets import viewletBase
from genweb6.core.portlets.manage_portlets.manager import gwManagePortletsFallbackViewletMixin


class gwManagePortletsFallbackViewletForServeiTic(gwManagePortletsFallbackViewletMixin, ManagePortletsFallbackViewlet, viewletBase):
    """ The override for the manage_portlets_fallback viewlet for IServeiTIC
    """

    index = ViewPageTemplateFile("templates/manage_portlets_fallback_serveitic.pt")

    def available(self):
        secman = getSecurityManager()
        if secman.checkPermission('Genweb: Manage home portlets', self.context):
            if self.request.steps[-1] in ['view']:
                return True
        return False

