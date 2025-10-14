import logging
from datetime import datetime
from typing import Dict, List
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus.flowables import Flowable
from reportlab.platypus import FrameBreak, Paragraph, Table, Image, Spacer
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Flowable
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT
from reportlab.lib import colors
from reportlab.lib.pagesizes import LETTER
from FMO_Letter.static_data import FIELD_SPECS, notice_info, assistance_msg, fundlist_notice
from Utils.utils import fixed_width, get_unique_filename, get_raw_data
from template import register_fonts, build_doc
from reportlab.platypus import Frame, KeepInFrame
# from Utils.document_templates import IRDocTemplate
from reportlab.platypus import BaseDocTemplate, PageTemplate
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Flowable, PageBreak

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

class Components:    
    def __init__(self, contract_data=None):
        self._contract_data = contract_data
        self._flow: List[Flowable] = []
        # self.styles = getSampleStyleSheet()
        self._contract_data = contract_data or {}


        self.styles_MonoSmall = ParagraphStyle(
            name="MonoSmall", 
            fontName="Courier", 
            fontSize=8.5, 
            leading=10, 
            alignment=TA_LEFT, 
            spaceAfter=0, 
            spaceBefore=0
           )
        self.styles_MonoBold = ParagraphStyle(
            name="MonoBold", 
            fontName="Courier-Bold", 
            fontSize=8.5, leading=10, 
            alignment=TA_LEFT, 
            spaceAfter=0, 
            spaceBefore=0
            )
        self.styles_Body = ParagraphStyle(
            name="Body", 
            fontName="Helvetica", 
            fontSize=8.5, 
            leading=10, 
            alignment=TA_LEFT, 
            spaceAfter=0, 
            spaceBefore=0
            )
        self.styles_Body_bold = ParagraphStyle(
            name="Body", 
            fontName="Helvetica-Bold", 
            fontSize=8, 
            leading=10, 
            alignment=TA_LEFT, 
            spaceAfter=0, 
            spaceBefore=0
            )
        
        #style for each para in the notice
        self.notice_info_styles = {
            "0": ParagraphStyle(
                name="Header",
                fontName="arial",
                # fontName=Cambria_FONT,
                fontSize=9,
                leading=12,
                alignment=TA_LEFT,
                spaceAfter=8,
            ),
            "1": ParagraphStyle(
                name="Body1",
                fontName="Calibri",
                # fontName=Cambria_FONT,
                fontSize=9,
                leading=12,
                alignment=TA_JUSTIFY,
                spaceAfter=6,
            ),
            "2": ParagraphStyle(
                name="FundList",
                fontName="calibri",
                fontSize=9.5,
                leading=12,
                alignment=TA_LEFT,
                spaceBefore=6,
                spaceAfter=6,
            ),
            "3": ParagraphStyle(
                name="Body2",
                fontName="Courier",
                fontSize=9,
                leading=12,
                alignment=TA_JUSTIFY,
                spaceAfter=6,
            ),
            "4": ParagraphStyle(
                name="SubHeader",
                fontName="Helvetica-Bold",
                fontSize=10,
                leading=13,
                alignment=TA_LEFT,
                spaceBefore=8,
                spaceAfter=4,
            ),
            "5": ParagraphStyle(
                name="IndentedText",
                fontName="Courier",
                fontSize=8.5,
                leading=11,
                alignment=TA_LEFT,
                leftIndent=10,
                spaceAfter=6,
            ),
            "6": ParagraphStyle(
                name="Signature",
                fontName="Courier-Bold",
                fontSize=9,
                leading=12,
                alignment=TA_LEFT,
                spaceBefore=10,
            ),
            "7": ParagraphStyle(
                name="SSN",
                fontName="Courier",
                fontSize=9,
                leading=12,
                alignment=TA_LEFT,
                spaceAfter=8,
            ),
            "8": ParagraphStyle(
                name="Address",
                fontName="Courier",
                fontSize=8.5,
                leading=11,
                alignment=TA_LEFT,
                spaceBefore=8,
            ),
        }
        
        self.fundlist_notice_styles = {
            "0": ParagraphStyle(
                name="Header",
                fontName="Helvetica-Bold",
                fontSize=11,
                leading=14,
                alignment=TA_LEFT,
                spaceAfter=8,
            ),
            "1": ParagraphStyle(
                name="Body1",
                fontName="Courier",
                fontSize=9,
                leading=12,
                alignment=TA_JUSTIFY,
                spaceAfter=6,
            ),
            "2": ParagraphStyle(
                name="FundList",
                fontName="Courier-Bold",
                fontSize=9.5,
                leading=12,
                alignment=TA_LEFT,
                spaceBefore=6,
                spaceAfter=6,
            ),
            "3": ParagraphStyle(
                name="Body2",
                fontName="Courier",
                fontSize=9,
                leading=12,
                alignment=TA_JUSTIFY,
                spaceAfter=6,
            ),
            "4": ParagraphStyle(
                name="SubHeader",
                fontName="Helvetica-Bold",
                fontSize=10,
                leading=13,
                alignment=TA_LEFT,
                spaceBefore=8,
                spaceAfter=4,
            ),
            "5": ParagraphStyle(
                name="IndentedText",
                fontName="Courier",
                fontSize=8.5,
                leading=11,
                alignment=TA_LEFT,
                leftIndent=10,
                spaceAfter=6,
            ),
            "6": ParagraphStyle(
                name="Signature",
                fontName="Courier-Bold",
                fontSize=9,
                leading=12,
                alignment=TA_LEFT,
                spaceBefore=10,
            ),
            "7": ParagraphStyle(
                name="SSN",
                fontName="Courier",
                fontSize=9,
                leading=12,
                alignment=TA_LEFT,
                spaceAfter=8,
            ),
            "8": ParagraphStyle(
                name="Address",
                fontName="Courier",
                fontSize=8.5,
                leading=11,
                alignment=TA_LEFT,
                spaceBefore=8,
            ),
        }

    def _create_address_string(self):
        addr_name_fw = fixed_width(self._contract_data.get('MAIL-ADDRESSEE-NAME', self._contract_data.get('ANNUITANT-NAME', '')), FIELD_SPECS['MAIL_ADDRESSEE_NAME'])
        addr_l1_fw = fixed_width(self._contract_data.get('ADDRESSEE-LINE1', ''), FIELD_SPECS['ADDRESSEE_LINE1'])
        addr_l2_fw = fixed_width(self._contract_data.get('ADDRESSEE-LINE2', ''), FIELD_SPECS['ADDRESSEE_LINE2'])
        addr_l3_fw = fixed_width(self._contract_data.get('ADDRESSEE-LINE3', ''), FIELD_SPECS['ADDRESSEE_LINE3'])
        city_state_zip_fw = fixed_width(self._contract_data.get('CITY_STATE_ZIP_CODE', ''), FIELD_SPECS['CITY_STATE_ZIP_CODE'])
        address_table = Table([
            ["",Paragraph(f'<b>{addr_name_fw}</b>', self.styles_MonoSmall)],
            ["",Paragraph(f'<b>{addr_l1_fw}</b>', self.styles_MonoSmall)],
            ["",Paragraph(f'<b>{addr_l2_fw}</b>' + (' ' + f'<b>{addr_l3_fw.strip()}</b>' if addr_l3_fw.strip() else ''), self.styles_MonoSmall)],
        # ], colWidths=[540]) #full width of table
        ], colWidths=[50,250], hAlign="LEFT")
        address_table.setStyle(TableStyle([
            ("BOX", (0,0), (-1,-1), 0, colors.black),
            ("GRID", (0,0), (-1,-1), 0, colors.black),
            ("LEFTPADDING", (0,0), (-1,-1), 0),
            ("RIGHTPADDING", (0,0), (-1,-1), 0),
            ("TOPPADDING", (0,0), (-1,-1), 0),
            ("BOTTOMPADDING", (0,0), (-1,-1), 0),
        ]))
        # return address_table
        self._flow.append(address_table)
        self._flow.append(Spacer(1, 8))
    
    def _header_block(self):
        header_block = [
                Paragraph("<b>Equitable Financial Life Insurance Company</b>", self.styles_MonoSmall),
                Paragraph("<b>Equitable Retirement Service Solutions</b>", self.styles_MonoSmall),
                Paragraph("<b>P.O. Box 1016</b>", self.styles_MonoSmall),
                Paragraph("<b>Charlotte NC 28201-1016</b>", self.styles_MonoSmall) 
            ]
        return header_block

    def	_add_date_and_title(self):
        plan_name_fw = fixed_width(self._contract_data.get('PLAN-MARKET-NAME', ''), FIELD_SPECS['PLAN_MARKET_NAME'])
        contract_date_fw = self._contract_data.get('CYCLE-DATE', '')

        contract_date_obj = datetime.strptime(contract_date_fw, "%Y%m%d")
        formatted_date = contract_date_obj.strftime("%B %d, %Y")
        
        date_and_title = Table([
            [Paragraph(f'<para alignment="right">{formatted_date}</para>',self.styles_Body)],
            [Spacer(1, 7)],
            [Paragraph(f'<b>{plan_name_fw.strip()}</b>', self.styles_Body)],
        ], colWidths=[280])
        date_and_title.setStyle(TableStyle([
            ("BOX", (0,0), (-1,-1), 0, colors.black),
            # ("GRID", (0,0), (-1,-1), 0, colors.black),
            ("VALIGN", (0,0), (-1,-1), "TOP"),
            ("LEFTPADDING", (0,0), (-1,-1), 1),
            ("RIGHTPADDING", (0,0), (-1,-1), 0),
            ("TOPPADDING", (0,0), (-1,-1), 0),
            ("BOTTOMPADDING", (0,0), (-1,-1), 0),
        ]))
        return date_and_title
        
    def _add_top_right_contract_info(self):
        date_str = self._contract_data.get('FMO-MATURE-DATE', '')  # default if not present
        date_object = datetime.strptime(date_str, "%Y%m%d")
        contract_date = date_object.strftime("%B %d, %Y")

        contract_number_fw = fixed_width(self._contract_data.get('CONTRACT-NUMBER', ''), 
                                        FIELD_SPECS['CONTRACT_NUMBER'], align='right')
        annuitant_fw = fixed_width(self._contract_data.get('ANNUITANT-NAME', ''), 
                                FIELD_SPECS['ANNUITANT_NAME'])
        owner_fw = fixed_width(self._contract_data.get('CONTRACT-OWNER-NAME', ''), 
                            FIELD_SPECS['CONTRACT_OWNER_NAME'])
        represent_fw = fixed_width(self._contract_data.get('REPRESENT-NAME', ''), 
                                FIELD_SPECS['REPRESENT_NAME'])
        phone_fw = fixed_width(self._contract_data.get('PHONE-NUMBER', ''), 
                            FIELD_SPECS['PHONE_NUMBER'])

        data = [
            ["Contract Number:", contract_number_fw],
            ["Contract Date:", contract_date],
            ["Name of Annuitant:", annuitant_fw.strip()],
            ["Contract Owner:", owner_fw.strip()],
            ["Your Representative:", represent_fw.strip()],
            ["Telephone:", phone_fw.strip()],
        ]

        contract_info_table = Table(data, colWidths=[110, 160], hAlign="LEFT")

        contract_info_table.setStyle(TableStyle([
            # 🔲 Draw grid lines for all cells (rows + columns)
            ("GRID", (0, 0), (-1, -1), 0.8, colors.black),

            # Outer border (optional — makes edges bolder)
            # ("BOX", (0, 0), (-1, -1), 1.2, colors.black),

            # Padding and alignment
            ("LEFTPADDING", (0, 0), (-1, -1), 1),
            ("RIGHTPADDING", (0, 0), (-1, -1), 3),
            ("TOPPADDING", (0, 0), (-1, -1), 2),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

            # Fonts for labels vs. values
            ("FONTNAME", (0, 0), (0, -1), "Helvetica"),  # Left column bold
            ("FONTNAME", (0, 0), (1, -1), "Helvetica"),       # Right column normal
            ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ]))

        return contract_info_table

    def _top_table(self, header_block, main_info_block):
        top_table = Table([
            ["", header_block, main_info_block]
        # ], colWidths=[30, 240, 270])  #3 columns with limited width
        ], colWidths=[50, 250, 280], hAlign="LEFT") #full width of table
        top_table.setStyle(TableStyle([
            ("GRID", (0,0), (-1,-1), 1, colors.black),
            # ("BOX", (0,0), (-1,-1), 0, colors.black),
            ("VALIGN", (0,0), (-1,-1), "TOP"),
            ("LEFTPADDING", (0,0), (-1,-1), 0),
            ("RIGHTPADDING", (0,0), (-1,-1), 0),
            ("TOPPADDING", (0,0), (-1,-1), 0),
            ("BOTTOMPADDING", (0,0), (-1,-1), 0),
        ]))
        # return top_table
        self._flow.append(top_table)
        self._flow.append(Spacer(1, 8))
    
    def _assistance_table(self):
        assist_table = Table([
            [Paragraph(assistance_msg,
                            self.styles_Body_bold), ""]
        # ], colWidths=[270, 270]) #full width of table
        ], colWidths=[270, 10], hAlign="RIGHT")
        assist_table.setStyle(TableStyle([
            ("BOX", (0,0), (-1,-1), 0, colors.black),
            ("GRID", (0,0), (-1,-1), 0, colors.black),
            ("LEFTPADDING", (0,0), (-1,-1), 1),
            ("RIGHTPADDING", (0,0), (-1,-1), 0),
            ("TOPPADDING", (0,0), (-1,-1), 0),
            ("BOTTOMPADDING", (0,0), (-1,-1), 0),
        ]))
        # return assist_table  
        self._flow.append(assist_table)        
        self._flow.append(Spacer(1, 8))
        
    def _add_notice_body(self, notice_data, notice_styles):
        """
        Creates a single-column table from fundlist_notice data,
        where each row can have its own style (font size, leading, spacing).
        """

        # Default fallback style
        default_style = ParagraphStyle(
            name="Default",
            fontName="Courier",
            fontSize=9,
            leading=12,
            alignment=TA_LEFT,
        )

        # 🧱 Build table data
        table_data = []
        for key, value in notice_data.items():
            if value and value[0].strip():
                text = value[0].replace("\n", "<br/>")
                style = notice_styles.get(key, default_style)
                table_data.append([Paragraph(text.strip(), style)])
            else:
                table_data.append([" "])

        # 🧾 Create table
        table = Table(table_data, colWidths=[580])

        # ✏️ Apply black border and padding
        table.setStyle(TableStyle([
            # ("GRID", (0, 0), (-1, -1), 0.8, colors.black),
            ("BOX", (0, 0), (-1, -1), 1, colors.black),
            ("LEFTPADDING", (0, 0), (-1, -1), 5),
            ("RIGHTPADDING", (0, 0), (-1, -1), 5),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ]))

        self._flow.append(table)
        self._flow.append(Spacer(1, 12))
              
        
    def	generate_entire_flow_components(self, filename="test_output.pdf"): 
        '''this method will contain code of generate_custom_pdf() method to call all internal methods'''

        filename = get_unique_filename(filename)       
        header_block = self._header_block()
        date_and_title = self._add_date_and_title()
        contract_info_table = self._add_top_right_contract_info()

        main_info_block = [date_and_title, Spacer(1, 10), contract_info_table]

        self._top_table(header_block, main_info_block)       
        self._create_address_string()        
        self._assistance_table()
        
        self._flow.append(FMOBar(LETTER[0] - 30, 22, "F M O   M A T U R I T Y   N O T I C E"))
        self._flow.append(Spacer(1, 12))
        
        self._add_notice_body(notice_info, self.notice_info_styles)
        self._flow.append(PageBreak())

        self._flow.append(self._top_table(header_block, main_info_block))
        self._create_address_string()        
        self._assistance_table()
        self._flow.append(FMOBar(LETTER[0] - 30, 22, "F M O   M A T U R I T Y   N O T I C E"))
        self._flow.append(Spacer(1, 12))
        # self._add_notice_body(fundlist_notice, self.fundlist_notice_styles)
        build_doc(self._flow, filename)

        
    
    # def	_generate_extras(): pass
    # def	_add_top_right_text(): pass
    # def	_add_bold_title(): pass
    
    # def	_add_signature_and_ending(): pass
    # def	_generate_no_unique_id_nigo_letter(): pass
        

    

