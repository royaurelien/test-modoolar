odoo.define('crm_yzi_calendar.quick_create', function (require) {
//odoo.define('web.CalendarQuickCreate', function (require) {

"use strict";

// var core = require('web.core');
// var Dialog = require('web.Dialog');
// var form_common = require('web.form_common');
var webCalQuickCreate = require('web.CalendarQuickCreate');
var core = require('web.core');
var Dialog = require('web.Dialog');
var relational_fields = require('web.relational_fields');

var studio_new_field = require('web_studio.NewFieldDialog');

var StandaloneFieldManagerMixin = require('web.StandaloneFieldManagerMixin');

var Many2one = relational_fields.FieldMany2One;

_.extend(webCalQuickCreate, StandaloneFieldManagerMixin);

// webCalQuickCreate.include(StandaloneFieldManagerMixin);

webCalQuickCreate.include({

    init: function (parent, buttons, options, dataTemplate, dataCalendar) {
        // debugger;
        // this._super(parent, {});
        // StandaloneFieldManagerMixin.init.apply(this, arguments);
        this._super.apply(this, arguments);
        StandaloneFieldManagerMixin.init.call(this);
        // this WON'T work, gives 'this.model.makeRecord' not found
        // StandaloneFieldManagerMixin.init.apply(this, arguments);

    },

    /**
     * @override
    willStart: function () {
        var self = this;
        debugger;
    },
     */

    start: function() {
        // debugger;

        var self = this;
        var defs = [];
        var record;
        var options = {
            mode: 'edit',
        };

        defs.push(this.model.makeRecord('res.partner', [{
            name: 'societe',
            relation: 'res.partner',
            type: 'many2one',
            // domain: [['relation', '=', this.model_name], ['ttype', '=', 'many2one']],
        }], {
            'societe': {
                can_create: false,
            }
        }).then(function (recordID) {
            record = self.model.get(recordID);
            self.many2one_field = new Many2one(self, 'societe', record, options);
            // self._registerWidget(recordID, 'field', self.many2one_field);
            self.many2one_field.nodeOptions.no_create_edit = !core.debug;
            self.many2one_field.appendTo(self.$('.o_many2one_field_societe'));
        }));

        defs.push(this.model.makeRecord('res.partner', [{
            name: 'contact',
            relation: 'res.partner',
            type: 'many2one',
            // domain: [['relation', '=', this.model_name], ['ttype', '=', 'many2one']],
        }], {
            'contact': {
                can_create: false,
            }
        }).then(function (recordID) {
            record = self.model.get(recordID);
            self.many2one_field = new Many2one(self, 'contact', record, options);
            // self._registerWidget(recordID, 'field', self.many2one_field);
            self.many2one_field.nodeOptions.no_create_edit = !core.debug;
            self.many2one_field.appendTo(self.$('.o_many2one_field_contact'));
        }));
    },

});

});
