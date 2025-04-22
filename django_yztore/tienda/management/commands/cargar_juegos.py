from django.core.management.base import BaseCommand
from tienda.models import Juego
from datetime import datetime
import os

class Command(BaseCommand):
    help = 'Carga los juegos iniciales en la base de datos'

    def handle(self, *args, **kwargs):
        juegos = [
            {
                'nombre': 'The Legend of Zelda: Tears of the Kingdom',
                'descripcion': 'La secuela de Breath of the Wild que expande el mundo de Hyrule.',
                'precio': 69.99,
                'precio_original': 69.99,
                'categoria': 'aventura',
                'imagen': 'zelda.jpg',
                'fecha_lanzamiento': '2023-05-12',
                'desarrollador': 'Nintendo',
                'plataforma': 'Nintendo Switch',
                'stock': 50,
                'destacado': True
            },
            {
                'nombre': 'Elden Ring',
                'descripcion': 'Un juego de rol de acción en un mundo abierto desarrollado por FromSoftware.',
                'precio': 59.99,
                'precio_original': 59.99,
                'categoria': 'rpg',
                'imagen': 'elden_ring.jpg',
                'fecha_lanzamiento': '2022-02-25',
                'desarrollador': 'FromSoftware',
                'plataforma': 'Multiplataforma',
                'stock': 30,
                'destacado': True
            },
            {
                'nombre': 'God of War Ragnarök',
                'descripcion': 'La secuela del aclamado God of War que continúa la historia de Kratos y Atreus.',
                'precio': 69.99,
                'precio_original': 69.99,
                'categoria': 'accion',
                'imagen': 'gow_ragnarok.jpg',
                'fecha_lanzamiento': '2022-11-09',
                'desarrollador': 'Santa Monica Studio',
                'plataforma': 'PlayStation 5',
                'stock': 40,
                'destacado': True
            },
            {
                'nombre': 'Hogwarts Legacy',
                'descripcion': 'Un RPG de acción ambientado en el mundo mágico de Harry Potter.',
                'precio': 59.99,
                'precio_original': 69.99,
                'descuento': 15,
                'categoria': 'rpg',
                'imagen': 'hogwarts_legacy.jpg',
                'fecha_lanzamiento': '2023-02-10',
                'desarrollador': 'Avalanche Software',
                'plataforma': 'Multiplataforma',
                'stock': 35
            },
            {
                'nombre': 'Starfield',
                'descripcion': 'Un nuevo RPG de Bethesda ambientado en el espacio.',
                'precio': 69.99,
                'precio_original': 69.99,
                'categoria': 'rpg',
                'imagen': 'starfield.jpg',
                'fecha_lanzamiento': '2023-09-06',
                'desarrollador': 'Bethesda Game Studios',
                'plataforma': 'Xbox Series X|S, PC',
                'stock': 45
            },
            {
                'nombre': 'Resident Evil 4 Remake',
                'descripcion': 'Una reimaginación del clásico juego de terror de Capcom.',
                'precio': 59.99,
                'precio_original': 59.99,
                'categoria': 'accion',
                'imagen': 're4_remake.jpg',
                'fecha_lanzamiento': '2023-03-24',
                'desarrollador': 'Capcom',
                'plataforma': 'Multiplataforma',
                'stock': 25
            },
            {
                'nombre': 'Street Fighter 6',
                'descripcion': 'La última entrega de la legendaria serie de juegos de lucha.',
                'precio': 59.99,
                'precio_original': 59.99,
                'categoria': 'accion',
                'imagen': 'sf6.jpg',
                'fecha_lanzamiento': '2023-06-02',
                'desarrollador': 'Capcom',
                'plataforma': 'Multiplataforma',
                'stock': 30
            },
            {
                'nombre': 'Diablo IV',
                'descripcion': 'El regreso de la aclamada serie de RPG de acción de Blizzard.',
                'precio': 69.99,
                'precio_original': 69.99,
                'categoria': 'rpg',
                'imagen': 'diablo4.jpg',
                'fecha_lanzamiento': '2023-06-06',
                'desarrollador': 'Blizzard Entertainment',
                'plataforma': 'Multiplataforma',
                'stock': 40
            },
            {
                'nombre': 'Final Fantasy XVI',
                'descripcion': 'La última entrega de la legendaria serie de RPG de Square Enix.',
                'precio': 69.99,
                'precio_original': 69.99,
                'categoria': 'rpg',
                'imagen': 'ff16.jpg',
                'fecha_lanzamiento': '2023-06-22',
                'desarrollador': 'Square Enix',
                'plataforma': 'PlayStation 5',
                'stock': 35
            },
            {
                'nombre': 'Marvel\'s Spider-Man 2',
                'descripcion': 'La secuela del exitoso juego de Spider-Man de Insomniac Games.',
                'precio': 69.99,
                'precio_original': 69.99,
                'categoria': 'accion',
                'imagen': 'spiderman2.jpg',
                'fecha_lanzamiento': '2023-10-20',
                'desarrollador': 'Insomniac Games',
                'plataforma': 'PlayStation 5',
                'stock': 45
            },
            {
                'nombre': 'Alan Wake 2',
                'descripcion': 'La secuela del aclamado juego de terror psicológico de Remedy.',
                'precio': 59.99,
                'precio_original': 59.99,
                'categoria': 'aventura',
                'imagen': 'alan_wake2.jpg',
                'fecha_lanzamiento': '2023-10-27',
                'desarrollador': 'Remedy Entertainment',
                'plataforma': 'Multiplataforma',
                'stock': 30
            },
            {
                'nombre': 'Assassin\'s Creed Mirage',
                'descripcion': 'Un regreso a las raíces de la serie Assassin\'s Creed.',
                'precio': 49.99,
                'precio_original': 49.99,
                'categoria': 'aventura',
                'imagen': 'ac_mirage.jpg',
                'fecha_lanzamiento': '2023-10-12',
                'desarrollador': 'Ubisoft',
                'plataforma': 'Multiplataforma',
                'stock': 40
            },
            {
                'nombre': 'Mortal Kombat 1',
                'descripcion': 'El reinicio de la legendaria serie de juegos de lucha.',
                'precio': 69.99,
                'precio_original': 69.99,
                'categoria': 'accion',
                'imagen': 'mk1.jpg',
                'fecha_lanzamiento': '2023-09-19',
                'desarrollador': 'NetherRealm Studios',
                'plataforma': 'Multiplataforma',
                'stock': 35
            },
            {
                'nombre': 'Forza Motorsport',
                'descripcion': 'La última entrega de la serie de simulación de carreras de Microsoft.',
                'precio': 69.99,
                'precio_original': 69.99,
                'categoria': 'carreras',
                'imagen': 'forza_motorsport.jpg',
                'fecha_lanzamiento': '2023-10-10',
                'desarrollador': 'Turn 10 Studios',
                'plataforma': 'Xbox Series X|S, PC',
                'stock': 30
            },
            {
                'nombre': 'Cities: Skylines II',
                'descripcion': 'La secuela del exitoso juego de simulación de ciudades.',
                'precio': 49.99,
                'precio_original': 49.99,
                'categoria': 'estrategia',
                'imagen': 'cities_skylines2.jpg',
                'fecha_lanzamiento': '2023-10-24',
                'desarrollador': 'Colossal Order',
                'plataforma': 'PC',
                'stock': 25
            },
            {
                'nombre': 'Lies of P',
                'descripcion': 'Un juego de acción y rol inspirado en el cuento de Pinocho.',
                'precio': 59.99,
                'precio_original': 59.99,
                'categoria': 'rpg',
                'imagen': 'lies_of_p.jpg',
                'fecha_lanzamiento': '2023-09-19',
                'desarrollador': 'Neowiz Games',
                'plataforma': 'Multiplataforma',
                'stock': 30
            }
        ]

        for juego_data in juegos:
            juego = Juego.objects.create(
                nombre=juego_data['nombre'],
                descripcion=juego_data['descripcion'],
                precio=juego_data['precio'],
                precio_original=juego_data.get('precio_original', juego_data['precio']),
                descuento=juego_data.get('descuento', 0),
                categoria=juego_data['categoria'],
                imagen=juego_data['imagen'],
                fecha_lanzamiento=datetime.strptime(juego_data['fecha_lanzamiento'], '%Y-%m-%d').date(),
                desarrollador=juego_data['desarrollador'],
                plataforma=juego_data['plataforma'],
                stock=juego_data['stock'],
                destacado=juego_data.get('destacado', False)
            )
            self.stdout.write(self.style.SUCCESS(f'Juego creado: {juego.nombre}')) 