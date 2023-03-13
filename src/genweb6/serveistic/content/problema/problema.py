# -*- coding: utf-8 -*-

from Products.Five.browser import BrowserView

from plone.dexterity.content import Item
from plone.supermodel import model
from zope import schema
from zope.interface import implementer

from genweb6.serveistic import _


class IProblema(model.Schema):

    title = schema.TextLine(
        title=_(u"Assumpte"),
        required=True,
    )

    description = schema.Text(
        title=_(u"Descripció"),
        required=False,
    )

    data_creacio = schema.Date(
        title=_(u"Data de creació"),
        required=False,
    )

    url = schema.TextLine(
        title=_(u"URL"),
        description=_(
            u"Direcció URL amb informació addicional sobre el problema"),
        required=False)

    data_resolucio = schema.Date(
        title=_(u"Data estimada de resolució"),
        required=False,
    )


@implementer(IProblema)
class Problema(Item):

    @property
    def b_icon_expr(self):
        return "exclamation-triangle-fill"


class View(BrowserView):
    pass
