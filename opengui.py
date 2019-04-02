
class MissingName(Exception):
    pass

class DuplicateName(Exception):
    pass


class Field:

    def __init__(
        self,
        name,
        value=None,
        original=None,
        default=None,
        label=None,
        options=None,
        labels=None,
        style=None,
        optional=False,
        multi=False,
        trigger=False,
        readonly=False,
        header=False,
        errors=None,
        fields=None
    ):

        self.name = name
        self.value = value
        self.original = original
        self.default = default
        self.label = label
        self.options = options
        self.labels = labels
        self.multi = multi
        self.style = style
        self.optional = optional
        self.trigger = trigger
        self.readonly = readonly
        self.header = header

        if errors is None:
            errors = []

        self.errors = errors

        if fields is not None:
            self.fields = Fields(values=self.value, originals=self.original, fields=fields)
        else:
            self.fields = None

    def append(self, *args, **kwargs):
        self.fields.append(*args, **kwargs)

    def extend(self, fields):
        self.fields.extend(fields)

    def validate(self):

        if self.fields:
            return self.fields.validate()

        if self.value is None and not self.optional:
            self.errors.append("missing value")
        elif self.value is not None and self.options and self.value not in self.options:
            self.errors.append("invalid value '%s'" % self.value)

        return not self.errors

    def __getattr__(self, attr):
        if attr == "values":
            return self.value
        elif attr == "originals":
            return self.original

    def __iter__(self):
        return iter(self.fields)

    def __getitem__(self, key):
        return self.fields[key]

    def __len__(self):
        return len(self.fields)

    def to_dict(self):

        out = {
            "name": self.name
        }

        if self.label is not None:
            out["label"] = self.label

        if self.value is not None:
            out["value"] = self.value

        if self.original is not None:
            out["original"] = self.original

        if self.default is not None:
            out["default"] = self.default

        if self.options is not None:
            out["options"] = self.options

        if self.labels is not None:
            out["labels"] = self.labels

        if self.style is not None:
            out["style"] = self.style

        if self.optional:
            out["optional"] = self.optional

        if self.multi:
            out["multi"] = self.multi

        if self.trigger:  
            out["trigger"] = self.trigger

        if self.readonly:  
            out["readonly"] = self.readonly

        if self.header:  
            out["header"] = self.header

        if self.errors:  
            out["errors"] = self.errors

        if self.fields:
            out["fields"] = self.fields.to_list()

        return out


class Fields:

    def __init__(self, values=None, originals=None, fields=None, errors=None):

        if values is None:
            values = {}

        if originals is None:
            originals = {}

        if errors is None:
            errors = []

        self.order = []
        self.names = {}
        self.values = values
        self.originals = originals
        self.errors = errors

        if fields is None:
            fields = []

        self.extend(fields)

    def append(self, *args, **kwargs):

        if len(args) == 1:
            kwargs = args[0]

        if "name" not in kwargs:
            raise MissingName("Missing name in %s" % kwargs)

        if kwargs["name"] in self.names:
            raise DuplicateName("Name %s exists" % kwargs["name"])

        if "value" not in kwargs and kwargs["name"] in self.values:
            kwargs["value"] = self.values[kwargs["name"]]

        if "original" not in kwargs and kwargs["name"] in self.originals:
            kwargs["original"] = self.originals[kwargs["name"]]

        field = Field(**kwargs)

        self.order.append(field)
        self.names[field.name] = field

    def extend(self, fields):

        for field in fields:
            self.append(**field)

    def validate(self):

        for name in self.values:
            if name not in self.names:
                self.errors.append("unknown field '%s'" % name)

        valid = not self.errors

        for field in self.order:
            valid = field.validate() and valid

        return valid

    def __iter__(self):
        return iter(self.order)

    def __getitem__(self, key):

        if isinstance(key, int):
            return self.order[key]
        elif isinstance(key, str):
            return self.names[key]

    def __len__(self):
        return len(self.order)

    def to_list(self):

        out = []

        for field in self.order:
            out.append(field.to_dict())

        return out
