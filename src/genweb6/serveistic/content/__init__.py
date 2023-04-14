# -*- coding: utf-8 -*-

from plone.app.dexterity.behaviors.metadata import ICategorization
from plone.app.dexterity.textindexer import utils


utils.searchable(ICategorization, 'subjects')