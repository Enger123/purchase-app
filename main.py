from fastapi import FastAPI
from typing import List, Optional
from models import Purs, NewPurs
import crud

app = FastAPI()

#/GET PURCHASES
@app.get("/purchases", response_model=List[Purs])
def show_purs() -> List[Purs]:
    return crud.show_purs()

#/GET PURCHASES ID
@app.get("/purchases/{id}", response_model=Purs)
def show_purs_id(id: int) -> Purs:
    return crud.show_purs_id(id)

#/GET PURCHASES DONE
@app.get("/purchases/done/all", response_model=List[Purs])
def show_done() -> List[Purs]:
    return crud.show_done()

#/GET PURCHASES ID OPTIONAL
@app.get("/search", response_model=List[Purs])
def search_pur(name : Optional[str]) -> List[Purs]:
    return crud.search_pur(name)

@app.get("/stats", response_model=dict)
def stats() -> dict:
    return crud.stats()

#/POST PURCHASES(ADD)
@app.post("/purchases", response_model=Purs)
def add_pur(purchase : NewPurs) -> Purs:
    return crud.add_pur(purchase)

#
#/DELETE PURCHASES
@app.delete("/purchases/{id}", response_model=dict)
def delete_pur(id : int) -> dict:
    return crud.delete_pur(id)

#/PUT PURCHASES(UPDATE)
@app.put("/purchases/{id}", response_model=Purs)
def change_pur(id : int, purchase : Purs) -> Purs:
    return crud.change_pur(id, purchase)

