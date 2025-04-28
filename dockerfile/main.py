from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./veiculos.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
Base = declarative_base()

SessionLocal = sessionmaker(bind=engine)
app = FastAPI()

class VeiculoDB(Base):
    __tablename__ = "veiculos"
    id = Column(Integer, primary_key=True, index=True)
    marca = Column(String, index=True)
    modelo = Column(String, index=True)
    ano = Column(Integer)

Base.metadata.create_all(bind=engine)

class Veiculo(BaseModel):
    marca: str
    modelo: str
    ano: int

class VeiculoResponse(Veiculo):
    id: int
    links: dict

    class Config:
        orm_mode = True

@app.post("/veiculos/", response_model=VeiculoResponse)
def criar_veiculo(veiculo: Veiculo):
    db = SessionLocal()
    db_veiculo = VeiculoDB(**veiculo.dict())
    db.add(db_veiculo)
    db.commit()
    db.refresh(db_veiculo)
    return to_hateoas(db_veiculo)

@app.get("/veiculos/", response_model=List[VeiculoResponse])
def listar_veiculos():
    db = SessionLocal()
    veiculos = db.query(VeiculoDB).all()
    return [to_hateoas(veiculo) for veiculo in veiculos]

@app.get("/veiculos/{veiculo_id}", response_model=VeiculoResponse)
def obter_veiculo(veiculo_id: int):
    db = SessionLocal()
    veiculo = db.query(VeiculoDB).filter(VeiculoDB.id == veiculo_id).first()
    if veiculo is None:
        raise HTTPException(status_code=404, detail="Veículo não encontrado")
    return to_hateoas(veiculo)

@app.put("/veiculos/{veiculo_id}", response_model=VeiculoResponse)
def atualizar_veiculo(veiculo_id: int, veiculo: Veiculo):
    db = SessionLocal()
    db_veiculo = db.query(VeiculoDB).filter(VeiculoDB.id == veiculo_id).first()
    if db_veiculo is None:
        raise HTTPException(status_code=404, detail="Veículo não encontrado")
    for key, value in veiculo.dict().items():
        setattr(db_veiculo, key, value)
    db.commit()
    db.refresh(db_veiculo)
    return to_hateoas(db_veiculo)

@app.delete("/veiculos/{veiculo_id}")
def deletar_veiculo(veiculo_id: int):
    db = SessionLocal()
    db_veiculo = db.query(VeiculoDB).filter(VeiculoDB.id == veiculo_id).first()
    if db_veiculo is None:
        raise HTTPException(status_code=404, detail="Veículo não encontrado")
    db.delete(db_veiculo)
    db.commit()
    return {"message": "Veículo deletado com sucesso"}

def to_hateoas(veiculo):
    return {
        "id": veiculo.id,
        "marca": veiculo.marca,
        "modelo": veiculo.modelo,
        "ano": veiculo.ano,
        "links": {
            "self": f"/veiculos/{veiculo.id}",
            "update": f"/veiculos/{veiculo.id}",
            "delete": f"/veiculos/{veiculo.id}",
        }
    }
