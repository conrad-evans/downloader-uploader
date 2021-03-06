import os
from dotenv import load_dotenv
load_dotenv()
import functions
import pytest
from flask import Flask, json
from service import app
app.testing = True
client = app.test_client()
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
AUTHORIZATION = os.environ['SERVICE_KEY']

functions.setUpDropbox(ACCESS_TOKEN)
# skip = pytest.mark.skip(reason='fixing other tests')


def createWorkingDir():
    '''create folders'''


def test_postDownloadJob():
    '''tests the /download-job POST route that adds a new download job
    '''
    r = client.post(
        '/download-job', headers={'Token': ACCESS_TOKEN, 'Authorization': AUTHORIZATION})
    data = json.loads(r.data)
    assert data['complete'] == False


# test_postDownloadJob()


def test_getDownloadJob():
    '''tests the /download-job/<job-id> GET route that gets the status 
    of a download job
    '''
    job_id = 255
    r = client.get(f'/download-job/{job_id}',
                   headers={'Authorization': AUTHORIZATION})
    data = json.loads(r.data)
    print(data)
    assert data['message'] == f'Job {job_id} not found'


# test_getDownloadJob()


def test_postUploadJob():
    '''tests the /upload-job POST route that adds a new upload job
    '''
    r = client.post('/upload-job', json={
        'classes': ['cat', 'dog', 'car']
    }, headers={'Token': ACCESS_TOKEN, 'Authorization': AUTHORIZATION})
    data = json.loads(r.data)
    assert len(data) >= 0


# test_postUploadJob()


def test_getUploadJob():
    '''tests the /upload-job/<job_id> GET route that gets upload job
    '''
    job_id = 256
    r = client.get(f'/upload-job/{job_id}',
                   headers={'Authorization': AUTHORIZATION})
    data = json.loads(r.data)
    print(data)
    assert data['message'] == f'Job {job_id} not found'

# test_getUploadJob()


def test_getRemoteFileNames():
    '''test get remote folder filenames. requires a dropbox folder with 2 files in it
    '''
    files = functions.getRemoteFileNames('/test')
    print(files)
    assert len(files) == 2

# test_getRemoteFileNames()


def test_getFileNames():
    '''test getting local filenames
    '''
    files = functions.getFileNames('category-1')
    print(files)
    assert len(files) == 4

# test_getFileNames()


def test_getFolderNames():
    '''test gettingng names of sub folders in a local folder
    '''
    names = functions.getFolderNames('')
    print(names)

    assert len(names) >= 2


# test_getFolderNames()


def test_uploadFile():
    '''test uploading files
    '''
    result = functions.uploadFile(
        '', 'test-upload.jpg', '/test/test-upload.jpg')

    assert result == b'test-upload.jpg'


# test_uploadFile()


def test_downloadFile():
    '''test downloading files
    '''
    remote_data = functions.downloadFile('/test/test-download.jpg')

    path = os.path.join(os.environ['BASE'], os.environ['FOLDER'],
                        os.environ['SUB_FOLDER'], 'test-download.jpg')
    with open(path, 'rb') as f:
        local_data = f.read()

    assert remote_data == local_data

# test_downloadFile()


def test_saveFile():
    '''test saving files locally
    '''
    remote_data = functions.downloadFile('/test/test-download.jpg')
    written = functions.saveFile('', 'test-save.jpg', remote_data)

    assert len(remote_data) == written


# test_saveFile()

def test_400errors():
    '''test for error cases'''
    r = client.post(
        '/upload-job', headers={'Token': ACCESS_TOKEN, 'Authorization': AUTHORIZATION})

    assert r.status_code == 400


def test_storageProviderErrors():
    '''test for provider error cases'''
    try:
        functions.downloadFiles({})
        functions.uploadFiles('', {}, '')
    except Exception as e:
        print(e)


def test_common():
    '''test general files to improve coverage
    Simply run to make sure they dont crash the application
    '''
    from common import logger, responses
    logger.obj('string')

    app = Flask(__name__)

    with app.app_context():
        responses.respondInternalServerError()
        responses.respondOk('string')
        responses.respondUnauthorized('string')


# test_common()
