from fastapi import FastAPI, HTTPException, Response
from sqladmin import Admin
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.encoders import jsonable_encoder

from classes.admin import authentication_backend
from classes.classes import Key, UserAdmin, UserKeys, LogView, Base
import datetime

engine = create_engine(
    "sqlite:///main.db",
    connect_args={"check_same_thread": False},
)

session = sessionmaker(bind=engine)()


app = FastAPI()
admin = Admin(app=app, engine=engine, authentication_backend=authentication_backend)

# for i in range(10):
#     session.add(Key(hwid=None, key=keygen.generate_key(10)))
#     session.commit()


# @app.get("/key_list")
# def read_root():
#     # Execute the query and get the results
#     keys = session.query(Key).all()
#     return jsonable_encoder(keys)

@app.get("/key_list/{serial}")
def find_key_by_hwid(serial: str):
    key = session.query(Key).filter_by(key=serial).first()
    if key is None:
        raise HTTPException(status_code=404, detail="Key not found")
    return jsonable_encoder(key)


@app.get("/auth/{hwid}/{serial}/{ip}")
def auth(response: Response, hwid: str, serial: str, ip: str):
    key = session.query(Key).filter_by(key=serial).first()

    if key is None:
        response.status_code = 919
        return HTTPException(status_code=919, detail="Откуда ты это блядь взял?")
    elif key.hwid is not None and key.hwid != hwid:
        response.status_code = 403
        return HTTPException(status_code=403, detail="Key ne tvoy")
    elif key.hwid is not None and key.hwid == hwid:
        if key.experiance_time < datetime.datetime.now().isoformat():
            response.status_code = 403
        else:
            response.status_code = 201
            return HTTPException(status_code=201, detail="Key now active")
    else:
        key.hwid = hwid
        key.experiance_time = (
            datetime.datetime.now() + datetime.timedelta(days=30)
        ).isoformat()
        key.ip = str(ip)
        session.commit()
        response.status_code = 200
        return HTTPException(status_code=200, detail="Key aktualizovano")


@app.get("/check_key/{hwid}/{serial}")
def check_key(response: Response, hwid: str, serial: str):
    key = session.query(Key).filter_by(hwid=hwid, key=serial).first()

    if key is None:
        response.status_code = 404
        return HTTPException(status_code=404, detail="Not found")
    else:
        response.status_code = 200
        return jsonable_encoder(key)


admin.add_view(UserAdmin)
admin.add_view(UserKeys)
admin.add_view(LogView)

Base.metadata.create_all(engine)
