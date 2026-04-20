from pydantic import BaseModel
class Purs(BaseModel):
    name: str
    done: bool

class NewPurs(BaseModel):
    name: str