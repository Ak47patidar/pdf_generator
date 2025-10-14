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
        
            
        # self._generate_extras()
    def _create_address_string(self):
        addr_name_fw = fixed_width(self._contract_data.get('MAIL-ADDRESSEE-NAME', self._contract_data.get('ANNUITANT-NAME', '')), FIELD_SPECS['MAIL_ADDRESSEE_NAME'])
        addr_l1_fw = fixed_width(self._contract_data.get('ADDRESSEE-LINE1', ''), FIELD_SPECS['ADDRESSEE_LINE1'])
        addr_l2_fw = fixed_width(self._contract_data.get('ADDRESSEE-LINE2', ''), FIELD_SPECS['ADDRESSEE_LINE2'])
        addr_l3_fw = fixed_width(self._contract_data.get('ADDRESSEE-LINE3', ''), FIELD_SPECS['ADDRESSEE_LINE3'])
        city_state_zip_fw = fixed_width(self._contract_data.get('CITY_STATE_ZIP_CODE', ''), FIELD_SPECS['CITY_STATE_ZIP_CODE'])
        address_table = Table([
            [Paragraph(f'<b>{addr_name_fw}</b>', self.styles_MonoSmall)],
            [Paragraph(f'<b>{addr_l1_fw}</b>', self.styles_MonoSmall)],
            [Paragraph(f'<b>{addr_l2_fw}</b>' + (' ' + f'<b>{addr_l3_fw.strip()}</b>' if addr_l3_fw.strip() else ''), self.styles_MonoSmall)],
        ], colWidths=[540])
        address_table.setStyle(TableStyle([
            ("BOX", (0,0), (-1,-1), 0, colors.black),
            ("LEFTPADDING", (0,0), (-1,-1), 30),
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
        ], colWidths=[270])
        date_and_title.setStyle(TableStyle([
            ("BOX", (0,0), (-1,-1), 0, colors.black),
            ("VALIGN", (0,0), (-1,-1), "TOP"),
            ("LEFTPADDING", (0,0), (-1,-1), 0),
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

        contract_info_table = Table(data, colWidths=[110, 140], hAlign="LEFT")

        contract_info_table.setStyle(TableStyle([
            # 🔲 Draw grid lines for all cells (rows + columns)
            ("GRID", (0, 0), (-1, -1), 0.8, colors.black),

            # Outer border (optional — makes edges bolder)
            ("BOX", (0, 0), (-1, -1), 1.2, colors.black),

            # Padding and alignment
            ("LEFTPADDING", (0, 0), (-1, -1), 3),
            ("RIGHTPADDING", (0, 0), (-1, -1), 3),
            ("TOPPADDING", (0, 0), (-1, -1), 2),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

            # Fonts for labels vs. values
            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),  # Left column bold
            ("FONTNAME", (1, 0), (1, -1), "Helvetica"),       # Right column normal
            ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ]))

        return contract_info_table

    def _top_table(self, header_block, main_info_block):
        top_table = Table([
            ["", header_block, main_info_block]
        ], colWidths=[30, 240, 270])
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
            ["", Paragraph(assistance_msg,
                            self.styles_Body_bold) ]
        ], colWidths=[270, 270])
        assist_table.setStyle(TableStyle([
            ("BOX", (0,0), (-1,-1), 0, colors.black),
            ("LEFTPADDING", (0,0), (-1,-1), 0),
            ("RIGHTPADDING", (0,0), (-1,-1), 0),
            ("TOPPADDING", (0,0), (-1,-1), 0),
            ("BOTTOMPADDING", (0,0), (-1,-1), 0),
        ]))
        # return assist_table  
        self._flow.append(assist_table)        
        self._flow.append(Spacer(1, 8))

    def _add_notice_body(self, flow):
        """
        Adds the formatted notice text inside a fixed coordinate frame area.
        Coordinates from provided data:
        x0=18, y0=255, x1=586, y1=652
        """
        body_lines = notice_info  # imported from static_data.py

        # Combine all text paragraphs into one continuous flow
        paragraphs = []
        notice_style = ParagraphStyle(
            name="NoticeText",
            fontName="Courier",
            fontSize=9,
            leading=12,
            alignment=TA_JUSTIFY,
            spaceBefore=0,
            spaceAfter=8,
        )

        for key, value in body_lines.items():
            if value and value[0].strip():
                paragraphs.append(Paragraph(value[0].strip(), notice_style))
            else:
                paragraphs.append(Spacer(1, 6))


        # Create frame coordinates (convert y from top-left to bottom-left)
        x0, y0, x1, y1 = 54, 255, 622.76, 652

        width = x1 - x0
        height = y1 - y0

        # Wrap all paragraphs into a frame box
        notice_frame = Frame(
            x0,
            y0,
            width,
            height,
            leftPadding=0,
            bottomPadding=0,
            rightPadding=0,
            topPadding=0,
            showBoundary=1,  # set to 1 to visualize during testing
        )

        # Keep paragraphs together within frame
        notice_story = KeepInFrame(width, height, paragraphs, mode="shrink")

        # Append the frame to flow
        self._flow.append(notice_story)


    def _add_fundlist_notice(self, flow):
        """
        Creates a single-column table from fundlist_notice data,
        preserving multiline text exactly as defined.
        """

        fund_notice_lines = fundlist_notice

        # Define paragraph style
        fundlist_style = ParagraphStyle(
            name="NoticeText",
            fontName="Courier",
            fontSize=9,
            leading=12,
            alignment=TA_JUSTIFY,
            spaceBefore=0,
            spaceAfter=4,
        )

        table_data = []
        for key, value in fund_notice_lines.items():
            if value and value[0].strip():
                # Preserve line breaks — replace real \n or split strings
                text = value[0].replace("\n", "<br/>")
                table_data.append([Paragraph(text.strip(), fundlist_style)])
            else:
                table_data.append([" "])

        # Create table
        table = Table(table_data, colWidths=[540])

        # Apply table styling
        table.setStyle(TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.8, colors.black),
            ("BOX", (0, 0), (-1, -1), 1, colors.black),
            ("LEFTPADDING", (0, 0), (-1, -1), 4),
            ("RIGHTPADDING", (0, 0), (-1, -1), 4),
            ("TOPPADDING", (0, 0), (-1, -1), 2),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
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
        
        self._add_notice_body(self._flow)
        self._flow.append(PageBreak())

        self._flow.append(self._top_table(header_block, main_info_block))
        self._create_address_string()        
        self._assistance_table()
        self._flow.append(FMOBar(LETTER[0] - 30, 22, "F M O   M A T U R I T Y   N O T I C E"))
        self._flow.append(Spacer(1, 12))
        self._add_fundlist_notice(self._flow)
        build_doc(self._flow, filename)

        
    
    # def	_generate_extras(): pass
    # def	_add_top_right_text(): pass
    # def	_add_bold_title(): pass
    
    # def	_add_signature_and_ending(): pass
    # def	_generate_no_unique_id_nigo_letter(): pass
        

    

