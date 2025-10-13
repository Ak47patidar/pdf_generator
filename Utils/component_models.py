import logging
from collections import defaultdict
from enum import Enum
from typing import Optional, List, Dict, Union

from dataclasses import dataclass


from Utils.errors import UnRecognizedType, RequiredDataNotProvided, ProcessingErrors

from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus.paraparser import ParaFrag
from reportlab.platypus.paragraph import Paragraph, FragLine, ParaLines

logger = logging.getLogger(__name__)
INT_MIN = -100


class StringFormattingOperations(Enum):
    BOLD = "BOLD"
    UNDERLINE = "UNDERLINE"
    ITALIC = "ITALIC"
    SUPER = "SUPER"
    NOOP = "NO_OPERATION"
    NOFORMAT = "NO_FORMATTING"


@dataclass
class ParagraphChunk:
    text: str
    operation: StringFormattingOperations
    additional_arguments: Optional[str] = None
    font_size: Optional[int] = 9
    font_name: Optional[str] = "Ant"

    @property
    def formatted_string(self) -> str:
        """
        Apply the operations and return the rendered paragraph
        :return: Return the rendered paragraph
        """
        result = ""
        if self.operation == StringFormattingOperations.NOOP:
            result += f'<font name="{self.font_name}" size="{self.font_size}" >{self.text}</font>'
        elif self.operation == StringFormattingOperations.NOFORMAT:
            return self.text
        elif self.operation == StringFormattingOperations.BOLD:
            result += (
                f'<font name="{self.font_name}-Bold" size="{self.font_size}" >{self.text}</font>'
            )
        elif self.operation == StringFormattingOperations.UNDERLINE:
            result += (
                f'<font name="{self.font_name}" size="{self.font_size}" ><u>{self.text}</u></font>'
            )
        elif self.operation == StringFormattingOperations.SUPER:
            rise = 6
            if self.additional_arguments:
                rise = int(self.additional_arguments)

            result += (
                f'<font name="{self.font_name}" size="{self.font_size}">'
                f"<super rise={rise}>{self.text}</super></font>"
            )
        elif self.operation == StringFormattingOperations.ITALIC:
            result += f'<font name="{self.font_name}i" size="{self.font_size}">{self.text}</font>'
        else:
            raise NotImplementedError(f"Found an unrecognized operation: {self.operation}")

        return result

    @staticmethod
    def get_para_of_fixed_width(
        text: str, style: ParagraphStyle, max_width: float = None, return_simple_lines: bool = False
    ) -> Union[Paragraph, List[Paragraph], List[str], str]:
        """
        Returns a Paragraph Object that is capped at max_width
        :param text: The Paragraph chunk or List of Chunks
        :param style: The style for the paragraph
        :param max_width: Max width of the column (in Inches) for which the paragraph is intended
        to be put in
        :param return_simple_lines: default False. If True returns a list of lines signifying each
        row. can NOT be used with formatted text
        :return: paragraph object that will split dictated by max_width
        """
        if isinstance(text, str):
            if max_width is None:
                raise RequiredDataNotProvided("Need max_width to split para")
            # Although double work it doesn't incur too much of an overhead
            split_lines = Paragraph(text, style=style).breakLines(max_width).lines
            if any([isinstance(obj, FragLine) for obj in split_lines]):
                if return_simple_lines:
                    raise ProcessingErrors(
                        "Unable to return simple lines as input contains formatted text"
                    )
                result: List[ParaFrag] = []
                for frag_line in split_lines:
                    result += frag_line.words
                logger.info(f"RESULT FRAGS: {result}")
                return Paragraph(text="", style=style, frags=result)

            if len(split_lines) < 2:
                if return_simple_lines:
                    return text  # nothing to do if no split
                return Paragraph(text, style=style)
            else:
                logger.debug(f"SPLIT LINES: {split_lines}")
                all_lines = [" ".join(line[1]) for line in split_lines]
                result: List[Union[Paragraph, str]] = []
                for line in all_lines:
                    if return_simple_lines:
                        result.append(line)
                    else:
                        result.append(Paragraph(line, style=style))
                return result
        else:
            raise UnRecognizedType(f"Don't support type: {type(text)}")

    @staticmethod
    def split_para_to_individual_lines(
        para_chunk, style: ParagraphStyle, max_width: float = None
    ) -> List[Paragraph]:
        """
        Returns a List of each split paragraph as a row
        For now ONLY usable for un-formatted strings
        :param para_chunk: The Paragraph chunk or List of Chunks
        :param style: The style for the paragraph
        :param max_width: Max width of the column (in Inches) for which the paragraph is intended to be put in
        :return: List if paragraph objects that don't split inside a row
        """
        if isinstance(para_chunk, ParagraphChunk):
            if max_width is None:
                raise RequiredDataNotProvided("Need max_width to split para")
            # Although double work it doesn't incur too much of an overhead
            split_lines = Paragraph(para_chunk.text, style=style).breakLines(max_width).lines
            if any([isinstance(obj, FragLine) for obj in split_lines]):
                result: List[List[ParaFrag]] = []
                for frag_line in split_lines:
                    if isinstance(frag_line, FragLine):
                        result.append(frag_line.words)
                    elif isinstance(frag_line, ParaLines):
                        if result:
                            result[-1] += frag_line.words
                        else:
                            result.append(frag_line.words)
                logger.info(f"RESULT FRAGS: {result}")
                return [Paragraph(text="", style=style, frags=para_frag) for para_frag in result]

            if len(split_lines) < 2:
                return [Paragraph(para_chunk.text, style=style)]
            else:
                logger.debug(f"SPLIT LINES: {split_lines}")
                all_lines = [" ".join(line[1]) for line in split_lines]
                result: List[Paragraph] = []
                for line in all_lines:
                    result.append(Paragraph(line, style=style))
                return result

        elif isinstance(para_chunk, list):
            result = []
            for para in para_chunk:
                result += ParagraphChunk.split_para_to_individual_lines(
                    para, style=style, max_width=max_width
                )
            return result
        else:
            raise UnRecognizedType(f"Don't support type: {type(para_chunk)}")
