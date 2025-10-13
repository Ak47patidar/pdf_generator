'''
Created on Apr 10, 2019

    @author: C117567
'''
import json
import logging
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase.ttfonts import TTFont, pdfmetrics
from reportlab.platypus import BaseDocTemplate, Flowable
from reportlab.pdfgen import canvas



logger = logging.getLogger(__name__)

pdfmetrics.registerFont(TTFont('Arial', 'Arial.TTF'))
pdfmetrics.registerFont(TTFont('Arial-Bold', 'Arialbd.ttf'))
pdfmetrics.registerFont(TTFont('Arial-BoldItalic', 'arialbi.ttf'))
pdfmetrics.registerFont(TTFont('Arial-Italic', 'ariali.ttf'))
pdfmetrics.registerFont(TTFont('Times', 'times.ttf'))

logo_width = 3 * inch
logo_height = .7 * inch

styles = getSampleStyleSheet()


# class Preformatted(Flowable):
#     """This is like the HTML <PRE> tag.
#     It attempts to display text exactly as you typed it in a fixed width "typewriter" font.
#     By default the line breaks are exactly where you put them, and it will not be wrapped.
#     You can optionally define a maximum line length and the code will be wrapped; and
#     extra characters to be inserted at the beginning of each wrapped line (e.g. '> ').
#     """
#
#     def __init__(self, text, style, bulletText = None, dedent=0, maxLineLength=None, splitChars=None, newLineChars=""):
#         """text is the text to display. If dedent is set then common leading space
#         will be chopped off the front (for example if the entire text is indented
#         6 spaces or more then each line will have 6 spaces removed from the front).
#         """
#         self.style = style
#         self.bulletText = bulletText
#         self.lines = _dedenter(text,dedent)
#         if text and maxLineLength:
#             self.lines = splitLines(
#                                 self.lines,
#                                 maxLineLength,
#                                 splitChars,
#                                 newLineChars
#                         )

class MyLineFlowable(Flowable):
    """
        A Custom Line Flowable
        How to use:
        plain black line
            self.line_1 = MyLineFlowable(525, lWidth = 0.5)
        create_section_divider method of GR_SOA class uses following 2 lines
        for grey section divider
            line = MyLineFlowable(525, lWidth = 1.5, tColor=sc.grey)
            line_2 = MyLineFlowable(0, height = 0, xS = -15, yS = -20, lWidth = 1.5,tColor=sc.grey)
    """

    def __init__(self, width, height=0, xS=0, yS=0, lWidth=1.0, tColor='black'):
        Flowable.__init__(self)
        self.width = width
        self.height = height
        self.line_width = lWidth
        self.txcolor = tColor
        self.xCord = xS
        self.yCord = yS

    def __repr__(self):
        return "Line(w=%s)" % self.width

    def draw(self):
        """
        draw the line
        """
        self.canv.setLineWidth(self.line_width)
        self.canv.setStrokeColor(self.txcolor)
        self.canv.line(self.xCord, self.yCord, self.width, self.height)

class IRDocTemplate(BaseDocTemplate):
    """Override the BaseDocTemplate class to split even/odd pages"""

    def __init__(self, *args, **kwargs):
        BaseDocTemplate.__init__(self, *args, **kwargs)
        self.__pageNum = 1

    def afterPage(self):
        """Called after all flowables have been drawn on a page"""

        # Increment pageNum since the page has been completed
        self.__pageNum += 1
        if self.__pageNum == 1:
            self._handle_nextPageTemplate('IR_SOA_page1_static_parts')
        if self.__pageNum % 2 == 0:
            self._handle_nextPageTemplate("evenpage")
        else:
            self._handle_nextPageTemplate("oddpage")


# ------IR---------CUSTOMIZED CANVAS-------
class PageNumCanvasIR(canvas.Canvas):
    print("inside PageNumCanvasIR")
    def __init__(self, *args, **kwargs):
        """Constructor"""
        canvas.Canvas.__init__(self, *args, **kwargs)
        self.pages = []

    def showPage(self):
        """
        On a page break, add information to the list
        """
        print("inside showPage")
        self.pages.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        canvas.Canvas.save(self)
        
    # def add_page(self):
    #     """
    #     Add the page number to each page (page x of y)
    #     """
    #     page_count = len(self.pages)

    #     # For adding a blank page
    #     blank_page_added = False
    #     if page_count % 2 != 0:  # if odd
    #         page_count += 1
    #         blank_page_added = True

    #     # for drawing page number
    #     for page in self.pages:
    #         self.__dict__.update(page)
    #         self.draw_page_number(page_count, blank_page_added)
    #         canvas.Canvas.showPage(self)

    #     canvas.Canvas.save(self)

    # # def draw_page_number(self, page_count, blank_page_added):
    #     """
    #     Add the page number
    #     """
    #     page = "Page %s of %s" % (self._pageNumber, page_count)
    #     self.setFont("Arial", 7)
    #     if self._pageNumber == 1:
    #         self.drawString(7.4 * inch, 0.19 * inch, page)
    #     if self._pageNumber > 1:

    #         if blank_page_added == True:
    #             self.drawString(7.4 * inch, 0.19 * inch, page)
    #             if self._pageNumber == (page_count - 1):
    #                 canvas.Canvas.showPage(self)
    #                 self.drawCentredString(4 * inch, 5.5 * inch, " ")
    #         elif blank_page_added == False:
    #             if self._pageNumber == page_count:
    #                 pass
    #             else:
    #                 self.drawString(7.4 * inch, 0.19 * inch, page)

