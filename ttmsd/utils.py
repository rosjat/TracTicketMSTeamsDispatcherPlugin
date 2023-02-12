# coding: utf-8

# Copyright (C) 2023 by Markus Rosjat<markus.rosjat@gmail.com>
# SPDX-FileCopyrightText: 2022 The TracTicketMSTeamsDispatcherPlugin Authors
#
# SPDX-License-Identifier: LGPL-2.1-or-later

from ttmsd.model import PayloadValue, TeamsFact, TeamsPayload, TeamsSection, Webhook


def setup_db_payload_values(env):
    with env.db_query as db:
        return [
            PayloadValue(id, name)
            for id, name in db("SELECT id, name FROM ttmsd_payload_values")
        ]


def setup_db_payload_types(env):
    with env.db_query as db:
        return [
            PayloadValue(id, name)
            for id, name in db("SELECT id, name FROM ttmsd_payload_types")
        ]


def setup_db_webhook_types(env):
    with env.db_query as db:
        return [
            PayloadValue(id, name)
            for id, name in db("SELECT id, name FROM ttmsd_webhook_types")
        ]


def get_payload_value_from_db_by_id(env, id):
    with env.db_query as db:
        return (
            [
                name
                for name in db(f"SELECT name FROM ttmsd_payload_values WHERE id={id};")
            ][0][0]
            .split("_")[1]
            .lower()
        )


def get_webhook_id_from_db(env, webhook):
    with env.db_query as db:
        webhooks = [
            id for id in db(f"SELECT id FROM ttmsd_webhooks WHERE id={webhook.id};")
        ]
        if len(webhooks) == 1:
            return webhooks[0]
    return 0


def get_webhooks_from_db(env):
    with env.db_query as db:
        webhooks = [
            Webhook(id, name, url, _type)
            for id, name, url, _type in db(
                "SELECT id, name, url, type FROM ttmsd_webhooks;"
            )
        ]
        return webhooks


def get_webhooks_from_db_by_type(env, type_id):
    with env.db_query as db:
        webhooks = [
            Webhook(id, name, url, _type)
            for id, name, url, _type in db(
                f"SELECT id, name, url, type FROM ttmsd_webhooks WHERE type={type_id};"
            )
        ]
    return webhooks


def insert_webhook_in_db(env, webhook):
    with env.db_transaction as db:
        db(
            f"INSERT INTO ttmsd_webhooks (name,url,type) VALUES ('{webhook.name}','{webhook.url}',{webhook.type});"
        )


def update_webhook_in_db(env, webhook):
    with env.db_transaction as db:
        db(
            f"UPDATE ttmsd_webhooks SET name='{webhook.name}',url='{webhook.url}',type={webhook.type} WHERE id={webhook.id};"
        )


def delete_webhook_in_db(env, webhook):
    with env.db_transaction as db:
        db(f"DELETE FROM ttmsd_webhooks WHERE id={webhook.id};")


def delete_webhook_by_id_in_db(env, id):
    with env.db_transaction as db:
        db(f"DELETE FROM ttmsd_webhooks WHERE id={id};")


def update_webhooks_in_db(env, webhooks):
    for webhook in webhooks:
        if get_webhook_id_from_db(env, webhook) == 0:
            insert_webhook_in_db(env, webhook)
        else:
            update_webhook_in_db(env, webhook)


def insert_payload_in_db_from_payload(env, payload):
    with env.db_transaction as db:
        db(
            f"INSERT INTO ttmsd_payloads (color,summary,type,webhook_id) VALUES ('{payload.themeColor}',{payload.summary},{payload.type},{payload.webhook_type});"
        )


def insert_section_in_db_from_payload(env, section):
    with env.db_transaction as db:
        db(
            f"INSERT INTO ttmsd_sections (title,subtitle,image_url,payload_id) VALUES ({section.activityTitle},{section.activitySubtitle},'{section.activityImage}',{section.payload_id});"
        )


def insert_fact_in_db_from_payload(env, fact):
    with env.db_transaction as db:
        db(
            f"INSERT INTO ttmsd_facts (name,value,section_id) VALUES ('{fact.name}',{fact.value},{fact.section_id});"
        )


def update_fact_in_db_from_payload(env, fact):
    with env.db_transaction as db:
        db(
            f"UPDATE ttmsd_facts SET name='{fact.name}', value={fact.value} WHERE id={fact.id} AND section_id={fact.section_id};"
        )


def update_section_in_db_from_payload(env, section):
    with env.db_transaction as db:
        db(
            f"UPDATE ttmsd_sections SET title={section.activityTitle}, subtitle={section.activitySubtitle}, image_url='{section.activityImage}' WHERE id={section.id} AND payload_id={section.payload_id};"
        )


def update_payload_in_db_from_payload(env, payload):
    with env.db_transaction as db:
        db(
            f"UPDATE ttmsd_payloads SET color='{payload.themeColor}', summary={payload.summary},type={payload.type}, webhook_id={payload.webhook_type} WHERE id={payload.id};"
        )


def update_db_from_payload(env, payload):
    with env.db_transaction as db:
        if payload.id == 0:
            insert_payload_in_db_from_payload(env, payload)
        else:
            update_payload_in_db_from_payload(env, payload)
        for section in payload.sections:
            if section.id == 0:
                insert_section_in_db_from_payload(env, section)
            else:
                update_section_in_db_from_payload(env, section)
            for fact in section.facts:
                if fact.id == 0:
                    insert_fact_in_db_from_payload(env, fact)
                    continue
                update_fact_in_db_from_payload(env, fact)


def update_db_from_payloads(env, payloads):
    for payload in payloads:
        update_db_from_payload(env, payload)


def get_payloads_from_db(env):
    return get_payloads_from_db_by_type(env)


def get_payloads_from_db_by_type(env, type_id=0):
    _payload_where = f""
    if type_id > 0:
        _payload_where = f"WHERE type={type_id}"
    _payload_query = f"SELECT id, color, summary, type, webhook_id FROM ttmsd_payloads {_payload_where};"
    with env.db_query as db:
        payloads = [
            TeamsPayload(id, webhook_id, color, summary, _type, [])
            for id, color, summary, _type, webhook_id in db(_payload_query)
        ]
        sections = [
            TeamsSection(id, payload_id, tile, subtitle, image_url, [], True)
            for id, payload_id, tile, subtitle, image_url in db(
                "SELECT id, payload_id, title, subtitle, image_url FROM ttmsd_sections;"
            )
        ]
        facts = [
            TeamsFact(id, section_id, name, value)
            for id, section_id, name, value in db(
                "SELECT id, section_id, name, value FROM ttmsd_facts;"
            )
        ]
    for fact in facts:
        for section in sections:
            if fact.section_id == section.id:
                section.facts.append(fact)
    for section in sections:
        for payload in payloads:
            if section.payload_id == payload.id:
                payload.sections.append(section)
    return payloads


def get_payloads_from_request(req):
    def _add_sections(payload):
        for _payload in payloads:
            parts = _payload.split("_")
            if len(parts) == 5:
                _section_id = int(parts[-1])
                if not _section_id in _payload_dict["sections"].keys():
                    _payload_dict["sections"].update({_section_id: {}})
                _payload_dict["sections"][_section_id].update(
                    {parts[-2]: payloads[_payload]}
                )
        _ = [
            [v[s].update({"facts": {}}) for s in v]
            for k, v in _payload_dict.items()
            if k == "sections"
        ]
        _ = [
            [
                TeamsSection(
                    int(sk),
                    payload.id,
                    int(sv["activityTitle"]),
                    int(sv["activitySubtitle"]),
                    sv["activityImage"],
                    [],
                    bool(sv["markdown"]),
                )
                for sk, sv in v.items()
            ]
            for k, v in _payload_dict.items()
            if k == "sections"
        ]
        payload.sections = _[0]

    def _add_facts(payload):
        for _payload in payloads:
            parts = _payload.split("_")
            if len(parts) == 6:
                if parts[-1].startswith("n"):
                    _fact_id = parts[-1]
                else:
                    _fact_id = int(parts[-1])
                _section_id = int(parts[-2])
                _ = _payload_dict["sections"][_section_id]
                if not _fact_id in _["facts"].keys():
                    _["facts"].update({_fact_id: {}})
                _["facts"][_fact_id].update({parts[-3]: payloads[_payload]})
        _ = [
            TeamsFact(k, _section_id, **v)
            if isinstance(k, int)
            else TeamsFact(0, _section_id, **v)
            for k, v in _["facts"].items()
        ]
        for f in _:
            _ = [s.facts.append(f) for s in payload.sections if s.id == f.section_id]

    def _create_payload():
        _payload_type = 0
        for payload in payloads:
            parts = payload.split("_")
            if parts[2] == "payloadtype":
                _payload_type = int(payloads[payload])
            if len(parts) == 3:
                _payload_id = int(parts[1])
                if not "id" in _payload_dict.keys():
                    _payload_dict.update({"id": _payload_id})
                _payload_dict.update({parts[-1]: payloads[payload]})
        _payload_dict.update({"sections": {}})
        _ = TeamsPayload(
            _payload_id,
            int(_payload_dict["webhooktype"]),
            _payload_dict["themeColor"][1:],
            int(_payload_dict["summary"]),
            int(_payload_type),
            [],
        )
        _add_sections(_)
        _add_facts(_)
        return _

    _ids = set(
        [
            int(arg.split("_")[1])
            for arg in req.args
            if arg.startswith("teams_") and arg.split("_")[1] != "0"
        ]
    )

    _temp = []
    for id in _ids:
        _payload_dict = {}
        payloads = {
            arg: req.args[arg]
            for arg in req.args
            if arg.startswith("teams_") and int(arg.split("_")[1]) == id
        }
        _temp.append(_create_payload())
    return _temp


def get_configuration_options(config, section) -> list[Webhook]:
    result = {}
    for option, value in config.options(section):
        parts = option.split(".")
        # this will change when we add more web hook types like discord
        # you can do it by hand in the config already but the dropdown
        # values will mess up if you change the values and save it ;)
        if len(parts) != 2:
            raise NotImplementedError("Options cant have only two parts!")
        wh_nr = int(parts[0].split("_")[-1:][0])
        if wh_nr in result.keys():
            result[wh_nr].update({parts[1]: value})
        else:
            result[wh_nr] = {parts[1]: value}
    return [Webhook(id=key, **result[key]) for key in result.keys()]


def get_web_hooks_from_dict(web_hook_dict):
    result = {}
    for key in web_hook_dict.keys():
        parts = key.split("_")
        wh_nr = int(parts[-1:][0])
        if wh_nr in result.keys():
            result[wh_nr].update({parts[2]: web_hook_dict[key]})
        else:
            result[wh_nr] = {parts[2]: web_hook_dict[key]}
    return [Webhook(id=key, **result[key]) for key in result.keys()]
