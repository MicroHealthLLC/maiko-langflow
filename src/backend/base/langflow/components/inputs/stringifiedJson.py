from langflow.custom import Component
from langflow.io import (
    MultilineInput,
    TableInput,
    Output,
)
from langflow.schema.table import EditMode
from langflow.schema.message import Message
import json

class StringifiedJsonInput(Component):
    display_name = "Stringified JSON Input"
    description = "Get stringified JSON inputs and output up to 10 fields."
    icon = "type"
    name = "StringifiedJsonInput"

    inputs = [
        MultilineInput(
            name="input_value",
            display_name="JSON",
            info="Stringified JSON body to be passed as input.",
        ),
        TableInput(
            name="output_schema",
            display_name="Output Schema",
            info="Define the structure and data types for the model's output.",
            required=True,
            table_schema=[
                {
                    "name": "name",
                    "display_name": "Name",
                    "type": "str",
                    "description": "Specify the name of the output field.",
                    "default": "field",
                    "edit_mode": EditMode.INLINE,
                },
                {
                    "name": "description",
                    "display_name": "Description",
                    "type": "str",
                    "description": "Describe the purpose of the output field.",
                    "default": "description of field",
                    "edit_mode": EditMode.POPOVER,
                },
                {
                    "name": "type",
                    "display_name": "Type",
                    "type": "str",
                    "edit_mode": EditMode.INLINE,
                    "description": (
                        "Indicate the data type of the output field (e.g., str, int, float, bool, list, dict)."
                    ),
                    "options": ["str", "int", "float", "bool", "list", "dict"],
                    "default": "str",
                },
                {
                    "name": "multiple",
                    "display_name": "Multiple",
                    "type": "boolean",
                    "description": "Set to True if this output field should be a list of the specified type.",
                    "default": "False",
                    "edit_mode": EditMode.INLINE,
                },
            ],
            value=[
                {
                    "name": "field",
                    "description": "description of field",
                    "type": "str",
                    "multiple": "False",
                }
            ],
        ),
    ]

    outputs = [
        Output(display_name="Field1", name="text1", method="field_response1"),
        Output(display_name="Field2", name="text2", method="field_response2"),
        Output(display_name="Field3", name="text3", method="field_response3"),
        Output(display_name="Field4", name="text4", method="field_response4"),
        Output(display_name="Field5", name="text5", method="field_response5"),
        Output(display_name="Field6", name="text6", method="field_response6"),
        Output(display_name="Field7", name="text7", method="field_response7"),
        Output(display_name="Field8", name="text8", method="field_response8"),
        Output(display_name="Field9", name="text9", method="field_response9"),
        Output(display_name="Field10", name="text10", method="field_response10"),
    ]

    def _parse_json_input(self):
        try:
            return json.loads(self.input_value)
        except json.JSONDecodeError:
            return {}
    
    def field_response1(self) -> Message:
        return self._process_field_response(0)
    
    def field_response2(self) -> Message:
        return self._process_field_response(1)

    def field_response3(self) -> Message:
        return self._process_field_response(2)

    def field_response4(self) -> Message:
        return self._process_field_response(3)

    def field_response5(self) -> Message:
        return self._process_field_response(4)

    def field_response6(self) -> Message:
        return self._process_field_response(5)

    def field_response7(self) -> Message:
        return self._process_field_response(6)

    def field_response8(self) -> Message:
        return self._process_field_response(7)

    def field_response9(self) -> Message:
        return self._process_field_response(8)

    def field_response10(self) -> Message:
        return self._process_field_response(9)

    def _process_field_response(self, index: int) -> Message:
        json_data = self._parse_json_input()
        if index >= len(self.output_schema):
            return Message(text="No schema defined for this field")
        
        schema = self.output_schema[index]
        
        field_name = schema.get('name', '')
        field_type = schema.get('type', 'str')
        is_multiple = schema.get('multiple', 'False') == 'true'
        
        value = json_data.get(field_name, '')
        
        if is_multiple and isinstance(value, list):
            value = value[0] if value else ''
        
        # Convert the value to the specified type
        if field_type == 'int':
            value = int(value) if value else 0
        elif field_type == 'float':
            value = float(value) if value else 0.0
        elif field_type == 'bool':
            value = bool(value) if value else False
        elif field_type in ['list', 'dict']:
            value = json.dumps(value) if value else ''
        else:  # default to string
            value = str(value)
        
        return Message(text=str(value))
