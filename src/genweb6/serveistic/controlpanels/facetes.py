# -*- coding: utf-8 -*-

from collective.z3cform.datagridfield.datagridfield import DataGridFieldFactory
from collective.z3cform.datagridfield.registry import DictRow
from plone.app.registry.browser import controlpanel
from plone.autoform import directives
from plone.supermodel import model
from zope import schema

from genweb6.serveistic import _


class ITableFacetes(model.Schema):
    faceta = schema.Choice(
        title=_(u'Faceta'),
        vocabulary='genweb.serveistic.vocabularies.facets',
        required=False)

    valor = schema.TextLine(
        title=_(u'Valor'),
        required=False)

    valor_es = schema.TextLine(
        title=_(u'Valor ES'),
        required=False)

    valor_en = schema.TextLine(
        title=_(u'Valor EN'),
        required=False)


class IServeisTICFacetesControlPanelSettings(model.Schema):

    model.fieldset('Facetes', _(u'Facetes'), fields=['facetes_table'])
    directives.widget(facetes_table=DataGridFieldFactory)
    facetes_table = schema.List(
        title=_(u'Facetes'),
        description=_(
            u'help_facetes_table',
            default=u'Afegir els valors per facetes de cerca'),
        value_type=DictRow(
            title=_(u'help_facetes_table'),
            schema=ITableFacetes),
        required=False
        )


class ServeisTICFacetesControlPanelSettingsForm(controlpanel.RegistryEditForm):

    schema = IServeisTICFacetesControlPanelSettings
    id = 'ServeisTICFacetesControlPanelSettingsForm'
    label = _(u'Genweb ServeisTIC settings')
    description = _(u'help_serveistic_settings_editform',
                    default=u'ServeisTIC configuration.')

    def updateFields(self):
        super(ServeisTICFacetesControlPanelSettingsForm, self).updateFields()

    def updateWidgets(self):
        super(ServeisTICFacetesControlPanelSettingsForm, self).updateWidgets()


class ServeisTICFacetesControlPanel(controlpanel.ControlPanelFormWrapper):
    form = ServeisTICFacetesControlPanelSettingsForm
