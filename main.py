from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base, SessionLocal
from models import Skill
from schemas import SkillCreate, SkillResponse

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "Welcome to SkillForge API!"}


@app.get("/skills", response_model=list[SkillResponse])
def get_skills():
    db = SessionLocal()
    skills = db.query(Skill).all()
    db.close()

    return skills


@app.post("/skills", response_model=SkillResponse)
def create_skill(skill: SkillCreate):
    db = SessionLocal()

    new_skill = Skill(
        name=skill.name,
        level=skill.level,
        progress=skill.progress
    )

    db.add(new_skill)
    db.commit()
    db.refresh(new_skill)
    db.close()

    return new_skill


@app.delete("/skills/{skill_id}")
def delete_skill(skill_id: int):
    db = SessionLocal()

    skill = db.query(Skill).filter(Skill.id == skill_id).first()

    if not skill:
        db.close()
        return {"message": "Skill not found"}

    db.delete(skill)
    db.commit()
    db.close()

    return {"message": "Skill deleted successfully"}


@app.put("/skills/{skill_id}", response_model=SkillResponse)
def update_skill(skill_id: int, skill: SkillCreate):
    db = SessionLocal()

    existing_skill = db.query(Skill).filter(Skill.id == skill_id).first()

    if not existing_skill:
        db.close()
        raise HTTPException(status_code=404, detail="Skill not found")

    existing_skill.name = skill.name
    existing_skill.level = skill.level
    existing_skill.progress = skill.progress

    db.commit()
    db.refresh(existing_skill)
    db.close()

    return existing_skill