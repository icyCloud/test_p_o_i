# -*- coding: utf8 -*-
from views.api.province import ProvinceAPIHandler

from views.index import IndexHandler
from views.login import LoginHandler, LogoutHandler
from views.user import UserManagerHandler
from views.provider import ProviderHandler
from views.firstvalid import FirstValidHandler
from views.second_valid import SecondValidHandler
from views.polymer import PolymerHandler
from views.roomtype import RoomTypeHandler
from views.api.provider import ProviderAPIHandler, ProviderQueryAPIHandler
from views.api.firstvalid import FirstValidAPIHandler, FirstValidStatusAPIHandelr, FirstValidRoomTypeAPIHandler
from views.api.secondvalid import SecondValidAPIHandler, SecondValidHotelAPIHandler, SecondValidRoomTypeAPIHandler
from views.api.hotel import HotelSearchAPIHandler, HotelAPIHandler
from views.api.hotel_mapping import HotelMappingAPIHandler, HotelMappingEbookingPushAPIHandler, HotelMappingEbookingBatchPushAPIHandler
from views.api.room_type_mapping import RoomTypeMappingAPIHandler, RoomTypeMappingEbookingPushAPIHandler, RoomTypeMappingEbookingBatchPushAPIHandler
from views.api.polymer import PolymerAPIHandler, PolymerHotelAPIHandler, PolymerRoomTypeAPIHandler
from views.api.hotel_mapping import HotelMappingEbookingDeleteAPIHandler
from views.api.roomtype import RoomTypeAPIHandler, RoomTypeInnerAPIHandler
from views.api.city import CityAPIHandler
from views.api.district import DistrictAPIHandler, DistrictByCityAPIHandler
from views.api.polymer import PolymerHotelLineHandler
from views.api.room_type_mapping import RoomTypeMappingEbookingDeleteAPIHandler
from views.ebooking import EbookingHandler
from views.api.ebooking import EbookingAPIHandler, MerchantListHandler

from views.hotels import HotelsHandler

from views.api.business_zone import BusinessZoneByCityAPIHandler
from views.api.elong import ElongAPIHandler

from views.poioperatelog import PoiOperateLogHandler
from views.api.poi_operate_log import OperateLogAPIHandler
handlers = [
        (r"/?", IndexHandler),
        (r"/login/?", LoginHandler),
        (r"/logout/?", LogoutHandler),
        (r"/usermanager/?", UserManagerHandler),
        (r"/usermanager/new/?", UserManagerHandler),
        (r"/usermanager/delete/(?P<user_id>\d+)/?", UserManagerHandler),
        (r"/usermanager/update/(?P<user_id>\d+)/?", UserManagerHandler),
        (r"/provider/?", ProviderHandler),
        (r"/api/provider/?", ProviderAPIHandler),
        (r"/api/provider/query?", ProviderQueryAPIHandler),
        (r"/firstvalid/?", FirstValidHandler),
        (r"/secondvalid/?", SecondValidHandler),
        (r"/api/firstvalid/?", FirstValidAPIHandler),
        (r"/api/secondvalid/?", SecondValidAPIHandler),
        (r"/api/firstvalid/hotel/(?P<hotel_mapping_id>\d+)/valid/?", FirstValidStatusAPIHandelr),
        (r"/api/firstvalid/roomtype/(?P<roomtype_mapping_id>\d+)/valid/?", FirstValidRoomTypeAPIHandler),
        (r"/api/hotel/search/?", HotelSearchAPIHandler),
        (r"/api/hotel/mapping/?", HotelMappingAPIHandler),
        (r"/api/room_type/mapping/?", RoomTypeMappingAPIHandler),
        (r"/api/secondvalid/hotel/(?P<hotel_mapping_id>\d+)/valid/?", SecondValidHotelAPIHandler),
        (r"/api/secondvalid/hotel/(?P<hotel_mapping_id>\d+)/reject/?", SecondValidHotelAPIHandler),
        (r"/api/secondvalid/roomtype/(?P<roomtype_mapping_id>\d+)/reject/?", SecondValidRoomTypeAPIHandler),
        (r"/api/secondvalid/roomtype/(?P<roomtype_mapping_id>\d+)/valid/?", SecondValidRoomTypeAPIHandler),
        (r"/polymer/?", PolymerHandler),
        (r"/api/polymer/?", PolymerAPIHandler),
        (r"/api/polymer/hotel/online/?", PolymerHotelAPIHandler),
        (r"/api/polymer/hotel/(?P<hotel_mapping_id>\d+)/reject/?", PolymerHotelAPIHandler),
        (r"/api/polymer/roomtype/(?P<roomtype_mapping_id>\d+)/reject/?", PolymerRoomTypeAPIHandler),
        (r"/api/polymer/roomtype/online/?", PolymerRoomTypeAPIHandler),
        (r"/hotel/(?P<hotel_id>\d+)/roomtype/?", RoomTypeHandler),
        (r"/api/hotel/(?P<hotel_id>\d+)/roomtype/?", RoomTypeAPIHandler),
        (r"/api/inner/hotel/(?P<hotel_id>\d+)/roomtype/?", RoomTypeInnerAPIHandler),
        (r"/api/city/?", CityAPIHandler),
        (r"/api/province/?", ProvinceAPIHandler),
        (r"/api/district/?", DistrictAPIHandler),
        (r"/api/city/(?P<city_id>\d+)/district/?", DistrictByCityAPIHandler),
        (r"/api/city/(?P<city_id>\d+)/businesszone/?", BusinessZoneByCityAPIHandler),

        (r"/api/hotel/(?P<hotel_id>\d+)/?", HotelAPIHandler),
        (r"/api/hotel/?", HotelAPIHandler),
        (r"/api/push/ebooking/hotel/?", HotelMappingEbookingPushAPIHandler),
        (r"/api/push/ebooking/hotels/?", HotelMappingEbookingBatchPushAPIHandler),
        (r"/api/push/ebooking/room/?", RoomTypeMappingEbookingPushAPIHandler),
        (r"/api/push/ebooking/rooms/?", RoomTypeMappingEbookingBatchPushAPIHandler),
        (r"/api/delete/ebooking/room/?",RoomTypeMappingEbookingDeleteAPIHandler),
        (r"/api/delete/ebooking/hotel/?",HotelMappingEbookingDeleteAPIHandler),

        (r"/polymer/ebooking/?", EbookingHandler),
        (r"/api/polymer/ebooking/?", EbookingAPIHandler),
        (r"/api/polymer/ebooking/merchant/all/?", MerchantListHandler),
        (r"/api/polymer/hotel/line?",PolymerHotelLineHandler),

        (r"/hotels/?", HotelsHandler),
        (r"/api/elong/hotel/(?P<hotel_id>\d+)/?", ElongAPIHandler),

        (r"/operatelog/?",PoiOperateLogHandler),
        (r"/api/operatelog/?",OperateLogAPIHandler),
        ]
