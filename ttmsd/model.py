# Copyright (C) 2023 by Markus Rosjat<markus.rosjat@gmail.com>
# SPDX-FileCopyrightText: 2022 The TracTicketMSTeamsDispatcherPlugin Authors
#
# SPDX-License-Identifier: LGPL-2.1-or-later

import datetime
import re
from dataclasses import asdict, dataclass, field
from json import dumps


@dataclass
class Webhook:
    id: int
    name: str
    url: str
    type: str


@dataclass
class PayloadBase:
    def json(self):
        return dumps(asdict(self))

    @classmethod
    def from_dict(cls, dictonary):
        """
        This is pretty ugly but it should do the trick for this usecase.
        We iterate over all the keys of the dict we pass to the function and
        if the key is in the dataclass fields we try to figure out the type
        of the dataclass field and add the key, value to the result dict.
        to get all the kwargs for returning an instance of the class we
        iterate over the dataclass field keys again and add missing key, value
        pairs to the result dict.

        NOTE:
        this will work for simple cases we dont wanna figure out if the dict
        has values like  lists or another dict!!!
        """
        result = {}
        for key in dictonary.keys():
            if key in cls.__dataclass_fields__.keys():
                result[key] = cls.__dataclass_fields__[key].type(dictonary[key])
        for key in cls.__dataclass_fields__.keys():
            if not key in result.keys():
                result[key] = cls.__dataclass_fields__[key]
        return cls(**result)

    def __str__(self) -> str:
        parts = re.split("(?<=.)(?=[A-Z])", self.__class__.__name__)
        return " ".join(parts)

    def build_dict_from_ticket(self, ticket, presets):
        _temp_dict = {}
        for key in self.__dataclass_fields__.keys():
            _ = getattr(self, key)
            if "id" in key:
                continue
            if isinstance(_, bool):
                _temp_dict.update({key: bool(_)})
                continue
            if isinstance(_, int):
                _ = [p.name for p in presets if _ == p.id][0].split("_")[-1].lower()
                _ = ticket[_]
                if isinstance(_, datetime.datetime):
                    _ = _.strftime("%d.%m.%Y %H:%M")
                _temp_dict.update({key: _})
                continue
                continue
            _temp_dict.update({key: _})
        return _temp_dict

    def _get_value_by_key_from_ticket(self, key: str, ticket):
        """
        Helper to extract a ticket value by passing in a payload placesholder key.
        If we can't get a value then we return an empty string.
        """
        _prefix = key.name.split("_")[0].lower()
        _key = key.name.split("_")[-1].lower()
        _values = ticket.values
        try:
            if _prefix == "ticket":
                return _values[_key]
        except:
            return ""


@dataclass
class PayloadValue(PayloadBase):
    id: int
    name: str


@dataclass
class TeamsFact(PayloadBase):
    id: int
    section_id: int
    name: str
    value: int


@dataclass
class TeamsSection(PayloadBase):
    id: int
    payload_id: int
    activityTitle: int
    activitySubtitle: int
    activityImage: str
    facts: list[TeamsFact]
    markdown: bool


@dataclass
class TeamsPayload(PayloadBase):
    id: int
    webhook_type: int
    themeColor: str
    summary: int
    type: int
    sections: list[TeamsSection]


@dataclass
class DiscordEmbed(PayloadBase):
    title: str
    description: str


@dataclass
class DiscordPayload(PayloadBase):
    content: str
    username: str
    embeds: list[DiscordEmbed]


@dataclass
class DiscordChangedPayload(DiscordPayload):
    ...
