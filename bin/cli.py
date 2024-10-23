import opengui

fields = [
    {
        "name": "egg",
        "default": "good"
    }
]

values = {}

print(opengui.Cli(fields=fields, values=values).ask())
