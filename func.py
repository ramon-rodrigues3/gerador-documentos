import requests
import base64
import datetime as dt
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker
from fastapi import Depends, HTTPException
from dotenv import load_dotenv, find_dotenv
from os import environ
import logging

load_dotenv(find_dotenv())

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ROOT_URL = environ.get("ROOT_URL")
DB_URL = environ.get("DB_URL")

engine = create_engine(DB_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_card(id) -> dict:
    acess_token = get_acess_token()
    url_bitrix = ROOT_URL + "crm.deal.get.json"

    response = requests.post(
        url_bitrix, 
        headers={'Content-Type': 'application/json'},
        json={
            "ID": id,
            "auth": acess_token
            }
    )

    card = response.json()['result']

    return card

def get_acess_token() -> str:
    refresh_token = get_refresh_token()
    client_id = 'local.6734b11b47b565.88493778'
    client_secret = 'TkdsVoICCKaicgSOsU2dDbipxz35IiRnY4IJ7AzhCBmezhlvt0'
    url = f"https://oauth.bitrix.info/oauth/token/?grant_type=refresh_token&client_id={client_id}&client_secret={client_secret}&refresh_token={refresh_token}"

    response = requests.get(url)
    #print(response.text) 
    if response.status_code == 200:
        dados = response.json()
        refresh_token_update(dados["refresh_token"])
        return dados["access_token"]
    raise Exception("Erro de execução")

def get_refresh_token() -> str:
    db: Session = SessionLocal()
    try:
        token = db.execute(text("SELECT token FROM bitrix_refresh_tokens WHERE id = 1")).scalar()
        if not token:
            raise HTTPException(
                status_code=403, 
                detail="A aplicação precisa de permissão"
            )
        return token
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Erro ao buscar token: {str(e)}"
        )
    finally:
        db.close()

def refresh_token_update(new_token: str) -> None:
    db = SessionLocal()
    try:
        result = db.execute(
            text("SELECT token FROM bitrix_refresh_tokens WHERE id = 1")
        ).fetchone()

        if result:
            db.execute(
                text("UPDATE bitrix_refresh_tokens SET token = :token WHERE id = 1"),
                {"token": new_token}
            )
        else:
            db.execute(
                text("INSERT INTO bitrix_refresh_tokens (id, token) VALUES (1, :token)"),
                {"token": new_token}
            )
        
        db.commit()

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500, 
            detail="Falha ao atualizar token"
        )
    finally:
        db.close()

def upload_files(id, lista) -> None:
    acess_token = get_acess_token()

    for arquivo in lista:
        campo = arquivo["campo"]
        caminho = arquivo.get("caminho")
        incluir_id = arquivo.get("incluir_id", False)

        file = open(caminho, 'rb').read() if caminho else arquivo["file"].read()

        encoded_file = base64.b64encode(file).decode('utf-8')
        nome_arquivo = arquivo['nome'] + '-' + id + '.pdf' if incluir_id else arquivo['nome']
        url_upload = ROOT_URL + "crm.deal.update.json"
        response = requests.post(
                url_upload, 
                headers={'Content-Type': 'application/json'}, 
                json={
                    "ID": id, 
                    "fields": {
                        campo: {
                            'fileData': [nome_arquivo, encoded_file]
                        } 
                    },
                    'auth': acess_token
                }
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
        case "234":
            return "Fissura do reservatório de água feito em fibra de vidro"
        case "236":
            return "Deformação do reservatório de água feito em polietileno"
        case _: 
            return " "

def irregularidade_correspondente(codigo: str) -> str:
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
        case "7802":
            return "Reparo impróprio."
        case "8032":
            return "Base desnivelada."
        case "8034":
            return "Estrutura imprópria para peso do reservatório."
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
        case "7808":
            return "3000 litros"
        case _:
            return ""

def estado_correspondente(codigo: str) -> str:
    match codigo:
        case "7694":
            return "Acre"
        case "7696":
            return "Alagoas"
        case "7698":
            return "Amapá"
        case "7700":
            return "Amazonas"
        case "7702":
            return "Bahia"
        case "7704":
            return "Ceará"
        case "7706":
            return "Distrito Federal"
        case "7708":
            return "Espírito Santo"
        case "7710":
            return "Goiás"
        case "7712":
            return "Maranhão"
        case "7714":
            return "Mato Grosso"
        case "7716":
            return "Mato Grosso do Sul"
        case "7718":
            return "Minas Gerais"
        case "7720":
            return "Pará"
        case "7722":
            return "Paraíba"
        case "7724":
            return "Paraná"
        case "7726":
            return "Pernambuco"
        case "7728":
            return "Piauí"
        case "7730":
            return "Rio de Janeiro"
        case "7732":
            return "Rio Grande do Norte"
        case "7734":
            return "Rio Grande do Sul"
        case "7736":
            return "Rondônia"
        case "7738":
            return "Roraima"
        case "7740":
            return "Santa Catarina"
        case "7742":
            return "São Paulo"
        case "7744":
            return "Sergipe"
        case "7746":
            return "Tocantins"
        case _:
            return ""
        
def proposta_correspondente(codigo: str) -> str:
    match codigo:
        case "7960":
            return "conceder um desconto de 10% na aquisição de um novo reservatório, similar ao sinistrado"
        case "7962":
            return "conceder um desconto de 15% na aquisição de um novo reservatório, similar ao sinistrado"
        case "7964":
            return "conceder um desconto de 20% na aquisição de um novo reservatório, similar ao sinistrado"
        case "7966":
            return "conceder um desconto de 25% na aquisição de um novo reservatório, similar ao sinistrado"
        case "7968":
            return "conceder um desconto de 30% na aquisição de um novo reservatório, similar ao sinistrado"
        case "7970":
            return "conceder um desconto de 35% na aquisição de um novo reservatório, similar ao sinistrado"
        case "7972":
            return "conceder um desconto de 40% na aquisição de um novo reservatório, similar ao sinistrado"
        case "7974":
            return "conceder um desconto de 45% na aquisição de um novo reservatório, similar ao sinistrado"
        case "7976":
            return "conceder um desconto de 50% na aquisição de um novo reservatório, similar ao sinistrado"
        case "7978":
            return "conceder um desconto de 55% na aquisição de um novo reservatório, similar ao sinistrado"
        case "7980":
            return "conceder um desconto de 60% na aquisição de um novo reservatório, similar ao sinistrado"
        case "7982":
            return "conceder um desconto de 65% na aquisição de um novo reservatório, similar ao sinistrado"
        case "7984":
            return "conceder um desconto de 70% na aquisição de um novo reservatório, similar ao sinistrado"
        case "7986":
            return "conceder um desconto de 75% na aquisição de um novo reservatório, similar ao sinistrado"
        case "7988":
            return "conceder um desconto de 80% na aquisição de um novo reservatório, similar ao sinistrado"
        case "7990":
            return "conceder um desconto de 85% na aquisição de um novo reservatório, similar ao sinistrado"
        case "7992":
            return "conceder um desconto de 90% na aquisição de um novo reservatório, similar ao sinistrado"
        case "7994":
            return "conceder um desconto de 95% na aquisição de um novo reservatório, similar ao sinistrado"
        case "7996":
            return "enviar um novo reservatório, similar ao sinistrado, sem custos"
        case _:
            return ""