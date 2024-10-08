import requests
import base64
import datetime as dt

def upload_files(id, lista):
    for arquivo in lista:
        campo = arquivo["campo"]
        file = arquivo["caminho"]
        encoded_file = base64.b64encode(file.read()).decode('utf-8')

        url_upload = "https://b24-r50tso.bitrix24.com.br/rest/1/qcjngtkucnuosey4/crm.deal.update.json"
        response = requests.post(
                url_upload, 
                headers={'Content-Type': 'application/json'}, 
                json={"ID": id, "fields": {
                    campo: {'fileData': [arquivo['nome'] + '-' + id + '.pdf', encoded_file]} }}
        )

def formatar_data_por_extenso(data):
    if isinstance(data, str):
        data = dt.datetime.strptime(data, "%Y-%m-%dT%H:%M:%S%z")
    
    nome_mes = obter_nome_mes(data.month)

    return f"{data.day} de {nome_mes} de {data.year}"

def obter_nome_mes(numero_mes):
    match numero_mes:
        case 1:
            return "Janeiro"
        case 2:
            return "Fevereiro"
        case 3:
            return "Março"
        case 4:
            return "Abril"
        case 5:
            return "Maio"
        case 6:
            return "Junho"
        case 7:
            return "Julho"
        case 8:
            return "Agosto"
        case 9:
            return "Setembro"
        case 10:
            return "Outubro"
        case 11:
            return "Novembro"
        case 12:
            return "Dezembro"

def get_ano(data):
    if isinstance(data, str):
        data = dt.datetime.strptime(data, '%Y-%m-%dT%H:%M:%S%z')
    
    return data.year

def defeito_correspondente(codigo: str) -> str:
    match codigo:
        case "218": 
            return "Reservatório instalado diretamente no chão."
        case "220": 
            return "Caixa instalada sobre areia ou similar."
        case "222": 
            return "Base menor que o fundo do reservatório."
        case "224": 
            return "Base feita de madeira."
        case "226": 
            return "Base gradeada."
        case "228": 
            return "Falta de ancoragem nas tubulações."
        case "230": 
            return "Motor bomba instalado sem a devida ancoragem, transmitindo vibração para a caixa d'água."
        case _: 
            return " "
        
def material_correspondente(codigo: str) -> str: 
    match codigo:
        case "234":
            return "Fibra de vidro"
        case "236":
            return "Polietileno"
        case _: 
            return " "

def capacidade_correspondente(codigo: str) -> str: 
    match codigo:
        case "238":
            return "150 litros"
        case "240":
            return "250 litros"
        case "242": 
            return "300 litros"
        case "244":
            return "500 litros"
        case "246":
            return "1000 litros"
        case "248":
            return "5000 litros"
        case "250":
            return "10000 litros"
        case "252":
            return "15000 litros"
        case "254":
            return "20000 litros"
