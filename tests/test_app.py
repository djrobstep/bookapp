
def test_home(client):
    resp = client.get('/')
    assert resp.status_code == 200


def test_book(client):
    resp = client.get('/book')
    assert resp.status_code == 200
    assert resp.json == []


def test_author(client):
    resp = client.get('/author_books')
    assert resp.status_code == 200
