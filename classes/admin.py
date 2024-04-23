from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from classes.classes import User

engine = create_engine(
    "sqlite:///main.db",
    connect_args={"check_same_thread": False},
)

session = sessionmaker(bind=engine)()

class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        usename, password = form["username"], form["password"]

        key = session.query(User).filter_by(name=usename, password=password).first()
        if key is None:
            return False
        request.session.update({"token": "..."})
        return True


        # if usename == "2Milan" and password == "7e9VAU3GsdNiuSERvs":
        #     request.session.update({"token": "..."})
        #     return True
        # else:
        #     return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")

        if not token:
            return False

        # Check the token in depth
        return True


authentication_backend = AdminAuth(secret_key="...")
