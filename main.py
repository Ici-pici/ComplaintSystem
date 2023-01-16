from config import create_app
from models import *

app = create_app()

@app.after_request
def after_interceptor(response):
    db.session.commit()
    return response


if __name__ == '__main__':
    app.run()

