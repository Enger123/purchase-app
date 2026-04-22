from fastapi import FastAPI, HTTPException
from typing import List, Dict, Optional
from models import Purs, NewPurs
import sqlite3

conn = sqlite3.connect('purs.db', check_same_thread=False)
cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS purchases(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name str,
done INTEGER
)""")

app = FastAPI()

def check_index(id: int):
    cur.execute("SELECT id FROM purchases WHERE id = ?", (id, ))
    purs = cur.fetchone()
    if not purs:
        raise HTTPException(status_code=404, detail='Nothing found with a given id')


#/GET PURCHASES
@app.get("/purchases", response_model=List[Purs])
def show_purs() -> List[Purs]:
    cur.execute("SELECT name, done FROM purchases")
    purs = cur.fetchall()
    return [Purs(name=p[0], done=bool(p[1])) for p in purs]

#/GET PURCHASES ID
@app.get("/purchases/{id}", response_model=Purs)
def show_purs_id(id: int) -> Purs:
    cur.execute("SELECT name, done FROM purchases WHERE id = ?", (id, ))
    pur = cur.fetchone()
    if not pur:
        raise HTTPException(status_code=404, detail="Nothing found")
    return Purs(name=pur[0], done=bool(pur[1]))

# # @app.get("/purchases/done", response_model=List[Purs])
# # def show_done() -> List[Purs]:
# #     done_purs = []
# #     for pur in purchases:
# #         if pur['done']:
# #             done_purs.append(pur)
# #     return [Purs(**p) for p in done_purs]
#
#/GET PURCHASES DONE
@app.get("/purchases/done/all", response_model=List[Purs])
def show_done() -> List[Purs]:
    cur.execute("SELECT name, done FROM purchases WHERE done = 1")
    purs = cur.fetchall()
    return [Purs(name=p[0], done=bool(p[1])) for p in purs]
#
# #/GET PURCHASES ID OPTIONAL
# @app.get("/search", response_model=List[Purs])
# def search_pur(name : Optional[str]) -> List[Purs]:
#     if name:
#         return [p for p in purchases if name.lower() in p['name'].lower()]
#     return []
#
@app.get("/stats", response_model=dict)
def stats() -> dict:
    cur.execute("SELECT name, done from purchases")
    all = cur.fetchall()
    cur.execute("SELECT name, done from purchases WHERE done = 1")
    done = cur.fetchall()
    cur.execute("SELECT name, done from purchases WHERE done = 0")
    not_done = cur.fetchall()
    return {
        'all': len(all),
        'done': len(done),
        'not_done': len(not_done)
    }

#/POST PURCHASES(ADD)
@app.post("/purchases", response_model=dict)
def add_pur(purchase : NewPurs) -> dict:
    cur.execute("INSERT INTO purchases (name, done) VALUES (?, ?)", (purchase.name, 0))
    conn.commit()
    return {'message': 'Додано'}

#
#/DELETE PURCHASES
@app.delete("/purchases/{id}", response_model=dict)
def delete_pur(id : int) -> dict:
    check_index(id)
    cur.execute("DELETE FROM purchases WHERE id = ?", (id, ))
    conn.commit()
    return {'message': 'Видалено'}


#
#/PUT PURCHASES(UPDATE)
@app.put("/purchases/{id}", response_model=dict)
def change_pur(id : int, purchase : Purs) -> dict:
    check_index(id)
    cur.execute("UPDATE purchases SET name = ?, done = ? WHERE id = ?", (purchase.name, purchase.done, id))
    conn.commit()
    if cur.rowcount == 0:
        return {'message': 'Задача не знайдена'}
    return {'message': 'Змінено'}

