from fpdf import FPDF
import datetime as dt
from io import BytesIO
from func import *

def gerar_declaracao(card: dict):
    pdf = FPDF(format='A4')
    pdf.add_page()
    pdf.set_margin(20.4)
    line_height = 6.35

    pdf.set_font('arial', size=21)
    pdf.cell(0, 12.7, '''**DECLARAÇÃO**''', align="C", markdown=True, ln=1)
    pdf.cell(0, 12.7, "", align="C", markdown=True, ln=1)

    pdf.set_font('arial', size=13)

    pdf.multi_cell(0, line_height,
        text = f"""Eu, **{card['UF_CRM_1727967417706']}**, inscrito no CPF de n° **{card['UF_CRM_1727204145431']}**, residente em **{card["UF_CRM_1727978359495"]}** declaro estar ciente de que o problema apresentado no reservatório de **{material_correspondente(card['UF_CRM_1727204729359'])}**, com capacidade para **{capacidade_correspondente(card['UF_CRM_1727204841910'])}**, marca FIBRASOL, adquirido através da compra realizada no estabelecimento **{card['UF_CRM_1727204292663']}**, cujo CNPJ consta **{card['UF_CRM_1727204337710']}**, foi ocasionado por erro de instalação, razão pela qual reconheço que a Indústria **não tem qualquer responsabilidade pela deformação do referido reservatório.**""", 
        align="J", markdown=True,
        ln=1)

    pdf.cell(0, line_height, "", align="C", markdown=True, ln=1)

    pdf.multi_cell(0, line_height, 
        text=f"**Devido à inexistência de vícios no referido produto**, declaro que aceito a proposta apresentada, por mera liberalidade, pela empresa **FIBRASOL**, a qual se dispõe a **{proposta_correspondente(card["UF_CRM_1745321600712"])}**, com intermédio da empresa revendedora.", 
        align="J", markdown=True
    )

    pdf.cell(0, line_height, "", align="C", markdown=True, ln=1)

    pdf.multi_cell(0, line_height, 
        text=f"Comprometo-me, desta forma, a seguir as orientações para a instalação do novo reservatório, bem como as normas técnicas previstas na **NBR 5626**, **NBR 14800**, e as demais expressas no manual de instalação fixado no produto, cujas cópias também foram entregues a mim nesta oportunidade.",
        align="J", 
        markdown=True,
        ln=1 
    )

    pdf.cell(0, line_height, "", align="C", markdown=True, ln=1)

    pdf.set_font('arial', size=14)
    pdf.multi_cell(0, line_height, 
        text=f"{card["UF_CRM_1727978359495"].strip()} - {estado_correspondente(card["UF_CRM_1727977680889"])}, {dt.datetime.now().strftime("%d/%m/%Y")}".upper(),
        align="L", 
        markdown=True,
        ln=1 
    )

    pdf.set_font('arial', size=13)
    pdf.cell(0, 50.8, "", align="C", markdown=True, ln=1)

    pdf.multi_cell(0, line_height, 
        text="____________________________________________________",
        align="C", 
        markdown=True,
        ln=1 
    )

    pdf.set_font('arial', size=16)
    pdf.multi_cell(0, line_height, 
        text=f"{card['UF_CRM_1727967417706']}".upper(),
        align="C", 
        markdown=True,
        ln=1 
    )
    pdf.multi_cell(0, line_height, 
        text=f"{card['UF_CRM_1727204145431']}".upper(),
        align="C", 
        markdown=True,
        ln=1 
    )

    arquivo = BytesIO()
    pdf.output(arquivo)
    arquivo.seek(0)
    return arquivo

