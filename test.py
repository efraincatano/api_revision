from src import app
import unittest
import requests

class Apitest(unittest.TestCase):

    api_url="http://127.0.0.1:5000/"
    historial_get="{}/obtenerhistorial/patente".format(api_url)
    ingreso_vehiculo = "/ingresarvehiculo".format(api_url)


    def test_uno_get(self):
        r = requets.get(Apitest.historial_get)
        self.assertEqual(r.status, 200)

    def test_dos_ingresar_vehiculo(self):
        r = requets.get(Apitest.ingreso_vehiculo)
        self.assertEqual(r.status, 201)


