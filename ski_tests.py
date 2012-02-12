import os
import ski_mtl
import unittest
import tempfile
import json

class SkiTestCase(unittest.TestCase):
    
    def setUp(self):
        self.app = ski_mtl.app.test_client()
        self.ski_data_url = "http://depot.ville.montreal.qc.ca/conditions-ski/data.xml"

    def test_homepage_works(self):
        rv = self.app.get('/')
        self.assertEqual(rv.status_code, 200)

    def test_invalide_xml_url(self):
        assert ski_mtl.getXML(self.ski_data_url + "bla") is False

    def test_get_xml_has_element_piste(self):
        tree =  ski_mtl.getXML(self.ski_data_url)
        assert tree.findall('piste')

    def test_get_conditions_works(self):
        rv = self.app.get('/conditions.json')
        self.assertEqual(rv.status_code, 200)
    def test_get_conditions_json(self):
        rv = self.app.get('/conditions.json')
        self.assertTrue(rv.data)
        self.assertTrue(json.loads(rv.data))


if __name__ == '__main__':
    unittest.main()
