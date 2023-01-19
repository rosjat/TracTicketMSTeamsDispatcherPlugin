# coding: utf-8

# Copyright (C) 2023 by Markus Rosjat<markus.rosjat@gmail.com>
# SPDX-FileCopyrightText: 2022 The TracTicketMSTeamsDispatcherPlugin Authors
#
# SPDX-License-Identifier: LGPL-2.1-or-later

from collections import namedtuple

WebHook = namedtuple("WebHook", ["id", "name", "url", "type"])


def get_configuration_options(config, section):
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
    return [WebHook(id=key, **result[key]) for key in result.keys()]


def get_web_hooks_from_dict(web_hook_dict):
    result = {}
    for key in web_hook_dict.keys():
        parts = key.split("_")
        wh_nr = int(parts[-1:][0])
        if wh_nr in result.keys():
            result[wh_nr].update({parts[2]: web_hook_dict[key]})
        else:
            result[wh_nr] = {parts[2]: web_hook_dict[key]}
        # if parts[1] == 'name'
    return [WebHook(id=key, **result[key]) for key in result.keys()]
