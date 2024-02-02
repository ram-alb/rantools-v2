XML_START = """<?xml version='1.0' encoding='UTF-8'?>
<bulkCmConfigDataFile
  xmlns:es="EricssonSpecificAttributes.xsd"
  xmlns:un="utranNrm.xsd"
  xmlns:xn="genericNrm.xsd"
  xmlns:gn="geranNrm.xsd"
  xmlns="configData.xsd">
  <fileHeader fileFormatVersion="32.615 V4.5" vendorName="Ericsson"/>
  <configData dnPrefix="Undefined">
    <xn:SubNetwork id="BSC">
"""


BSC_END_XML = """
    </xn:ManagedElement>
  </xn:MeContext>
"""

BSC_COMMON_START_XML = """
  <xn:VsDataContainer id="1">
    <xn:attributes>
      <xn:vsDataType>vsDataBscFunction</xn:vsDataType>
      <xn:vsDataFormatVersion>EricssonSpecificAttributes</xn:vsDataFormatVersion>
      <es:vsDataBscFunction>
        <es:userLabel></es:userLabel>
        <es:bscFunctionId>1</es:bscFunctionId>
      </es:vsDataBscFunction>
    </xn:attributes>

    <xn:VsDataContainer id="1">
      <xn:attributes>
        <xn:vsDataType>vsDataBscM</xn:vsDataType>
        <xn:vsDataFormatVersion>EricssonSpecificAttributes</xn:vsDataFormatVersion>
        <es:vsDataBscM></es:vsDataBscM>
      </xn:attributes>
"""

BSC_COMMON_END_XML = """
    </xn:VsDataContainer>
  </xn:VsDataContainer>
"""

GERAN_CELLS_START_XML = """
  <xn:VsDataContainer id="1">
    <xn:attributes>
      <xn:vsDataType>vsDataGeranCellM</xn:vsDataType>
      <xn:vsDataFormatVersion>EricssonSpecificAttributes</xn:vsDataFormatVersion>
      <es:vsDataGeranCellM>
      <es:geranCellMId>1</es:geranCellMId>
      </es:vsDataGeranCellM>
    </xn:attributes>
"""
GERAN_CELLS_END_XML = '</xn:VsDataContainer>'

UTRA_NETWORK_START_XML = """
  <xn:VsDataContainer id="1">
    <xn:attributes>
      <xn:vsDataType>vsDataUtraNetwork</xn:vsDataType>
      <xn:vsDataFormatVersion>EricssonSpecificAttributes</xn:vsDataFormatVersion>
      <es:vsDataUtraNetwork></es:vsDataUtraNetwork>
    </xn:attributes>
"""
UTRA_NETWORK_END_XML = '</xn:VsDataContainer>'


def make_xml_end(date_time):
    """Make a closing section of a XML file."""
    return f"""
          </xn:SubNetwork>
        </configData>
        <fileFooter dateTime="{date_time}+06:00"/>
      </bulkCmConfigDataFile>
    """


def make_utran_externals_xml(bsc_ext_utran_cells):
    """Make a section of a XML file for adding utran external cells."""
    external_cells = []
    for ext_cell in bsc_ext_utran_cells:
        ext_cell_xml = f"""
          <xn:VsDataContainer id="{ext_cell["externalUtranCellId"]}" modifier="create">
            <xn:attributes>
              <xn:vsDataType>vsDataExternalUtranCell</xn:vsDataType>
              <xn:vsDataFormatVersion>EricssonSpecificAttributes</xn:vsDataFormatVersion>
              <es:vsDataExternalUtranCell>
                <es:utranId>{ext_cell["utranId"]}</es:utranId>
                <es:mrsl>{ext_cell["mrsl"]}</es:mrsl>
                <es:scrCode>{ext_cell["scrCode"]}</es:scrCode>
                <es:externalUtranCellId>{ext_cell["externalUtranCellId"]}</es:externalUtranCellId>
                <es:fddArfcn>{ext_cell["fddArfcn"]}</es:fddArfcn>
              </es:vsDataExternalUtranCell>
            </xn:attributes>
          </xn:VsDataContainer>
        """
        external_cells.append(ext_cell_xml)

    external_cells_xml = ''.join(external_cells)

    return f'{UTRA_NETWORK_START_XML}{external_cells_xml}{UTRA_NETWORK_END_XML}\n'


def make_utran_relations_xml(bsc_utran_relations):
    """Make a section of an XML file for adding G2U relations."""
    gu_relatins_xml = []
    for geran_cell, cell_utran_realtions in bsc_utran_relations.items():
        geran_cell_xml = f"""
          <xn:VsDataContainer id="{geran_cell}">
            <xn:attributes>
              <xn:vsDataType>vsDataGeranCell</xn:vsDataType>
              <xn:vsDataFormatVersion>EricssonSpecificAttributes</xn:vsDataFormatVersion>
              <es:vsDataGeranCell></es:vsDataGeranCell>
            </xn:attributes>
        """

        utran_neighbors = []
        for utran_neighbor in cell_utran_realtions:
            utran_relation_xml = f"""
              <xn:VsDataContainer id="{utran_neighbor}" modifier="create">
                <xn:attributes>
                  <xn:vsDataType>vsDataUtranCellRelation</xn:vsDataType>
                  <xn:vsDataFormatVersion>EricssonSpecificAttributes</xn:vsDataFormatVersion>
                  <es:vsDataUtranCellRelation>
                    <es:utranCellRelationId>{utran_neighbor}</es:utranCellRelationId>
                  </es:vsDataUtranCellRelation>
                </xn:attributes>
              </xn:VsDataContainer>
            """
            utran_neighbors.append(utran_relation_xml)
        utran_neighbors_xml = ''.join(utran_neighbors)
        geran_cell_utran_relations_xml = (
            f'{geran_cell_xml}{utran_neighbors_xml}{GERAN_CELLS_END_XML}\n'
        )
        gu_relatins_xml.append(geran_cell_utran_relations_xml)

    bsc_utran_relations_xml = ''.join(gu_relatins_xml)

    return f'{GERAN_CELLS_START_XML}{bsc_utran_relations_xml}{GERAN_CELLS_END_XML}\n'


def make_g2u_nbr_adding_xml(utran_external_cells, utran_relations, date_time):
    """Make a XML file for adding G2U neighbors using ENM Bulk Configuration."""
    report_path = f'neighbors/reports/G2U_nbr_create_{date_time}.xml'

    with open(report_path, 'w') as xml_file:
        xml_file.write(XML_START)

        for bsc_name, bsc_ext_utran_cells in utran_external_cells.items():
            bsc_start_xml = f"""
              <xn:MeContext id="{bsc_name}">
                <xn:ManagedElement id="{bsc_name}">
            """
            xml_file.write(bsc_start_xml)
            xml_file.write(BSC_COMMON_START_XML)

            utran_external_cells_xml = make_utran_externals_xml(bsc_ext_utran_cells)
            xml_file.write(utran_external_cells_xml)

            utran_relations_xml = make_utran_relations_xml(utran_relations[bsc_name])
            xml_file.write(utran_relations_xml)

            xml_file.write(BSC_COMMON_END_XML)
            xml_file.write(BSC_END_XML)

        xml_file.write(make_xml_end(date_time))

    return report_path
