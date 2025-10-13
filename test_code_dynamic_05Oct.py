import os
from reportlab.lib.pagesizes import LETTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Flowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib import colors
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from utils import get_data
from reportlab.lib.units import inch
from datetime import datetime
from static_data import FIELD_SPECS, notice_info, assistance_msg


# -------------------- Font registration --------------------
def register_fonts():
    font_map = {}
    try:
        pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))
        pdfmetrics.registerFont(TTFont('Arial-Bold', 'Arialbd.ttf'))
        pdfmetrics.registerFont(TTFont('Arial-Italic', 'Ariali.ttf'))
        pdfmetrics.registerFont(TTFont('Arial-BoldItalic', 'Arialbi.ttf'))
        font_map['arial'] = ('Arial', 'Arial-Bold')
    except Exception:
        font_map['arial'] = ('Helvetica', 'Helvetica-Bold')
    try:
        pdfmetrics.registerFont(TTFont('Arial-Black', 'ariblk.ttf'))
        font_map['arial_black'] = 'Arial-Black'
    except Exception:
        font_map['arial_black'] = 'Helvetica-Bold'
    try:
        pdfmetrics.registerFont(TTFont('Calibri', 'calibri.ttf'))
        pdfmetrics.registerFont(TTFont('Calibri-Bold', 'calibrib.ttf'))
        pdfmetrics.registerFont(TTFont('Calibri-Italic', 'calibrii.ttf'))
        pdfmetrics.registerFont(TTFont('Calibri-BoldItalic', 'calibriz.ttf'))
        font_map['calibri'] = ('Calibri', 'Calibri-Bold')
    except Exception:
        font_map['calibri'] = ('Helvetica', 'Helvetica-Bold')
    try:
        pdfmetrics.registerFont(TTFont('TimesNewRoman', 'times.ttf'))
        pdfmetrics.registerFont(TTFont('TimesNewRoman-Bold', 'timesbd.ttf'))
        pdfmetrics.registerFont(TTFont('TimesNewRoman-Italic', 'timesi.ttf'))
        pdfmetrics.registerFont(TTFont('TimesNewRoman-BoldItalic', 'timesbi.ttf'))
        font_map['times'] = ('TimesNewRoman', 'TimesNewRoman-Bold')
    except Exception:
        font_map['times'] = ('Times-Roman', 'Times-Bold')
    try:
        pdfmetrics.registerFont(TTFont('CadiaMono-SemiLight', 'CadiaMono-SemiLight.ttf'))
        font_map['cadia_mono_semilight'] = 'CadiaMono-SemiLight'
    except Exception:
        font_map['cadia_mono_semilight'] = 'Courier'
    try:
        pdfmetrics.registerFont(TTFont('CadiaMono-Bold', 'CadiaMono-Bold.ttf'))
        font_map['cadia_mono_bold'] = 'CadiaMono-Bold'
    except Exception:
        font_map['cadia_mono_bold'] = 'Courier-Bold'
    try:
        pdfmetrics.registerFont(TTFont('CadiaMono-Light', 'CadiaMono-Light.ttf'))
        font_map['cadia_mono_light'] = 'CadiaMono-Light'
    except Exception:
        font_map['cadia_mono_light'] = 'Courier'
    return font_map

FONT_MAP = register_fonts()
DEFAULT_FONT, DEFAULT_BOLD = FONT_MAP['arial']
CALIBRI_FONT, CALIBRI_BOLD = FONT_MAP['calibri']
TIMES_FONT, TIMES_BOLD = FONT_MAP['times']
ARIAL_BLACK = FONT_MAP['arial_black']
CADIA_MONO_SEMILIGHT = FONT_MAP['cadia_mono_semilight']
CADIA_MONO_BOLD = FONT_MAP['cadia_mono_bold']
CADIA_MONO_LIGHT = FONT_MAP['cadia_mono_light']


# -------------------- Helper functions --------------------

def fixed_width(value, length, align='left'):
    """Truncate or pad a value to the exact fixed width.

    Args:
        value: value to format (None -> blank)
        length: integer length in characters
        align: 'left' or 'right' (padding side)
    Returns:
        fixed-width string of exactly `length` characters
    """
    if value is None:
        s = ''
    else:
        s = str(value)
    # remove newlines
    s = s.replace('\n', ' ').replace('\r', ' ')
    if len(s) > length:
        return s[:length]
    if align == 'right':
        return s.rjust(length)
    return s.ljust(length)


def get_unique_filename(filename):
    output_dir = "A_Output_pdf"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    base = os.path.join(output_dir, os.path.splitext(os.path.basename(filename))[0])
    ext = os.path.splitext(filename)[1]
    counter = 1
    new_filename = f"{base}{ext}"
    while os.path.exists(new_filename):
        new_filename = f"{base}_{counter}{ext}"
        counter += 1
    return new_filename


class MyLineFlowable(Flowable):
    def __init__(self, width, lWidth=2):
        Flowable.__init__(self)
        self.width = width
        self.line_width = lWidth

    def draw(self):
        self.canv.setLineWidth(self.line_width)
        self.canv.setStrokeColor(colors.black)
        self.canv.line(0, 0, self.width, 0)


# -------------------- Main PDF generator (accepts a data dict) --------------------

def generate_custom_pdf(data=None, filename="test_output.pdf"):
    if data is None:
        raise ValueError("Data dictionary is required for PDF generation.")

    nd = {k.upper(): v for k, v in data.items()}


    filename = get_unique_filename(filename)
    doc = SimpleDocTemplate(filename, 
                            pagesize=LETTER, 
                            rightMargin=10, 
                            leftMargin=10, 
                            topMargin=45, 
                            bottomMargin=30)
    styles = getSampleStyleSheet()

    # monospaced paragraph styles for fixed-width fields
    styles.add(ParagraphStyle(name="MonoSmall", 
                              fontName="Courier", 
                              fontSize=8.5, 
                              leading=10, 
                              alignment=TA_LEFT, 
                              spaceAfter=0, 
                              spaceBefore=0))
    styles.add(ParagraphStyle(name="MonoBold", 
                              fontName="Courier-Bold", 
                              fontSize=8.5, leading=10, 
                              alignment=TA_LEFT, 
                              spaceAfter=0, 
                              spaceBefore=0))
    styles.add(ParagraphStyle(name="Body", 
                              fontName="Helvetica", 
                              fontSize=8.5, 
                              leading=10, 
                              alignment=TA_LEFT, 
                              spaceAfter=0, 
                              spaceBefore=0))

    flow = []

    # --- Build header using fixed-width field formatting where appropriate ---

    # Format key fields to fixed widths
    contract_number_fw = fixed_width(nd.get('CONTRACT-NUMBER', ''), FIELD_SPECS['CONTRACT_NUMBER'], align='right')
    annuitant_fw = fixed_width(nd.get('ANNUITANT-NAME', ''), FIELD_SPECS['ANNUITANT_NAME'])
    owner_fw = fixed_width(nd.get('CONTRACT-OWNER-NAME', ''), FIELD_SPECS['CONTRACT_OWNER_NAME'])
    represent_fw = fixed_width(nd.get('REPRESENT-NAME', ''), FIELD_SPECS['REPRESENT_NAME'])
    phone_fw = fixed_width(nd.get('PHONE-NUMBER', ''), FIELD_SPECS['PHONE_NUMBER'])

    header_block = [
        Paragraph("<b>Equitable Financial Life Insurance Company</b>", styles["MonoSmall"]),
        Paragraph("<b>Equitable Retirement Service Solutions</b>", styles["MonoSmall"]),
        Paragraph("<b>P.O. Box 1016</b>", styles["MonoSmall"]),
        Paragraph("<b>Charlotte NC 28201-1016</b>", styles["MonoSmall"]) 
    ]

    plan_name_fw = fixed_width(nd.get('PLAN-MARKET-NAME', ''), FIELD_SPECS['PLAN_MARKET_NAME'])
    date_str = nd.get('FMO-MATURE-DATE', '')  # default if not present
    contract_date_fw = nd.get('CYCLE-DATE', '')

    date_object = datetime.strptime(date_str, "%Y%m%d")
    contract_date = date_object.strftime("%B %d, %Y")
    contract_date_obj = datetime.strptime(contract_date_fw, "%Y%m%d")
    formatted_date = contract_date_obj.strftime("%B %d, %Y")

    date_and_title = Table([
        [Paragraph(f'<para alignment="right">{formatted_date}</para>', styles["Body"])],
        [Spacer(1, 7)],
        [Paragraph(f'<b>{plan_name_fw.strip()}</b>', styles["Body"])],
    ], colWidths=[270])
    date_and_title.setStyle(TableStyle([
        ("BOX", (0,0), (-1,-1), 0, colors.black),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING", (0,0), (-1,-1), 0),
        ("RIGHTPADDING", (0,0), (-1,-1), 0),
        ("TOPPADDING", (0,0), (-1,-1), 0),
        ("BOTTOMPADDING", (0,0), (-1,-1), 0),
    ]))

    # Contract info: use fixed width values where visually helpful
    contract_info_table = Table([
        [Paragraph("Contract Number:", styles["Body"]), Paragraph(contract_number_fw, styles["Body"])],
        [Paragraph("Contract Date:", styles["Body"]), Paragraph(contract_date, styles["Body"])],
        [Paragraph("Name of Annuitant:", styles["Body"]), Paragraph(annuitant_fw.strip(), styles["Body"])],
        [Paragraph("Contract Owner:", styles["Body"]), Paragraph(owner_fw.strip(), styles["Body"])],
        [Paragraph("Your Representative:", styles["Body"]), Paragraph(represent_fw.strip(), styles["Body"])],
        [Paragraph("Telephone:", styles["Body"]), Paragraph(phone_fw.strip(), styles["Body"])],
    ], colWidths=[110, 140], hAlign="LEFT")
    contract_info_table.setStyle(TableStyle([
        ("BOX", (0,0), (-1,-1), 0, colors.black),
        ("LEFTPADDING", (0,0), (-1,-1), 0),
        ("RIGHTPADDING", (0,0), (-1,-1), 0),
        ("TOPPADDING", (0,0), (-1,-1), 0),
        ("BOTTOMPADDING", (0,0), (-1,-1), 0),
    ]))

    main_info_block = [date_and_title, Spacer(1, 10), contract_info_table]

    top_table = Table([
        ["", header_block, main_info_block]
    ], colWidths=[30, 240, 270])
    top_table.setStyle(TableStyle([
        ("BOX", (0,0), (-1,-1), 0, colors.black),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING", (0,0), (-1,-1), 0),
        ("RIGHTPADDING", (0,0), (-1,-1), 0),
        ("TOPPADDING", (0,0), (-1,-1), 0),
        ("BOTTOMPADDING", (0,0), (-1,-1), 0),
    ]))
    flow.append(top_table)
    flow.append(Spacer(1, 8))

    # Address block: split and apply fixed widths to each line
    # import pdb; pdb.set_trace()
    
    addr_name_fw = fixed_width(nd.get('MAIL-ADDRESSEE-NAME', nd.get('ANNUITANT-NAME', '')), FIELD_SPECS['MAIL_ADDRESSEE_NAME'])
    addr_l1_fw = fixed_width(nd.get('ADDRESSEE-LINE1', ''), FIELD_SPECS['ADDRESSEE_LINE1'])
    addr_l2_fw = fixed_width(nd.get('ADDRESSEE-LINE2', ''), FIELD_SPECS['ADDRESSEE_LINE2'])
    addr_l3_fw = fixed_width(nd.get('ADDRESSEE-LINE3', ''), FIELD_SPECS['ADDRESSEE_LINE3'])
    city_state_zip_fw = fixed_width(nd.get('CITY_STATE_ZIP_CODE', ''), FIELD_SPECS['CITY_STATE_ZIP_CODE'])

    address_table = Table([
        [Paragraph(f'<b>{addr_name_fw}</b>', styles["MonoSmall"])],
        [Paragraph(f'<b>{addr_l1_fw}</b>', styles["MonoSmall"])],
        [Paragraph(f'<b>{addr_l2_fw}</b>' + (' ' + f'<b>{addr_l3_fw.strip()}</b>' if addr_l3_fw.strip() else ''), styles["MonoSmall"])],
    ], colWidths=[540])
    address_table.setStyle(TableStyle([
        ("BOX", (0,0), (-1,-1), 0, colors.black),
        ("LEFTPADDING", (0,0), (-1,-1), 30),
        ("RIGHTPADDING", (0,0), (-1,-1), 0),
        ("TOPPADDING", (0,0), (-1,-1), 0),
        ("BOTTOMPADDING", (0,0), (-1,-1), 0),
    ]))
    flow.append(address_table)
    flow.append(Spacer(1, 8))

    # Assistance block (keeps same text)
    assist_table = Table([
        ["", Paragraph(assistance_msg,
                       styles["Body"]) ]
    ], colWidths=[270, 270])
    assist_table.setStyle(TableStyle([
        ("BOX", (0,0), (-1,-1), 0, colors.black),
        ("LEFTPADDING", (0,0), (-1,-1), 0),
        ("RIGHTPADDING", (0,0), (-1,-1), 0),
        ("TOPPADDING", (0,0), (-1,-1), 0),
        ("BOTTOMPADDING", (0,0), (-1,-1), 0),
    ]))
    flow.append(assist_table)
    flow.append(Spacer(1, 8))

    # FMO Bar
    class FMOBar(Flowable):
        def __init__(self, width, height, text):
            Flowable.__init__(self)
            self.width = width
            self.height = height
            self.text = text

        def draw(self):
            self.canv.setFillColorRGB(0.7, 0.7, 0.7)
            self.canv.rect(0, 0, self.width, self.height, fill=1, stroke=0)
            self.canv.setFillColor(colors.black)
            self.canv.setFont("Helvetica-Bold", 16)
            self.canv.drawCentredString(self.width / 2, 5, self.text)

    flow.append(FMOBar(LETTER[0] - 30, 22, "F M O   M A T U R I T Y   N O T I C E"))
    flow.append(Spacer(1, 12))

    body_lines = notice_info  # imported from static_data.py
    for line in body_lines.values():
        if line:
            flow.append(Paragraph(line[0], styles["Body"]))
        else:
            flow.append(Spacer(1, 4))

    doc.build(flow)
    print(f"✅ PDF generated: {filename}")


if __name__ == '__main__':
    data= get_data('A_input_pdf/ECOTN.D1.FMO.SAMPLE.FILE.CLIENT')
    generate_custom_pdf(data[0])
