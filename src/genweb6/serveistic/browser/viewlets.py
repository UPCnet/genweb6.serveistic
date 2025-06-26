# -*- coding: utf-8 -*-
from eea.facetednavigation.subtypes.interfaces import IFacetedNavigable
from html import escape
from plone.app.multilingual.interfaces import ILanguageRootFolder
from plone.base.utils import safe_text
from zope.component import getMultiAdapter

from genweb6.core.browser.viewlets import GWGlobalSectionsViewlet
from genweb6.core.browser.viewlets import headerViewlet as headerViewletBase
from genweb6.core.browser.viewlets import heroViewlet as heroViewletBase
from genweb6.core.interfaces import IHomePage
from genweb6.core.utils import genwebHeaderConfig
from genweb6.serveistic import _
from genweb6.serveistic.content.serveitic.serveitic import IServeiTIC
from genweb6.serveistic.utilities import get_servei
from genweb6.upc.browser.viewlets import titleViewlet

import re


class headerViewlet(headerViewletBase):

  @property
  def servei(self):
    return get_servei(self)

  def custom_search(self):
    servei = self.servei

    if not servei:
      return {'literal': None,
              'path': None}

    return {'literal': _(u'Cerca en el servei'),
            'path': '/'.join(servei.getPhysicalPath()[0:5])}


class heroViewlet(heroViewletBase, GWGlobalSectionsViewlet):

  @property
  def servei(self):
    return get_servei(self)

  def custom_hero(self):
    servei = self.servei

    if not servei:
      return {'is_servei': False}

    servei_url = servei.absolute_url()

    if servei.image:
      image_url = servei_url + '/@@images/image'
    else:
      base_hero = self.getHeroHeader()
      image_url = base_hero if base_hero else None

    return {'is_servei': True,
            'is_title_servei_h1': IServeiTIC.providedBy(self.context),
            'servei_url': servei_url,
            'image': image_url,
            'title': servei.title}

  @property
  def navtree_path(self):
    return '/'.join(self.servei.getPhysicalPath())

  @property
  def portal_tabs(self):
    return []

  def customize_query(self, query):
    query.pop('Language')

  def render_serveinav(self):
    return self.build_tree('/'.join(self.servei.getPhysicalPath()))

  def isHomepage(self):
    if IHomePage.providedBy(self.context):

      # Homepage normal
      if ILanguageRootFolder.providedBy(self.context) and self.request.steps[-1] == 'homepage':
          return True

      # Homepage con tiles
      parent = self.context.aq_parent
      if ILanguageRootFolder.providedBy(parent) and hasattr(parent, 'default_page') and parent.default_page == self.context.id and self.request.steps[-1] == 'layout_view':
          return True

    else:
      return ILanguageRootFolder.providedBy(self.context) and IFacetedNavigable.providedBy(self.context)


class titleViewletServeistic(titleViewlet):

  @property
  def servei(self):
    return get_servei(self)

  def update(self):
    super(titleViewletServeistic, self).update()
    portal_state = getMultiAdapter(
      (self.context, self.request), name="plone_portal_state"
    )

    context_state = getMultiAdapter(
      (self.context, self.request), name="plone_context_state"
    )

    page_title = escape(safe_text(context_state.object_title()))
    seo_title = getattr(self.context, 'seo_title', None)
    if seo_title:
      page_title = escape(safe_text(seo_title))

    portal_title = escape(safe_text(portal_state.navigation_root_title()))

    genweb_title = getattr(genwebHeaderConfig(), 'html_title_%s' % self.pref_lang(), 'Genweb UPC')

    if not genweb_title:
      genweb_title = 'Genweb UPC'

    genweb_title = escape(safe_text(re.sub(r'(<.*?>)', r'', genweb_title)))

    marca_UPC = escape(safe_text(u"UPC. Universitat Politècnica de Catalunya"))

    if page_title == portal_title:
      self.site_title = u"%s &mdash; %s" % (genweb_title, marca_UPC)
    else:
      servei = self.servei
      if servei and hasattr(servei, 'title') and page_title != escape(safe_text(servei.title)):
        self.site_title = u"%s &mdash; %s &mdash; %s &mdash; %s" % (page_title, escape(safe_text(servei.title)), genweb_title, marca_UPC)
      else:
        self.site_title = u"%s &mdash; %s &mdash; %s" % (page_title, genweb_title, marca_UPC)