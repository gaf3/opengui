opengui
=======

Library for building dynamic forms, forms whose options and even fields change based on values in other fields.

This doesn't involve rendering dynamic forms, just making creating and altering the structures thereof.

# Example

```python

# Create a single multi select field

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

# If they select textarea, add it

if "textarea" in (fields["types"].value or []):
    fields.append({
        "name": "people",
        "style": "textarea"
    })
    fields.ready = True

# If they selected option, add a format, then check what format they selected

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

# If they add subfields, add two, and make the second optional

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

# Retrn as a dict

return fields.to_dict(), 200
```

More [here](https://github.com/gaf3/opengui)
