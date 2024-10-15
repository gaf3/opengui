.. created by sphinxter
.. default-domain:: py

opengui.Fields
==============

.. currentmodule:: opengui

.. class:: Fields(values: dict = None, originals: dict = None, fields: 'list[dict]' = None, errors: 'list[str]' = None, valid: bool = None, validation: <built-in function callable> = None, ready: bool = None)

    Class for creating and manipulating fields

    :param values: Field values to use, key by name
    :type values: dict
    :param originals: Field orginal values to use, key by name
    :type originals: dict
    :param fields: Field to use in dict form, not instances
    :type fields: list[dict]
    :param errors: Overall errors
    :type errors: list[str]
    :param valid: Whether valid overall
    :type valid: bool
    :param validation: Function to use to validate across fields
    :type validation: callable
    :param ready: Whether ready overall
    :type ready: bool

    .. attribute:: errors
        :type: list[str]

        Overall errors

    .. attribute:: names
        :type: dict[str, opengui.Field]

        Fields by name

    .. attribute:: order
        :type: list[opengui.Field]

        Fields in order

    .. attribute:: originals
        :type: dict

        Field orginal values to use, key by name

    .. attribute:: ready
        :type: bool

        Whether ready overall

    .. attribute:: valid
        :type: bool

        Whether valid overall

    .. attribute:: validation
        :type: callable

        Function to use to validate across fields

    .. attribute:: values
        :type: dict

        Field values to use, key by name

    .. method:: __contains__(key: str) -> bool

        Check to see if field exists

        :param key: field name
        :type key: str
        :rtype: bool

        **Usage**

        ::

            fields = Fields(fields=[{"name": "foo"}])
            "foo" in fields
            # True
            "bar" in fields
            # False

    .. method:: __getitem__(key: str) -> 'opengui.Field'

        Retrieve a field by name or number

        :param key: field name
        :type key: str
        :rtype: opengui.Field

        **Usage**

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

    .. method:: __iter__()

        Allows iteration over fields

        **Usage**

        ::

            fields = Fields(fields=[{"name": "foo"},{"name": "bar"}])
            for field in fields:
                field.name
            # "foo"
            # "bar"

    .. method:: __len__() -> int

        Returns the number of fields

        :rtype: int

        **Usage**

        ::

            fields = Fields(fields=[{"name": "foo"},{"name": "bar"}])
            len(fields)
            # 2

    .. method:: append(*args, **kwargs)

        Adds a field (as dict) to these Fields

        :param args: single arg dict to use as kwargs
        :param kwargs: kwargs to use in :any:`Field` creation
        :raises DuplicateName: if name is already used
        :raises MissingName: if no name is sent

        **Usage**

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

    .. method:: cli() -> dict

        Returns dict of values from getting input from the cli

        :rtype: dict

        **Usage**

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

    .. method:: extend(fields: 'list[dict]')

        Adds a list of fields

        :param fields: List of field dicts (not instances)
        :type fields: list[dict]

        **Usage**

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

    .. method:: to_dict() -> dict

        Returns dict representation of fields

        :rtype: dict

        **Usage**

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

    .. method:: to_list() -> 'list[dict]'

        Returns list of field dicts

        :rtype: list[dict]

        **Usage**

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

    .. method:: update(*args, **kwargs)

        If exists, updates field, adds field if not

        :param args: single arg dict to use as kwargs
        :param kwargs: kwargs to use in :any:`Field` update
        :raises MissingName: if no name is sent

        **Usage**

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

    .. method:: validate(store=True) -> bool

        Validates the data in all fields, even if validation isn't set. Returns errors.

        * If if a key is values doesn't matcha a field, adds 'unknown field' to errors

        * Calls validate on all fields

        * If validation is set, calls the function with this and errors

        :param store: whether to store the errors (if any) and valid
        :return: Whether everything is valid
        :rtype: bool
