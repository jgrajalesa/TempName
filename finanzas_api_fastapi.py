from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware
from uuid import uuid4

app = FastAPI(title="API Finanzas Personales", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== MODELOS =====
class TransaccionIn(BaseModel):
    tipo: str = Field(..., regex="^(ingreso|gasto)$")
    descripcion: str
    monto: float

class TransaccionOut(TransaccionIn):
    id: str

class Categoria(BaseModel):
    id: str
    nombre: str

class CategoriaIn(BaseModel):
    nombre: str

class PresupuestoIn(BaseModel):
    mes: str  # formato YYYY-MM
    monto: float

class Presupuesto(PresupuestoIn):
    id: str

# ===== ALMACENAMIENTO EN MEMORIA =====
transacciones: List[TransaccionOut] = []
categorias: List[Categoria] = []
presupuestos: List[Presupuesto] = []

# ===== ENDPOINTS TRANSACCIONES =====
@app.post("/transacciones", response_model=TransaccionOut, status_code=201)
def crear_transaccion(trans: TransaccionIn):
    monto = abs(trans.monto)
    if trans.tipo == "gasto":
        monto = -monto
    nueva = TransaccionOut(**trans.dict(), monto=monto, id=str(uuid4()))
    transacciones.append(nueva)
    return nueva

@app.get("/transacciones", response_model=List[TransaccionOut])
def listar_transacciones():
    return transacciones

@app.put("/transacciones/{trans_id}", response_model=TransaccionOut)
def editar_transaccion(trans_id: str, trans: TransaccionIn):
    for i, t in enumerate(transacciones):
        if t.id == trans_id:
            monto = abs(trans.monto)
            if trans.tipo == "gasto":
                monto = -monto
            actualizado = TransaccionOut(**trans.dict(), monto=monto, id=trans_id)
            transacciones[i] = actualizado
            return actualizado
    raise HTTPException(status_code=404, detail="Transacción no encontrada")

@app.delete("/transacciones/{trans_id}", status_code=204)
def eliminar_transaccion(trans_id: str):
    global transacciones
    transacciones = [t for t in transacciones if t.id != trans_id]
    return

# ===== ENDPOINTS CATEGORIAS =====
@app.post("/categorias", response_model=Categoria, status_code=201)
def crear_categoria(cat: CategoriaIn):
    nueva = Categoria(id=str(uuid4()), nombre=cat.nombre)
    categorias.append(nueva)
    return nueva

@app.get("/categorias", response_model=List[Categoria])
def listar_categorias():
    return categorias

@app.put("/categorias/{cat_id}", response_model=Categoria)
def editar_categoria(cat_id: str, cat: CategoriaIn):
    for i, c in enumerate(categorias):
        if c.id == cat_id:
            actualizado = Categoria(id=cat_id, nombre=cat.nombre)
            categorias[i] = actualizado
            return actualizado
    raise HTTPException(status_code=404, detail="Categoría no encontrada")

@app.delete("/categorias/{cat_id}", status_code=204)
def eliminar_categoria(cat_id: str):
    global categorias
    categorias = [c for c in categorias if c.id != cat_id]
    return

# ===== ENDPOINTS PRESUPUESTO =====
@app.post("/presupuesto", response_model=Presupuesto, status_code=201)
def crear_presupuesto(p: PresupuestoIn):
    nuevo = Presupuesto(**p.dict(), id=str(uuid4()))
    presupuestos.append(nuevo)
    return nuevo

@app.get("/presupuesto/{mes}", response_model=Presupuesto)
def ver_presupuesto(mes: str):
    for p in presupuestos:
        if p.mes == mes:
            return p
    raise HTTPException(status_code=404, detail="Presupuesto no encontrado")

@app.put("/presupuesto/{mes}", response_model=Presupuesto)
def modificar_presupuesto(mes: str, nuevo: PresupuestoIn):
    for i, p in enumerate(presupuestos):
        if p.mes == mes:
            actualizado = Presupuesto(**nuevo.dict(), id=p.id)
            presupuestos[i] = actualizado
            return actualizado
    raise HTTPException(status_code=404, detail="Presupuesto no encontrado")

@app.delete("/presupuesto/{mes}", status_code=204)
def eliminar_presupuesto(mes: str):
    global presupuestos
    presupuestos = [p for p in presupuestos if p.mes != mes]
    return
