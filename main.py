from fastapi import FastAPI, HTTPException
import requests, func, gerar_declaracao, gerar_laudo

app = FastAPI()

@app.get('/gerar-relatorios/{id}')
async def gerar_relatorios(id: str):
    try:
        url_bitrix = "https://b24-r50tso.bitrix24.com.br/rest/1/qcjngtkucnuosey4/crm.deal.get.json"
        card = requests.post(
            url_bitrix, 
            headers={'Content-Type': 'application/json'},
            json={"ID": id}
        ).json()['result']
    except requests.exceptions.HTTPError as http_err:
        raise HTTPException(status_code=500, detail=f"Erro HTTP ao conectar com Bitrix24: {http_err}")
    except requests.exceptions.RequestException as err:
        raise HTTPException(status_code=500, detail=f"Erro de conexão ao Bitrix24: {err}")
    
    try:
        declaracao = gerar_declaracao.gerar_declaracao(card)
        laudo = gerar_laudo.gerar_laudo(card)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar relatórios: {e}")
    
    try:
        func.upload_files("12558", [{"caminho": declaracao, "campo": "UF_CRM_1728310643", "nome": "declaracao"}, 
            {"caminho": laudo, "campo": "UF_CRM_1727210242545", "nome": "laudo"}])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao fazer upload dos arquivos: {e}")

    return {"sucesso": True}

