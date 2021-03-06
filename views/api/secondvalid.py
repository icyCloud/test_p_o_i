# -*- coding: utf-8 -*-

from tornado.util import ObjectDict
from tornado import gen

from views.base import BtwBaseHandler, StockHandler
from mixin.hotelmixin import HotelMixin

from tools.auth import auth_login, auth_permission
from constants import PERMISSIONS
from models.hotel_mapping import HotelMappingModel as HotelMapping
from models.hotel import HotelModel as Hotel
from models.room_type_mapping import RoomTypeMappingModel as RoomTypeMapping
from models.room_type import RoomTypeModel as RoomType
from models.poi_operate_log_mapping import PoiOperateLogModel as PoiOperateLogMapping
from models.city import CityModel
from models.district import DistrictModel
from config import motivations
from config import modules
import traceback

from tools.log import Log, log_request
import time

class SecondValidAPIHandler(StockHandler, HotelMixin):

    @auth_login(json=True)
    @auth_permission(PERMISSIONS.admin | PERMISSIONS.second_valid, json=True)
    @log_request
    def get(self):
        start = self.get_query_argument('start', 0)
        limit = self.get_query_argument('limit', 20)

        provider_id = self.get_query_argument('provider_id', None)
        hotel_name = self.get_query_argument('hotel_name', None)
        city_id = self.get_query_argument('city_id', None)
        status = self.get_query_argument('statusId',-1)

        Log.info(">> get show in second valid")
        t0 = time.time() 
        hotel_mappings, total = HotelMapping.gets_show_in_secondvalid(self.db,
                provider_id=provider_id, hotel_name=hotel_name, city_id=city_id,
                start=start, limit=limit,status=status)
        t1 = time.time()
        Log.info(">> show in second cost {}".format(t1 - t0))

        hotels = [hotel.todict() for hotel in hotel_mappings]

        t2 = time.time()
        self.merge_main_hotel_info(hotels)
        t3 = time.time()
        Log.info(">> merge main hotel info cost {}".format(t3 - t2))

        t4 = time.time()
        self.merge_room_type_mapping(hotels)
        t5 = time.time()
        Log.info(">> merge roomtype mapping cost {}".format(t5 - t4))

        t6 = time.time()
        self.add_provider_roomtype(hotels)
        t7 = time.time()
        Log.info(">> add provider roomtype cost {}".format(t7 - t6))

        self.finish_json(result=dict(
            hotel_mappings=hotels,
            roomtypes=self.roomtypes,
            start=start,
            limit=limit,
            total=total))

    
    def merge_room_type_mapping(self, hotel_dicts):

        provider_hotel_ids = [hotel.provider_hotel_id for hotel in hotel_dicts]
        provider_hotel_ids = {}.fromkeys(provider_hotel_ids).keys()
        provider_hotel_ids.sort()

        roomtype_mappings = RoomTypeMapping.get_secondvalid_by_provider_hotel_ids(self.db, provider_hotel_ids)
        roomtype_mappings = [mapping.todict() for mapping in roomtype_mappings]

        main_hotel_ids = [mapping.main_hotel_id for mapping in roomtype_mappings]
        main_hotel_ids = {}.fromkeys(main_hotel_ids).keys()
        main_hotel_ids.sort()

        self.roomtypes = RoomType.gets_by_hotel_ids(self.db, main_hotel_ids)
        self.roomtypes =[roomtype.todict() for roomtype in self.roomtypes]


        self.merge_room_type(self.roomtypes, roomtype_mappings)
        for hotel in hotel_dicts:
            roomtype_mapping_dicts = [
                roomtype_mapping
                for roomtype_mapping in roomtype_mappings
                if hotel.provider_id == roomtype_mapping.provider_id\
                        and hotel.provider_hotel_id == roomtype_mapping.provider_hotel_id]
            hotel['roomtype_mappings'] = roomtype_mapping_dicts
            
    def merge_room_type(self, roomtypes, room_type_mapping_dicts):
        for mapping in room_type_mapping_dicts:
            for roomtype in roomtypes:
                if mapping.main_roomtype_id == roomtype.id:
                    mapping['main_roomtype'] = roomtype


class SecondValidHotelAPIHandler(BtwBaseHandler):

    @auth_login(json=True)
    @auth_permission(PERMISSIONS.admin | PERMISSIONS.second_valid, json=True)
    def put(self, hotel_mapping_id):
        Log.info("Second>>Hotel {}>>Valid>> user:{}".format(hotel_mapping_id, self.current_user))
        hotel_mapping = HotelMapping.get_by_id(self.db, hotel_mapping_id)
        if hotel_mapping and hotel_mapping.status == hotel_mapping.STATUS.wait_second_valid\
                and hotel_mapping.main_hotel_id != 0:

            hotels = HotelMapping.get_by_chain_id_and_main_hotel_id(self.db, hotel_mapping.provider_id, hotel_mapping.main_hotel_id)
            for hotel in hotels:
                if hotel.id != hotel_mapping.id and hotel.status > hotel_mapping.status:
                    self.finish_json(errcode=402, errmsg=u"已有Hotel{}绑定相同基础酒店".format(hotel.provider_hotel_name))
                    return

            hotel_mapping = HotelMapping.set_secondvalid_complete(self.db, hotel_mapping_id)

            try:
                module = modules['second_valid']
                motivation = motivations['pass_hotel']
                operator = self.current_user
                poi_hotel_id = hotel_mapping.main_hotel_id
                otaId = hotel_mapping.provider_id
                hotelName = hotel_mapping.provider_hotel_name
                hotelModel = Hotel.get_by_id(self.db,id=poi_hotel_id)
                operate_content = hotelName + "<->" + hotelModel.name
                hotel_id = hotel_mapping_id
                PoiOperateLogMapping.record_log(self.db,otaId=otaId,hotelName=hotelName,module=module,motivation=motivation,operator=operator,poi_hotel_id=poi_hotel_id,operate_content=operate_content,hotel_id=hotel_id)
            except Exception,e:
                traceback.print_exc()

            self.finish_json(result=ObjectDict(
                hotel_mapping=hotel_mapping.todict(),
                ))
        else:
            self.finish_json(errcode=401, errmsg="not in second valid")

    @auth_login(json=True)
    @auth_permission(PERMISSIONS.admin | PERMISSIONS.second_valid, json=True)
    def delete(self, hotel_mapping_id):
        Log.info("Second>>Hotel {}>>Delete>> user:{}".format(hotel_mapping_id, self.current_user))
        hotel_mapping = HotelMapping.get_by_id(self.db, hotel_mapping_id)
        if hotel_mapping and hotel_mapping.status == hotel_mapping.STATUS.wait_second_valid:
            hotel_mapping = HotelMapping.revert_to_firstvalid(self.db, hotel_mapping_id)
            RoomTypeMapping.revert_to_firstvalid_by_provider_hotel_id(self.db, hotel_mapping.provider_hotel_id)

            try:
                module = modules['second_valid']
                motivation = motivations['back_hotel']
                operator = self.current_user
                poi_hotel_id = hotel_mapping.main_hotel_id
                otaId = hotel_mapping.provider_id
                hotelName = hotel_mapping.provider_hotel_name
                hotelModel = Hotel.get_by_id(self.db,id=poi_hotel_id)
                operate_content = hotelName + "<->" + hotelModel.name
                hotel_id = hotel_mapping_id
                PoiOperateLogMapping.record_log(self.db,otaId=otaId,hotelName=hotelName,module=module,motivation=motivation,operator=operator,poi_hotel_id=poi_hotel_id,operate_content=operate_content,hotel_id=hotel_id)
            except Exception,e:
                traceback.print_exc()

            self.finish_json(result=ObjectDict(
                hotel_mapping=hotel_mapping.todict(),
                ))
        else:
            self.finish_json(errcode=401, errmsg="not in second valid")


class SecondValidRoomTypeAPIHandler(BtwBaseHandler):

    @auth_login(json=True)
    @auth_permission(PERMISSIONS.admin | PERMISSIONS.second_valid, json=True)
    def put(self, roomtype_mapping_id):
        Log.info("Second>>RoomType {}>>Valid>> user:{}".format(roomtype_mapping_id, self.current_user))
        mapping = RoomTypeMapping.get_by_id(self.db, roomtype_mapping_id)
        if mapping and mapping.status == mapping.STATUS.wait_second_valid\
                and mapping.main_hotel_id != 0:
            mapping = RoomTypeMapping.set_secondvalid_complete(self.db, roomtype_mapping_id)

            try:
                module = modules['second_valid']
                motivation = motivations['pass_roomtype']
                operator = self.current_user
                poi_hotel_id = mapping.main_hotel_id
                poi_roomtype_id = mapping.main_roomtype_id
                otaId = mapping.provider_id
                hotel_id = mapping.provider_hotel_id
                hotelModel = HotelMapping.get_by_provider_and_main_hotel(self.db,otaId,hotel_id,poi_hotel_id)
                hotelName = hotelModel.provider_hotel_name
                roomType = RoomType.get_by_id(self.db,id=poi_roomtype_id)
                operate_content = mapping.provider_roomtype_name + " <-> " + roomType.name

                PoiOperateLogMapping.record_log(self.db,otaId=otaId,hotelName=hotelName,module=module,motivation=motivation,operator=operator,
                                                poi_hotel_id=poi_hotel_id,operate_content=operate_content,hotel_id=hotel_id,poi_roomtype_id=poi_roomtype_id)
            except Exception,e:
                traceback.print_exc()

            self.finish_json(result=ObjectDict(
                roomtype_mapping=mapping.todict(),
                ))
        else:
            self.finish_json(errcode=401, errmsg="not in second valid")



    @auth_login(json=True)
    @auth_permission(PERMISSIONS.admin | PERMISSIONS.second_valid, json=True)
    def delete(self, roomtype_mapping_id):
        Log.info("Second>>RoomType {}>>Delete>> user:{}".format(roomtype_mapping_id, self.current_user))
        mapping = RoomTypeMapping.get_by_id(self.db, roomtype_mapping_id)
        if mapping and mapping.status == mapping.STATUS.wait_second_valid:
            mapping = RoomTypeMapping.revert_to_firstvalid(self.db, roomtype_mapping_id)

            try:
                module = modules['second_valid']
                motivation = motivations['back_roomtype']
                operator = self.current_user
                poi_hotel_id = mapping.main_hotel_id
                poi_roomtype_id = mapping.main_roomtype_id
                otaId = mapping.provider_id
                hotel_id = mapping.provider_hotel_id
                hotelModel = HotelMapping.get_by_provider_and_main_hotel(self.db,otaId,hotel_id,poi_hotel_id)
                hotelName = hotelModel.provider_hotel_name
                roomType = RoomType.get_by_id(self.db,id=poi_roomtype_id)
                operate_content = mapping.provider_roomtype_name + " <-> " + roomType.name

                PoiOperateLogMapping.record_log(self.db,otaId=otaId,hotelName=hotelName,module=module,motivation=motivation,operator=operator,
                                                poi_hotel_id=poi_hotel_id,operate_content=operate_content,hotel_id=hotel_id,poi_roomtype_id=poi_roomtype_id)
            except Exception,e:
                traceback.print_exc()

            self.finish_json(result=ObjectDict(
                roomtype_mapping=mapping.todict(),
                ))
        else:
            self.finish_json(errcode=401, errmsg="not in second valid")
