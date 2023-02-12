# coding: utf-8

# Copyright (C) 2023 by Markus Rosjat<markus.rosjat@gmail.com>
# SPDX-FileCopyrightText: 2022 The TracTicketMSTeamsDispatcherPlugin Authors
#
# SPDX-License-Identifier: LGPL-2.1-or-later

from trac.admin import IAdminPanelProvider
from trac.core import Component, implements
from trac.util.translation import N_, _, gettext
from trac.web.api import IRequestFilter
from trac.web.chrome import ITemplateProvider, add_script, add_stylesheet

from ttmsd.model import TeamsSection
from ttmsd.utils import (
    delete_webhook_by_id_in_db,
    get_configuration_options,
    get_payloads_from_db,
    get_payloads_from_request,
    get_web_hooks_from_dict,
    get_webhooks_from_db,
    setup_db_payload_types,
    setup_db_payload_values,
    setup_db_webhook_types,
    update_db_from_payloads,
    update_webhooks_in_db,
)


class TicketTeamDispatcherAdminPanel(Component):
    """Abstract Base to provide shared functionality fro subclasses"""

    implements(IAdminPanelProvider, ITemplateProvider, IRequestFilter)

    _section = "msteams-dispatcher"
    _type = "undefined"
    _label = N_("(Undefined)"), N_("(Undefined)")

    abstract = True

    def get_admin_panels(self, req):
        if "TICKET_ADMIN" in req.perm:
            yield (
                "ttmsd",
                _("Webhook Dispatcher"),
                self._type,
                gettext(self._label[1]),
            )

    def render_admin_panel(self, req, cat, page, path_info):
        # Trap AssertionErrors and convert them to TracErrors
        try:
            return self._render_admin_panel(req, cat, page, path_info)
        except AssertionError as e:
            raise TracError(e) from e

    def _render_admin_panel(self, req, cat, page, path_info):
        raise NotImplemented(
            "Class inheriting from TicketAdminPanel has not "
            "implemented the _render_admin_panel method."
        )

    def get_templates_dirs(self):
        from pkg_resources import resource_filename

        return [
            resource_filename(__name__, "templates"),
        ]

    def get_htdocs_dirs(self):
        from pkg_resources import resource_filename

        yield "ttmsd", resource_filename(__name__, "htdocs")

    def post_process_request(self, req, template, data, content_type):
        add_script(req, "ttmsd/ttmsd.js")
        add_stylesheet(req, "ttmsd/ttmsd.css")
        return template, data, content_type

    def pre_process_request(self, req, handler):
        return handler


class WebhookAdminPanel(TicketTeamDispatcherAdminPanel):
    """Provides functions related to webhook management"""

    _type = "webhooks"
    _label = N_("Webhook"), N_("Webhooks")

    def _render_admin_panel(self, req, category, page, path_info):
        req.perm.require("TICKET_ADMIN")
        web_hooks = self.get_web_hooks()
        if req.method == "POST":
            action: str = req.args.get("apply-action")
            if action == "set-connector":
                to_delete = req.args.get("webhook_delete_list").split(",")[1:]
                print(to_delete)
                tmp = {}
                [
                    tmp.update({key: req.args[key]})
                    for key in req.args.keys()
                    if key.startswith("web_hook")
                ]
                updated_web_hooks = get_web_hooks_from_dict(tmp)
                self.set_web_hooks(updated_web_hooks, to_delete)
            req.redirect(req.href.admin(category, page))
        return "msteams_dispatcher_admin.html", {
            "web_hooks": web_hooks,
            "web_hook_types": setup_db_webhook_types(self.env),
            "json_presets": [
                preset.json() for preset in setup_db_webhook_types(self.env)
            ],
        }

    def get_web_hooks(self):
        return get_webhooks_from_db(self.env)

    def _get_configuration_options(self, section):
        return get_configuration_options(self.config, section)

    def set_web_hooks(self, web_hooks, to_delete):
        # we are not clever here we simply delete the old web hooks before we add the new ones.
        if len(to_delete) > 0:
            for id in to_delete:
                delete_webhook_by_id_in_db(self.env, id)
        update_webhooks_in_db(self.env, web_hooks)


class PayloadAdminPanel(TicketTeamDispatcherAdminPanel):
    """Provides functions related to payload management"""

    implements(IRequestFilter)

    _type = "payloads"
    _label = N_("Payload"), N_("Payloads")
    _payload_values = []

    def _render_admin_panel(self, req, category, page, path_info):
        payloads = []
        req.perm.require("TICKET_ADMIN")
        if req.method == "POST":
            action: str = req.args.get("apply-action")
            if action == "set-connector":
                payloads = get_payloads_from_request(req)
                # we got the payloads now and we need to store the changes in the db
                update_db_from_payloads(self.env, payloads)
        payloads = get_payloads_from_db(self.env)
        return "msteams_dispatcher_payload_admin.html", {
            "payloads": payloads,
            "presets": setup_db_payload_values(self.env),
            "types": setup_db_payload_types(self.env),
            "wh_types": setup_db_webhook_types(self.env),
            "json_presets": [
                preset.json() for preset in setup_db_payload_values(self.env)
            ],
        }
