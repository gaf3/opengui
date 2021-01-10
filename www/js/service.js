window.DRApp = new DoTRoute.Application();

DRApp.load = function (name) {
    return $.ajax({url: name + ".html", async: false}).responseText;
}

$.ajaxPrefilter(function(options, originalOptions, jqXHR) {});

DRApp.group = $.ajax({url: "/api/group", async: false}).responseJSON.group;

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
    home: function() {
        this.application.render(this.it);
    },
    url: function(params) {
        if (params && Object.keys(params).length) {
            return "/api/" + this.singular + "?" + $.param(params);
        } else {
            return "/api/" + this.singular;
        }
    },
    id_url: function() {
        return this.url() + "/" + this.application.current.path.id;
    },
    route: function(action, id) {
        if (id) {
            this.application.go(this.singular + "_" + action, id);
        } else {
            this.application.go(this.singular + "_" + action);
        }
    },
    list: function() {
        this.it = this.rest("GET",this.url());
        this.application.render(this.it);
    },
    fields_change: function() {
        this.it = this.rest("OPTIONS",this.url(), this.fields_request());
        this.application.render(this.it);
    },
    field_value(field, value, values) {
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
            } else if (field.options) {
                if (field.multi) {
                    values[field.name] = [];
                    $("input[name='" + full_name + "']:checked").each(function () {
                        this.field_value(field, $(this).val(), values[field.name]);
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
        request[this.singular] = this.fields_values();
        return request;
    },
    create: function() {
        this.it = this.rest("OPTIONS",this.url());
        this.application.render(this.it);
    },
    create_save: function() {
        var request = this.fields_request();
        this.it = this.rest("OPTIONS",this.url(), request);
        if (this.it.hasOwnProperty('errors')) {
            this.application.render(this.it);
        } else {
            this.route("retrieve", this.rest("POST",this.url(), request)[this.singular].id);
        }
    },
    retrieve: function() {
        this.it = this.rest("OPTIONS",this.id_url());
        this.application.render(this.it);
    },
    update: function() {
        this.it = this.rest("OPTIONS",this.id_url());
        this.application.render(this.it);
    },
    update_save: function() {
        var request = this.fields_request();
        this.it = this.rest("OPTIONS",this.id_url(), request);
        if (this.it.hasOwnProperty('errors')) {
            this.application.render(this.it);
        } else {
            this.rest("PATCH",this.id_url(), request);
            this.route("retrieve", this.application.current.path.id);
        }
    },
    delete: function() {
        if (confirm("Are you sure?")) {
            this.rest("DELETE", this.id_url());
            this.route("list");
        }
    }
});

// Service

DRApp.partial("Header",DRApp.load("header"));
DRApp.partial("Form",DRApp.load("form"));
DRApp.partial("Footer",DRApp.load("footer"));

DRApp.template("Home",DRApp.load("home"),null,DRApp.partials);
DRApp.template("Fields",DRApp.load("fields"),null,DRApp.partials);
DRApp.template("Create",DRApp.load("create"),null,DRApp.partials);
DRApp.template("Retrieve",DRApp.load("retrieve"),null,DRApp.partials);
DRApp.template("Update",DRApp.load("update"),null,DRApp.partials);

DRApp.route("home","/","Home","Base","home");