import logging
import os
import shutil
from copy import deepcopy
from typing import List

import click
from lxml import etree
from onix_splitter.utils import clear_folder


class ONIXSplitter:
    """Splits large ONIX collections into 1-item chunks."""

    XML_EXTENSION = ".xml"

    def __init__(self) -> None:
        """Create a new instance of ONIXSplitter class."""
        self._logger = logging.getLogger(__name__)

    def split(
        self,
        item_identifiers: List[str],
        metadata_folder: str,
        books_folder: str,
        covers_folder: str,
        output_folder: str,
    ) -> None:
        """Extract items with specified identifiers and save them as 1-item ONIX collections
            in the specified output directory.

        :param item_identifiers: List of item identifiers to be extracted
            from the large ONIX collections stored in the metadata folder
        :type item_identifiers: List[str]

        :param metadata_folder: Folder containing XML metadata files describing large ONIX collections
        :type metadata_folder: str

        :param books_folder: Folder containing books
            NOTE: The tool assumes that the folder has flat structure
        :type books_folder: str

        :param covers_folder: Folder containing book covers
            NOTE: The tool assumes that the folder has flat structure
        :type covers_folder: str

        :param output_folder: The folder where the resulting 1-item ONIX collections will be stored
        :type output_folder: str
        """
        self._logger.info(
            f"Started extracting items {item_identifiers}."
            f"Metadata folder: {metadata_folder}."
            f"Books folder: {books_folder}."
            f"Covers folder: {covers_folder}."
            f"Output folder: {output_folder}"
        )

        clear_folder(output_folder)

        item_identifiers = set(item_identifiers)

        for root_folder, folders, files in os.walk(metadata_folder):
            for file in files:
                absolute_file_path = os.path.abspath(
                    os.path.join(metadata_folder, root_folder, file)
                )
                _, extension = os.path.splitext(absolute_file_path)

                if extension == self.XML_EXTENSION:
                    metadata_xml_tree = etree.parse(absolute_file_path)
                    metadata_xml_root = metadata_xml_tree.getroot()
                    product_tags = metadata_xml_root.findall("product")

                    for product_tag in product_tags:
                        identifier_tags = product_tag.findall("productidentifier")

                        for identifier_tag in identifier_tags:
                            identifier_type = identifier_tag.xpath("b221")[0].text

                            if identifier_type == "02" or identifier_type == "15":
                                identifier = identifier_tag.xpath("b244")[0].text

                                if identifier in item_identifiers:
                                    item_output_folder = os.path.abspath(
                                        os.path.join(output_folder, identifier)
                                    )

                                    if not os.path.exists(item_output_folder):
                                        os.mkdir(item_output_folder)

                                    item_xml_root = etree.Element("ONIXmessage")
                                    item_xml_root.append(deepcopy(product_tag))

                                    item_metadata_file = os.path.join(
                                        item_output_folder, f"{identifier}.xml"
                                    )
                                    item_xml_root.getroottree().write(
                                        item_metadata_file
                                    )

                                    item_book_file = os.path.join(
                                        books_folder, f"{identifier}.pdf"
                                    )
                                    new_book_file = os.path.join(
                                        item_output_folder, f"{identifier}.pdf"
                                    )

                                    if os.path.exists(item_book_file):
                                        shutil.copyfile(item_book_file, new_book_file)

                                    item_cover_file = os.path.join(
                                        covers_folder, f"{identifier}.jpg"
                                    )
                                    new_cover_file = os.path.join(
                                        item_output_folder, f"{identifier}.jpg"
                                    )

                                    if os.path.exists(item_cover_file):
                                        shutil.copyfile(item_cover_file, new_cover_file)


@click.command()
@click.option(
    "--identifiers",
    "-i",
    help="Comma-separated list of book identifiers to be extracted from the ONIX collection",
    required=True,
    type=str,
)
@click.option(
    "--metadata-folder",
    "-mf",
    help="Full path to the directory containing metadata",
    required=True,
    type=str,
)
@click.option(
    "--books-folder",
    "-bf",
    help="Full path to the directory containing books",
    required=True,
    type=str,
)
@click.option(
    "--covers-folder",
    "-cf",
    help="Full path to the directory containing covers",
    required=True,
    type=str,
)
@click.option(
    "--output-folder",
    "-of",
    help="Full path to the output directory where the resulting ONIX file will be saved",
    required=True,
    type=str,
)
def split(
    identifiers, metadata_folder, books_folder, covers_folder, output_folder
) -> None:
    """Extract items with specified identifiers and save them as 1-item ONIX collections
    in the specified output directory."""
    identifiers_set = identifiers.split(",")

    splitter = ONIXSplitter()
    splitter.split(
        identifiers_set, metadata_folder, books_folder, covers_folder, output_folder
    )
