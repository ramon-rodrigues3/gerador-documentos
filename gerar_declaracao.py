from fpdf import FPDF
import datetime as dt
from io import BytesIO
from func import *

def gerar_declaracao(card: dict):
    pdf = FPDF(format='A4')
    pdf.add_page()
    pdf.set_margin(20.4)
    line_height = 6.35

    pdf.set_font('arial', size=14)
    pdf.cell(0, 12.7, '''**DECLARAÇÃO**''', align="C", markdown=True, ln=1)
    pdf.cell(0, 12.7, "", align="C", markdown=True, ln=1)

    pdf.set_font('arial', size=12)

    pdf.multi_cell(0, line_height,
        text = f"Eu, {card['UF_CRM_1727967417706']}, inscrito no CPF sob o n.º {card['UF_CRM_1727204145431']}, por meio deste instrumento, declaro estar ciente de que o problema apresentado no reservatório de {capacidade_correspondente(card['UF_CRM_1727204841910'])} em {material_correspondente(card['UF_CRM_1727204729359'])}, marca Fibrasol, adquirido na {card['UF_CRM_1727204292663']}, empresa inscrita no CNPJ nº {card['UF_CRM_1727204337710']}, foi ocasionado por erro de instalação, razão pela qual reconheço que a indústria Fibrasol não tem qualquer responsabilidade pelo rompimento do referido reservatório.", 
        align="L", markdown=True,
        ln=1)

    pdf.cell(0, line_height, "", align="C", markdown=True, ln=1)

    pdf.multi_cell(0, line_height, text=f"Diante da inexistência de vício/defeito de fabricação, declaro que aceito a proposta, feita por mera liberalidade pela empresa Fibrasol, de {card['UF_CRM_1727210375909']}.",
    )

    pdf.cell(0, line_height, "", align="C", markdown=True, ln=1)

    pdf.multi_cell(0, line_height, 
        text=f"Comprometo-me a seguir as orientações para a instalação do novo produto, conforme consignado no laudo técnico nº {card.get('ID')}/{get_ano(card.get('DATE_CREATE'))}, bem como as normas técnicas previstas na NBR 5626 e as instruções contidas no manual de instalação, cujas cópias me foram entregues.",
        align="L", 
        markdown=True,
        ln=1 
    )

    pdf.cell(0, line_height, "", align="C", markdown=True, ln=1)

    pdf.multi_cell(0, line_height, 
        text=f"Jequié, {formatar_data_por_extenso(dt.datetime.now())}",
        align="L", 
        markdown=True,
        ln=1 
    )

    pdf.cell(0, 12.7, "", align="C", markdown=True, ln=1)

    pdf.multi_cell(0, line_height, 
        text="_______________________________________",
        align="L", 
        markdown=True,
        ln=1 
    )

    pdf.multi_cell(0, line_height, 
        text="Assinatura do Cliente",
        align="L", 
        markdown=True,
        ln=1 
    )

    pdf.cell(0, 12.7, "", align="C", markdown=True, ln=1)

    pdf.multi_cell(0, line_height, 
        text="Recebi o novo produto em perfeito estado na data ",
        align="L", 
        markdown=True,
        ln=1 
    )

    pdf.multi_cell(0, 12.7, 
        text="_______/___________________/_______",
        align="L", 
        markdown=True,
        ln=1 
    )

    pdf.cell(0, line_height, "", align="C", markdown=True, ln=1)

    pdf.multi_cell(0, line_height, 
        text="_______________________________________",
        align="L", 
        markdown=True,
        ln=1 
    )

    pdf.multi_cell(0, line_height, 
        text="Assinatura do Cliente",
        align="L", 
        markdown=True,
        ln=1 
    )

    arquivo = BytesIO()
    pdf.output(arquivo)
    arquivo.seek(0)
    return arquivo

