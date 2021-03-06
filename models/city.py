# -*- coding: utf-8 -*-

from models import Base
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import BIT, INTEGER, VARCHAR, DATETIME
from tornado.util import ObjectDict

import cache

class CityModel(Base):

    __tablename__ = 'city'
    __table_args__ = {
        'mysql_charset': 'utf8', 'mysql_engine': 'InnoDB'}

    id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    name = Column(VARCHAR(45), nullable=False)
    qunar_id = Column('qunarId', VARCHAR(50), nullable=False)
    elong_id = Column('elongId', VARCHAR(50), nullable=False)
    ctrip_id = Column('ctripId', INTEGER(unsigned=True), nullable=False)
    prov_id = Column('provId', INTEGER(unsigned=True), nullable=False)

    MC_ALL_CITY = __tablename__ + "mc_all_city"
    MC_ALL_CITY_DICT = __tablename__ + "mc_all_city_dict"

    @classmethod
    @cache.mc(MC_ALL_CITY)
    def get_all(cls, session):
        return session.query(CityModel).all()

    @classmethod
    @cache.mc(MC_ALL_CITY_DICT)
    def get_all_dicts(cls, session):
        citys = cls.get_all(session)
        return [city.todict() for city in citys]

    @classmethod
    def get_by_ids(cls, session, ids):
        return session.query(CityModel)\
                .filter(CityModel.id.in_(ids))\
                .all()

    def todict(self):
        return ObjectDict(
                id=self.id,
                name=self.name,
                prov_id=self.prov_id,
                )

