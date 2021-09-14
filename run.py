from webapp import app, db
from webapp.models import User

if __name__ == "__main__":
    db.create_all()
    # Create an user for testing purposes

    app.run(host="0.0.0.0", debug=True)
