# -*- coding: utf-8 -*-

import logging
from datetime import datetime
from twisted.internet import defer
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, Float, ForeignKey, Boolean
from server.servbase import Base
from server.servparties import Partie
from util.utiltools import get_module_attributes
import goughScaleParams as pms


logger = logging.getLogger("le2m")


class PartieGS(Partie):
    __tablename__ = "partie_goughScale"
    __mapper_args__ = {'polymorphic_identity': 'goughScale'}
    partie_id = Column(Integer, ForeignKey('parties.id'), primary_key=True)
    repetitions = relationship('RepetitionsGS')

    def __init__(self, le2mserv, joueur):
        super(PartieGS, self).__init__(
            nom="goughScale", nom_court="GS",
            joueur=joueur, le2mserv=le2mserv)
        self.GS_gain_ecus = 0
        self.GS_gain_euros = 0

    @defer.inlineCallbacks
    def configure(self):
        logger.debug(u"{} Configure".format(self.joueur))
        yield (self.remote.callRemote("configure", get_module_attributes(pms)))
        self.joueur.info(u"Ok")

    @defer.inlineCallbacks
    def newperiod(self, period):
        """
        Create a new period and inform the remote
        If this is the first period then empty the historic
        :param periode:
        :return:
        """
        logger.debug(u"{} New Period".format(self.joueur))
        self.currentperiod = RepetitionsGS(period)
        self.le2mserv.gestionnaire_base.ajouter(self.currentperiod)
        self.repetitions.append(self.currentperiod)
        yield (self.remote.callRemote("newperiod", period))
        logger.info(u"{} Ready for period {}".format(self.joueur, period))

    @defer.inlineCallbacks
    def display_decision(self):
        """
        Display the decision screen on the remote
        Get back the decision
        :return:
        """
        logger.debug(u"{} Decision".format(self.joueur))
        debut = datetime.now()
        decisions = yield(self.remote.callRemote(
            "display_decision"))
        self.currentperiod.GS_decisiontime = (datetime.now() - debut).seconds
        for k, v in decisions:
            setattr(self.currentperiod, "GS_{}".format(k), v)
        self.joueur.info(u"Ok")
        self.joueur.remove_waitmode()

    def compute_periodpayoff(self):
        """
        Compute the payoff for the period
        :return:
        """
        logger.debug(u"{} Period Payoff".format(self.joueur))
        self.currentperiod.GS_periodpayoff = 0

        # cumulative payoff since the first period
        if self.currentperiod.GS_period < 2:
            self.currentperiod.GS_cumulativepayoff = \
                self.currentperiod.GS_periodpayoff
        else: 
            previousperiod = self.periods[self.currentperiod.GS_period - 1]
            self.currentperiod.GS_cumulativepayoff = \
                previousperiod.GS_cumulativepayoff + \
                self.currentperiod.GS_periodpayoff

        # we store the period in the self.periodes dictionnary
        self.periods[self.currentperiod.GS_period] = self.currentperiod

        logger.debug(u"{} Period Payoff {}".format(
            self.joueur,
            self.currentperiod.GS_periodpayoff))

    @defer.inlineCallbacks
    def display_summary(self, *args):
        """
        Send a dictionary with the period content values to the remote.
        The remote creates the text and the history
        :param args:
        :return:
        """
        logger.debug(u"{} Summary".format(self.joueur))
        yield(self.remote.callRemote(
            "display_summary", self.currentperiod.todict()))
        self.joueur.info("Ok")
        self.joueur.remove_waitmode()

    @defer.inlineCallbacks
    def compute_partpayoff(self):
        """
        Compute the payoff for the part and set it on the remote.
        The remote stores it and creates the corresponding text for display
        (if asked)
        :return:
        """
        logger.debug(u"{} Part Payoff".format(self.joueur))

        self.GS_gain_ecus = self.currentperiod.GS_cumulativepayoff
        self.GS_gain_euros = float(self.GS_gain_ecus) * float(pms.TAUX_CONVERSION)
        yield (self.remote.callRemote(
            "set_payoffs", self.GS_gain_euros, self.GS_gain_ecus))

        logger.info(u'{} Payoff ecus {} Payoff euros {:.2f}'.format(
            self.joueur, self.GS_gain_ecus, self.GS_gain_euros))


class RepetitionsGS(Base):
    __tablename__ = 'partie_goughScale_repetitions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    partie_partie_id = Column(
        Integer,
        ForeignKey("partie_goughScale.partie_id"))

    GS_period = Column(Integer)
    GS_competent = Column(Boolean)
    GS_naturel = Column(Boolean)
    GS_astucieux = Column(Boolean)
    GS_prudent = Column(Boolean)
    GS_confiant = Column(Boolean)
    GS_tourne_vers_soi = Column(Boolean)
    GS_ordinaire = Column(Boolean)
    GS_drole = Column(Boolean)
    GS_conservateur = Column(Boolean)
    GS_individualiste = Column(Boolean)
    GS_conformiste = Column(Boolean)
    GS_decontracte = Column(Boolean)
    GS_insatisfait = Column(Boolean)
    GS_clairvoyant = Column(Boolean)
    GS_mefiant = Column(Boolean)
    GS_honnete = Column(Boolean)
    GS_intelligent = Column(Boolean)
    GS_bien_eleve = Column(Boolean)
    GS_tres_curieux = Column(Boolean)
    GS_inventif = Column(Boolean)
    GS_imaginatif = Column(Boolean)
    GS_peu_curieux = Column(Boolean)
    GS_reflechi = Column(Boolean)
    GS_sincere = Column(Boolean)
    GS_ingenieux = Column(Boolean)
    GS_confiant_en_soi = Column(Boolean)
    GS_sexy = Column(Boolean)
    GS_soumis = Column(Boolean)
    GS_snob = Column(Boolean)
    GS_non_conformiste = Column(Boolean)
    GS_decisiontime = Column(Integer)
    GS_periodpayoff = Column(Float)
    GS_cumulativepayoff = Column(Float)

    def __init__(self, period):
        self.GS_decisiontime = 0
        self.GS_periodpayoff = 0
        self.GS_cumulativepayoff = 0

    def todict(self, joueur=None):
        temp = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        if joueur:
            temp["joueur"] = joueur
        return temp

