# coding: utf-8

# Copyright (C) 2023 by Markus Rosjat<markus.rosjat@gmail.com>
# SPDX-FileCopyrightText: 2022 The TracTicketMSTeamsDispatcherPlugin Authors
#
# SPDX-License-Identifier: LGPL-2.1-or-later

import json

import requests
from trac.core import Component, implements
from trac.ticket.api import ITicketChangeListener

from ttmsd.utils import get_configuration_options


def discord_change_payload(ticket_id, comment, values):
    embed = {"description": comment, "title": values["description"]}

    data = {
        "content": f"Ticket #{str(ticket_id)}",
        "username": "Trac",
        "embeds": [embed],
    }
    return data


def create_payload(payload, ticket_id, values):
    title = "Ticket #%s" % str(ticket_id)
    payload = {
        "@type": "MessageCard",
        "@context": "http://schema.org/extensions",
        "themeColor": "007600",
        "summary": values["summary"],
        "sections": [
            {
                "activityTitle": title,
                "activitySubtitle": values["component"],
                "activityImage": "https://teamsnodesample.azurewebsites.net/static/img/image5.png",
                "facts": [
                    {"name": "Status:", "value": values["status"]},
                    {
                        "name": "Erstellt:",
                        "value": values["time"].strftime("%d.%m.%Y %H:%M"),
                    },
                    {"name": "Kunde:", "value": values["component"]},
                    {"name": "Priority:", "value": values["priority"]},
                    {"name": "Beschreibung:", "value": values["description"]},
                ],
                "markdown": True,
            }
        ],
    }
    return json.dumps(payload, indent=4)


def change_payload(ticket_id, comment, values):
    title = "Ticket #%s" % str(ticket_id)
    payload = {
        "@type": "MessageCard",
        "@context": "http://schema.org/extensions",
        "themeColor": "007600",
        "summary": values["summary"],
        "sections": [
            {
                "activityTitle": title,
                "activitySubtitle": values["component"],
                "activityImage": "https://teamsnodesample.azurewebsites.net/static/img/image5.png",
                "facts": [
                    {"name": "Status:", "value": values["status"]},
                    {
                        "name": "Bearbeitet am:",
                        "value": values["time"].strftime("%d.%m.%Y %H:%M"),
                    },
                    {"name": "Kunde:", "value": values["component"]},
                    {"name": "Priority:", "value": values["priority"]},
                    {"name": "Eintrag:", "value": comment},
                    {"name": "Bearbeiter:", "value": values["owner"]},
                ],
                "markdown": True,
            }
        ],
    }
    return json.dumps(payload, indent=4)


class TicketMsTeamsNotification(Component):
    implements(ITicketChangeListener)
    _section = "msteams-dispatcher"

    def ticket_created(self, ticket):
        notify_ms_teams = ticket.values["ttmsd"]
        if notify_ms_teams:
            for web_hook in get_configuration_options(self.config, self._section):
                if web_hook.type == "MS Teams":
                    requests.post(
                        web_hook.url, create_payload(ticket.id, ticket.values)
                    )

    def ticket_changed(self, ticket, comment, author, old_values):
        notify_ms_teams = ticket.values["ttmsd"]
        if notify_ms_teams:
            for web_hook in get_configuration_options(self.config, self._section):
                if web_hook.type == "Discord":
                    requests.post(
                        web_hook.url,
                        json=discord_change_payload(ticket.id, comment, ticket.values),
                    )
                    continue
                if web_hook.type == "MS Teams":
                    requests.post(
                        web_hook.url, change_payload(ticket.id, comment, ticket.values)
                    )
                    continue

    def ticket_deleted(self, ticket):
        pass

    def ticket_comment_modified(self, ticket, cdate, author, comment, old_comment):
        pass

    def ticket_change_deleted(self, ticket, cdate, changes):
        pass
