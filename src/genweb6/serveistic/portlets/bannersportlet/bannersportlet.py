# -*- coding: utf-8 -*-

from Products.CMFPlone import PloneMessageFactory as _
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone import api
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from zope import schema
from zope.formlib import form
from zope.interface import implementer
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
from zope.component.hooks import getSite

from genweb6.serveistic.utilities import get_servei
from genweb6.serveistic.data_access.banner import BannerDataReporter


def get_vocabulary_type():
    values = [u"Global", u"Local"]
    return SimpleVocabulary([
        SimpleTerm(title=_(value), value=value, token=token)
        for token, value in enumerate(values)])


class IBannersPortlet(IPortletDataProvider):
    """ A portlet which can show actived.
    """
    banner_type = schema.Choice(
        title=_(u"Tipus"),
        required=True,
        vocabulary=get_vocabulary_type())


@implementer(IBannersPortlet)
class Assignment(base.Assignment):

    title = _(u'label_banner_serveis', default=u'Serveis Tic Banners')

    def __init__(self, banner_type=u"Local"):
        self.banner_type = banner_type

    @property
    def title(self):
        return _(u"Banners TIC ({0})".format(
            getattr(self, 'banner_type', '?')))


class Renderer(base.Renderer):

    render = ViewPageTemplateFile('bannersportlet.pt')

    def portal_url(self):
        return self.portal().absolute_url()

    def portal(self):
        return api.portal.get()

    def getBanners(self):
        reporter = BannerDataReporter(api.portal.get_tool("portal_catalog"))

        if self.data.banner_type == u"Local":
            return reporter.list_by_servei(get_servei(self))

        elif self.data.banner_type == u"Global":

            context_path = self.context.getPhysicalPath()
            site = getSite()
            site_path = site.getPhysicalPath()
            relative_path_parts = context_path[len(site_path):]

            if relative_path_parts:
                lang_folder = relative_path_parts[0]
            else:
                lang_folder = 'ca'

            banners_path = '/'.join(site_path + (lang_folder, f'banners-{lang_folder}'))
            banners = reporter.list_by_path(banners_path)

            if not banners:
                banners_path_ca = '/'.join(site_path + ('ca', 'banners-ca'))
                banners = reporter.list_by_path(banners_path_ca)

            return banners

        else:
            return []


    def getAltAndTitle(self, altortitle, open_in_new_window):
        """ Funcio que extreu idioma actiu i afegeix al alt i al title de les imatges del banner
            el literal Obriu l'enllac en una finestra nova.
        """
        if open_in_new_window:
            return '%s, %s' % (altortitle, self.portal().translate(_('obrir_link_finestra_nova', default=u"(obriu en una finestra nova)")))
        else:
            return '%s' % (altortitle)


class AddForm(base.AddForm):
    schema = IBannersPortlet
    label = _(u"Afegeix portlet de notifications")
    description = _(u"Aquest portlet mostra les notificacions")

    def create(self, data):
        return Assignment(
            banner_type=data.get('banner_type', u"Local"))


class EditForm(base.EditForm):
    schema = IBannersPortlet
    label = _(u"Edita el portlet de banners TIC")
    description = _(u"Aquest portlet mostra els banners TIC")
