# -*- coding: utf-8 -*-
import unittest
import json
import ski_mtl
from ski_mtl import Track


class SkiTestCase(unittest.TestCase):
    def setUp(self):
        self.ski_url = "http://depot.ville.montreal.qc.ca/conditions-ski/data.xml"

        ski_mtl.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'
        #ski_mtl.app.config['SQLALCHEMY_DATABASE_URI'] = \
                #'postgresql+psycopg2://{}:{}@/ski_mtl_test'.format('testuser', 'toto')
        ski_mtl.db.create_all()

        self.app = ski_mtl.app.test_client()

    def tearDown(self):
        ski_mtl.db.drop_all()


class PagesTestCase(SkiTestCase):
    """Test function related pages"""

    def test_homepage_works(self):
        rv = self.app.get('/')
        assert rv.status_code == 200

    def test_old_page_redirect(self):
        rv = self.app.get('/static/index.html')
        assert rv.status_code == 302
        rv = self.app.get('/static/index.html', follow_redirects=True)
        assert '<h1 id="logo">Ski Montreal</h1>' in rv.data

    def test_upload_page_works(self):
        rv = self.app.get('/upload')
        assert rv.status_code == 200


class UploadTestCase(SkiTestCase):
    """Test uploading files"""

    def test_bad_file_upload(self):
        with open("test.txt") as f:
            rv = self.app.post('/upload', data=dict(file=f))
        assert rv.status_code == 415
        assert "Type de fichier invalide" in rv.data

    def test_valid_file_upload(self):
        with open("test.gpx") as f:
            rv = self.app.post('/upload', data=dict(file=f))
        assert rv.status_code == 200
        assert "Le fichier à été téléversé avec succès" in rv.data

    def test_upload_same_file(self):
        with open("test.gpx") as f:
            rv = self.app.post('/upload', data=dict(file=f))
        assert rv.status_code == 200
        assert "Le fichier à été téléversé avec succès" in rv.data

        with open("test.gpx") as f:
            rv = self.app.post('/upload', data=dict(file=f))
        assert rv.status_code == 200
        assert "Le fichier à été téléversé avec succès" in rv.data


class DataTestCase(SkiTestCase):
    """Test function related to data"""

    def test_invalide_xml_url(self):
        assert ski_mtl.getXML(self.ski_url + "bla") is None

    def test_get_xml_has_element_piste(self):
        tree = ski_mtl.getXML(self.ski_url)
        assert tree is not None
        assert tree.findall('piste')

    def test_get_conditions(self):
        rv = self.app.get('/conditions.json')
        assert rv.status_code == 200

        assert rv.data is not None

        x = json.loads(rv.data)
        assert type(x) == dict

    def test_get_gpx_by_name(self):
        with open("test.gpx") as f:
            rv = self.app.post('/upload', data=dict(file=f))

        rv = self.app.get('/gpx/get/test.gpx')
        assert rv.status_code == 200
        assert rv.mimetype == "application/gpx+xml"
        with open('test.gpx') as f:
            assert rv.data == f.read()

    def test_get_invalid_gpx(self):
        rv = self.app.get('/gpx/get/nope.gpx')
        assert rv.status_code == 404

    def test_get_gpx_list(self):
        with open("test.gpx") as f:
            rv = self.app.post('/upload', data=dict(file=f))

        rv = self.app.get('/gpx/list')
        assert rv.status_code == 200
        assert rv.data is not None
        x = json.loads(rv.data)
        assert type(x) == list


if __name__ == '__main__':
    unittest.main()
