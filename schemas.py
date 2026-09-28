from pydantic import BaseModel


class SkillCreate(BaseModel):
    name: str
    level: str
    progress: int = 0


class SkillResponse(BaseModel):
    id: int
    name: str
    level: str
    progress: int

    class Config:
        from_attributes = True