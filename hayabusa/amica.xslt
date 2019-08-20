<xsl:stylesheet version="1.0" 
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
  xmlns:p="http://pds.nasa.gov/pds4/pds/v1" 
  xmlns:disp="http://pds.nasa.gov/pds4/disp/v1" 
  xmlns:img="http://pds.nasa.gov/pds4/img/v1" 
  xmlns:cart="http://pds.nasa.gov/pds4/cart/v1">

  <xsl:template match="/">
    <xsl:processing-instruction name="xml-model">
      <xsl:text>href="http://pds.nasa.gov/pds4/cart/v1/PDS4_CART_1700.sch" scnematypens="http://purl.oclc.org/dsdl/schematron"</xsl:text>
    </xsl:processing-instruction>
    <xsl:processing-instruction name="xml-model">
      <xsl:text>href="http://pds.nasa.gov/pds4/img/v1/PDS4_IMG_1A10_1510.sch" scnematypens="http://purl.oclc.org/dsdl/schematron"</xsl:text>
    </xsl:processing-instruction>
    <xsl:processing-instruction name="xml-model">
      <xsl:text>href="http://pds.nasa.gov/pds4/disp/v1/PDS4_DISP_1700.sch" scnematypens="http://purl.oclc.org/dsdl/schematron"</xsl:text>
    </xsl:processing-instruction>
    <xsl:processing-instruction name="xml-model">
      <xsl:text>href="http://pds.nasa.gov/pds4/pds/v1/PDS4_PDS_1A00.sch" scnematypens="http://purl.oclc.org/dsdl/schematron"</xsl:text>
    </xsl:processing-instruction>

    <xsl:apply-templates select="p:Product_Observational"/>
  </xsl:template>

  <xsl:template match="p:Product_Observational">
    <xsl:copy>
      <xsl:attribute name="xsi:schemaLocation">
        <xsl:text>http://pds.nasa.gov/pds4/pds/v1 http://pds.nasa.gov/pds4/pds/v1/PDS4_PDS_1800.xsd http://pds.nasa.gov/pds4/disp/v1 http://pds.nasa.gov/pds4/disp/v1/PDS4_DISP_1700.xsd http://pds.nasa.gov/pds4/img/v1 http://pds.nasa.gov/pds4/img/v1/PDS4_IMG_1A10_1510.xsd http://pds.nasa.gov/pds4/cart/v1 http://pds.nasa.gov/pds4/cart/v1/PDS4_CART_1700.xsd</xsl:text>
      </xsl:attribute>
      <xsl:copy-of select="p:Identification_Area"/>
      <xsl:apply-templates select="p:Observation_Area"/>
      <xsl:copy-of select="p:File_Area_Observational"/>
    </xsl:copy>
  </xsl:template>

  <xsl:template match="p:Observation_Area">
    <xsl:copy>
      <xsl:choose>
        <xsl:when test="p:TimeCoordinates">
          <xsl:copy-of select="p:Time_Coordinates"/>
        </xsl:when>
        <xsl:otherwise>
          <xsl:call-template name="nilTime"/>
        </xsl:otherwise>
      </xsl:choose>
      <xsl:choose>
        <xsl:when test="p:InvestigationArea">
          <xsl:copy-of select="p:Time_Coordinates"/>
        </xsl:when>
        <xsl:otherwise>
          <xsl:call-template name="defaultInvestigationArea"/>
        </xsl:otherwise>
      </xsl:choose>
      <xsl:choose>
        <xsl:when test="p:Observing_System">
          <xsl:copy-of select="p:Observing_System"/>
        </xsl:when>
        <xsl:otherwise>
          <xsl:call-template name="defaultObservingSystem"/>
        </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="p:Discipline_Area"/>
    </xsl:copy>
  </xsl:template>

  <xsl:template name="nilTime">
    <xsl:element name="Time_Coordinates" namespace="http://pds.nasa.gov/pds4/pds/v1">
      <xsl:element name="start_date_time" namespace="http://pds.nasa.gov/pds4/pds/v1">
        <xsl:attribute name="xsi:nil">true</xsl:attribute>
        <xsl:attribute name="xsi:nilReason">inapplicable</xsl:attribute>
      </xsl:element>
      <xsl:element name="stop_date_time" namespace="http://pds.nasa.gov/pds4/pds/v1">
        <xsl:attribute name="xsi:nil">true</xsl:attribute>
        <xsl:attribute name="xsi:nilReason">inapplicable</xsl:attribute>
      </xsl:element>
    </xsl:element>
  </xsl:template>

  <xsl:template name="defaultObservingSystem">
    <xsl:element name="Observing_System" namespace="http://pds.nasa.gov/pds4/pds/v1">
      <xsl:element name="name" namespace="http://pds.nasa.gov/pds4/pds/v1">
        <xsl:text>HAYABUSA AMICA</xsl:text>
      </xsl:element>
      <xsl:element name="Observing_System_Component" namespace="http://pds.nasa.gov/pds4/pds/v1">
        <xsl:element name="name" namespace="http://pds.nasa.gov/pds4/pds/v1">
          <xsl:text>HAYABUSA</xsl:text>
        </xsl:element>
        <xsl:element name="type" namespace="http://pds.nasa.gov/pds4/pds/v1">
          <xsl:text>Spacecraft</xsl:text>
        </xsl:element>
      </xsl:element>
      <xsl:element name="Observing_System_Component" namespace="http://pds.nasa.gov/pds4/pds/v1">
        <xsl:element name="name" namespace="http://pds.nasa.gov/pds4/pds/v1">
          <xsl:text>AMICA</xsl:text>
        </xsl:element>
        <xsl:element name="type" namespace="http://pds.nasa.gov/pds4/pds/v1">
          <xsl:text>Instrument</xsl:text>
        </xsl:element>
      </xsl:element>
    </xsl:element>
  </xsl:template>

  <xsl:template name="defaultInvestigationArea">
    <xsl:element name="Investigation_Area" namespace="http://pds.nasa.gov/pds4/pds/v1">
      <xsl:element name="name" namespace="http://pds.nasa.gov/pds4/pds/v1">
        <xsl:text>HAYABUSA</xsl:text>
      </xsl:element>
      <xsl:element name="type" namespace="http://pds.nasa.gov/pds4/pds/v1">
        <xsl:text>Mission</xsl:text>
      </xsl:element>
      <xsl:element name="Internal_Reference" namespace="http://pds.nasa.gov/pds4/pds/v1">
        <xsl:element name="lid_reference" namespace="http://pds.nasa.gov/pds4/pds/v1">
          <xsl:text>urn:nasa:pds:TBD</xsl:text>
        </xsl:element>
        <xsl:element name="reference_type" namespace="http://pds.nasa.gov/pds4/pds/v1">
          <xsl:text>data_to_investigation</xsl:text>
        </xsl:element>
      </xsl:element>
    </xsl:element>
  </xsl:template>

  <xsl:template match="p:Discipline_Area">
    <xsl:copy>
      <xsl:copy-of select="disp:Display_Settings"/>
      <xsl:apply-templates select="img:Imaging"/>
      <xsl:apply-templates select="cart:Cartography"/>
    </xsl:copy>
  </xsl:template>

  <xsl:template match="img:Imaging">
    <xsl:copy>
      <xsl:apply-templates select="img:Local_Internal_Reference"/>
      <xsl:element name="img:Command_Parameters">
        <xsl:apply-templates select="img:Command_Parameters"/>
        <xsl:apply-templates select="img:Radiometric_Correction_Parameters"/>
        <xsl:element name="img:Image_Product_Information">
          <xsl:apply-templates select="img:Image_Product_Information/img:Filter"/>
          <xsl:apply-templates select="img:Downsample_Parameters"/>
          <xsl:apply-templates select="img:Subframe_Parameters"/>
        </xsl:element>
      </xsl:element>
    </xsl:copy>
  </xsl:template>

  <xsl:template match="img:Local_Internal_Reference">
    <xsl:element name="Local_Internal_Reference" namespace="http://pds.nasa.gov/pds4/pds/v1">
      <xsl:element name="local_identifier_reference" namespace="http://pds.nasa.gov/pds4/pds/v1">
        <xsl:value-of select="img:local_identifier_reference"/>
      </xsl:element>
      <xsl:element name="local_reference_type" namespace="http://pds.nasa.gov/pds4/pds/v1">
        <xsl:value-of select="img:local_reference_type"/>
      </xsl:element>
    </xsl:element>
  </xsl:template>

  <xsl:template match="img:Command_Parameters">
    <xsl:element name="img:Exposure_Parameters">
      <xsl:copy-of select="img:exposure_duration"/>
    </xsl:element>
  </xsl:template>

  <xsl:template match="img:Radiometric_Correction_Parameters">
    <xsl:element name="img:Data_Correction_Parameters">
      <xsl:element name="img:Data_Correction">
        <xsl:element name="img:active_flag">
          <xsl:text>true</xsl:text>
        </xsl:element>
        <xsl:element name="img:data_correction_type">
          <xsl:text>Radiometric</xsl:text>
        </xsl:element>
        <xsl:element name="img:Radiometric_Correction_Parameters">
          <xsl:element name="img:radiometric_correction_type_name">
            <xsl:text>Radiance-calibrated</xsl:text>
          </xsl:element>
          <xsl:element name="img:radiance_scaling_factor">
            <xsl:attribute name="unit">
              <xsl:text>W/m**3/sr</xsl:text>
            </xsl:attribute>
            <xsl:value-of select="img:radiance_scaling_factor_WO_units"/>
          </xsl:element>
          <xsl:element name="img:radiance_offset">
            <xsl:attribute name="unit">
              <xsl:text>W/m**3/sr</xsl:text>
            </xsl:attribute>
            <xsl:text>0</xsl:text>
          </xsl:element>
        </xsl:element>
      </xsl:element>
    </xsl:element>
  </xsl:template>

  <xsl:template match="img:Filter">
    <xsl:copy>
      <xsl:copy-of select="img:filter_name[position()=1]"/>
      <xsl:copy-of select="img:filter_id[position()=1]"/>
      <xsl:copy-of select="img:filter_number"/>
      <xsl:copy-of select="img:bandwidth"/>
      <xsl:copy-of select="img:center_filter_wavelength"/>
    </xsl:copy>
  </xsl:template>

  <xsl:template match="img:Downsample_Parameters">
    <xsl:element name="img:Downsampling_Parameters">
      <xsl:element name="img:Pixel_Averaging_Dimensions">
        <xsl:element name="img:height_pixels">
          <xsl:attribute name="unit">
            <xsl:text>pixel</xsl:text>
          </xsl:attribute>
          <xsl:value-of select="img:pixel_averaging_height"/>
        </xsl:element>
        <xsl:element name="img:width_pixels">
          <xsl:attribute name="unit">
            <xsl:text>pixel</xsl:text>
          </xsl:attribute>
          <xsl:value-of select="img:pixel_averaging_width"/>
        </xsl:element>
      </xsl:element>
    </xsl:element>
  </xsl:template>

  <xsl:template match="img:Subframe_Parameters">
    <xsl:element name="img:first_line">
      <xsl:value-of select="img:first_line + 1"/>
    </xsl:element>
    <xsl:element name="img:first_sample">
      <xsl:value-of select="img:first_sample + 1"/>
    </xsl:element>
    <xsl:element name="img:lines">
      <xsl:value-of select="img:lines"/>
    </xsl:element>
    <xsl:element name="img:samples">
      <xsl:value-of select="img:samples"/>
    </xsl:element>
  </xsl:template>

  <xsl:template match="cart:Cartography">
    <xsl:copy>
      <xsl:call-template name="cartographyInternalReference"/>
      <xsl:copy-of select="*"/>
    </xsl:copy>
  </xsl:template>

  <xsl:template name="cartographyInternalReference">
    <xsl:element name="Local_Internal_Reference" namespace="http://pds.nasa.gov/pds4/pds/v1">
      <xsl:element name="local_identifier_reference" namespace="http://pds.nasa.gov/pds4/pds/v1">
        <xsl:text>Image_Array_Object</xsl:text>
      </xsl:element>
      <xsl:element name="local_reference_type" namespace="http://pds.nasa.gov/pds4/pds/v1">
        <xsl:text>cartography_parameters_to_image_object</xsl:text>
      </xsl:element>
    </xsl:element>
  </xsl:template>
</xsl:stylesheet>