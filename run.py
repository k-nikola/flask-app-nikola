from webapp import app, db
from webapp.models import User

if __name__ == "__main__":
    db.create_all()
    # Create an user for testing purposes
    try:
        db.session.add(
            User(
                username="test1234",
                name="test1234",
                email_address="test1234@mail.com",
                password="asdasd",
            )
        )
        db.session.commit()
    except:
        pass
    app.run(host="0.0.0.0", debug=True)
