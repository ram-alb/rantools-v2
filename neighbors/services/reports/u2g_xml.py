XML_START = """<?xml version='1.0' encoding='UTF-8'?>
    <bulkCmConfigDataFile xmlns:es="EricssonSpecificAttributes.xsd"
        xmlns:un="utranNrm.xsd"
        xmlns:xn="genericNrm.xsd"
        xmlns:gn="geranNrm.xsd"
        xmlns="configData.xsd">
        <fileHeader fileFormatVersion="32.615 V4.5" vendorName="Ericsson"/>
        <configData dnPrefix="Undefined">
            <xn:SubNetwork id="RNC">
"""

XML_SUBNETWORK_END = """
            </xn:SubNetwork>
        </configData>
"""

XML_RNC_END = """
            </xn:VsDataContainer>
        </xn:ManagedElement>
    </xn:MeContext>
"""


def _make_xml_end(date_time):
    return f"""
        <fileFooter dateTime="{date_time}+06:00"/>
    </bulkCmConfigDataFile>
    """


def make_geran_externals_xml(ext_gsm_network_id, rnc_ext_geran_cells):
    """Make a section of a XML file for adding external geran cells."""
    geran_externals = []

    xml_data_container_start = f"""
        <xn:VsDataContainer id="{ext_gsm_network_id}">
            <xn:attributes>
                <xn:vsDataType>vsDataExternalGsmNetwork</xn:vsDataType>
                <xn:vsDataFormatVersion>EricssonSpecificAttributes</xn:vsDataFormatVersion>
                <es:vsDataExternalGsmNetwork></es:vsDataExternalGsmNetwork>
            </xn:attributes>
    """

    xml_data_container_end = '</xn:VsDataContainer>'
    geran_externals.append(xml_data_container_start)

    for ext_geran_cell in rnc_ext_geran_cells:
        xml_ext_geran_cell = f"""
            <xn:VsDataContainer id="{ext_geran_cell.gsm_cell}" modifier="create">
                <xn:attributes>
                    <xn:vsDataType>vsDataExternalGsmCell</xn:vsDataType>
                    <xn:vsDataFormatVersion>EricssonSpecificAttributes</xn:vsDataFormatVersion>
                    <es:vsDataExternalGsmCell>
                        <es:userLabel>{ext_geran_cell.gsm_cell}</es:userLabel>
                        <es:bcc>{ext_geran_cell.bcc}</es:bcc>
                        <es:bandIndicator>{ext_geran_cell.band_indicator}</es:bandIndicator>
                        <es:ExternalGsmCellId>{ext_geran_cell.external_gsm_cell_id}</es:ExternalGsmCellId>
                        <es:maxTxPowerUl>{ext_geran_cell.max_txpower_ul}</es:maxTxPowerUl>
                        <es:cellIdentity>{ext_geran_cell.cell_identity}</es:cellIdentity>
                        <es:qRxLevMin>{ext_geran_cell.qrxlev_min}</es:qRxLevMin>
                        <es:individualOffset>{ext_geran_cell.individual_offset}</es:individualOffset>
                        <es:bcchFrequency>{ext_geran_cell.bcch_frequency}</es:bcchFrequency>
                        <es:lac>{ext_geran_cell.lac}</es:lac>
                        <es:ncc>{ext_geran_cell.ncc}</es:ncc>
                    </es:vsDataExternalGsmCell>
                </xn:attributes>
            </xn:VsDataContainer>
        """
        geran_externals.append(xml_ext_geran_cell)
    geran_externals.append(xml_data_container_end)

    return geran_externals


def make_gsm_relations_xml(rnc_gsm_realtions):
    """Make a section of an XML file for adding U2G relations."""
    u2g_relations = []
    for utran_cell, gsm_relations in rnc_gsm_realtions.items():
        xml_utran_cell = f"""
            <xn:VsDataContainer id="{utran_cell}">
                <xn:attributes>
                    <xn:vsDataType>vsDataUtranCell</xn:vsDataType>
                    <xn:vsDataFormatVersion>EricssonSpecificAttributes</xn:vsDataFormatVersion>
                    <es:vsDataUtranCell></es:vsDataUtranCell>
                </xn:attributes>
        """
        gsm_neighbors = []
        for gsm_relation in gsm_relations:
            rnc_name, ext_gsm_network_id, gsm_cell = gsm_relation
            xml_gsm_relation = f"""
                <xn:VsDataContainer id="{gsm_cell}" modifier="create">
                    <xn:attributes>
                        <xn:vsDataType>vsDataGsmRelation</xn:vsDataType>
                        <xn:vsDataFormatVersion>EricssonSpecificAttributes</xn:vsDataFormatVersion>
                        <es:vsDataGsmRelation>
                            <es:externalGsmCellRef>SubNetwork=RNC,MeContext={rnc_name},ManagedElement=1,vsDataRncFunction=1,vsDataExternalGsmNetwork={ext_gsm_network_id},vsDataExternalGsmCell={gsm_cell}</es:externalGsmCellRef>
                            <es:mobilityRelationType>HO_AND_CELL_RESEL</es:mobilityRelationType>
                            <es:qOffset1sn>50</es:qOffset1sn>
                            <es:selectionPriority>0</es:selectionPriority>
                            <es:GsmRelationId>{gsm_cell}</es:GsmRelationId>
                        </es:vsDataGsmRelation>
                    </xn:attributes>
                </xn:VsDataContainer>
            """
            gsm_neighbors.append(xml_gsm_relation)
        xml_gsm_neighbors = ''.join(gsm_neighbors)
        xml_utran_cell_gsm_relations = f'{xml_utran_cell}{xml_gsm_neighbors}</xn:VsDataContainer>'
        u2g_relations.append(xml_utran_cell_gsm_relations)
    return u2g_relations


def make_u2g_nbr_adding_xml(external_geran_cells, geran_realtions, date_time):
    """Make a XML file for adding U2G neighbors using ENM Bulk Configuration."""
    report_path = f'neighbors/reports/U2G_nbr_adding_{date_time}.xml'

    with open(report_path, 'w') as xml_file:
        xml_file.write(XML_START)
        for rnc_key, ext_gsm_cells in external_geran_cells.items():
            rnc, ext_gsm_network_id = rnc_key.split('-')
            rnc_start = f"""
                <xn:MeContext id="{rnc}">
                <xn:ManagedElement id="1">
                    <xn:VsDataContainer id="1">
                        <xn:attributes>
                            <xn:vsDataType>vsDataRncFunction</xn:vsDataType>
                            <xn:vsDataFormatVersion>EricssonSpecificAttributes</xn:vsDataFormatVersion>
                            <es:vsDataRncFunction></es:vsDataRncFunction>
                        </xn:attributes>
            """
            xml_file.write(rnc_start)

            geran_externals = make_geran_externals_xml(ext_gsm_network_id, ext_gsm_cells)
            xml_file.write('\n'.join(geran_externals))

            gsm_relations = make_gsm_relations_xml(geran_realtions[rnc_key])
            xml_file.write('\n'.join(gsm_relations))

            xml_file.write(XML_RNC_END)
        xml_file.write(XML_SUBNETWORK_END)
        xml_file.write(_make_xml_end(date_time))

    return report_path
