# -*- coding: utf-8 -*-

from genweb6.core.browser.viewlets import headerViewlet as headerViewletBase
from genweb6.core.browser.viewlets import heroViewlet as heroViewletBase
from genweb6.serveistic import _
from genweb6.serveistic.content.serveitic.serveitic import IServeiTIC
from genweb6.serveistic.utilities import get_servei


class headerViewlet(headerViewletBase):

  def custom_search(self):
    servei = get_servei(self)
    
    if not servei:
      return {'literal': None,
              'path': None}
    
    return {'literal': _(u'Cerca en el servei'),
            'path': '/'.join(servei.getPhysicalPath()[0:5])}
    

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
    