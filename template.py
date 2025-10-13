from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Flowable
from reportlab.lib.pagesizes import LETTER
from Utils.utils import fixed_width, get_unique_filename


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

from Utils.document_templates import PageNumCanvasIR
def build_doc(flow, filename):
    filename = get_unique_filename(filename)
    doc = SimpleDocTemplate(filename, 
                            pagesize=LETTER, 
                            rightMargin=10, 
                            leftMargin=10, 
                            topMargin=45, 
                            bottomMargin=30)
    doc.build(flow)
    # doc.build(flow, canvasmaker=PageNumCanvasIR)
    print(f"✅ PDF generated: {filename}")
    

def register_fonts(font_config):
    pass

def _page_footer_and_header(canvas):
    pass

def _letter_first_page_static_parts(canvas):
    pass

def _define_page_frames(canvas):
    pass


def config_next_page():
    pass


def create_PageNumCanvasIR():
    pass
