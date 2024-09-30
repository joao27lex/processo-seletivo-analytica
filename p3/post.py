from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime
import uvicorn

app = FastAPI()

class Usuario_Dados(BaseModel):
    name: str = Field(pattern = r'^[A-Z][a-zA-Zà-úÀ-Ú]*(\s[A-Z][a-zA-Zà-úÀ-Ú]*)*$')
    birthdate: str = Field(pattern = r'^\d{4}-\d{2}-\d{2}$')
    date: str = Field(pattern = r'^\d{4}-\d{2}-\d{2}$')

@app.post("/age")
async def dados_usuario(user_data: Usuario_Dados):
    
    name = user_data.name 
    
    # Converte as datas para int e as separa no traço
    ano_niver, mes_niver, dia_niver = map(int, user_data.birthdate.split('-'))
    birthdate = datetime(ano_niver, mes_niver, dia_niver)

     
    ano_futuro, mes_futuro, dia_futuro = map(int, user_data.date.split('-'))
    date = datetime(ano_futuro, mes_futuro, dia_futuro)

    if date <= datetime.now():
        raise HTTPException(status_code=400, detail='A data futura não deve ser igual ou mais antiga que a data de hoje')

    data_futura_formatada = f"{dia_futuro}/{mes_futuro}/{ano_futuro}"

    idade_hoje = ((datetime.now() - birthdate).days) // 365
    idade_futura = ((date - birthdate).days) // 365

    return {
        "quote": f"Olá, {name}! Você tem {idade_hoje} anos e em {data_futura_formatada} você terá {idade_futura} anos!",
        "ageNow": idade_hoje,
        "ageThen": idade_futura
    }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)
