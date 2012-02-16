import ski_mtl
import unittest
import json


class SkiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = ski_mtl.app.test_client()
        self.ski_url = "http://depot.ville.montreal.qc.ca/conditions-ski/data.xml"


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
        assert rv.data == "invalid file"

    def test_valid_file_upload(self):
        with open("test.gpx") as f:
            rv = self.app.post('/upload', data=dict(file=f))
        assert rv.data == "ok"

    def test_upload_same_file(self):
        with open("test.gpx") as f:
            rv = self.app.post('/upload', data=dict(file=f))
        assert rv.data == "ok"

        with open("test.gpx") as f:
            rv = self.app.post('/upload', data=dict(file=f))
        assert rv.data == "ok"


class DataTestCase(SkiTestCase):
    """Test function related to data"""

    def test_invalide_xml_url(self):
        assert ski_mtl.getXML(self.ski_url + "bla") is False

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
        rv = self.app.get('/gpx/get/test.gpx')
        assert rv.status_code == 200
        with open('test.gpx') as f:
            assert rv.data == f.read()

    def test_get_gpx_list(self):
        rv = self.app.get('/gpx/list')
        assert rv.status_code == 200
        assert rv.data is not None
        x = json.loads(rv.data)
        assert type(x) == list
        print len(x)
        print len(ski_mtl.Track.query.all())
        assert len(x) == len(ski_mtl.Track.query.all())


if __name__ == '__main__':
    unittest.main()
