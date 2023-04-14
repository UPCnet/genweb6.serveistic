# -*- coding: utf-8 -*-

from plone.app.layout.navigation.root import getNavigationRoot
from plone.base.interfaces import INavigationSchema
from plone.base.utils import safe_callable
from plone.registry.interfaces import IRegistry
from zope.component import getUtility

from genweb6.core.browser.viewlets import linksFooterViewlet as linksFooterViewletBase
from genweb6.core.browser.viewlets import headerViewlet as headerViewletBase
from genweb6.core.browser.viewlets import heroViewlet as heroViewletBase
from genweb6.serveistic import _
from genweb6.serveistic.content.serveitic.serveitic import IServeiTIC
from genweb6.serveistic.utilities import get_servei


class customizeEntries():
  
  def _getNavQuery(self):
    registry = getUtility(IRegistry)
    navigation_settings = registry.forInterface(
        INavigationSchema, prefix="plone", check=False
    )
    customQuery = getattr(self.context, "getCustomNavQuery", False)
    if customQuery is not None and safe_callable(customQuery):
        query = customQuery()
    else:
        query = {}

    query["path"] = {"query": getNavigationRoot(self.context), "depth": 1}
    query["portal_type"] = tuple([pt for pt in navigation_settings.displayed_types if pt != 'serveitic'])
    query["sort_on"] = navigation_settings.sort_tabs_on
    if navigation_settings.sort_tabs_reversed:
        query["sort_order"] = "reverse"
    else:
        query["sort_order"] = "ascending"

    if navigation_settings.filter_on_workflow:
        query["review_state"] = navigation_settings.workflow_states_to_show

    query["is_default_page"] = False

    if not navigation_settings.show_excluded_items:
        query["exclude_from_nav"] = False

    if not navigation_settings.nonfolderish_tabs:
        query["is_folderish"] = True
        
    return query


class headerViewlet(headerViewletBase):

  def custom_search(self):
    servei = get_servei(self)
    
    if not servei:
      return {'literal': None,
              'path': None}
    
    return {'literal': _(u'Cerca en el servei'),
            'path': '/'.join(servei.getPhysicalPath()[0:5])}

  
  def customize_query(self, query):
    query['portal_type']['query'] = tuple([pt for pt in self.settings.displayed_types if pt != 'serveitic'])
    

class linksFooterViewlet(linksFooterViewletBase):
  
  def customize_query(self, query):
    query['portal_type']['query'] = tuple([pt for pt in self.settings.displayed_types if pt != 'serveitic'])


class heroViewlet(heroViewletBase):
  
  def custom_hero(self):
    servei = get_servei(self)
    
    if not servei:
      return {'is_servei': False}     
    
    servei_url = '/'.join(servei.getPhysicalPath()[0:5]) 
    
    if servei.image:
      image_url = servei_url + '/@@images/image'
    else:
      base_hero = self.getHeroHeader()
      image_url = base_hero['src'] if base_hero else None
      
    return {'is_servei': True,
            'is_current_servei': IServeiTIC.providedBy(self.context),
            'servei_url': servei_url,
            'image': image_url,
            'title': servei.title} 
    