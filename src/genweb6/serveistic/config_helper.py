# -*- coding: utf-8 -*-

from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

import configparser
import os


def get_absolute_path(relative_path):
    return os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        relative_path)


def build_facets_vocabulary():
    facets = ["Proveïdor / Unitat",
              "Usuaris",
              "Servei / Àrea",
              "Àmbit",
              "Faceta 1",
              "Faceta 2",
              "Faceta 3",
              "Faceta 4",
              "Faceta 5",
              "Faceta 6",
              "Faceta 7",
              "Faceta 8"]

    return SimpleVocabulary([
        SimpleTerm(
            title=facet,
            value=facet,
            token=index)
        for index, facet in enumerate(facets)])

config = configparser.ConfigParser()
config.read(get_absolute_path('serveistic.cfg'))

facets_vocabulary = build_facets_vocabulary()
