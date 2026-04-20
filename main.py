from fastapi import FastAPI, HTTPException
from typing import List, Dict, Optional
from models import Purs, NewPurs
from data import purchases

app = FastAPI()

def get_index(id: int) -> int:
    if 1 <= id <= len(purchases):
        return id - 1
    raise HTTPException(status_code=404, detail='Nothing found with a given id')


#/GET PURCHASES
@app.get("/purchases", response_model=List[Purs])
def show_purs() -> List[Purs]:
    return [Purs(**p) for p in purchases]

#/GET PURCHASES ID
@app.get("/purchases/{id}", response_model=Purs)
def show_purs_id(id: int) -> Purs:
    index = get_index(id)
    return purchases[index]

# @app.get("/purchases/done", response_model=List[Purs])
# def show_done() -> List[Purs]:
#     done_purs = []
#     for pur in purchases:
#         if pur['done']:
#             done_purs.append(pur)
#     return [Purs(**p) for p in done_purs]

#/GET PURCHASES DONE
@app.get("/purchases/done", response_model=List[Purs])
def show_done() -> List[Purs]:
    return [Purs(**p) for p in purchases if p['done']]

#/GET PURCHASES ID OPTIONAL
@app.get("/search", response_model=List[Purs])
def search_pur(name : Optional[str]) -> List[Purs]:
    if name:
        return [p for p in purchases if name.lower() in p['name'].lower()]
    return []

@app.get("/stats", response_model=dict)
def stats() -> dict:
    gen_stat=[]
    done=[]
    not_done=[]
    for pur in purchases:
        gen_stat.append(pur)
        if pur['done']:
            done.append(pur)
        else:
            not_done.append(pur)
    return {
        'total': len(gen_stat),
        'done': len(done),
        'not_done': len(not_done)
    }

#/POST PURCHASES(ADD)
@app.post("/purchases", response_model=List[Purs])
def add_pur(purchase : NewPurs) -> List[Purs]:
    new_pur = {'name': purchase.name, 'done': False}
    purchases.append(new_pur)
    return [Purs(**p) for p in purchases]

#/DELETE PURCHASES
@app.delete("/purchases/{id}", response_model=dict)
def delete_pur(id : int) -> dict:
    index = get_index(id)
    del purchases[index]
    return {'message': 'deleted'}

#/PUT PURCHASES(UPDATE)
@app.put("/purchases/{id}", response_model=Purs)
def change_pur(id : int, purchase : Purs) -> Purs:
    index = get_index(id)
    purchases[index] = {'name': purchase.name, 'done': purchase.done}
    return purchases[index]

