#import requests
import datetime
import base64
from main import *
from func import *

def upload():
    with open("guia.pdf", 'rb') as file:
        encoded_file = base64.b64encode(file.read()).decode('utf-8')
        url_upload = "https://b24-r50tso.bitrix24.com.br/rest/1/qcjngtkucnuosey4/crm.deal.update.json"
        
        card = requests.post(
                url_upload, 
                headers={'Content-Type': 'application/json'}, 
                json={"ID": "12558", "fields": {
                    "UF_CRM_1727210242545": {'fileData': ['arquivo.pdf', encoded_file]} }}
        )

    print(card.text)

def busca():
    url_upload = "https://b24-r50tso.bitrix24.com.br/rest/1/qcjngtkucnuosey4/crm.deal.get.json"
    card = requests.post(
                url_upload, 
                headers={'Content-Type': 'application/json'}, 
                json={"ID": "12558"}
    )

    print(card.text)

def outro():
    url = "https://b24-r50tso.bitrix24.com.br/rest/1/qcjngtkucnuosey4/disk.file.getExternalLink"
    card = requests.post(url, json={'id': 17136})

    print(card.text)

def main():
    # url_bitrix = "https://b24-r50tso.bitrix24.com.br/rest/1/qcjngtkucnuosey4/crm.deal.get.json"
    
    # """card = requests.post(
    #     url_bitrix, 
    #     headers={'Content-Type': 'application/json'},
    #     json={"ID": "12558"}
    # ).json()["result"]"""

    # card = func.get_card("12558")

    # caminho = gerar_declaracao.gerar_declaracao(card)
    # laudo = gerar_laudo.gerar_laudo(card)

    # func.upload_files("12558", [{"caminho": caminho, "campo": "UF_CRM_1728310643", "nome": "declaracao"}, 
    #     {"caminho": laudo, "campo": "UF_CRM_1727210242545", "nome": "laudo"}])
    card = get_card(47598)
    proposta = card["UF_CRM_1727210375909"]
    capacidade = card['UF_CRM_1727204841910']
    print(f"'{proposta.strip()}'")
    print(capacidade_correspondente(capacidade))
    #print(dt)

    #gerar_declaracao.gerar_declaracao(card)
    #gerar_laudo.gerar_laudo(card)
    #get_refresh_token()

if __name__ == "__main__":
    main()
