from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse
import requests, func, gerar_declaracao, gerar_laudo

app = FastAPI()

@app.get('/gerar-relatorios/{id}')
@app.post('/gerar-relatorios/{id}')
async def gerar_relatorios(id: str):
    try:
        card = func.get_card(id)
    except requests.exceptions.HTTPError as http_err:
        raise HTTPException(status_code=500, detail=f"Erro HTTP ao conectar com Bitrix24: {http_err}")
    except requests.exceptions.RequestException as err:
        raise HTTPException(status_code=500, detail=f"Erro de conexão ao Bitrix24: {err}")
    
    print("card encontrado")
    try:
        declaracao = gerar_declaracao.gerar_declaracao(card)
        laudo = gerar_laudo.gerar_laudo(card)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar relatórios: {e}")
    
    print("cards gerados")
    try:
        func.upload_files(id, [{"caminho": declaracao, "campo": "UF_CRM_1728310643", "nome": "declaracao"}, 
            {"caminho": laudo, "campo": "UF_CRM_1727210242545", "nome": "laudo"}])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao fazer upload dos arquivos: {e}")

    print("upload feito")
    return {"sucesso": True}

@app.get("/auth")
async def pagina_autorizacao():
    return HTMLResponse(open("pages/auth.html").read())

@app.get("/auth/sucess")
async def receber_autorizacao(code: str, state: str, domain: str, member_id: str, scope: str, server_domain: str):
    client_id = 'local.6734b11b47b565.88493778'
    client_secret = 'TkdsVoICCKaicgSOsU2dDbipxz35IiRnY4IJ7AzhCBmezhlvt0'

    url = f"""https://oauth.bitrix.info/oauth/token/?grant_type=authorization_code&client_id={client_id}&client_secret={client_secret}&code={code}"""

    retorno = requests.get(url)
    token = retorno.json()["refresh_token"]
    func.refresh_token_update(token)
    return HTMLResponse(open("pages/sucess.html").read())
