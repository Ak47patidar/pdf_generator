
from reportlab.lib.pagesizes import LETTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Flowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib import colors

from template import register_fonts, build_doc
from utils import get_data, get_unique_filename, fixed_width, get_raw_data
from reportlab.lib.units import inch
from datetime import datetime
from static_data import FIELD_SPECS, notice_info, assistance_msg
from components import Components


# -------------------- Helper functions --------------------

class MyLineFlowable(Flowable):
    def __init__(self, width, lWidth=2):
        Flowable.__init__(self)
        self.width = width
        self.line_width = lWidth

    def draw(self):
        self.canv.setLineWidth(self.line_width)
        self.canv.setStrokeColor(colors.black)
        self.canv.line(0, 0, self.width, 0)


if __name__ == '__main__':
    data= get_data('A_input_pdf\ECOTN.D1.FMO.SAMPLE.FILE.CLIENT')
    raw_data = get_raw_data(data[0])
    comp = Components(raw_data)
    comp.generate_entire_flow_components(filename="test_output.pdf")
    

