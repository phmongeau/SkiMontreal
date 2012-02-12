import os
import ski_mtl
import unittest
import tempfile
import json

class SkiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = ski_mtl.app.test_client()
        self.ski_data_url = "http://depot.ville.montreal.qc.ca/conditions-ski/data.xml"
        
class PagesTestCase(SkiTestCase):
    """Test function related pages"""

    def test_homepage_works(self):
        rv = self.app.get('/')
        self.assertEqual(rv.status_code, 200)

    def test_old_page_redirect(self):
        rv = self.app.get('/static/index.html')
        self.assertEqual(rv.status_code, 302)
        rv = self.app.get('/static/index.html', follow_redirects=True)
        assert '<h1 id="logo">Ski Montreal</h1>' in rv.data

    def test_upload_page_works(self):
        rv = self.app.get('/upload')
        self.assertEqual(rv.status_code, 200)



class UploadTestCase(SkiTestCase):
    """Test uploading files"""

    def test_bad_file_upload(self):
        with open("test.txt") as f:
            rv = self.app.post('/upload', data = dict(
                file = f))
        assert rv.data == "invalid file"

    def test_valid_file_upload(self):
        with open("test.gpx") as f:
            rv = self.app.post('/upload', data = dict(
                file = f))
        assert rv.data == "ok"



class DataTestCase(SkiTestCase):
    """Test function related to data"""

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
