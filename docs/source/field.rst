.. created by sphinxter
.. default-domain:: py

opengui.Field
=============

.. currentmodule:: opengui

.. class:: Field(name, value=None, original=None, default=None, options=None, required=False, multi=False, trigger=False, readonly=False, validation=None, content=None, errors=None, fields=None)

    Class for creating and manipulating a field

    :param name: name of the field
    :param value: value of the field
    :param original: original value (if updating)
    :param default: default value
    :param options: list of options to choose from
    :param required: whether reuired
    :param multi: whether multiple options can be selected
    :param trigger: whether to reload if value changed
    :param readonly: whether read only
    :param validation: validation, see :any:`Field.validation`
    :param content: customer attributes
    :param errors: list of errors
    :param fields: sub fields of :any:`Fields`

    .. attribute:: ATTRIBUTES

        List of actual attributes vs. what goes in content

    .. attribute:: content
        :type: dict

        Custom attributes

    .. attribute:: default

        Default value

    .. attribute:: errors
        :type: list

        List of error for this field

    .. attribute:: fields
        :type: opengui.Fields

        Sub fields of this field

    .. attribute:: multi
        :type: bool

        Whether can select multiple values

    .. attribute:: name
        :type: str

        Name of the field

    .. attribute:: options
        :type: list

        List of options

    .. attribute:: original

        The orginal value (when updating)

    .. attribute:: readonly
        :type: bool

        Whether readonly

    .. attribute:: required
        :type: bool

        Whether required

    .. attribute:: trigger
        :type: bool

        Whether changes should trigger a reload

    .. attribute:: validation
        :type: str or callable

        How to validate

        If str, will use as regex. If regex doesn't match value, will add to errors.

        If callable, will call with value and current list of errors. Add to list of errors if invalid.

    .. attribute:: value

        The value(s)

    .. method:: __contains__(key: str) -> bool

        Check to see if sub field exists

        :param key: field name
        :type key: str
        :rtype: bool

        **Usage**

        ::

            field = Field("one", fields=[{"name": "foo"}])
            "foo" in field
            # True
            "bar" in field
            # False

    .. method:: __getattr__(attr: str)

        Shorthand for `field.values` returning `field.value` and `orginal/s` too. Used so this
        and :any:`Fields` have feature parity

        :param attr: Either 'values' or 'orginals'
        :type attr: str

        **Usage**

        ::

            field.value = "foo"
            field.values
            # "foo"

    .. method:: __getitem__(key: str) -> 'opengui.Field'

        Retrieves a sub field by name

        :param key: field name
        :type key: str
        :rtype: opengui.Field

        **Usage**

        ::

            field = Field("many", fields=[{"name": "foo"},{"name": "bar"}])
            field["foo"].name:
            # "foo"
            # "bar"

    .. method:: __iter__()

        Allows iteration over sub fields

        **Usage**

        ::

            field = Field("many", fields=[{"name": "foo"},{"name": "bar"}])
            for sub in field:
                sub.name
            # "foo"
            # "bar"

    .. method:: __len__() -> int

        Returns the number of sub fields

        :rtype: int

        **Usage**

        ::

            field = Field("many", fields=[{"name": "foo"},{"name": "bar"}])
            len(field)
            # 2

    .. method:: append(*args, **kwargs)

        Appends a field onto this Field's sub fields

        :param args:
        :param kwargs:

        **Usage**

        Check out :any:`Fields.append`

    .. method:: extend(fields)

        Extens a field onto this Field's sub fields

        :param fields:

        **Usage**

        Check out :any:`Fields.extend`

    .. method:: to_dict() -> dict

        Returns dictionary representation of field

        The content dict values will be added to the dict as long as
        they're not part of attributes.

        :rtype: dict

        **Usage**

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

    .. method:: validate(store=True) -> bool

        Validates the data in the field, even if validation isn't set. Returns errors.

        * If value is None and default is not, set value to default

        * If value is None and readonly is True, sets value to original

        * If value is still None and required, adds 'missing value' to errors

        * If multi is set and value is not None but not a list, adds 'multi requires list' to errors

        * If options is set,if value isn't within, adds 'invalid value' or 'invalid values' (listing the invalid ones) to errors

        * If validation is set, applies it. See :any:`Field.validation` for more

        :param store: whether to store the errors (if any) on the Field
        :return: Whether valid or not
        :rtype: bool
