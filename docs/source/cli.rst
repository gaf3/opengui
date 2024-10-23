.. created by sphinxter
.. default-domain:: py

opengui.Cli
===========

.. currentmodule:: opengui

.. class:: Cli(values: dict = None, fields: 'list[dict]' = None, engine: yaes.Engine = None)

    Class for answering fields at a cli

    :param values: Field values to use, key by name
    :type values: dict
    :param fields: Field to use in dict form, not instances
    :type fields: list[dict]
    :param engine: Yaes Engine to use for cli()
    :type engine: Engine

    .. attribute:: engine
        :type: bool

        Yaes Engine to use

    .. attribute:: fields
        :type: list[dict]

        Field to use in dict form, not instances

    .. attribute:: values
        :type: dict

        Field values to use, key by name

    .. method:: ask() -> dict

        Returns dict of values from getting input from the cli

        :rtype: dict

        **Usage**

        Taken from its unittest::

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

    .. method:: input(field, prompt=None, default=None)

        Get inputs

        :param field: field
        :param prompt: prompt
        :param default: default

        **Usage**

        Taken from its unittest::

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

    .. method:: question() -> opengui.Field

        Returns teh next question, transformed by yeas

        :rtype: Field

        **Usage**

        Taken from its unittest::

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
