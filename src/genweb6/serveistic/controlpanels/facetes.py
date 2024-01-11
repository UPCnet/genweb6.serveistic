# -*- coding: utf-8 -*-
from Products.statusmessages.interfaces import IStatusMessage

from collective.z3cform.datagridfield.datagridfield import DataGridFieldFactory
from collective.z3cform.datagridfield.registry import DictRow
from plone.app.registry.browser import controlpanel
from plone.autoform import directives
from plone.dexterity.interfaces import IDexteritySchema
from plone.supermodel import model
from z3c.form import button
from zope import schema
from zope.ramcache import ram

from genweb6.serveistic import _


class ITableFacetes(model.Schema, IDexteritySchema):

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


class IServeisTICFacetesControlPanelSettings(model.Schema, IDexteritySchema):

    model.fieldset('Facetes', _(u'Facetes'), fields=['facetes_table'])
    directives.widget(facetes_table=DataGridFieldFactory)
    facetes_table = schema.List(
        title=_(u'Facetes'),
        description=_(u'help_facetes_table'),
        value_type=DictRow(schema=ITableFacetes),
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

    @button.buttonAndHandler(_('Save'), name='save')
    def handleSave(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        replace_facetes_table = []
        facetes_table = data.get('facetes_table', [])
        for facet in facetes_table:
            facet['faceta'] = facet['faceta'][0]
            replace_facetes_table.append(facet)

        data['facetes_table'] = replace_facetes_table
        self.applyChanges(data)

        ram.caches.clear()

        IStatusMessage(self.request).addStatusMessage(_("Changes saved"), "info")
        self.request.response.redirect(self.request.getURL())

    @button.buttonAndHandler(_("Cancel"), name='cancel')
    def handleCancel(self, action):
        IStatusMessage(self.request).addStatusMessage(_("Changes canceled."), "info")
        self.request.response.redirect(self.context.absolute_url() + '/' + self.control_panel_view)


class ServeisTICFacetesControlPanel(controlpanel.ControlPanelFormWrapper):
    form = ServeisTICFacetesControlPanelSettingsForm
