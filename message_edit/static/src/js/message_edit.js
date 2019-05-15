odoo.define('message_edit.message_edit', function(require) {
    var core = require('web.core');
    var data = require('web.data');
    var _t = core._t;
    var chatThread = require('mail.ChatThread');
    var dialogs = require('web.view_dialogs');
    var chatManager = require('mail.chat_manager');
    var makeMessage =  chatManager.make_message;

    chatThread.include({
        events: _.extend({}, chatThread.prototype.events, {
            'click .fa-edit': '_onMessageEdit',
        }),

        _onMessageEdit: function (event) {
            // Method to open dialog to change message
            var self = this;
            var messageObj = $(event.currentTarget);
            var messageId = parseInt(event.target.dataset['messageId'], 10);
            var $message = messageObj.parents('.o_thread_message');
            var context = {"message_edit": true};
            this._rpc({
                model: "mail.message",
                method: 'get_edit_formview_id',
                args: [[messageId]],
                context: context,
            }).then(function (view_id) {
                var onSaved = function(record) {
                    // Since we migth be both in field of form and in chatter we can't use setValue
                    // Instead we update the body manually through the js
                    var updatedBody = record.data.body;
                    var contentElement = $message.find('.o_thread_message_content');
                    // We use indexOf, since innerHTML has a lot of breaks inside
                    if (contentElement[0].innerHTML.indexOf(updatedBody) == -1) {
                        contentElement[0].innerHTML = updatedBody;
                        messageObj.parent().addClass("already_changed");
                    };
                };
                new dialogs.FormViewDialog(self, {
                    res_model: "mail.message",
                    res_id: messageId,
                    context: context,
                    title: _t("Edit Message"),
                    view_id: view_id,
                    readonly: false,
                    on_saved: onSaved,
                    shouldSaveLocally: false,
                }).open();
            });
        },

    });

    // To pass 'changed' to the interface
    chatManager.make_message = function(data) {
        message = makeMessage(data);
        message.changed = data.changed;
        return message
    }

});
