# -*- coding: utf-8 -*-

from Products.statusmessages.interfaces import IStatusMessage

from plone.app.registry.browser import controlpanel
from plone.autoform.directives import read_permission
from plone.autoform.directives import write_permission
from plone.dexterity.interfaces import IDexteritySchema
from plone.supermodel import model
from z3c.form import button
from zope import schema
from zope.ramcache import ram

from genweb6.serveistic import _


class IServeisTICControlPanelSettings(model.Schema, IDexteritySchema):
    """ Global Genweb settings. This describes records stored in the
    configuration registry and obtainable via plone.registry.
    """

    model.fieldset(
        'General',
        _(u'General'),
        fields=['url_info_serveistic', 'show_filters'])

    url_info_serveistic = schema.TextLine(
        title=_(u"URL d'informació de Serveis TIC"),
        description=_(u"URL on enllaça la i de la barra superior del lloc "
                      u"web de Serveis TIC"),
        required=False)

    show_filters = schema.Bool(
        title=_(u"Desplegar filtres de cerca"),
        description=_(u"Desplega el filtres de cerca que trobem a la pàgina  "
                      u"principal"),
        required=False)

    model.fieldset(
        'Servei Web Problemes',
        _(u'Servei Web Problemes'),
        fields=['ws_problemes_endpoint',
                'ws_problemes_login_username', 'ws_problemes_login_password'])

    ws_problemes_endpoint = schema.TextLine(
        title=_(u'URL'),
        required=False)

    ws_problemes_login_username = schema.TextLine(
        title=_(u'Usuari'),
        required=False)

    ws_problemes_login_password = schema.Password(
        title=_(u'Contrasenya'),
        required=False)

    model.fieldset(
        'Servei Web Indicadors',
        _(u'Servei Web Indicadors'),
        fields=['ws_indicadors_service_id',
                'ws_indicadors_endpoint', 'ws_indicadors_key'])

    ws_indicadors_service_id = schema.TextLine(
        title=_(u"Identificador al servei web d'Indicadors"),
        description=_(u"Identificador de Serveis TIC al servei web"),
        required=False)

    ws_indicadors_endpoint = schema.TextLine(
        title=_(u'URL'),
        required=False)

    ws_indicadors_key = schema.Password(
        title=_(u'API key'),
        required=False)

    model.fieldset(
        'Actualitzacio Indicadors',
        _(u"Actualització d'Indicadors"),
        fields=['update_indicadors_passphrase']
    )

    update_indicadors_passphrase = schema.TextLine(
        title=_(u"Contrasenya"),
        description=_(
            u"Contrasenya necessària per a fer servir la vista "
            u"d'actualització (valor del paràmetre 'passphrase')"),
        required=False
    )

    model.fieldset(
        'Google Analytics',
        _(u"Google Analytics"),
        fields=['ga_key_json', 'ga_view_id']
    )

    ga_key_json = schema.Text(
        title=_(u"Clau de la API"),
        description=_(u"Contingut JSON de la clau de la API"),
        required=False
    )

    ga_view_id = schema.TextLine(
        title=_(u"Id de visualització"),
        description=_(
            u"Identificador de la visualització de serveistic.upc.edu"),
        required=False
    )

    # MIGRACIO

    model.fieldset(
        'Migration',
        _(u'Migració'),
        fields=['enable_suscribers'],
    )

    read_permission(enable_suscribers='genweb.webmaster')
    write_permission(enable_suscribers='genweb.manager')
    enable_suscribers = schema.Bool(
        title=_(u'Habilitar notificacions'),
        required=False,
        default=False,
    )


class ServeisTICControlPanelSettingsForm(controlpanel.RegistryEditForm):

    schema = IServeisTICControlPanelSettings
    id = 'ServeisTICControlPanelSettingsForm'
    label = _(u'Genweb ServeisTIC settings')
    description = _(u'help_serveistic_settings_editform',
                    default=u'ServeisTIC configuration.')

    def updateFields(self):
        super(ServeisTICControlPanelSettingsForm, self).updateFields()

    def updateWidgets(self):
        super(ServeisTICControlPanelSettingsForm, self).updateWidgets()

    def fix_password_fields(self, data):
        """
        Keep the stored value for the password fields not updated in the
        current request, i.e. those containing a None value.
        This method is needed since the password fields are not filled with
        their stored value when the edit form is loaded.
        """
        if not data['ws_problemes_login_password']:
            data['ws_problemes_login_password'] = \
                self.getContent().ws_problemes_login_password

        if not data['ws_indicadors_key']:
            data['ws_indicadors_key'] = \
                self.getContent().ws_indicadors_key

    @button.buttonAndHandler(_('Save'), name=None)
    def handleSave(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        self.fix_password_fields(data)
        self.applyChanges(data)

        ram.caches.clear()

        IStatusMessage(self.request).addStatusMessage(_(u'Changes saved'),
                                                      'info')
        self.context.REQUEST.RESPONSE.redirect('@@serveistic-controlpanel')

    @button.buttonAndHandler(_('Cancel'), name='cancel')
    def handleCancel(self, action):
        IStatusMessage(self.request).addStatusMessage(_(u'Edit cancelled'),
                                                      'info')
        self.request.response.redirect('%s/%s' % (self.context.absolute_url(),
                                                  self.control_panel_view))


class ServeisTICControlPanel(controlpanel.ControlPanelFormWrapper):
    form = ServeisTICControlPanelSettingsForm
