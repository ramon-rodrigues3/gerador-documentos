from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse
import requests, func, gerar_declaracao, gerar_laudo
from datetime import datetime, date
import bitrix

app = FastAPI()

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
    
    try:
        func.upload_files(id, [
            {"file": declaracao, "campo": "UF_CRM_1728310643", "nome": "declaracao", "incluir_id": True}, 
            #{"caminho": laudo, "campo": "UF_CRM_1727210242545", "nome": "laudo"}
            {"caminho": "docs/TERMO DE GARANTIA 2024.pdf", "campo": "UF_CRM_1745342775495", "nome": "TERMO DE GARANTIA 2024.pdf"},
            {"caminho": "docs/MANUAL DE INSTALAÇÃO FIBRASOL 2024.pdf", "campo": "UF_CRM_1745342810726", "nome": "MANUAL DE INSTALAÇÃO FIBRASOL 2024.pdf"},
            {"caminho": "docs/CATÁLOGO TÉCNICO - FIBRASOL_2024. (1)-compactado.pdf", "campo": "UF_CRM_1745342871251", "nome": "CATÁLOGO TÉCNICO - FIBRASOL_2024. (1)-compactado.pdf"},
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

@app.post('/verificar-duplicatas')
def verificar_duplicatas(id: str):

    def diferenca_dias(data: str) -> int:
        data = datetime.fromisoformat(data).date()
        data_atual = date.today()

        return (data_atual - data).days


    negocio = bitrix.deal_get(id)

    id_negocio = negocio.get('ID')
    estagio_negocio = negocio.get('STAGE_ID')
    codigo_cliente_negocio = negocio.get('UF_CRM_1716208405435')
    pipeline_negocio = negocio.get('CATEGORY_ID')

    if estagio_negocio != 'NEW' or pipeline_negocio != '0':
        return JSONResponse(
            {
                "error": {
                    "code": "FORBIDDEN_DELETION_CONSTRAINT",
                    "message": "Este Negócio não é verificável da coluna atual",
                    "details": f"STAGE_ID: {estagio_negocio} | CATEGORY_ID: {pipeline_negocio}"
                }
            }, 
            status_code=403
        )
    
    if not codigo_cliente_negocio:
        return JSONResponse(
            {
                "error": {
                    "code": "MISSING_REQUIRED_FIELD",
                    "message": "O código do cliente (UF_CRM_1716208405435) é um campo obrigatório e não foi encontrado ou está vazio para o negócio fornecido.",
                    "details": "Não é possível verificar duplicatas sem um código de cliente válido."
                }
            }, 
            status_code=400
        )

    negocios_do_mesmo_cliente = bitrix.deal_list(
        {
            "=UF_CRM_1716208405435": codigo_cliente_negocio,
            "!ID": id_negocio,
            "CATEGORY_ID": 0
        },
        ['STAGE_ID', 'STAGE_SEMANTIC_ID', 'CLOSEDATE']
    )

    if not negocios_do_mesmo_cliente:
        return JSONResponse(
            {
                "status": "success", 
                "message": "Item não é duplicado.", 
                "is_duplicate": False 
            },
            status_code=200
        )
    
    for outro in negocios_do_mesmo_cliente:
        outro_estagio = outro.get('STAGE_ID')
        outro_estagio_semantico = outro.get('STAGE_SEMANTIC_ID')
        outro_data_fechameto = outro.get('CLOSEDATE')

        if outro_estagio_semantico.upper() == 'P':
            bitrix.deal_delete(id)
            return JSONResponse(
                {
                    "status": "success",
                    "message": "Negócio duplicado detectado e excluído com sucesso.",
                    "is_duplicate": True,
                    "deleted_item_id": id
                },
                status_code=200
            )

        if not outro_data_fechameto:
            continue

        diferenca = diferenca_dias(outro_data_fechameto)

        if outro_estagio == 'WON' and diferenca < 45:
            bitrix.deal_delete(id)
            return JSONResponse(
                {
                    "status": "success",
                    "message": "Negócio duplicado detectado e excluído com sucesso.",
                    "is_duplicate": True,
                    "deleted_item_id": id
                },
                status_code=200
            )

        if outro_estagio in ['LOSE', 'UC_388957'] and diferenca < 15:
            bitrix.deal_delete(id)
            return JSONResponse(
                {
                    "status": "success",
                    "message": "Negócio duplicado detectado e excluído com sucesso.",
                    "is_duplicate": True,
                    "deleted_item_id": id
                },
                status_code=200
            )

    return JSONResponse(
        {
            "status": "success", 
            "message": "Item não é duplicado.", 
            "is_duplicate": False 
        },
        status_code=200
    )

@app.post('/verificar-credito')
def verificar_credito(id: str):
    negocio = bitrix.deal_get(id)

    estagio = negocio.get('STAGE_ID')
    pipeline = negocio.get("CATEGORY_ID")

    if estagio != "C16:EXECUTING" or pipeline != "16":
        return JSONResponse(
            {
                "error": {
                    "code": "FORBIDDEN_DELETION_CONSTRAINT",
                    "message": "Este Negócio não é verificável da coluna atual",
                    "details": f"STAGE_ID: {estagio} | CATEGORY_ID: {pipeline}"
                }
            }, 
            status_code=403
        )

    codigo_cliente = negocio.get('UF_CRM_1716208405435')

    if not codigo_cliente:
        return JSONResponse(
            {
                "error": {
                    "code": "MISSING_REQUIRED_FIELD",
                    "message": "O código do cliente (UF_CRM_1716208405435) é um campo obrigatório e não foi encontrado ou está vazio para o negócio fornecido.",
                    "details": "Não é possível verificar crédito sem um código de cliente válido."
                }
            }, 
            status_code=400
        )

    equivalente_em_cobranca = bitrix.deal_list(
        {
            "CATEGORY_ID": '12',
            "!STAGE_ID": ['C12:WON'],
            "=UF_CRM_1716208405435": codigo_cliente
        },
        []
    )

    if equivalente_em_cobranca:
        bitrix.deal_update(id, {"STAGE_ID": "C16:UC_IMYYXY"})
        return JSONResponse(
        {
            "status": "success", 
            "message": "O cliente está no funil de cobrança. Negócio enviado para 'Cobrança Prioritária'.", 
            "in_cobranca": True 
        },
        status_code=200
    )
    else:
        bitrix.deal_update(id, {"STAGE_ID": "C16:FINAL_INVOICE"})
        return JSONResponse(
        {
            "status": "success", 
            "message": "O cliente não está no funil de cobrança. Negócio enviado para 'Pronto para Entrega'.", 
            "in_cobranca": False 
        },
        status_code=200
    )
