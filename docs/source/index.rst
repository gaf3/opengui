.. created by sphinxter
.. default-domain:: py

opengui
=======

.. toctree::
    :maxdepth: 1
    :glob:
    :hidden:

    self
    fields
    field
    cli

.. module:: opengui

Library for building dynamic forms

**Usage**

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

.. exception:: DuplicateName

    Indicates a name is already in Fields

.. exception:: MissingName

    Indicates a name is not found in Fields
