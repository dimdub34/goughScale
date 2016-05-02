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


