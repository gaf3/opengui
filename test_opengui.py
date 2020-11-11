import unittest

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
        self.assertFalse(field.optional)
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
            optional="pants",
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
        self.assertEqual(field.optional, "pants")
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

        field = opengui.Field(name="a")
        self.assertFalse(field.validate())
        self.assertEqual(field.errors, ["missing value"])

        field = opengui.Field(name="a", multi=True)
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

        field = opengui.Field(name="c", options=[1,2], optional=True)
        self.assertTrue(field.validate())

        field = opengui.Field(name="d", options=[1,2])
        field.value = 1
        self.assertTrue(field.validate())

        field = opengui.Field(name="e", fields=[
            {"name": "f"},
            {"name": "g"}
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

        def sure(field):

            if field.value != "sure":
                field.errors.append("not sure")

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
            optional="pants",
            multi="functional",
            trigger="ed",
            readonly="yes",
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
            "optional": "pants",
            "multi": "functional",
            "trigger": "ed",
            "readonly": "yes",
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
            {"name": "f"},
            {"name": "g"}
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
            {"name": "f"},
            {"name": "g"}
        ])
        self.assertFalse(fields.validate())
        self.assertEqual(fields["f"].errors, ["missing value"])
        self.assertEqual(fields["g"].errors, ["missing value"])

        fields = opengui.Fields(values={"f": 1, "g": 2}, fields=[
            {"name": "f"},
            {"name": "g"}
        ])
        self.assertTrue(fields.validate())
        self.assertTrue(fields.valid)

        def unequal(fields):

            if fields["h"].value == fields["i"].value:
                fields.valid = False
                fields.errors.append("h and i must be unequal")

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
