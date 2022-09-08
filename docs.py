#!/usr/bin/env python

import sphinxter
import opengui

sphinxter.Sphinxter(opengui, titles={
    "field": "opengui.Field",
    "fields": "opengui.Fields"
}, toctree=["self", "fields", "field"]).process()
