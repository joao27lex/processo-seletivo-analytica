from fastapi import FastAPI, HTTPException
import httpx
import uvicorn

app = FastAPI()

async def get_JSON(caminho: str):
    async with httpx.AsyncClient() as client:
        resposta = await client.get(caminho)
        
        if resposta.status_code != 200:
            raise HTTPException(status_code=500, detail="Erro na obtenção dos dados da API")
        
        return resposta.json()


@app.get("/municipio-bairros")
async def obter_id_municipio(municipio: str):
    json_municipios = await get_JSON("https://servicodados.ibge.gov.br/api/v1/localidades/municipios")
    
    id_municipio = None
    for i in json_municipios:
        if i['nome'].lower() == municipio.lower().replace("-", " "):
            id_municipio = i['id']
            print(f'O id do {municipio} é {id_municipio}')
            
    
    if id_municipio is None:
        raise HTTPException(status_code=404, detail=f'{municipio.replace("-", " ")} não encontrado na API do IBGE')
    

    json_bairros = await get_JSON(f"https://servicodados.ibge.gov.br/api/v1/localidades/municipios/{id_municipio}/distritos")
    
    
    return {
        "municipio": municipio.replace("-", " "),
        "bairros": [bairro['nome'] for bairro in json_bairros]  
    }

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
