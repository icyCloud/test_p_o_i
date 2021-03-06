# -*- coding: utf-8 -*-

from models import Base
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import BIT, INTEGER, VARCHAR, DATETIME, TIMESTAMP, TINYINT
from sqlalchemy.sql import exists, text
from tornado.util import ObjectDict
from sqlalchemy import  or_, and_


class RoomTypeMappingModel(Base):

    __tablename__ = 'roomTypeMapping'
    __table_args__ = {
        'mysql_charset': 'utf8', 'mysql_engine': 'InnoDB'}

    STATUS = ObjectDict({
        'init': 0,
        'wait_first_valid': 1,
        'wait_second_valid': 2,
        'valid_complete': 3
            })


    id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    provider_id = Column('chainId', INTEGER(unsigned=True), nullable=False)
    provider_hotel_id = Column('chainHotelId', VARCHAR(50), nullable=False)
    provider_roomtype_id = Column('chainRoomTypeId', VARCHAR(50), nullable=False)
    provider_roomtype_name = Column('chainRoomTypeName', VARCHAR(50), nullable=False)
    main_hotel_id = Column('mainHotelId', INTEGER(unsigned=True), nullable=False)
    main_roomtype_id = Column('mainRoomTypeId', INTEGER(unsigned=True), nullable=False)
    status = Column(TINYINT(4, unsigned=True), nullable=False)
    match_status = Column('match_status', TINYINT(4, unsigned=True), nullable=False, default=1)
    is_online = Column('onlineStatus', INTEGER, nullable=False, default=0)
    is_delete = Column('isDelete', BIT, nullable=False, default=0)
    is_new =  Column('isNew', BIT, nullable=False, default=0)
    ts_update = Column('tsUpdate', TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    info = Column(VARCHAR(100))

    @classmethod
    def new_roomtype_mapping_from_ebooking(cls, session, provider_hotel_id, provider_roomtype_id, provider_roomtype_name, main_hotel_id, main_roomtype_id):
        mapping = RoomTypeMappingModel(provider_id=6, provider_hotel_id=str(provider_hotel_id), provider_roomtype_id=provider_roomtype_id, provider_roomtype_name=provider_roomtype_name, main_hotel_id=main_hotel_id, main_roomtype_id=main_roomtype_id, status=cls.STATUS.valid_complete, is_new=1)
        session.add(mapping)
        session.commit()
        return mapping

    @classmethod
    def get_by_provider_roomtype(cls, session, provider_id, provider_roomtype_id,chain_hotel_id):
        return session.query(RoomTypeMappingModel)\
                .filter(RoomTypeMappingModel.provider_id == provider_id)\
                .filter(RoomTypeMappingModel.provider_hotel_id==str(chain_hotel_id))\
                .filter(RoomTypeMappingModel.provider_roomtype_id == str(provider_roomtype_id))\
                .filter(RoomTypeMappingModel.is_delete == 0)\
                .first()

    @classmethod
    def get_by_provider_and_main_roomtype(cls, session, provider_id, provider_roomtype_id, main_roomtype_id,chain_hotel_id,is_delete=0):
        query = session.query(RoomTypeMappingModel)\
                .filter(RoomTypeMappingModel.provider_id == provider_id)\
                .filter(RoomTypeMappingModel.provider_hotel_id==str(chain_hotel_id))\
                .filter(RoomTypeMappingModel.provider_roomtype_id == str(provider_roomtype_id),
                        RoomTypeMappingModel.main_roomtype_id == main_roomtype_id)
        if is_delete != -1:
            query.filter(RoomTypeMappingModel.is_delete == is_delete)
        return query.first()


    @classmethod
    def get_by_id(cls, session, id):
        return session.query(RoomTypeMappingModel)\
                .filter(RoomTypeMappingModel.id == id, RoomTypeMappingModel.is_delete == 0)\
                .first()

    @classmethod
    def get_by_ids(cls, session, ids):
        return session.query(RoomTypeMappingModel)\
                .filter(RoomTypeMappingModel.id.in_(ids))\
                .filter(RoomTypeMappingModel.is_delete == 0)\
                .all()

    @classmethod
    def gets_by_provider_hotel_id(cls, session, id):
        return session.query(RoomTypeMappingModel)\
                .filter(RoomTypeMappingModel.provider_hotel_id == str(id))\
                .filter(RoomTypeMappingModel.is_delete == 0)\
                .all()

    @classmethod
    def get_by_provider_hotel_ids(cls, session, ids):
        return session.query(RoomTypeMappingModel)\
                .filter(RoomTypeMappingModel.provider_hotel_id.in_(ids))\
                .filter(RoomTypeMappingModel.is_delete == 0)\
                .all()

    @classmethod
    def get_firstvalid_by_provider_hotel_ids(cls, session, ids):
        return session.query(RoomTypeMappingModel)\
                .filter(RoomTypeMappingModel.provider_hotel_id.in_(ids))\
                .filter(RoomTypeMappingModel.is_delete == 0)\
                .filter(RoomTypeMappingModel.status != cls.STATUS.init)\
                .all()

    @classmethod
    def get_secondvalid_by_provider_hotel_ids(cls, session, ids):
        return session.query(RoomTypeMappingModel)\
                .filter(RoomTypeMappingModel.provider_hotel_id.in_(ids))\
                .filter(RoomTypeMappingModel.is_delete == 0)\
                .filter(or_(RoomTypeMappingModel.status == cls.STATUS.wait_second_valid,RoomTypeMappingModel.status == cls.STATUS.valid_complete))\
                .all()

    @classmethod
    def get_polymer_provider_hotel_ids(cls, session, ids):
        return session.query(RoomTypeMappingModel)\
                .filter(RoomTypeMappingModel.provider_hotel_id.in_(ids))\
                .filter(RoomTypeMappingModel.is_delete == 0)\
                .filter(RoomTypeMappingModel.status == cls.STATUS.valid_complete)\
                .all()

    @classmethod
    def get_polymer_by_provider_hotels(cls, session, provider_id, ids):
        return session.query(RoomTypeMappingModel)\
                .filter(RoomTypeMappingModel.provider_id == provider_id)\
                .filter(RoomTypeMappingModel.provider_hotel_id.in_(ids))\
                .filter(RoomTypeMappingModel.is_delete == 0)\
                .filter(RoomTypeMappingModel.status == cls.STATUS.valid_complete)\
                .all()

    @classmethod
    def gets_wait_firstvalid_by_provider(cls, session, provider_id):
        return session.query(RoomTypeMappingModel)\
                .filter(RoomTypeMappingModel.is_delete == 0)\
                .filter(RoomTypeMappingModel.status == cls.STATUS.wait_first_valid)\
                .filter(RoomTypeMappingModel.provider_id == provider_id)\
                .all()

    @classmethod
    def gets_wait_firstvalid_by_provider_and_hotel(cls, session, provider_id, hotel_id):
        return session.query(RoomTypeMappingModel)\
                .filter(RoomTypeMappingModel.is_delete == 0)\
                .filter(RoomTypeMappingModel.status == cls.STATUS.wait_first_valid)\
                .filter(RoomTypeMappingModel.provider_id == provider_id)\
                .filter(RoomTypeMappingModel.provider_hotel_id == str(hotel_id))\
                .all()

    @classmethod
    def gets_show_in_first_valid(cls, session, provider_id=None, hotel_name=None, city_id=None,
                                 start=0, limit=20,status=-1, match_status=0):
        from models.hotel_mapping import HotelMappingModel
        stmt = and_(HotelMappingModel.provider_id == RoomTypeMappingModel.provider_id,
                HotelMappingModel.provider_hotel_id == RoomTypeMappingModel.provider_hotel_id,
                HotelMappingModel.main_hotel_id == RoomTypeMappingModel.main_hotel_id,
                HotelMappingModel.main_hotel_id > 0,
                HotelMappingModel.status >= HotelMappingModel.STATUS.wait_first_valid,
                HotelMappingModel.is_delete == 0)

        query = session.query(HotelMappingModel, RoomTypeMappingModel).filter(RoomTypeMappingModel.match_status == match_status)
        if provider_id:
            query = query.filter(HotelMappingModel.provider_id == provider_id)
        if city_id:
            query = query.filter(HotelMappingModel.city_id == city_id)
        if hotel_name:
            query = query.filter(HotelMappingModel.provider_hotel_name.like(u'%{}%'.format(hotel_name)))
        if status != -1:
            query = query.filter(HotelMappingModel.status == status)

        query = query\
            .filter(RoomTypeMappingModel.provider_id != 6)\
            .filter(RoomTypeMappingModel.is_delete == 0)\
            .filter(RoomTypeMappingModel.status != cls.STATUS.init)
        # if status == -1:
        query = query.filter(stmt)
        # else:
        #         query = query.filter(and_(stmt))


        r = query.offset(start).limit(limit).all()
        total = query.count()

        return r, total

    @classmethod
    def gets_wait_secondvalid_by_provider(cls, session, provider_id):
        return session.query(RoomTypeMappingModel)\
                .filter(RoomTypeMappingModel.is_delete == 0)\
                .filter(RoomTypeMappingModel.status == cls.STATUS.wait_second_valid)\
                .filter(RoomTypeMappingModel.provider_id == provider_id)\
                .all()

    @classmethod
    def reset_mapping_by_provider_hotel_id(cls, session, provider_hotel_id, main_hotel_id):
        session.query(RoomTypeMappingModel)\
                .filter(RoomTypeMappingModel.provider_hotel_id == str(provider_hotel_id))\
                .filter(RoomTypeMappingModel.is_delete == 0)\
                .update({RoomTypeMappingModel.main_hotel_id: main_hotel_id,
                         RoomTypeMappingModel.main_roomtype_id: 0,
                         RoomTypeMappingModel.status: cls.STATUS.init})
        session.commit()

    @classmethod
    def reset_mapping_by_id(cls, session, id, main_hotel_id):
        session.query(RoomTypeMappingModel)\
                .filter(RoomTypeMappingModel.id == id)\
                .filter(RoomTypeMappingModel.is_delete == 0)\
                .update({RoomTypeMappingModel.main_hotel_id: main_hotel_id,
                         RoomTypeMappingModel.main_roomtype_id: 0,
                         RoomTypeMappingModel.status: cls.STATUS.wait_first_valid})
        session.commit()

    @classmethod
    def update_main_hotel_id(cls, session, id, main_roomtype_id):
        r = cls.get_by_id(session, id)
        if r:
            r.main_roomtype_id = main_roomtype_id
            r.status = cls.STATUS.wait_first_valid
            session.commit()
        return r

    @classmethod
    def set_firstvalid_complete(cls, session, id):
        r = cls.get_by_id(session, id)
        if r:
            r.status = cls.STATUS.wait_second_valid
            r.match_status = 1
            session.commit()
        return r

    @classmethod
    def set_secondvalid_complete(cls, session, id):
        r = cls.get_by_id(session, id)
        if r:
            r.status = cls.STATUS.valid_complete
            session.commit()
        return r

    @classmethod
    def revert_to_firstvalid(cls, session, id):
        r = cls.get_by_id(session, id)
        if r:
            r.status = cls.STATUS.wait_first_valid
            r.is_online = -1
            session.commit()
        return r

    @classmethod
    def revert_to_firstvalid_by_provider_hotel_id(cls, session, provider_hotel_id):
        session.query(RoomTypeMappingModel)\
                .filter(RoomTypeMappingModel.provider_hotel_id == str(provider_hotel_id))\
                .filter(RoomTypeMappingModel.is_delete == 0)\
                .update({RoomTypeMappingModel.status: cls.STATUS.wait_first_valid,
                            RoomTypeMappingModel.is_online: -1})
        session.commit()

    @classmethod
    def disable_by_provider_hotel_id(cls, session, provider_hotel_id):
        session.query(RoomTypeMappingModel)\
                .filter(RoomTypeMappingModel.provider_hotel_id == str(provider_hotel_id))\
                .filter(RoomTypeMappingModel.is_delete == 0)\
                .update({RoomTypeMappingModel.is_online: -1})
        session.commit()

    @classmethod
    def set_online(cls, session, id, is_online):
        r = cls.get_by_id(session, id)
        if r:
            if is_online == 0:
                is_online = -1
            r.is_online =  is_online
            r.is_new = 0
            session.commit()

        return r

    @classmethod
    def delete_mapping_by_provider_hotel_id(cls, session, provider_id,provider_hotel_id, provider_roomtype_id, is_delete=1):
        session.query(RoomTypeMappingModel)\
                .filter(RoomTypeMappingModel.provider_id == provider_id)\
                .filter(RoomTypeMappingModel.provider_hotel_id == str(provider_hotel_id))\
                .filter(RoomTypeMappingModel.provider_roomtype_id == str(provider_roomtype_id))\
                .update({
                         RoomTypeMappingModel.is_delete: is_delete})
        session.commit()

    @classmethod
    def delete_mapping_by_hotel_id(cls, session, provider_id,provider_hotel_id, is_delete=1):
        session.query(RoomTypeMappingModel)\
                .filter(RoomTypeMappingModel.provider_id == provider_id)\
                .filter(RoomTypeMappingModel.provider_hotel_id == str(provider_hotel_id))\
                .update({
                         RoomTypeMappingModel.is_delete: is_delete})
        session.commit()

    def todict(self):
        return ObjectDict(
                id=self.id,
                provider_id=self.provider_id,
                provider_hotel_id=self.provider_hotel_id,
                provider_roomtype_id=self.provider_roomtype_id,
                provider_roomtype_name=self.provider_roomtype_name,
                main_hotel_id=self.main_hotel_id,
                main_roomtype_id=self.main_roomtype_id,
                status=self.status,
                is_online=self.is_online,
                is_delete=self.is_delete,
                info=self.info,
                is_new=self.is_new,
                )
    #
    # def todict_all(self):
    #     _dict = self.todict()
    #     _dict['area'] = self['room_size'];
    #     return ObjectDict(
    #         id=self.id,
    #         provider_id=self.provider_id,
    #         provider_hotel_id=self.provider_hotel_id,
    #         provider_roomtype_id=self.provider_roomtype_id,
    #         provider_roomtype_name=self.provider_roomtype_name,
    #         main_hotel_id=self.main_hotel_id,
    #         main_roomtype_id=self.main_roomtype_id,
    #         status=self.status,
    #         is_online=self.is_online,
    #         is_delete=self.is_delete,
    #         info=self.info,
    #         is_new=self.is_new,
    #         provider_roomtype={}
    #
    #     )
    # roomtype_mapping['provider_roomtype'] = roomtype
    #                     roomtype_mapping['provider_roomtype']['area'] = roomtype.get('room_size', 0)
    #                     roomtype_mapping['provider_roomtype']['description'] = roomtype.get('desc', '')
    #                     roomtype_mapping['provider_roomtype']['capacity'] = roomtype.get('occupancy', '')
    #                     roomtype_mapping['provider_roomtype_name'] = roomtype.get('name')