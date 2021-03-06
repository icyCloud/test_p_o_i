# -*- coding: utf-8 -*-

from models import Base
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import BIT, INTEGER, VARCHAR, DATETIME, TIMESTAMP, TINYINT, FLOAT
from tornado.util import ObjectDict

class RoomTypeModel(Base):

    __tablename__ = 'RoomType'
    __table_args__ = {
        'mysql_charset': 'utf8', 'mysql_engine': 'InnoDB'}


    id = Column(INTEGER, primary_key=True, autoincrement=True)
    chain_id = Column("chainId", INTEGER, nullable=False)
    hotel_id = Column('chainHotelId', VARCHAR(60), nullable=False)
    roomtype_id = Column('chainRoomTypeId', VARCHAR(60), nullable=False)
    name = Column('Name', VARCHAR(30), nullable=False)
    room_size = Column('RoomSize', VARCHAR(20), nullable=False)
    bed_type = Column('BedType', TINYINT(4), nullable=False)
    floor = Column('Floor', VARCHAR(30), nullable=False)
    occupancy = Column('Occupancy', TINYINT(4), nullable=False)
    facility = Column('Facility', VARCHAR(250), nullable=False)
    desc = Column('Desc', VARCHAR(200), nullable=False)


    @classmethod
    def get_by_id(cls, session, id):
        return session.query(RoomTypeModel)\
                .filter(RoomTypeModel.id == id)\
                .first()

    @classmethod
    def get_by_ids(cls, session, ids):
        return session.query(RoomTypeModel)\
                .filter(RoomTypeModel.id.in_(ids))\
                .all()

    @classmethod
    def gets_by_hotel_id(cls, session, hotel_id):
        return session.query(RoomTypeModel)\
                .filter(RoomTypeModel.hotel_id == hotel_id)\
                .all()

    @classmethod
    def gets_by_chain_and_hotel_ids(cls, session, chain_id, hotel_ids):
        return session.query(RoomTypeModel)\
                .filter(RoomTypeModel.chain_id == chain_id)\
                .filter(RoomTypeModel.hotel_id.in_(hotel_ids))\
                .all()

    @classmethod
    def gets_by_hotel_ids(cls, session, hotel_ids):
        return session.query(RoomTypeModel)\
                .filter(RoomTypeModel.hotel_id.in_(hotel_ids))\
                .all()

    def todict(self):
        return ObjectDict(
                id=self.id,
                hotel_id=self.hotel_id,
                roomtype_id=self.roomtype_id,
                chain_id=self.chain_id,
                name=self.name,
                room_size=self.room_size,
                bed_type=self.bed_type,
                floor=self.floor,
                occupancy=self.occupancy,
                facility=self.facility,
                desc=self.desc,
                )
