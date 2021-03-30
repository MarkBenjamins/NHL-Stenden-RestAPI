import json
import jsonschema
from lxml.etree import XMLSchema
from lxml import etree
import os

dirname = os.path.dirname(__file__)

def is_valid_xml(xml):
    filenameXML = os.path.join(dirname, "../Schemas/XSD/datasetXSD.xsd")
    xsd = XMLSchema(etree.parse(filenameXML))
    xml_object = etree.fromstring(xml)
    return xsd.validate(xml_object)

def is_valid_json(json_string):
    filenameJSON = os.path.join(dirname, "../Schemas/JSON/datasetJSON.json")
    with open(filenameJSON) as file:
        try:
            schema = json.load(file)
        except json.JSONDecodeError:
            False
    json_object = json.loads(json_string)
    ref_resolver = jsonschema.RefResolver(base_uri='file:' + filenameJSON + '/', referrer=schema)
    try:
        jsonschema.validate(json_object, schema, resolver=ref_resolver)
        True
    except jsonschema.exceptions.ValidationError as errorMessage:
        print(errorMessage.message)
        False