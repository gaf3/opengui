window.DRApp = new DoTRoute.Application();

DRApp.load = function (name) {
    return $.ajax({url: name + ".html", async: false}).responseText;
}

$.ajaxPrefilter(function(options, originalOptions, jqXHR) {});

DRApp.controller("Base",null,{
    rest: function(type,url,data) {
        var response = $.ajax({
            type: type,
            url: url,
            contentType: "application/json",
            data: data ? JSON.stringify(data) : (type != 'GET' ? '{}' : null),
            dataType: "json",
            async: false
        });
        if ((response.status != 200) && (response.status != 201) && (response.status != 202)) {
            alert(type + ": " + url + " failed");
            throw (type + ": " + url + " failed");
        }
        return response.responseJSON;
    },
    fields_change: function() {
        this.it = this.rest("OPTIONS","api/example", this.fields_request());
        this.application.render(this.it);
    },
    field_value: function(field, value, values) {
        for (var option = 0; option < field.options.length; option++) {
            if (value == field.options[option]) {
                if (Array.isArray(values)) {
                    values.push(field.options[option]);
                } else {
                    values[field.name] = field.options[option];
                }
            }
        }
    },
    fields_values: function(prefix, fields) {
        prefix = prefix || [];
        fields = fields || this.it.fields;
        var values = {};
        for (var index = 0; index < fields.length; index++) {
            var field = fields[index];
            if (field.fields) {
                values[field.name] = this.fields_values(prefix.concat(field.name), field.fields);
                continue;
            }
            var full_name = prefix.concat(field.name).join('-').replace(/\./g, '-');
            if (field.readonly) {
                continue
            } else if (field.options && field.style != "select") {
                if (field.multi) {
                    values[field.name] = [];
                    var that = this;
                    $("input[name='" + full_name + "']:checked").each(function () {
                        that.field_value(field, $(this).val(), values[field.name]);
                    });
                } else {
                    this.field_value(field, $("input[name='" + full_name+ "']:checked").val(), values);
                }
            } else {
                values[field.name] = $('#' + full_name).val();
            }
            if (field.name == "yaml" && values[field.name] == "") {
                values[field.name] = "{}";
            }
        }
        return values;
    },
    fields_request: function() {
        var request = {};
        request['values'] = this.fields_values();
        return request;
    },
    create: function() {
        this.it = this.rest("OPTIONS","api/example");
        this.application.render(this.it);
    },
    create_save: function() {
        var request = this.fields_request();
        this.it = this.rest("OPTIONS","api/example", request);
        if (this.it.errors && this.it.errors.length) {
            this.application.render(this.it);
        } else {
            this.application.render(this.it);
            alert(JSON.stringify(this.rest("POST","api/example", request), null, 2));
        }
    }
});

// Service

DRApp.partial("Header",DRApp.load("header"));
DRApp.partial("Form",DRApp.load("form"));
DRApp.partial("Footer",DRApp.load("footer"));

DRApp.template("Fields",DRApp.load("fields"),null,DRApp.partials);
DRApp.template("Create",DRApp.load("create"),null,DRApp.partials);

DRApp.route("home","/","Create","Base","create");
