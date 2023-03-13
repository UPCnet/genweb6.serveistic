# -*- coding: utf-8 -*-

from Products.Five.browser import BrowserView

from plone.app.dexterity import textindexer
from plone.app.textfield import RichText
from plone.dexterity.browser import add
from plone.dexterity.browser import edit
from plone.dexterity.content import Item
from plone.indexer import indexer
from plone.supermodel import model
from z3c.form import interfaces
from zope import schema
from zope.interface import implementer
from zope.schema.vocabulary import SimpleVocabulary

from genweb6.serveistic import _
from genweb6.serveistic.utilities import build_vocabulary
from genweb6.serveistic.utilities import get_servei


tipus_values = [u"Avís", u"Notificació", u"Novetat"]


class INotificacioTIC(model.Schema):

    title = schema.TextLine(
        title=_(u"Títol"),
        required=True)

    description = schema.Text(
        title=_(u"Descripció"),
        required=False,
    )

    cos = RichText(
        title=_(u"Cos de la notificació"),
        required=True,
    )

    textindexer.searchable('tipus')
    tipus = schema.Choice(
        title=_(u'Tipus de notificació'),
        required=True,
        vocabulary=SimpleVocabulary(build_vocabulary(tipus_values)))

    is_general = schema.Bool(
        title=_(u"Fes que aparegui a la pàgina d'inici"),
        description=_(u"Marca la caixa si vols que la notificació aparegui "
                      u"també a la pàgina d'inici"),
        required=False)


@indexer(INotificacioTIC)
def tipus(context):
    return context.tipus


class AddForm(add.DefaultAddForm):

    def updateFields(self):
        super(AddForm, self).updateWidgets()
        if not get_servei(self):
            self.widgets['is_general'].mode = interfaces.HIDDEN_MODE
            self.widgets['is_general'].value = True


class AddView(add.DefaultAddView):
    form = AddForm


class EditForm(edit.DefaultEditForm):

    def updateFields(self):
        super(EditForm, self).updateWidgets()
        if not get_servei(self):
            self.widgets['is_general'].mode = interfaces.HIDDEN_MODE


@implementer(INotificacioTIC)
class NotificacioTIC(Item):

    @property
    def b_icon_expr(self):
        return "exclamation-circle-fill"


class View(BrowserView):
    pass
