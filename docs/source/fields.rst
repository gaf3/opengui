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
