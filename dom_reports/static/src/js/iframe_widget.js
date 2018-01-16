odoo.define('dom_reports.iframe_widget', function (require) { // has to be the same as folder name
"use strict";

var core = require('web.core');
// var formats = require('web.formats');
// var common = require('web.form_common');
var widget = require('web.Widget');
var registry = require('web.field_registry');
var AbstractField = require('web.AbstractField');

var _t = core._t;
var QWeb = core.qweb;

var utils = require('web.utils');
// var dom_utils = require('web.dom_utils');

var IFrameWidget = AbstractField.extend({

    // when the input changes (litteraly the <input> tag)
    // we take the value written in it and and set it as our internal value
    /*
    events: {
        'change input': function (e) {
            if (!this.get('effective_readonly')) {
                this.internal_set_value($(e.currentTarget).val());
            }
        }
    },*/
    init: function() {
        this._super.apply(this, arguments);
        this.set("value", "");
    },
    // called immediately after the widget is added to the DOM
    // bind events in it so they are effective right away.
    // to redisplay the field based on readyness
    start: function() {
        this.on("change:effective_readonly", this, function() {
            this.display_field();
            this.render_value();
        });
        this.display_field();
        return this._super();
    },
    display_field: function() {

        var doc_id = undefined;
        try {
            var doc_id = this.value.data.id;
        } catch(err) {
            return;
        }

        if(!doc_id) {
            return
        }

        this.$el.html(QWeb.render("dom_reports.IFrameWidget", {
            widget: this,
            doc_id: doc_id,
        }));
    },
    render_value: function() {
        if (this.get("effective_readonly")) {
            this.$(".oe_field_color_content").css("background-color", this.get("value") || "#FFFFFF");
        } else {
            this.$("input").val(this.get("value") || "#FFFFFF");
        }
    },
});

// core.form_widget_registry.add('iframe_widget', IFrameWidget);
registry.add('dr_iframe_widget', IFrameWidget)

});
