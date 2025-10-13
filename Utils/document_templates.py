from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.pdfbase.pdfdoc import PDFDictionary
from reportlab.lib.enums import TA_LEFT, TA_JUSTIFY
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import grey
from reportlab.pdfgen.textobject import PDFTextObject
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    FrameBreak,
    PageTemplate,
    Paragraph,
    Table,
    Flowable,
)
from collections import OrderedDict
from datetime import datetime

from Utils.component_models import ParagraphChunk, StringFormattingOperations

class IRDocTemplate(BaseDocTemplate):
    """
    Override the BaseDocTemplate class to split even/odd pages or conditions on even or odd pages

    This implementation affects both RC and ACCUM SOAs. So, keep that in mind before making changes
    """

    def __init__(self, *args, **kwargs):
        BaseDocTemplate.__init__(self, *args, **kwargs)
        self.__pageNum = 1

    def afterPage(self):
        """
        Called after all flowables have been drawn on a page
        """
        # Increment pageNum since the page has been completed
        self.__pageNum += 1
        if self.__pageNum == 1:
            self._handle_nextPageTemplate("page_1")
        if self.__pageNum % 2 == 0:
            self._handle_nextPageTemplate("evenpage")
        else:
            self._handle_nextPageTemplate("oddpage")

    def _handle_nextPageTemplate(self, template_id):
        """
        Handle the next page template based on the template ID
        """
        frame_id = f"{template_id}_frame"
        if frame_id not in self.frames:
            raise ValueError(f"Frame {frame_id} not found in frames")
        frame = self.frames[frame_id]
        if frame.canFitWidth(self.__pageNum):
            self.addPageTemplates([PageTemplate(id=template_id, frames=[frame])])

class PageNumCanvasIR(canvas.Canvas):
    """
    An extended canvas to do post processing on pages such as add page numbers and PPD
    """

    def __init__(self, *args, **kwargs):
        """Constructor"""
        canvas.Canvas.__init__(self, *args, **kwargs)
        self.pages = []

    def showPage(self):
        """
        On a page break, add information to the list
        """
        self.pages.append(dict(self.__dict__))

    def save(self):
        """
        Add the page number to each page (page x of y)
        """
        for page_info in self.pages:
            if 'pageNum' in page_info:
                self.draw_page_number(page_info["pageNum"], len(self.pages))

    def draw_page_number(self, page_number, total_pages):
        """
        Draw the page number on the canvas
        """
        self.setFont("Helvetica", 8)
        self.setFillColor(grey(0.8))
        self.drawString(550, 10, f"Page {page_number} of {total_pages}")