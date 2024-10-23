opengui
=======

Library for building dynamic forms, forms whose options and even fields change based on values in other fields.

This doesn't involve rendering dynamic forms, just making creating and altering the structures thereof.

# GUI Example

Some Python code in [service.py](api/lig/service.py) that generate some basic field dynamically

```python

# Create a single multi select field

fields = opengui.Fields(
    values=values,
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

Universal [doTRoute.js](http://gaf3.github.io/dotroute/) [form.html](gui/www/form.html) to display a dynamic form:

```html
{{?it.message}}
<div class="uk-alert uk-alert-success">
    {{=it.message}}
</div>
{{?}}
{{?it.errors && it.errors.length}}
<div class="uk-alert uk-alert-danger">
    {{~it.errors :error}}
        {{=error}}<br/>
    {{~}}
</div>
{{?}}
<form class="uk-form uk-form-horizontal">
    {{= DRApp.templates.Fields(it) }}
    <br/>
</form>
```

Universal [doTRoute.js](http://gaf3.github.io/dotroute/) [fields.html](gui/www/fields.html) to display all sorts of combinations, including sub fields:

```html
{{~it.fields :field}}
    {{ var prefix = it.prefix || []; }}
    {{ var full_name = prefix.concat(field.name).join('-').replace(/\./g, '-'); }}
    {{ var value = field.value || field.default || (field.multi ? [] : ''); }}
    {{ var readonly = field.readonly || it.readonly; }}
    {{?field.fields || field.name == "yaml"}}
    <div class="uk-form-row"><hr/></div>
    {{?}}
    <div class="uk-form-row">
        <label class="uk-form-label" for="{{=field.name}}"><strong>{{=field.label || field.name}}</strong></label>
        <div class="uk-form-controls">
    {{?field.style == "textarea"}}
        {{?readonly}}
            {{?field.name == "yaml"}}<pre>{{?}}{{=value}}{{?field.name == "yaml"}}</pre>{{?}}
        {{??}}
            <textarea
                rows='7' cols='42'
                id="{{!full_name}}"
                placeholder="{{!field.label || field.name}}"
                {{?field.trigger}}OnInput="DRApp.current.controller.fields_change();"{{?}}
            >{{=value}}</textarea>
        {{?}}
    {{??field.style == "select" && !readonly}}
            <select id="{{!full_name}}" {{?field.trigger}}OnChange="DRApp.current.controller.fields_change();"{{?}}>
        {{?field.optional}}
                <option value=''></option>
        {{?}}
        {{~field.options :option}}
                <option value='{{!option}}' {{?value == option}}selected{{?}}>
                    {{= field.labels ? field.labels[option] : option}}
                </option>
        {{~}}
            </select>
    {{??field.options}}
        {{?readonly}}
            {{?field.multi}}
                {{~value :option}}
            {{= field.labels ? field.labels[option] : option}}<br/>
                {{~}}
            {{??}}
            {{= field.labels ? field.labels[value] : value}}<br/>
            {{?}}
        {{??}}
            {{~field.options :option}}
            <input
                value="{{!option}}"
            {{?field.multi}}
                type="checkbox" name="{{!full_name}}"
                {{?value.indexOf(option) > -1}}checked{{?}}
            {{??}}
                type="radio" name="{{!full_name}}"
                {{?value == option}}checked{{?}}
            {{?}}
                {{?field.trigger}}OnClick="DRApp.current.controller.fields_change();"{{?}}
            />
            {{= field.labels ? field.labels[option] : option}}<br/>
            {{~}}
        {{?}}
    {{??!field.fields}}
        {{?readonly}}
            {{= field.style == "datetime" ? (new Date(value*1000)).toLocaleString() : value}}
        {{??}}
            <input
                id="{{!full_name}}"
                placeholder="{{!field.label || field.name}}"
                value="{{!value}}"
                {{?field.trigger}}OnInput="DRApp.current.controller.fields_change();"{{?}}
                type="text"
            />
        {{?}}
            <br/>
    {{?}}
    {{?field.errors}}
            <span class='uk-form uk-text-danger'>
        {{~field.errors :error}}
                {{=error}}
        {{~}}
            </span>
    {{?}}
    {{?field.description}}
            <dfn>{{=field.description.replace(/\n/g, "<br/>")}}</dfn><br/>
    {{?}}
    {{?field.link}}
        {{ var links = Array.isArray(field.link) ? field.link : [field.link]; }}
        {{~links: link}}
            <a href="{{!link.url || link}}" target="{{!link.target || '_blank'}}">{{=link.name || link.url || link}}</a><br/>
        {{~}}
    {{?}}
        </div>
    </div>
    {{?field.fields}}
        {{= DRApp.templates.Fields({fields: field.fields, readonly: readonly, prefix: prefix.concat(field.name)}) }}
    {{?}}
{{~}}
```

Which looks like this:

![OpenGUI Exmaple](example.png)

If you're familer with Docker Desktop, Kubernetes, and Tilt `make up` and hit space.

Navigate to `http://localhost:7971/` and give it a whirl.

# Cli Example

Just took this from the from the unittests:

```python
@unittest.mock.patch("builtins.print")
@unittest.mock.patch("builtins.input")
def test_ask(self, mock_input, mock_print):

    cli = opengui.Cli(
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
                "default": "yin"
            },
            {
                "name": "multiple",
                "multi": True,
                "options": "{[ fs ]}",
                "default": ["fun", "foe"]
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
        ],
        values={
            "fs": ["fee", "fie", "foe", "fum"]
        }
    )

    mock_input.side_effect = [
        "",
        "bitch",
        "fish",
        "0",
        "3",
        "1",
        "fish 0 6",
        "",
        "1 3",
        "",
        "y",
        "n"
    ]


    self.assertEqual(cli.ask(), {
        "basic": "bitch",
        "single": "yin",
        "multiple": ["fee", "foe"],
        "yah": True,
        "sure": True,
        "nah": False,
        "fs": ["fee", "fie", "foe", "fum"]
    })

    mock_print.assert_has_calls([
        unittest.mock.call('  be basic'),
        unittest.mock.call("must match '^bitch$'"),
        unittest.mock.call('[1] Yin'),
        unittest.mock.call('[2] Yang'),
        unittest.mock.call('invalid choice: fish'),
        unittest.mock.call('[1] Yin'),
        unittest.mock.call('[2] Yang'),
        unittest.mock.call('invalid choice: 0'),
        unittest.mock.call('[1] Yin'),
        unittest.mock.call('[2] Yang'),
        unittest.mock.call('invalid choice: 3'),
        unittest.mock.call('[1] Yin'),
        unittest.mock.call('[2] Yang'),
        unittest.mock.call('[1] fee'),
        unittest.mock.call('[2] fie'),
        unittest.mock.call('[3] foe'),
        unittest.mock.call('[4] fum'),
        unittest.mock.call("invalid choices: ['fish', '0', '6']"),
        unittest.mock.call('[1] fee'),
        unittest.mock.call('[2] fie'),
        unittest.mock.call('[3] foe'),
        unittest.mock.call('[4] fum'),
        unittest.mock.call("invalid values ['fun']"),
        unittest.mock.call('[1] fee'),
        unittest.mock.call('[2] fie'),
        unittest.mock.call('[3] foe'),
        unittest.mock.call('[4] fum')
    ])

    mock_input.assert_has_calls([
        unittest.mock.call('basic: '),
        unittest.mock.call('enter index - single: '),
        unittest.mock.call('enter index - single: '),
        unittest.mock.call('enter index - single: '),
        unittest.mock.call('enter index - single: '),
        unittest.mock.call('enter multiple indexes, separated by spaces - multiple: '),
        unittest.mock.call('enter multiple indexes, separated by spaces - multiple: '),
        unittest.mock.call('enter multiple indexes, separated by spaces - multiple: '),
        unittest.mock.call('enter value y/n - yah: '),
        unittest.mock.call('enter value y/n - sure: '),
        unittest.mock.call('enter value y/n - nah: ')
    ])
```

And fields use [yaes.Engine](https://yaes.readthedocs.io/en/latest/) for transformaton each time a question is asked:

```python
fields = opengui.Fields(
    fields=[
        {"name": "a", "label": "{{ lab }}", "stuff": "{[ things ]}"},
        {"name": "b"}
    ],
    errors=['boo'],
    valid=True,
    ready=False
)

values = {"lab": "A", "things": [1, 2, 3]}

self.assertEqual(fields.question(values).to_dict(), {
    "name": "a",
    "label": "A",
    "stuff": [1, 2, 3]
})
```

# Documentation

It's lacking at this point, but check out the [tests](test_opengui.py) to see what you can do.
