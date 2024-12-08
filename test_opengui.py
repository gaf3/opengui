import unittest
import unittest.mock

import opengui


class TestMissingName(unittest.TestCase):

    def test___init__(self):

        self.assertEqual(str(opengui.MissingName("whoops")), "whoops")


class TestDuplicateName(unittest.TestCase):

    def test___init__(self):

        self.assertEqual(str(opengui.DuplicateName("whoops")), "whoops")


class TestField(unittest.TestCase):

    maxDiff = None

    def test___init__(self):

        field = opengui.Field("unit")

        self.assertEqual(field.name, "unit")
        self.assertIsNone(field.value)
        self.assertIsNone(field.original)
        self.assertIsNone(field.default)
        self.assertIsNone(field.options)
        self.assertFalse(field.required)
        self.assertFalse(field.multi)
        self.assertFalse(field.trigger)
        self.assertFalse(field.readonly)
        self.assertEqual(field.content, {})
        self.assertEqual(field.errors, [])
        self.assertIsNone(field.fields)

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
            validation="thyself",
            content={"a": 1},
            errors="whoops",
            fields=[{"name": "a"}]
        )

        self.assertEqual(field.name, "unit")
        self.assertEqual(field.value, "test")
        self.assertEqual(field.original, "recipe")
        self.assertEqual(field.default, "factory")
        self.assertEqual(field.options, "family")
        self.assertEqual(field.required, "pants")
        self.assertEqual(field.multi, "functional")
        self.assertEqual(field.trigger, "ed")
        self.assertEqual(field.readonly, "yes")
        self.assertEqual(field.validation, "thyself")
        self.assertEqual(field.content, {"a": 1})
        self.assertEqual(field.errors, "whoops")
        self.assertEqual(field.fields[0].name, "a")

    def test_append(self):

        field = opengui.Field(name="a", value={"b": 1}, original={"b": 2}, fields=[])

        field.append({"name": "b", "label": "B"})

        self.assertEqual(field.fields[0].name, "b")
        self.assertEqual(field.fields[0].value, 1)
        self.assertEqual(field.fields[0].original, 2)
        self.assertEqual(field.fields[0].content, {"label": "B"})

    def test_extend(self):

        field = opengui.Field(name="a", fields=[])

        field.extend([
            {"name": "b"},
            {"name": "c"}
        ])

        self.assertEqual(len(field.fields), 2)
        self.assertEqual(field.fields[0].name, "b")
        self.assertEqual(field.fields[1].name, "c")

    def test_validate(self):

        field = opengui.Field(name="a", required=True)
        self.assertFalse(field.validate())
        self.assertEqual(field.errors, ["missing value"])

        field = opengui.Field(name="a", multi=True, required=True)
        self.assertFalse(field.validate())
        self.assertEqual(field.errors, ["missing value"])

        field = opengui.Field(name="a", multi=True, value=0)
        self.assertFalse(field.validate())
        self.assertEqual(field.errors, ["multi requires list"])

        field = opengui.Field(name="b", default=2)
        self.assertTrue(field.validate())
        self.assertEqual(field.value, 2)

        field = opengui.Field(name="b", readonly=True, original=2)
        self.assertTrue(field.validate())
        self.assertEqual(field.value, 2)

        field = opengui.Field(name="b", readonly=True)
        self.assertTrue(field.validate())

        field = opengui.Field(name="c", options=[1,2])
        field.value = 0
        self.assertFalse(field.validate())
        self.assertEqual(field.errors, ["invalid value '0'"])

        field = opengui.Field(name="c", options=[1,2], multi=True)
        field.value = [0]
        self.assertFalse(field.validate())
        self.assertEqual(field.errors, ["invalid values [0]"])

        field = opengui.Field(name="d", options=[1,2])
        field.value = 1
        self.assertTrue(field.validate())

        field = opengui.Field(name="c", multi=True)
        field.value = [0]
        self.assertTrue(field.validate())

        field = opengui.Field(name="e", fields=[
            {"name": "f", "required": True},
            {"name": "g", "required": True}
        ])
        self.assertFalse(field.validate())
        self.assertEqual(field["f"].errors, ["missing value"])
        self.assertEqual(field["g"].errors, ["missing value"])

        field = opengui.Field(name="h", validation="yep")
        field.value = "yepyep"
        self.assertTrue(field.validate())
        field.value = "nope"
        self.assertFalse(field.validate())
        self.assertEqual(field.errors, ["must match 'yep'"])

        def sure(field, errors):

            if field.value != "sure":
                errors.append("not sure")

            return not errors

        field = opengui.Field(name="i", required=True, validation=sure)
        self.assertFalse(field.validate())
        self.assertEqual(field.errors, ["missing value"])

        field = opengui.Field(name="i", validation=sure)
        field.value = "sure"
        self.assertTrue(field.validate())
        field.value = "nope"
        self.assertFalse(field.validate())
        self.assertEqual(field.errors, ["not sure"])

    def test___getattr__(self):

        field = opengui.Field("a", value="b", original="c")

        self.assertEqual(field.values, "b")
        self.assertEqual(field.originals, "c")

    def test___iter__(self):

        field = opengui.Field(name="a", fields=[
            {"name": "b"},
            {"name": "c"}
        ])

        self.assertEqual([subfield.name for subfield in field], ["b", "c"])

    def test____contains__(self):

        field = opengui.Field(name="a", fields=[
            {"name": "b"},
            {
                "name": "c",
                "fields": [
                    {
                        "name": "d"
                    }
                ]
            }
        ])

        self.assertIn("b", field)
        self.assertIn("d", field["c"])

    def test____getitem__(self):

        field = opengui.Field(name="a", fields=[
            {"name": "b"},
            {
                "name": "c",
                "fields": [
                    {
                        "name": "d"
                    }
                ]
            }
        ])

        self.assertEqual(field[0].name, "b")
        self.assertEqual(field[1][0].name, "d")
        self.assertEqual(field["c"].name, "c")
        self.assertEqual(field["c"]["d"].name, "d")

    def test____len__(self):

        field = opengui.Field(name="a", fields=[
            {"name": "a"},
            {"name": "b"}
        ])

        self.assertEqual(len(field), 2)

    def test_to_dict(self):

        field = opengui.Field("unit")

        self.assertEqual(field.to_dict(), {
            "name": "unit"
        })

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

        self.assertEqual(field.to_dict(), {
            "name": "unit",
            "value": "test",
            "original": "recipe",
            "default": "factory",
            "options": "family",
            "required": "pants",
            "multi": "functional",
            "trigger": "ed",
            "readonly": "yes",
            "validation": "sure",
            "label": "yep",
            "errors": "whoops",
            "fields": [{"name": "a"}]
        })


class TestFields(unittest.TestCase):

    maxDiff = None

    def test___init__(self):

        fields = opengui.Fields()

        self.assertEqual(fields.order, [])
        self.assertEqual(fields.names, {})
        self.assertEqual(fields.values, {})
        self.assertEqual(fields.originals, {})

        fields = opengui.Fields(
            values={
                "a": 1,
                "b": {
                    "c": 2
                }
            },
            originals={
                "a": 3,
                "b": {
                    "c": 4
                }
            },
            fields=[
                {
                    "name": "a"
                },
                {
                    "name": "b",
                    "fields": [
                        {
                            "name": "c"
                        }
                    ]
                }
            ],
            validation="thyself"
        )

        self.assertEqual(fields.values, {
            "a": 1,
            "b": {
                "c": 2
            }
        })
        self.assertEqual(fields.originals, {
            "a": 3,
            "b": {
                "c": 4
            }
        })
        self.assertEqual(fields.order[0].name, "a")
        self.assertEqual(fields.names["a"].value, 1)
        self.assertEqual(fields.names["a"].original, 3)
        self.assertEqual(fields.order[1].name, "b")
        self.assertEqual(fields.names["b"].value, {
            "c": 2
        })
        self.assertEqual(fields.names["b"].original, {
            "c": 4
        })
        self.assertEqual(fields.order[1].fields[0].name, "c")
        self.assertEqual(fields.names["b"].fields.names["c"].value, 2)
        self.assertEqual(fields.names["b"].fields.names["c"].original, 4)
        self.assertEqual(fields.validation, "thyself")

    def test_append(self):

        fields = opengui.Fields(values={"a": 1}, originals={"a": 2})

        fields.append({"name": "a", "label": "A"})

        self.assertEqual(fields.order[0].name, "a")
        self.assertEqual(fields.order[0].content["label"], "A")
        self.assertEqual(fields.order[0].value, 1)
        self.assertEqual(fields.order[0].original, 2)
        self.assertEqual(fields.names["a"].content["label"], "A")

        self.assertRaisesRegex(opengui.MissingName, "Missing name in {}", fields.append)
        self.assertRaisesRegex(opengui.DuplicateName, "Name a exists", fields.append, name="a")

    def test_update(self):

        fields = opengui.Fields(values={"a": 1}, originals={"a": 2})

        fields.update({"name": "a", "label": "A"})

        self.assertEqual(fields.order[0].name, "a")
        self.assertEqual(fields.order[0].content["label"], "A")
        self.assertEqual(fields.order[0].value, 1)
        self.assertEqual(fields.order[0].original, 2)
        self.assertEqual(fields.names["a"].content["label"], "A")

        fields.update({"name": "a", "more": "B"})

        self.assertEqual(len(fields.order), 1)
        self.assertEqual(fields.order[0].name, "a")
        self.assertEqual(fields.order[0].content["label"], "A")
        self.assertEqual(fields.order[0].value, 1)
        self.assertEqual(fields.order[0].original, 2)
        self.assertEqual(fields.names["a"].content["label"], "A")
        self.assertEqual(fields.names["a"].content["more"], "B")

        self.assertRaisesRegex(opengui.MissingName, "Missing name in {}", fields.update)

    def test_extend(self):

        fields = opengui.Fields()

        fields.extend([
            {"name": "a"},
            {"name": "b"}
        ])

        self.assertEqual(len(fields.order), 2)
        self.assertEqual(fields.order[0].name, "a")
        self.assertEqual(fields.order[1].name, "b")

    def test_validate(self):

        fields = opengui.Fields(values={"e": 1}, fields=[
            {"name": "f", "required": True},
            {"name": "g", "required": True}
        ])
        self.assertFalse(fields.validate())
        self.assertFalse(fields.valid)
        self.assertEqual(fields.errors, ["unknown field 'e'"])
        self.assertEqual(fields["f"].errors, ["missing value"])
        self.assertEqual(fields["g"].errors, ["missing value"])

        fields = opengui.Fields(values={"e": 1})
        self.assertFalse(fields.validate())
        self.assertEqual(fields.errors, ["unknown field 'e'"])

        fields = opengui.Fields(fields=[
            {"name": "f", "required": True},
            {"name": "g", "required": True}
        ])
        self.assertFalse(fields.validate())
        self.assertEqual(fields["f"].errors, ["missing value"])
        self.assertEqual(fields["g"].errors, ["missing value"])

        fields = opengui.Fields(values={"f": 1, "g": 2}, fields=[
            {"name": "f", "required": True},
            {"name": "g", "required": True}
        ])
        self.assertTrue(fields.validate())
        self.assertTrue(fields.valid)

        def unequal(fields, errors):

            if fields["h"].value == fields["i"].value:
                errors.append("h and i must be unequal")

            return not errors

        fields = opengui.Fields(values={"h": 1, "i": 1}, fields=[
            {"name": "h"},
            {"name": "i"}
        ], validation=unequal)
        self.assertFalse(fields.validate())
        self.assertFalse(fields.valid)
        self.assertEqual(fields.errors, ["h and i must be unequal"])

    def test___iter__(self):

        fields = opengui.Fields(fields=[
            {"name": "a"},
            {"name": "b"}
        ])

        self.assertEqual([field.name for field in fields], ["a", "b"])

    def test____contains__(self):

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

        self.assertIn("a", fields)
        self.assertIn("c", fields["b"])

    def test____getitem__(self):

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

        self.assertEqual(fields[0].name, "a")
        self.assertEqual(fields[1][0].name, "c")
        self.assertEqual(fields["a"].name, "a")
        self.assertEqual(fields["b"]["c"].name, "c")

    def test____len__(self):

        fields = opengui.Fields(fields=[
            {"name": "a"},
            {"name": "b"}
        ])

        self.assertEqual(len(fields), 2)

    def test_to_list(self):

        fields = opengui.Fields(fields=[
            {"name": "a", "label": "A"},
            {"name": "b"}
        ])

        self.assertEqual(fields.to_list(), [
            {"name": "a", "label": "A"},
            {"name": "b"}
        ])


    def test_to_dict(self):

        fields = opengui.Fields(
            fields=[
                {"name": "a", "label": "A"},
                {"name": "b"}
            ],
            errors=['boo'],
            valid=True,
            ready=False
        )

        self.assertEqual(fields.to_dict(), {
            "fields": [
                {"name": "a", "label": "A"},
                {"name": "b"}
            ],
            "errors": [
                "boo"
            ],
            "valid": True,
            "ready": False
        })

class TestCli(unittest.TestCase):

    maxDiff = None

    def test___init__(self):

        cli = opengui.Cli(values="a", fields="b", engine="c")

        self.assertEqual(cli.values, "a")
        self.assertEqual(cli.fields, "b")
        self.assertEqual(cli.engine, "c")

    @unittest.mock.patch("builtins.input")
    @unittest.mock.patch("readline.set_pre_input_hook")
    def test_input(self, mock_hook, mock_input):

        field = opengui.Field(name="a")

        mock_input.return_value = "b"

        cli = opengui.Cli()

        self.assertEqual(cli.input(field), "b")

        mock_input.assert_has_calls([
            unittest.mock.call("a: "),
        ])

        self.assertEqual(cli.input(field, "c: "), "b")

        mock_input.assert_has_calls([
            unittest.mock.call("c: "),
        ])

    def test_question(self):

        cli = opengui.Cli(
            fields=[
                {"name": "a", "label": "{{ lab }}", "stuff": "{[ {{ people }} ]}"},
                {"name": "b"}
            ],
            values={"lab": "A", "people": "things", "things": [1, 2, 3]}
        )

        self.assertEqual(cli.question().to_dict(), {
            "name": "a",
            "label": "A",
            "stuff": [1, 2, 3]
        })

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
                    "name": "multi-option",
                    "multi": True,
                    "options": "{[ fs ]}",
                    "default": ["fun", "foe"]
                },
                {
                    "name": "multi-text",
                    "multi": True,
                    "default": ["pun", "poe"]
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
            "pun crow",
            "",
            "y",
            "n"
        ]


        self.assertEqual(cli.ask(), {
            "basic": "bitch",
            "single": "yin",
            "multi-option": ["fee", "foe"],
            "multi-text": ["pun", "crow"],
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
            unittest.mock.call('enter multiple indexes, separated by spaces - multi-option: '),
            unittest.mock.call('enter multiple indexes, separated by spaces - multi-option: '),
            unittest.mock.call('enter multiple indexes, separated by spaces - multi-option: '),
            unittest.mock.call('enter multiple values, separated by spaces - multi-text: '),
            unittest.mock.call('enter value y/n - yah: '),
            unittest.mock.call('enter value y/n - sure: '),
            unittest.mock.call('enter value y/n - nah: ')
        ])
