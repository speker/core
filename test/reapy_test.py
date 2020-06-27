import unittest
import requests
from core.reapy import ReaPy


class ValidatorsTestCase(unittest.TestCase):
    def test_rea_py_json_dumps(self):
        self.assertTrue(ReaPy.json().dumps({"test": "test"}))

    def test_api_basvuru_detay_get(self):
        req = requests.get('http://127.0.0.1:7979/api/basvuru/detay')
        print('get')
        self.assertTrue(req.json()['data']['success'])

    def test_api_basvuru_detay_post(self):
        req = requests.post('http://127.0.0.1:7979/api/basvuru/detay', json={'vergi_numarasi': '1'})
        print('post', req.json())
        self.assertTrue(req.json()['data']['success'])

    def test_api_basvuru_paydas_get(self):
        req = requests.get('http://127.0.0.1:7979/api/basvuru/paydas')
        print('get', req.json())
        self.assertTrue(req.json()['data']['success'])

    def test_api_finans_ozet_get(self):
        req = requests.get('http://127.0.0.1:7979/api/finans/ozet')
        print('get', req.json())
        self.assertTrue(req.json()['data']['success'])



if __name__ == '__main__':
    unittest.main()
