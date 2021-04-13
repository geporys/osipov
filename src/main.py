from fastapi import FastAPI, File, Form
from fastapi.staticfiles import StaticFiles
from enum import Enum

import psycopg2
conn = psycopg2.connect(dbname='potato', user='postgres',
                        password='postgres', host='localhost')

app = FastAPI()


class Type(str, Enum):
    potato = "potato"
    other = "other"


@app.post("/file")
async def create_file(file: bytes = File(...), type: Type = Form(...)):
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO images(image, type) VALUES(%s, %s) RETURNING id;""", (file, type))
    id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    return {"id": str(id), "type": type}


app.mount("/static", StaticFiles(directory="static",
                                 html="static"), name="static")
