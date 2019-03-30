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
        self.assertIsNone(field.label)
        self.assertIsNone(field.values)
        self.assertIsNone(field.style)
        self.assertFalse(field.multi)
        self.assertFalse(field.trigger)
        self.assertFalse(field.readonly)
        self.assertFalse(field.header)
        self.assertIsNone(field.fields)

        field = opengui.Field(
            "unit",
            value="test",
            original="recipe",
            label="tribal",
            values="family",
            labels="societal",
            style="flair",
            multi="functional",
            trigger="ed",
            readonly="yes",
            header="hr",
            fields=[{"name": "a"}]
        )

        self.assertEqual(field.name, "unit")
        self.assertEqual(field.value, "test")
        self.assertEqual(field.original, "recipe")
        self.assertEqual(field.label, "tribal")
        self.assertEqual(field.values, "family")
        self.assertEqual(field.labels, "societal")
        self.assertEqual(field.style, "flair")
        self.assertEqual(field.multi, "functional")
        self.assertEqual(field.trigger, "ed")
        self.assertEqual(field.readonly, "yes")
        self.assertEqual(field.header, "hr")
        self.assertEqual(field.fields[0].name, "a")

    def test_append(self):

        field = opengui.Field(name="a", value={"b": 1}, original={"b": 2}, fields=[])

        field.append(name="b", label="B")

        self.assertEqual(field.fields[0].name, "b")
        self.assertEqual(field.fields[0].label, "B")
        self.assertEqual(field.fields[0].value, 1)
        self.assertEqual(field.fields[0].original, 2)


    def test_extend(self):

        field = opengui.Field(name="a", fields=[])

        field.extend([
            {"name": "b"},
            {"name": "c"}
        ])

        self.assertEqual(len(field.fields), 2)
        self.assertEqual(field.fields[0].name, "b")
        self.assertEqual(field.fields[1].name, "c")

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
            label="tribal",
            values="family",
            labels="societal",
            style="flair",
            multi="functional",
            trigger="ed",
            readonly="yes",
            header="hr",
            fields=[{"name": "a"}]
        )

        self.assertEqual(field.to_dict(), {
            "name": "unit",
            "value": "test",
            "original": "recipe",
            "label": "tribal",
            "values": "family",
            "labels": "societal",
            "style": "flair",
            "multi": "functional",
            "trigger": "ed",
            "readonly": "yes",
            "header": "hr",
            "fields": [{"name": "a"}]
        })


class TestForm(unittest.TestCase):

    maxDiff = None

    def test___init__(self):

        form = opengui.Form()

        self.assertEqual(form.fields, [])
        self.assertEqual(form.names, {})
        self.assertEqual(form.values, {})
        self.assertEqual(form.originals, {})

        form = opengui.Form(
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
            ]
        )

        self.assertEqual(form.values, {
            "a": 1,
            "b": {
                "c": 2
            }
        })
        self.assertEqual(form.originals, {
            "a": 3,
            "b": {
                "c": 4
            }
        })
        self.assertEqual(form.fields[0].name, "a")
        self.assertEqual(form.names["a"].value, 1)
        self.assertEqual(form.names["a"].original, 3)
        self.assertEqual(form.fields[1].name, "b")
        self.assertEqual(form.names["b"].value, {
            "c": 2
        })
        self.assertEqual(form.names["b"].original, {
            "c": 4
        })
        self.assertEqual(form.fields[1].fields[0].name, "c")
        self.assertEqual(form.names["b"].fields.names["c"].value, 2)
        self.assertEqual(form.names["b"].fields.names["c"].original, 4)

    def test_append(self):

        form = opengui.Form(values={"a": 1}, originals={"a": 2})

        form.append(name="a", label="A")

        self.assertEqual(form.fields[0].name, "a")
        self.assertEqual(form.fields[0].label, "A")
        self.assertEqual(form.fields[0].value, 1)
        self.assertEqual(form.fields[0].original, 2)
        self.assertEqual(form.names["a"].label, "A")

        self.assertRaisesRegex(opengui.MissingName, "Missing name in {}", form.append)
        self.assertRaisesRegex(opengui.DuplicateName, "Name a exists", form.append, name="a")

    def test_extend(self):

        form = opengui.Form()

        form.extend([
            {"name": "a"},
            {"name": "b"}
        ])

        self.assertEqual(len(form.fields), 2)
        self.assertEqual(form.fields[0].name, "a")
        self.assertEqual(form.fields[1].name, "b")

    def test___iter__(self):

        form = opengui.Form(fields=[
            {"name": "a"},
            {"name": "b"}
        ])

        self.assertEqual([field.name for field in form], ["a", "b"])

    def test____getitem__(self):

        form = opengui.Form(fields=[
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

        self.assertEqual(form[0].name, "a")
        self.assertEqual(form[1][0].name, "c")
        self.assertEqual(form["a"].name, "a")
        self.assertEqual(form["b"]["c"].name, "c")

    def test____len__(self):

        form = opengui.Form(fields=[
            {"name": "a"},
            {"name": "b"}
        ])

        self.assertEqual(len(form), 2)

    def test_to_list(self):

        form = opengui.Form(fields=[
            {"name": "a"},
            {"name": "b"}
        ])

        self.assertEqual(form.to_list(), [
            {"name": "a"},
            {"name": "b"}
        ])
