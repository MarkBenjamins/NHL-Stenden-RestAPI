from lxml.etree import XMLSchema
from lxml import etree
import os
import json
import jsonschema

def is_valid_xml(xml):
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, "../Schemas/XSD/datasetXSD.xsd")
    xsd = XMLSchema(etree.parse(filename))
    xml_object = etree.fromstring(xml)
    return xsd.validate(xml_object)


def is_valid_json(json_string):
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, "../Schemas/JSON/datasetJSON.json")
    with open(filename) as f:
        try:
            schema = json.load(f)
        except json.JSONDecodeError:
            return False
    json_object = json.loads(json_string)
    ref_resolver = jsonschema.RefResolver(base_uri='file:' + filename + '/', referrer=schema)
    try:
        jsonschema.validate(json_object, schema, resolver=ref_resolver)
        return True
    except jsonschema.exceptions.ValidationError as e:
        print(e.message)
        return False
