from pydantic import BaseModel
class Purs(BaseModel):
    id: int
    name: str
    done: bool

class NewPurs(BaseModel):
    name: str