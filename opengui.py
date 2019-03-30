
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
        multi=False,
        trigger=False,
        readonly=False,
        header=False,
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
        self.trigger = trigger
        self.readonly = readonly
        self.header = header

        if fields is not None:
            self.fields = Form(values=self.value, originals=self.original, fields=fields)
        else:
            self.fields = None

    def append(self, **kwargs):
        self.fields.append(**kwargs)

    def extend(self, fields):
        self.fields.extend(fields)

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

        if self.multi:
            out["multi"] = self.multi

        if self.trigger:  
            out["trigger"] = self.trigger

        if self.readonly:  
            out["readonly"] = self.readonly

        if self.header:  
            out["header"] = self.header

        if self.fields:
            out["fields"] = self.fields.to_list()

        return out


class Form:

    def __init__(self, values=None, originals=None, fields=None):

        if values is None:
            values = {}

        if originals is None:
            originals = {}

        self.fields = []
        self.names = {}
        self.values = values
        self.originals = originals

        if fields is None:
            fields = []

        self.extend(fields)

    def append(self, **kwargs):

        if "name" not in kwargs:
            raise MissingName("Missing name in %s" % kwargs)

        if kwargs["name"] in self.names:
            raise DuplicateName("Name %s exists" % kwargs["name"])

        if "value" not in kwargs and kwargs["name"] in self.values:
            kwargs["value"] = self.values[kwargs["name"]]

        if "original" not in kwargs and kwargs["name"] in self.originals:
            kwargs["original"] = self.originals[kwargs["name"]]

        field = Field(**kwargs)

        self.fields.append(field)
        self.names[field.name] = field

    def extend(self, fields):

        for field in fields:
            self.append(**field)

    def __iter__(self):
        return iter(self.fields)

    def __getitem__(self, key):

        if isinstance(key, int):
            return self.fields[key]
        elif isinstance(key, str):
            return self.names[key]

    def __len__(self):
        return len(self.fields)

    def to_list(self):

        out = []

        for field in self.fields:
            out.append(field.to_dict())

        return out
