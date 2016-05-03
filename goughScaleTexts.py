# -*- coding: utf-8 -*-
"""
This module contains the texts of the part (server and remote)
"""

from util.utiltools import get_pluriel
import goughScaleParams as pms
from util.utili18n import le2mtrans
import os
import configuration.configparam as params
import gettext
from collections import OrderedDict


localedir = os.path.join(params.getp("PARTSDIR"), "goughScale", "locale")
trans_GS = gettext.translation(
  "goughScale", localedir, languages=[params.getp("LANG")]).ugettext


def get_histo_head():
    return [le2mtrans(u"Period"), le2mtrans(u"Decision"),
             le2mtrans(u"Period\npayoff"), le2mtrans(u"Cumulative\npayoff")]


def get_text_explanation():
    return trans_GS(u"")


def get_text_summary(period_content):
    txt = trans_GS(u"Summary text")
    return txt


# the key is the variable name and the value the text to display
GS_items = OrderedDict()
GS_items["competent"] = trans_GS(u"Compétent")
GS_items["naturel"] = trans_GS(u"Peu naturel/le")
GS_items["astucieux"] = trans_GS(u"Astucieux/se")
GS_items["prudent"] = trans_GS(u"Prudent/e")
GS_items["confiant"] = trans_GS(u"Confiant/e")
GS_items["tourne_vers_soi"] = trans_GS(u"Tourné/e vers soi")
GS_items["ordinaire"] = trans_GS(u"Ordinaire")
GS_items["drole"] = trans_GS(u"Drôle")
GS_items["conservateur"] = trans_GS(u"Conservateur/trice")
GS_items["individualiste"] = trans_GS(u"Individualiste")
GS_items["conformiste"] = trans_GS(u"Conformiste")
GS_items["decontracte"] = trans_GS(u"Décontracté/e")
GS_items["insatisfait"] = trans_GS(u"Insatisfait/e")
GS_items["clairvoyant"] = trans_GS(u"Clairvoyant/e")
GS_items["mefiant"] = trans_GS(u"Méfiant/e")
GS_items["honnete"] = trans_GS(u"Honnête")
GS_items["intelligent"] = trans_GS(u"Intelligent/e")
GS_items["bien_eleve"] = trans_GS(u"Bien élevé/e")
GS_items["tres_curieux"] = trans_GS(u"Très curieux/se")
GS_items["inventif"] = trans_GS(u"Inventif/ve")
GS_items["imaginatif"] = trans_GS(u"Imaginatif/ve")
GS_items["confiant"] = trans_GS(u"Confiante/e")
GS_items["peu_curieux"] = trans_GS(u"Peu curieux/se")
GS_items["reflechi"] = trans_GS(u"Réfléchi/e")
GS_items["sincere"] = trans_GS(u"Sincère")
GS_items["ingenieux"] = trans_GS(u"Ingénieux/se")
GS_items["confiant_en_soi"] = trans_GS(u"Confiant/e en soi")
GS_items["sexy"] = trans_GS(u"Sexy")
GS_items["soumis"] = trans_GS(u"Soumis/e")
GS_items["snob"] = trans_GS(u"Snob")
GS_items["non_conformiste"] = trans_GS(u"Non conformiste")







