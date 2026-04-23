from database import cur, conn
from fastapi import HTTPException
from typing import List, Optional
from models import Purs, NewPurs


def change_to_purs(purs : List[tuple]) -> List[Purs]:
    return [Purs(id = p[0], name=p[1], done=bool(p[2])) for p in purs]

def check_index(id: int):
    cur.execute("SELECT id FROM purchases WHERE id = ?", (id, ))
    purs = cur.fetchone()
    if not purs:
        raise HTTPException(status_code=404, detail='Nothing found with a given id')

def search_pur(name: Optional[str]) -> List[Purs]:
    cur.execute("SELECT * FROM purchases")
    purs = cur.fetchall()
    if name:
        return [Purs(id=p[0], name=p[1], done=bool(p[2])) for p in purs if p[1].lower() == name.lower()]
    return []

def show_purs() -> List[Purs]:
    cur.execute("SELECT * FROM purchases")
    purs = cur.fetchall()
    return change_to_purs(purs)

def show_purs_id(id: int) -> Purs:
    cur.execute("SELECT name, done FROM purchases WHERE id = ?", (id, ))
    pur = cur.fetchone()
    if not pur:
        raise HTTPException(status_code=404, detail="Nothing found")
    return Purs(id= pur[0], name=pur[1], done=bool(pur[2]))

def show_done() -> List[Purs]:
    cur.execute("SELECT * FROM purchases WHERE done = 1")
    purs = cur.fetchall()
    return change_to_purs(purs)

def stats() -> dict:
    cur.execute("SELECT COUNT(*) FROM purchases")
    all_count = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM purchases WHERE done = 1")
    done_count = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM purchases WHERE done = 0")
    not_done_count = cur.fetchone()[0]
    return {
        'all_counter': all_count,
        'done_counter': done_count,
        'not_done_counter': not_done_count
    }

def add_pur(purchase : NewPurs) -> Purs:
    cur.execute("INSERT INTO purchases (name, done) VALUES (?, ?)", (purchase.name, 0))
    conn.commit()
    new_id = cur.lastrowid()
    return Purs(id=new_id, name=purchase.name, done=False)

def delete_pur(id : int) -> dict:
    check_index(id)
    cur.execute("DELETE FROM purchases WHERE id = ?", (id, ))
    conn.commit()
    return {'message': 'Видалено'}

def change_pur(id : int, purchase : Purs) -> Purs:
    check_index(id)
    cur.execute("UPDATE purchases SET name = ?, done = ? WHERE id = ?", (purchase.name, purchase.done, id))
    conn.commit()
    return Purs(id=id, name=purchase.name, done=purchase.done)