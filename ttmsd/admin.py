# coding: utf-8

# Copyright (C) 2023 by Markus Rosjat<markus.rosjat@gmail.com>
# SPDX-FileCopyrightText: 2022 The TracTicketMSTeamsDispatcherPlugin Authors
#
# SPDX-License-Identifier: LGPL-2.1-or-later

from trac.admin import IAdminPanelProvider
from trac.core import Component, implements
from trac.env import IEnvironmentSetupParticipant
from trac.util.translation import _
from trac.web.api import IRequestFilter
from trac.web.chrome import ITemplateProvider, add_script

from ttmsd.utils import get_configuration_options, get_web_hooks_from_dict


class TicketTeamDispatcherAdmin(Component):
    """Provides functions related to registration"""

    implements(
        IAdminPanelProvider,
        IEnvironmentSetupParticipant,
        ITemplateProvider,
        IRequestFilter,
    )

    _section = "msteams-dispatcher"
    _web_hook_types = ["MS Teams", "Discord"]
    # IEnvironmentSetupParticipant methods

    def environment_created(self):
        self.upgrade_environment()

    def environment_needs_upgrade(self, db=None):
        return "ttmsd" not in self.config["ticket-custom"]

    def upgrade_environment(self, db=None):
        self.config.set("ticket-custom", "ttmsd", "checkbox")
        self.config.set("ticket-custom", "ttmsd.label", "Notify MS Teams")
        self.config.set("ticket-custom", "ttmsd.value", 1)
        self.config.set(self._section, "web_hook_1.name", "")
        self.config.set(self._section, "web_hook_1.url", "")
        self.config.set(self._section, "web_hook_1.type", "MS Teams")
        self.config.save()

    # IAdminPanelProvider methods

    def get_admin_panels(self, req):
        if "TICKET_ADMIN" in req.perm:
            yield "ticket", "Ticket System", "ttmsd", "MS Teams Dispatcher"

    def render_admin_panel(self, req, category, page, path_info):
        req.perm.require("TICKET_ADMIN")
        web_hooks = self.get_web_hooks()
        if req.method == "POST":
            action: str = req.args.get("apply-action")
            if action == "set-connector":
                tmp = {}
                [
                    tmp.update({key: req.args[key]})
                    for key in req.args.keys()
                    if key.startswith("web_hook")
                ]
                updated_web_hooks = get_web_hooks_from_dict(tmp)
                self.set_web_hooks(updated_web_hooks)
            req.redirect(req.href.admin(category, page))
        return "msteams_dispatcher_admin.html", {
            "web_hooks": web_hooks,
            "web_hook_types": self._web_hook_types,
        }

    def get_templates_dirs(self):
        from pkg_resources import resource_filename

        return [
            resource_filename(__name__, "templates"),
        ]

    def get_htdocs_dirs(self):
        from pkg_resources import resource_filename

        yield "ttmsd", resource_filename(__name__, "htdocs")

    def get_web_hooks(self):
        return self._get_configuration_options(self._section)

    def _get_configuration_options(self, section):
        return get_configuration_options(self.config, section)

    def set_web_hooks(self, web_hooks):
        # we are not clever here we simply delete the old web hooks before we add the new ones.
        [
            self.config.remove(self._section, option)
            for option, value in self.config.options(self._section)
        ]
        for web_hook in web_hooks:
            id, name, url, t = web_hook
            if url:
                self.config.set(self._section, f"web_hook_{id}.name", name)
                self.config.set(self._section, f"web_hook_{id}.url", url)
                self.config.set(self._section, f"web_hook_{id}.type", t)
        self.config.save()

    def post_process_request(self, req, template, data, content_type):
        add_script(req, "ttmsd/ttmsd.js")
        return template, data, content_type

    def pre_process_request(self, req, handler):
        return handler
