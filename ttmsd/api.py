# coding: utf-8

# Copyright (C) 2023 by Markus Rosjat<markus.rosjat@gmail.com>
# SPDX-FileCopyrightText: 2022 The TracTicketMSTeamsDispatcherPlugin Authors
#
# SPDX-License-Identifier: LGPL-2.1-or-later

import json

import requests
from trac.core import Component, implements
from trac.ticket.api import ITicketChangeListener

from ttmsd.model import DiscordPayload, PayloadValue, TeamsPayload
from ttmsd.utils import (
    get_payloads_from_db_by_type,
    get_webhooks_from_db_by_type,
    setup_db_payload_values,
)


class TicketMsTeamsNotification(Component):
    """Component to handle payloads on ticket creation, update, deletion."""

    implements(ITicketChangeListener)
    _section = "msteams-dispatcher"

    def __init__(self, *args, **kwargs) -> None:
        self._payload_values = setup_db_payload_values(self.env)
        super().__init__(*args, **kwargs)

    def ticket_created(self, ticket):
        notify_ms_teams = ticket.values["ttmsd"]
        if notify_ms_teams:
            self._send_payload(ticket, 1, 1)

    def ticket_changed(self, ticket, comment, author, old_values):
        notify_ms_teams = ticket.values["ttmsd"]
        if notify_ms_teams:
            self._send_payload(ticket, 1, 2)

    def ticket_deleted(self, ticket):
        notify_ms_teams = ticket.values["ttmsd"]
        if notify_ms_teams:
            # this is just a PoC since we might want to pass the args given to a payload
            # so we might make more _send_xxx_payload methods to accommodate this ....
            self._send_payload(ticket, 1, 3)

    def ticket_comment_modified(self, ticket, cdate, author, comment, old_comment):
        notify_ms_teams = ticket.values["ttmsd"]
        if notify_ms_teams:
            # this is just a PoC since we might want to pass the args given to a payload
            # so we might make more _send_xxx_payload methods to accommodate this ....
            self._send_payload(ticket, 1, 4)

    def ticket_change_deleted(self, ticket, cdate, changes):
        notify_ms_teams = ticket.values["ttmsd"]
        if notify_ms_teams:
            # this is just a PoC since we might want to pass the args given to a payload
            # so we might make more _send_xxx_payload methods to accommodate this ....
            self._send_payload(1, 5)

    def _send_payload(self, ticket, webhook_type: int, payload_type: int):
        _web_hooks = get_webhooks_from_db_by_type(self.env, webhook_type)
        for web_hook in _web_hooks:
            if webhook_type == 1:
                _create_payload = self._create_teams_payload
            if webhook_type == 2:
                _create_payload = self._create_discord_payload
            payloads = get_payloads_from_db_by_type(self.env, payload_type)
            for payload in payloads:
                requests.post(
                    web_hook.url,
                    _create_payload(
                        payload,
                        ticket,
                    ),
                    timeout=5,
                )

    def _create_teams_payload(
        self,
        payload: TeamsPayload,
        ticket,
    ):
        _ = (
            [v.name for v in self._payload_values if v.id == payload.summary][0]
            .split("_")[1]
            .lower()
        )
        _summary = ticket.values[_]
        _title = "Ticket #%s" % str(ticket.id)
        _sections = []
        for section in payload.sections:
            _s = section.build_dict_from_ticket(ticket.values, self._payload_values)
            _s["facts"] = []
            for fact in section.facts:
                _ = fact.build_dict_from_ticket(ticket.values, self._payload_values)
                _s["facts"].append(_)
            _sections.append(_s)
            _sections[0]["activityTitle"] = _title
        _payload = {
            "@type": "MessageCard",
            "@context": "http://schema.org/extensions",
            "themeColor": payload.themeColor,
            "summary": _summary,
            "sections": _sections,
        }
        return json.dumps(_payload, indent=4)

    def _create_discord_payload(
        self,
        payload: DiscordPayload,
        ticket,
    ):
        """
        embed = {"description": comment, "title": values["description"]}

        data = {
            "content": f"Ticket #{str(ticket_id)}",
            "username": "Trac",
            "embeds": [embed],
        }
        return data
        """
        pass
