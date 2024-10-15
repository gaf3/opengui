"""
description: Library for building dynamic forms
usage: |
    Create a single multi select field::

        fields = opengui.Fields(
            values=values, # Values of the fields in key:value dict.
            fields=[
                {
                    "name": "types",
                    "options": [
                        "textarea",
                        "options",
                        "fields"
                    ],
                    "multi": True,
                    "trigger": True
                }
            ]
        )

    If they select textarea, add it::

        if "textarea" in (fields["types"].value or []):
            fields.append({
                "name": "people",
                "style": "textarea"
            })
            fields.ready = True

    If they selected option, add a format, then check what format they selected::

        if "options" in (fields["types"].value or []):
            fields.append({
                "name": "style",
                "options": [
                    "radios",
                    "select"
                ],
                "default": "radios",
                "trigger": True
            })
            fields.append({
                "name": "stuff",
                "options": [
                    "fee",
                    "fie",
                    "foe",
                    "fum"
                ],
                "style": fields["style"].value
            })
            fields.ready = True

    If they add subfields, add two, and make the second optional::

        if "fields" in (fields["types"].value or []):
            fields.append({
                "name": "things",
                "fields": [
                    {
                        "name": "yin",
                    },
                    {
                        "name": "yang",
                        "optional": True
                    }
                ]
            })
            fields.ready = True

    Serve as dict::

        fields.to_dict()
        # {
        #     "fields": [
        #         {
        #             "name": "types",
        #             "options": [
        #                 "textarea",
        #                 "options",
        #                 "fields"
        #             ],
        #             "multi": True,
        #             "trigger": True
        #         }
        #     ],
        #     "ready": False
        # }
"""

# pylint: disable=too-many-instance-attributes,too-many-arguments,too-many-branches,inconsistent-return-statements,too-many-nested-blocks

import re

class MissingName(Exception):
    """
    Indicates a name is not found in Fields
    """

class DuplicateName(Exception):
    """
    Indicates a name is already in Fields
    """


class Field:
    """
    description: Class for creating and manipulating a field
    document: field
    """

    name = None         # Name of the field
    "type: str"
    value = None        # The value(s)
    original = None     # The orginal value (when updating)
    default = None      # Default value
    options = None      # List of options
    "type: list"
    required = None     # Whether required
    "type: bool"
    multi = None        # Whether can select multiple values
    "type: bool"
    trigger = None      # Whether changes should trigger a reload
    "type: bool"
    readonly = None     # Whether readonly
    "type: bool"
    validation = None   # How to validate
    """
    type:
    - str
    - callable
    description: |
        If str, will use as regex. If regex doesn't match value, will add to errors.

        If callable, will call with value and current list of errors. Add to list of errors if invalid.
    """
    content = None      # Custom attributes
    "type: dict"
    errors = None       # List of error for this field
    "type: list"
    fields = None       # Sub fields of this field
    "type: opengui.Fields"

    ATTRIBUTES = [
        "name",
        "value",
        "original",
        "default",
        "options",
        "required",
        "multi",
        "trigger",
        "readonly",
        "validation",
        "content",
        "errors",
        "fields"
    ] # List of actual attributes vs. what goes in content

    def __init__(self,
        name,               # name of the field
        value=None,         # value of the field
        original=None,      # original value (if updating)
        default=None,       # default value
        options=None,       # list of options to choose from
        required=False,     # whether reuired
        multi=False,        # whether multiple options can be selected
        trigger=False,      # whether to reload if value changed
        readonly=False,     # whether read only
        validation=None,    # validation, see :any:`Field.validation`
        content=None,       # customer attributes
        errors=None,        # list of errors
        fields=None         # sub fields of :any:`Fields`
    ):

        self.name = name
        self.value = value
        self.original = original
        self.default = default
        self.options = options
        self.required = required
        self.multi = multi
        self.trigger = trigger
        self.readonly = readonly
        self.validation = validation

        if content is None:
            content = {}

        self.content = content

        if errors is None:
            errors = []

        self.errors = errors

        if fields is not None:
            self.fields = Fields(values=self.value, originals=self.original, fields=fields)
        else:
            self.fields = None

    def append(self, *args, **kwargs):
        """
        description: Appends a field onto this Field's sub fields
        usage: Check out :any:`Fields.append`
        """

        self.fields.append(*args, **kwargs)

    def extend(self, fields):
        """
        description: Extens a field onto this Field's sub fields
        usage: Check out :any:`Fields.extend`
        """

        self.fields.extend(fields)

    def validate(self,
        store=True  # whether to store the errors (if any) on the Field
    )->bool:
        """
        description: |
            Validates the data in the field, even if validation isn't set. Returns errors.

            * If value is None and default is not, set value to default

            * If value is None and readonly is True, sets value to original

            * If value is still None and required, adds 'missing value' to errors

            * If multi is set and value is not None but not a list, adds 'multi requires list' to errors

            * If options is set,if value isn't within, adds 'invalid value' or 'invalid values' (listing the invalid ones) to errors

            * If validation is set, applies it. See :any:`Field.validation` for more
        return: Whether valid or not
        """

        if self.fields:
            return self.fields.validate(store)

        errors = []

        if self.value is None and self.default is not None:
            self.value = self.default
        if self.value is None and self.readonly:
            self.value = self.original
        elif self.value is None and self.required:
            errors.append("missing value")
        elif self.value is not None and self.multi and not isinstance(self.value,list):
            errors.append("multi requires list")
        elif self.value is not None and self.multi:
            invalid = []
            for value in self.values:
                if value not in self.options:
                    invalid.append(value)
            if invalid:
                errors.append(f"invalid values {invalid}")
        elif self.value is not None and self.options and self.value not in self.options:
            errors.append(f"invalid value '{self.value}'")

        if self.validation:
            if self.value is not None:
                if isinstance(self.validation, str):
                    if not re.match(self.validation, self.value):
                        errors.append(f"must match '{self.validation}'")
                else:
                    self.validation(self, errors)

        if store:
            self.errors = errors

        return not errors

    def __getattr__(self,
        attr:str    # Either 'values' or 'orginals'
    ):
        """
        description: |
            Shorthand for `field.values` returning `field.value` and `orginal/s` too. Used so this
            and :any:`Fields` have feature parity
        usage: |
            ::

                field.value = "foo"
                field.values
                # "foo"
        """
        if attr == "values":
            return self.value

        if attr == "originals":
            return self.original

    def __iter__(self):
        """
        description: Allows iteration over sub fields
        usage: |
            ::

                field = Field("many", fields=[{"name": "foo"},{"name": "bar"}])
                for sub in field:
                    sub.name
                # "foo"
                # "bar"
        """
        return iter(self.fields)

    def __contains__(self,
        key:str # field name
    )->bool:
        """
        description: Check to see if sub field exists
        usage: |
            ::

                field = Field("one", fields=[{"name": "foo"}])
                "foo" in field
                # True
                "bar" in field
                # False
        """
        return self.fields and key in self.fields

    def __getitem__(self,
        key:str # field name
    )->'opengui.Field':
        """
        description: Retrieves a sub field by name
        usage: |
            ::

                field = Field("many", fields=[{"name": "foo"},{"name": "bar"}])
                field["foo"].name:
                # "foo"
                # "bar"
        """
        return self.fields[key]

    def __len__(self)->int:
        """
        description: Returns the number of sub fields
        usage: |
            ::

                field = Field("many", fields=[{"name": "foo"},{"name": "bar"}])
                len(field)
                # 2
        """
        return len(self.fields)

    def to_dict(self)->dict:
        """
        description: |
            Returns dictionary representation of field

            The content dict values will be added to the dict as long as
            they're not part of attributes.
        usage: |
            ::

                field = opengui.Field(
                    "unit",
                    value="test",
                    original="recipe",
                    default="factory",
                    options="family",
                    required="pants",
                    multi="functional",
                    trigger="ed",
                    readonly="yes",
                    validation="sure",
                    content={"name": "nope", "label": "yep"},
                    errors="whoops",
                    fields=[{"name": "a"}]
                )

                # field.to_dict()
                # {
                #     "name": "unit",
                #     "value": "test",
                #     "original": "recipe",
                #     "default": "factory",
                #     "options": "family",
                #     "required": "pants",
                #     "multi": "functional",
                #     "trigger": "ed",
                #     "readonly": "yes",
                #     "validation": "sure",
                #     "label": "yep",
                #     "errors": "whoops",
                #     "fields": [{"name": "a"}]
                # }
        """

        out = {
            "name": self.name
        }

        if self.value is not None:
            out["value"] = self.value

        if self.original is not None:
            out["original"] = self.original

        if self.default is not None:
            out["default"] = self.default

        if self.options is not None:
            out["options"] = self.options

        if self.required:
            out["required"] = self.required

        if self.multi:
            out["multi"] = self.multi

        if self.trigger:
            out["trigger"] = self.trigger

        if self.readonly:
            out["readonly"] = self.readonly

        if isinstance(self.validation, str):
            out["validation"] = self.validation

        if self.content:
            out.update({key: value for key, value in self.content.items() if key not in self.ATTRIBUTES})

        if self.errors:
            out["errors"] = self.errors

        if self.fields:
            out["fields"] = self.fields.to_list()

        return out


class Fields:
    """
    description: Class for creating and manipulating fields
    document: fields
    """

    order = None        # Fields in order
    "type: list[opengui.Field]"
    names = None        # Fields by name
    "type: dict[str, opengui.Field]"
    values = None       # Field values to use, key by name
    "type: dict"
    originals = None    # Field orginal values to use, key by name
    "type: dict"
    errors = None       # Overall errors
    "type: list[str]"
    valid = None        # Whether valid overall
    "type: bool"
    validation = None   # Function to use to validate across fields
    "type: callable"
    ready = None        # Whether ready overall
    "type: bool"

    def __init__(self,
        values:dict=None,           # Field values to use, key by name
        originals:dict=None,        # Field orginal values to use, key by name
        fields:'list[dict]'=None,     # Field to use in dict form, not instances
        errors:'list[str]'=None,      # Overall errors
        valid:bool=None,            # Whether valid overall
        validation:callable=None,   # Function to use to validate across fields
        ready:bool=None             # Whether ready overall
    ):

        if values is None:
            values = {}

        if originals is None:
            originals = {}

        if errors is None:

            errors = []

        self.order = []
        self.names = {}
        self.values = values
        self.originals = originals
        self.errors = errors
        self.valid = valid
        self.validation = validation
        self.ready = ready

        if fields is None:
            fields = []

        self.extend(fields)

    def append(self,
        *args,      # single arg dict to use as kwargs
        **kwargs    # kwargs to use in :any:`Field` creation
    ):
        """
        description: Adds a field (as dict) to these Fields
        usage: |
            ::

                fields = opengui.Fields(values={"a": 1}, originals={"a": 2})

                fields.append({"name": "a", "label": "A"})

                fields.order[0].name
                # a
                fields.order[0].content["label"]
                # "A"
                fields.order[0].value
                # 1
                fields.order[0].original
                # 2
        raises:
            MissingName: if no name is sent
            DuplicateName: if name is already used
        """

        if len(args) == 1:
            kwargs = args[0]

        if "name" not in kwargs:
            raise MissingName(f"Missing name in {kwargs}")

        if kwargs["name"] in self.names:
            raise DuplicateName(f"Name {kwargs['name']} exists")

        if "value" not in kwargs and kwargs["name"] in self.values:
            kwargs["value"] = self.values[kwargs["name"]]

        if "original" not in kwargs and kwargs["name"] in self.originals:
            kwargs["original"] = self.originals[kwargs["name"]]

        attributes = {}

        attributes["content"] = kwargs.get("content", {})

        for key,value in kwargs.items():
            if key in Field.ATTRIBUTES:
                attributes[key] = value
            else:
                attributes["content"][key] = value

        field = Field(**attributes)

        self.order.append(field)
        self.names[field.name] = field

    def update(self,
        *args,      # single arg dict to use as kwargs
        **kwargs    # kwargs to use in :any:`Field` update
    ):
        """
        description: If exists, updates field, adds field if not
        usage: |
            ::

                fields = opengui.Fields(values={"a": 1}, originals={"a": 2})

                fields.update({"name": "a", "label": "A"})

                fields.order[0].name
                # a
                fields.order[0].content["label"]
                # "A"
                fields.order[0].value
                # 1
                fields.order[0].original
                # 2

                fields.update({"name": "a", "more": "B"})

                fields.order[0].content["more"]
                # "B"
        raises:
            MissingName: if no name is sent
        """

        if len(args) == 1:
            kwargs = args[0]

        if "name" not in kwargs:
            raise MissingName(f"Missing name in {kwargs}")

        if kwargs["name"] not in self.names:
            self.append(**kwargs)
            return

        field = self.names[kwargs["name"]]

        for key, value in kwargs.items():
            if key in Field.ATTRIBUTES:
                setattr(field, key, value)
            else:
                field.content[key] = value

    def extend(self,
        fields:'list[dict]'   # List of field dicts (not instances)
    ):
        """
        description: Adds a list of fields
        usage: |
            ::

                fields = opengui.Fields()

                fields.extend([
                    {"name": "a"},
                    {"name": "b"}
                ])

                len(fields.order)
                # 2
                fields.order[0].name
                # "a"
                fields.order[1].name
                # "b"
        """

        for field in fields:
            self.append(**field)

    def validate(self,
        store=True  # whether to store the errors (if any) and valid
    )->bool:
        """
        description: |
            Validates the data in all fields, even if validation isn't set. Returns errors.

            * If if a key is values doesn't matcha a field, adds 'unknown field' to errors

            * Calls validate on all fields

            * If validation is set, calls the function with this and errors
        return: Whether everything is valid
        """
        valid = True
        errors = []

        for name in self.values:
            if name not in self.names:
                errors.append(f"unknown field '{name}'")

        valid = not errors

        for field in self.order:
            valid = field.validate(store) and valid

        if self.validation is not None:
            valid = self.validation(self, errors) and valid

        if store:
            self.valid = valid
            self.errors = errors

        return valid

    def __iter__(self):
        """
        description: Allows iteration over fields
        usage: |
            ::

                fields = Fields(fields=[{"name": "foo"},{"name": "bar"}])
                for field in fields:
                    field.name
                # "foo"
                # "bar"
        """
        return iter(self.order)

    def __contains__(self,
        key:str # field name
    )->bool:
        """
        description: Check to see if field exists
        usage: |
            ::

                fields = Fields(fields=[{"name": "foo"}])
                "foo" in fields
                # True
                "bar" in fields
                # False
        """

        return key in self.names

    def __getitem__(self,
        key:str # field name
    )->'opengui.Field':
        """
        description: Retrieve a field by name or number
        usage: |
            ::

                fields = opengui.Fields(fields=[
                    {"name": "a"},
                    {
                        "name": "b",
                        "fields": [
                            {
                                "name": "c"
                            }
                        ]
                    }
                ])

                fields[0].name
                # "a"
                fields[1][0].name
                # "c"
                fields["a"].name
                # "a"
                fields["b"]["c"].name
                # "c"
        """

        if isinstance(key, int):
            return self.order[key]

        if isinstance(key, str):
            return self.names[key]

    def __len__(self)->int:
        """
        description: Returns the number of fields
        usage: |
            ::

                fields = Fields(fields=[{"name": "foo"},{"name": "bar"}])
                len(fields)
                # 2
        """
        return len(self.order)

    def to_list(self)->'list[dict]':
        """
        description: Returns list of field dicts
        usage: |
            ::

                fields = opengui.Fields(fields=[
                    {"name": "a", "label": "A"},
                    {"name": "b"}
                ])

                fields.to_list()
                # [
                #     {"name": "a", "label": "A"},
                #     {"name": "b"}
                # ]
        """
        out = []

        for field in self.order:
            out.append(field.to_dict())

        return out

    def to_dict(self)->dict:
        """
        description: Returns dict representation of fields
        usage: |
            ::

                fields = opengui.Fields(
                    fields=[
                        {"name": "a", "label": "A"},
                        {"name": "b"}
                    ],
                    errors=['boo'],
                    valid=True,
                    ready=False
                ))

                fields.to_dict()
                # {
                #     "fields": [
                #         {"name": "a", "label": "A"},
                #         {"name": "b"}
                #     ],
                #     "errors": [
                #         "boo"
                #     ],
                #     "valid": True,
                #     "ready": False
                # }
        """

        out = {
            "fields": self.to_list()
        }

        if self.errors is not None:
            out["errors"] = self.errors

        if self.valid is not None:
            out["valid"] = self.valid

        if self.ready is not None:
            out["ready"] = self.ready

        return out

    def cli(self)->dict:
        """
        description: Returns dict of values from getting input from the cli
        usage: |
            Taken from its unittest::

                @unittest.mock.patch("builtins.print")
                @unittest.mock.patch("builtins.input")
                def test_cli(self, mock_input, mock_print):

                    fields = opengui.Fields(
                        fields=[
                            {
                                "name": "basic",
                                "description": "be basic",
                                "default": "badass",
                                "validation": "^bitch$"
                            },
                            {
                                "name": "single",
                                "options": ["yin", "yang"],
                                "labels": {
                                    "yin": "Yin",
                                    "yang": "Yang"
                                },
                                "default": "yon"
                            },
                            {
                                "name": "multiple",
                                "multi": True,
                                "options": ["fee", "fie", "foe", "fum"],
                                "default": ["fun"]
                            },
                            {
                                "name": "yah",
                                "bool": True,
                                "default": True
                            },
                            {
                                "name": "sure",
                                "bool": True
                            },
                            {
                                "name": "nah",
                                "bool": True
                            }
                        ]
                    )

                    mock_input.side_effect = [
                        "",
                        "bitch",
                        "fish",
                        "0",
                        "3",
                        "",
                        "1",
                        "fish 0 6",
                        "",
                        "1 3",
                        "",
                        "y",
                        "n"
                    ]

                    self.assertEqual(fields.cli(), {
                        "basic": "bitch",
                        "single": "yin",
                        "multiple": ["fee", "foe"],
                        "yah": True,
                        "sure": True,
                        "nah": False
                    })

                    mock_print.assert_has_calls([
                        unittest.mock.call("basic:"),
                        unittest.mock.call("  be basic"),
                        unittest.mock.call("  default: badass"),
                        unittest.mock.call("enter value: "),
                        unittest.mock.call("must match '^bitch$'"),
                        unittest.mock.call("enter value: "),
                        unittest.mock.call("single:"),
                        unittest.mock.call("  default: yon"),
                        unittest.mock.call("[1] Yin"),
                        unittest.mock.call("[2] Yang"),
                        unittest.mock.call("enter value: "),
                        unittest.mock.call("invalid choice: fish"),
                        unittest.mock.call("[1] Yin"),
                        unittest.mock.call("[2] Yang"),
                        unittest.mock.call("enter value: "),
                        unittest.mock.call("invalid choice: 0"),
                        unittest.mock.call("[1] Yin"),
                        unittest.mock.call("[2] Yang"),
                        unittest.mock.call("enter value: "),
                        unittest.mock.call("invalid choice: 3"),
                        unittest.mock.call("[1] Yin"),
                        unittest.mock.call("[2] Yang"),
                        unittest.mock.call("enter value: "),
                        unittest.mock.call("invalid value 'yon'"),
                        unittest.mock.call("[1] Yin"),
                        unittest.mock.call("[2] Yang"),
                        unittest.mock.call("enter value: "),
                        unittest.mock.call("multiple:"),
                        unittest.mock.call("  default: ['fun']"),
                        unittest.mock.call("[1] fee"),
                        unittest.mock.call("[2] fie"),
                        unittest.mock.call("[3] foe"),
                        unittest.mock.call("[4] fum"),
                        unittest.mock.call("enter multiple values, separated by spaces: "),
                        unittest.mock.call("invalid choices: ['fish', '0', '6']"),
                        unittest.mock.call("[1] fee"),
                        unittest.mock.call("[2] fie"),
                        unittest.mock.call("[3] foe"),
                        unittest.mock.call("[4] fum"),
                        unittest.mock.call("enter multiple values, separated by spaces: "),
                        unittest.mock.call("invalid values ['fun']"),
                        unittest.mock.call("[1] fee"),
                        unittest.mock.call("[2] fie"),
                        unittest.mock.call("[3] foe"),
                        unittest.mock.call("[4] fum"),
                        unittest.mock.call("enter multiple values, separated by spaces: "),
                    ])

        """

        values = {}

        for field in self:

            print(f"{field.name}:")

            if "description" in field.content:
                print(f"  {field.content['description']}")

            if field.default is not None:
                print(f"  default: {field.default}")

            while True:

                if field.options:

                    labels = field.content.get("labels")

                    for index, option in enumerate(field.options):

                        print(f"[{index+1}] {labels[option] if labels else option}")

                    if field.multi:
                        print("enter multiple values, separated by spaces: ")

                        value = input()

                        if value:

                            indexes = value.split()

                            invalid = []
                            for index in indexes:
                                if not index.isdigit() or int(index) < 1 or int(index) > len(field.options):
                                    invalid.append(index)

                            if invalid:
                                print(f"invalid choices: {invalid}")
                                continue

                            field.value = [field.options[int(index)-1] for index in indexes]

                        else:

                            field.value = field.default

                    else:
                        print("enter value: ")

                        index = input()

                        if index:

                            if index.isdigit() and int(index) > 0 and int(index) <= len(field.options):
                                field.value = field.options[int(index)-1]
                            else:
                                print(f"invalid choice: {index}")
                                continue

                        else:

                            field.value = field.default

                elif field.content.get("bool"):

                    print("enter value y/n: ")
                    value = input()
                    field.value = value.lower() == 'y' if value else field.default

                else:

                    print("enter value: ")
                    field.value = input() or field.default

                if field.validate():
                    values[field.name] = field.value
                    break

                for error in field.errors:
                    print(error)

        return values
