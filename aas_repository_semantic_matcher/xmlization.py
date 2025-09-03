import xml.etree.ElementTree as ET
from xml.dom import minidom


def create_root():
    # Create the root element
    root = ET.Element("links")
    return root


def add_link(root, link_type, comment):
    # Create a <link> element and set its attributes
    link = ET.SubElement(root, "link")
    link.set("type", link_type)
    link.set("comment", comment)
    return link


def add_element(link, element_id, name, model, tool, element_class):
    # Create an <element> element and set its attributes
    element = ET.SubElement(link, "element")
    element.set("id", element_id)
    element.set("name", name)
    element.set("model", model)
    element.set("tool", tool)
    element_class_element = ET.SubElement(element, "elementClass")
    element_class_element.text = element_class


def write_xml_to_string(root):
    # Convert the ElementTree to a string and format it
    xml_str = ET.tostring(root, encoding='utf-8', method='xml')
    pretty_xml_str = minidom.parseString(xml_str).toprettyxml(indent="    ")
    return pretty_xml_str
