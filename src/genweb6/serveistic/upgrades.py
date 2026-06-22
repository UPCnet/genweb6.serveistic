# -*- coding: utf-8 -*-
from plone import api

from genweb6.serveistic.setuphandlers import reindex_servei_facetas

import logging
import transaction


logger = logging.getLogger(__name__)

PROFILE_ID = 'profile-genweb6.serveistic:default'

IMPORT_STEPS = (
    'catalog',
    'plone.app.registry',
    'genweb6.serveistic.various',
)


def upgrade_import_profile(context):
    """Reimport serveistic profile steps and reindex servei_facetas."""
    setup = api.portal.get_tool(name='portal_setup')
    for step in IMPORT_STEPS:
        logger.info('Running import step %s for %s', step, PROFILE_ID)
        setup.runImportStepFromProfile(PROFILE_ID, step)
    reindex_servei_facetas()
    transaction.commit()
