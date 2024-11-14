from fpdf import FPDF
from io import BytesIO
from func import *

def gerar_laudo(card):
    laudo = FPDF(format="A4")
    laudo.add_page()
    laudo.set_margin(20.4)
    line_height = 6.35

    laudo.set_font('helvetica', size=14)
    laudo.multi_cell(0, line_height, f'**LAUDO TÉCNICO {card["ID"]}/{get_ano(card["DATE_CREATE"])}**', 0, "C", markdown=True, ln=1)

    laudo.multi_cell(0, line_height, "", 0, "C", markdown=True, ln=1)

    laudo.set_font('helvetica', size=12)

    laudo.multi_cell(0, line_height, f'**CONSUMIDOR FINAL (RECLAMANTE):** Sr.(a). {card["UF_CRM_1727967417706"]}, portador do CPF n° {card["UF_CRM_1727204145431"]}, residente na {card["UF_CRM_1727204166054"]}, {card["UF_CRM_1728049409"]}, {card["UF_CRM_1727978206065"]}, {card["UF_CRM_1727978359495"]} - {card["UF_CRM_1727978206065"]}.', 0, "J", markdown=True, ln=1)

    laudo.multi_cell(0, line_height, "", 0, "C", markdown=True, ln=1)

    laudo.multi_cell(0, line_height, f'**COMERCIANTE:** {card["UF_CRM_1727204292663"]}, empresa inscrita sob o CNPJ n° {card["UF_CRM_1727204337710"]}', 0, "J", markdown=True, ln=1)

    laudo.multi_cell(0, line_height, "", 0, "C", markdown=True, ln=1)

    laudo.multi_cell(0, line_height, f'**DEFEITO RECLAMADO:** Deformação do reservatório de água feito em {material_correspondente(card["UF_CRM_1727204729359"])} marca FIBRASOL, com capacidade de armazenamento de {capacidade_correspondente(card["UF_CRM_1727204841910"])}. ', 0, "J", markdown=True, ln=1)

    laudo.multi_cell(0, line_height, "", 0, "C", markdown=True, ln=1)

    laudo.multi_cell(0, line_height, '**OBJETIVO:** Emissão de laudo técnico sobre as causas da deformação do reservatório.', 0, "J", markdown=True, ln=1)

    laudo.multi_cell(0, line_height, "", 0, "C", markdown=True, ln=1)

    laudo.multi_cell(0, line_height, f'**INTRODUÇÃO:** No dia {formatar_data_por_extenso(card["UF_CRM_1727204059184"])}, o reclamante comunicou à fabricante que o reservatório adquirido naquela loja, citada acima, tinha sofrido uma deformação, apresentando fotos para comprovar a referida deformação. Por sua vez a fabricante encaminhou no dia posterior o representante Marcelo Lima de Moraes, para fazer alguns registros do ocorrido.', 0, "J", markdown=True, ln=1)

    laudo.multi_cell(0, line_height, "", 0, "C", markdown=True, ln=1)

    laudo.multi_cell(0, line_height, 'Com base na imagem, que acompanha o presente laudo, podemos detectar que ocorreram irregularidades no assentamento, o que ocasionou a deformação do reservatório.', 0, "J", markdown=True, ln=1)

    laudo.multi_cell(0, line_height, "", 0, "C", markdown=True, ln=1)

    laudo.multi_cell(0, 12.7, "Seguem abaixo as irregularidades detectadas:", 0, "J", markdown=True, ln=1)

    for i in range(0, len(card["UF_CRM_1727204591503"])):
        laudo.multi_cell(0, line_height, f"   {i + 1}) {defeito_correspondente(str(card['UF_CRM_1727204591503'][i]))}", 0, "J", markdown=True, ln=1)

    laudo.multi_cell(0, 12.7, "O item 3 do Termo de Garantia, assim dispõe:", 0, "J", markdown=True, ln=1)

    laudo.image('imagens/termo-garantia.png', "C")

    laudo.multi_cell(0, line_height, "", 0, "C", markdown=True, ln=1)

    laudo.multi_cell(0, line_height, "Seguem, em anexo, o termo de garantia que ilustra as normas seguidas pela empresa FIBRASOL, bem como o manual de instalação que acompanha TODAS as Caixas d'água de fibra de vidro e polietileno fabricadas pela empresa, ambos disponíveis para download no site: www.fibrasol.com.br.", 0, "J", markdown=True, ln=1)

    laudo.multi_cell(0, line_height, "", 0, "C", markdown=True, ln=1)

    laudo.multi_cell(0, line_height, "**CONCLUSÃO:** A deformação da caixa d'água não ocorreu por vício/defeito de fabricação, e sim por erros de instalação, o que importa na perda da garantia. ", 0, "J", markdown=True, ln=1)

    laudo.multi_cell(0, 12.7, "", 0, "C", markdown=True, ln=1)

    laudo.multi_cell(0, line_height, f'Jequié, {formatar_data_por_extenso(dt.datetime.now())}', 0, "J", markdown=True, ln=1)

    laudo.multi_cell(0, line_height, "**Michel Barreto**", 0, "J", markdown=True, ln=1)

    laudo.multi_cell(0, line_height, "**Eng. Civil CREA/BA 84147**", 0, "J", markdown=True, ln=1)

    laudo.add_page()

    laudo.image('imagens/termo-de-garantia.png', "C")
    laudo.image('imagens/como-instalar.png', "C")
    laudo.image('imagens/como-instalar-2.png', "C")
    laudo.multi_cell(0, 12.7, "", 0, "C", markdown=True, ln=1)

    imagens_ocorrido = ["UF_CRM_1727204248815", "UF_CRM_1727976978826", "UF_CRM_1727976993920", "UF_CRM_1727977009520", "UF_CRM_1727977032584"]

    for codigo in imagens_ocorrido:
        if codigo in card.keys():
            url = "https://b24-r50tso.bitrix24.com.br" + (card[codigo]["downloadUrl"]) #.replace('\/', '/' )
            response = requests.get(url)
            imagem = BytesIO(response.content)

            laudo.image(imagem, "C", w=laudo.epw)

    arquivo = BytesIO()
    laudo.output(arquivo)
    arquivo.seek(0)
    return arquivo
