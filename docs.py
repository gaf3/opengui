#!/usr/bin/env python

import sphinxter
import opengui

sphinxter.Sphinxter(opengui, titles={
    "field": "opengui.Field",
    "fields": "opengui.Fields",
    "cli": "opengui.Cli"
}, toctree=["self", "fields", "field", "cli"]).process()
