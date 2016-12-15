from bookapp import get_app

from config import DB_URL

app = get_app(db=DB_URL)
