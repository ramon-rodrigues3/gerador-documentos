from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse
import requests, func, gerar_declaracao, gerar_laudo

app = FastAPI()

def ler_pdf_em_bytes(caminho):
    try: 
        with open(caminho, 'rb') as file:
            file_bytes = file.read()
            return file_bytes
    except FileNotFoundError:
        print(f"Falha ao ler arquivo: {caminho}")
        raise
    except Exception as e:
        print(f"Falha inesperada ao ler arquivo: {e}")
        raise

@app.get('/gerar-relatorios/{id}')
@app.post('/gerar-relatorios/{id}')
async def gerar_relatorios(id: str):
    try:
        card = func.get_card(id)
    except requests.exceptions.HTTPError as http_err:
        raise HTTPException(status_code=500, detail=f"Erro HTTP ao conectar com Bitrix24: {http_err}")
    except requests.exceptions.RequestException as err:
        print(f"Erro de conexão ao Bitrix24: {err}")
        raise HTTPException(status_code=500, detail=f"Erro de conexão ao Bitrix24: {err}")
    
    try:
        declaracao = gerar_declaracao.gerar_declaracao(card)
        #laudo = gerar_laudo.gerar_laudo(card)
    except Exception as e:
        print(f"Erro ao gerar relatórios: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao gerar relatórios: {e}")

    termo_garantia = ler_pdf_em_bytes("docs/TERMO DE GARANTIA 2024.pdf")
    manual_instalacao = ler_pdf_em_bytes("docs/MANUAL DE INSTALAÇÃO FIBRASOL 2024.pdf")
    catalogo_tecnico = ler_pdf_em_bytes("docs/CATÁLOGO TÉCNICO - FIBRASOL_2024. (1)-compactado.pdf")
    
    try:
        func.upload_files(id, [
            {"caminho": declaracao, "campo": "UF_CRM_1728310643", "nome": "declaracao", "incluir_id": True}, 
            #{"caminho": laudo, "campo": "UF_CRM_1727210242545", "nome": "laudo"}
            {"caminho": termo_garantia, "campo": "UF_CRM_1745342775495", "nome": "TERMO DE GARANTIA 2024.pdf"},
            {"caminho": manual_instalacao, "campo": "UF_CRM_1745342810726", "nome": "MANUAL DE INSTALAÇÃO FIBRASOL 2024.pdf"},
            {"caminho": catalogo_tecnico, "campo": "UF_CRM_1745342871251", "nome": "CATÁLOGO TÉCNICO - FIBRASOL_2024. (1)-compactado.pdf"},
        ])
    except Exception as e:
        print(f"Erro ao fazer upload dos arquivos: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao fazer upload dos arquivos: {e}")

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
