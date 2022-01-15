from flask_restful import Resource, reqparse
from models.hotel import HotelModel

hoteis = [
    {
        'hotel_id': 'alpha',
        'nome': 'Alpha Hotel',
        'estrelas': 4.3,
        'diaria': 420.45,
        'cidade': 'Olinda'
    },
    {
        'hotel_id': 'bravo',
        'nome': 'Bravo Hotel',
        'estrelas': 4.7,
        'diaria': 569.00,
        'cidade': 'Recife'
    },
    {
        'hotel_id': 'nexos',
        'nome': 'Nexos Hotel',
        'estrelas': 4.0,
        'diaria': 330.65,
        'cidade': 'Rio de Janeiro'
    },
]

class Hoteis(Resource):
    def get(self):
        return {'hoteis': [hotel.json() for hotel in HotelModel.query.all()]} # SELECT * FROM hoteis

class Hotel(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome', type=str, required=True, help="The field 'nome' can not be left blank")
    argumentos.add_argument('estrelas', type=float, required=True, help="The field 'estrelas' can not be left blank")
    argumentos.add_argument('diaria')
    argumentos.add_argument('cidade')

    def get(self):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json()
        return {'message': 'Hotel not found'}, 404
    
    def post(self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return {'message': 'Hotel id "{}" already existis'.format(hotel_id)}, 400
            
        dados = Hotel.argumentos.parse_args()
        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel()
        except:
            return {'message': 'An internal error ocurred while trying to save hotel'}, 500 # internal server error
        
        return hotel.json()

    def put(self, hotel_id):
        dados = Hotel.argumentos.parse_args()
        hotel = HotelModel(hotel_id, **dados)


        hotel_encontrado = HotelModel.find_hotel(hotel_id)

        if hotel_encontrado:
            hotel_encontrado.update_hotel(**dados)
            hotel_encontrado.save_hotel()
            return hotel_encontrado.json(), 200 # hotel alterado
        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel()
        except:
            return {'message': 'An internal error ocurred while trying to save hotel'}, 500 # internal server error
        return hotel.json(), 201 # hotel criado

    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            try:
                hotel.delete_hotel()
            except: 
                return {'message': 'An internal error ocurred while trying to delete hotel'}, 500 # internal server error
            return {'message': 'hotel deleted'} 
        return {'message': 'hotel not found'}, 404