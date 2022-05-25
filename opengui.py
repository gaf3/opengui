import re

class MissingName(Exception):
    pass

class DuplicateName(Exception):
    pass


class Field:

    ATTRIBUTES = [
        "name",
        "value",
        "original",
        "default",
        "options",
        "required",
        "multi",
        "trigger",
        "readonly",
        "validation",
        "content",
        "errors",
        "fields"
    ]

    def __init__(
        self,
        name,
        value=None,
        original=None,
        default=None,
        options=None,
        required=False,
        multi=False,
        trigger=False,
        readonly=False,
        validation=None,
        content=None,
        errors=None,
        fields=None
    ):

        self.name = name
        self.value = value
        self.original = original
        self.default = default
        self.options = options
        self.required = required
        self.multi = multi
        self.trigger = trigger
        self.readonly = readonly
        self.validation = validation

        if content is None:
            content = {}

        self.content = content

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

    def validate(self, store=True):

        if self.fields:
            return self.fields.validate(store)

        errors = []

        if self.value is None and self.default:
            self.value = self.default
        if self.value is None and self.readonly:
            self.value = self.original
        elif self.value is None and self.required:
            errors.append("missing value")
        elif self.value is not None and self.multi and not isinstance(self.value,list):
            errors.append("multi requires list")
        elif self.value is not None and self.multi:
            invalid = []
            for value in self.values:
                if value not in self.options:
                    invalid.append(value)
            if invalid:
                errors.append("invalid values %s" % invalid)
        elif self.value is not None and self.options and self.value not in self.options:
            errors.append("invalid value '%s'" % self.value)

        if self.validation:
            if self.value is not None:
                if isinstance(self.validation, str):
                    if not re.match(self.validation, self.value):
                        errors.append("must match '%s'" % self.validation)
                else:
                    self.validation(self, errors)

        if store:
            self.errors = errors

        return not errors

    def __getattr__(self, attr):
        if attr == "values":
            return self.value
        elif attr == "originals":
            return self.original

    def __iter__(self):
        return iter(self.fields)

    def __contains__(self, key):
        return self.fields and key in self.fields

    def __getitem__(self, key):
        return self.fields[key]

    def __len__(self):
        return len(self.fields)

    def to_dict(self):

        out = {
            "name": self.name
        }

        if self.value is not None:
            out["value"] = self.value

        if self.original is not None:
            out["original"] = self.original

        if self.default is not None:
            out["default"] = self.default

        if self.options is not None:
            out["options"] = self.options

        if self.required:
            out["required"] = self.required

        if self.multi:
            out["multi"] = self.multi

        if self.trigger:
            out["trigger"] = self.trigger

        if self.readonly:
            out["readonly"] = self.readonly

        if isinstance(self.validation, str):
            out["validation"] = self.validation

        if self.content:
            out.update({key: value for key, value in self.content.items() if key not in self.ATTRIBUTES})

        if self.errors:
            out["errors"] = self.errors

        if self.fields:
            out["fields"] = self.fields.to_list()

        return out


class Fields:

    def __init__(self, values=None, originals=None, fields=None, errors=None, valid=None, validation=None, ready=None):

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
        self.valid = valid
        self.validation = validation
        self.ready = ready

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

        attributes = {}

        attributes["content"] = kwargs.get("content", {})

        for key,value in kwargs.items():
            if key in Field.ATTRIBUTES:
                attributes[key] = value
            else:
                attributes["content"][key] = value

        field = Field(**attributes)

        self.order.append(field)
        self.names[field.name] = field

    def update(self, *args, **kwargs):

        if len(args) == 1:
            kwargs = args[0]

        if "name" not in kwargs:
            raise MissingName("Missing name in %s" % kwargs)

        if kwargs["name"] not in self.names:
            self.append(**kwargs)
            return

        field = self.names[kwargs["name"]]

        for key, value in kwargs.items():
            if key in Field.ATTRIBUTES:
                setattr(field, key, value)
            else:
                field.content[key] = value

    def extend(self, fields):

        for field in fields:
            self.append(**field)

    def validate(self, store=True):

        valid = True
        errors = []

        for name in self.values:
            if name not in self.names:
                errors.append("unknown field '%s'" % name)

        valid = not errors

        for field in self.order:
            valid = field.validate(store) and valid

        if self.validation is not None:
            valid = self.validation(self, errors) and valid

        if store:
            self.valid = valid
            self.errors = errors

        return valid

    def __iter__(self):
        return iter(self.order)

    def __contains__(self, key):

        return key in self.names

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

    def to_dict(self):

        out = {
            "fields": self.to_list()
        }

        if self.errors is not None:
            out["errors"] = self.errors

        if self.valid is not None:
            out["valid"] = self.valid

        if self.ready is not None:
            out["ready"] = self.ready

        return out
