# -*- coding: utf-8 -*-
"""
This module contains the GUI
"""

import logging
from PyQt4 import QtGui, QtCore
from util.utili18n import le2mtrans
import goughScaleParams as pms
from goughScaleTexts import trans_GS
import goughScaleTexts as texts_GS
from client.cltgui.cltguiwidgets import WExplication
import random


logger = logging.getLogger("le2m")


class GuiDecision(QtGui.QDialog):
    def __init__(self, defered, automatique, parent):
        super(GuiDecision, self).__init__(parent)

        # variables
        self._defered = defered
        self._automatique = automatique

        layout = QtGui.QVBoxLayout(self)

        wexplanation = WExplication(
            text=texts_GS.get_text_explanation(),
            size=(450, 80), parent=self)
        layout.addWidget(wexplanation)

        grid = QtGui.QGridLayout()
        layout.addLayout(grid)

        self._checkboxes = {}
        row, col = 0, 0
        for k, v in texts_GS.GS_items.viewitems():
            check = QtGui.QCheckBox()
            check.setText(v)
            self._checkboxes[k] = check
            grid.addWidget(check, row, col)
            col += 1
            if col == 5:
                row += 1
                col = 0

        buttons = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok)
        buttons.accepted.connect(self._accept)
        layout.addWidget(buttons)

        self.setWindowTitle(trans_GS(u"Title"))
        self.adjustSize()
        self.setFixedSize(self.size())

        if self._automatique:
            for v in self._checkboxes.viewvalues():
                v.setChecked(bool(random.randint(0, 1)))
            self._timer_automatique = QtCore.QTimer()
            self._timer_automatique.timeout.connect(
                buttons.button(QtGui.QDialogButtonBox.Ok).click)
            self._timer_automatique.start(7000)
                
    def reject(self):
        pass
    
    def _accept(self):
        try:
            self._timer_automatique.stop()
        except AttributeError:
            pass

        inputs = {}
        for k, v in self._checkboxes.viewitems():
            inputs[k] = v.isChecked()

        if not self._automatique:
            confirmation = QtGui.QMessageBox.question(
                self, le2mtrans(u"Confirmation"),
                le2mtrans(u"Do you confirm your choices?"),
                QtGui.QMessageBox.No | QtGui.QMessageBox.Yes)
            if confirmation != QtGui.QMessageBox.Yes: 
                return
        logger.info(u"Send back {}".format(inputs))
        self.accept()
        self._defered.callback(inputs)
