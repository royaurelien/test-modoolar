# -*- coding: utf-8 -*-
{
    "name": "Message / Note Editing",
    "version": "11.0.1.0.3",
    "category": "Discuss",
    "author": "Odoo Tools",
    "website": "https://odootools.com/apps/11.0/message-note-editing-18",
    "license": "Other proprietary",
    "application": True,
    "installable": True,
    "auto_install": False,
    "depends": [
        "mail"
    ],
    "data": [
        "data/data.xml",
        "security/ir.model.access.csv",
        "views/templates.xml",
        "views/mail_message_view.xml"
    ],
    "qweb": [
        "static/src/xml/message_edit.xml"
    ],
    "js": [
        
    ],
    "demo": [
        
    ],
    "external_dependencies": {},
    "summary": "The tool to correct accidental mistakes in messages and notes",
    "description": """
    You have logged a long note and suddenly understand that there is a mistake. Some mistakes, such as misprints, are just irritating. Others, such as commercial offer peculiarities, might have critical consequences since they mislead you or your colleagues. Faced that situation Odoo users attach a new message. However, it is a bad option: everything becomes ambiguous, and contradictions disorient users. The proper solution is to update a current note, but to keep a clear history of changes for references. The app is the tool to address this challenge.

    The tool works both for logged notes and for sent messages
    Update body content any time from document threads, form channels, and from direct discussions
    Editing is simple: push the 'pencil' button, introduce a change, and save it
    Modified records are marked red: <strong>nobody is confused</strong>
    Updates are kept in clear and easy-reached history. Refer it in case of arguable issues
    Users are allowed to edit <strong>only own</strong> messages and notes
    Notes and messages to edit
    Thread before changes
    Wizard to update comment (only body is editable)
    Thread after changes
    History of updates is kept for references
    Users might modify only own messages and notes
    Change messages from Odoo channels
    Even direct messages are possible to update
    Modified messages are distinguishable in Odoo Inbox
""",
    "images": [
        "static/description/main.png"
    ],
    "price": "44.0",
    "currency": "EUR",
}