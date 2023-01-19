<!--
SPDX-FileCopyrightText: 2022 The TracTicketMSTeamsDispatcherPlugin Authors

SPDX-License-Identifier: LGPL-2.1-or-later
-->

TracTicketMSTeamsDispatcher
============================


This is a work in progress, the plugin is in a state of development and is more or less a playground for myself to get an feeling for Trac Plugin Development.

If you are a someone who wants to help with this just send me a message.

**_NOTE:_ the code is tested on a Trac 1.5.x so it will work with python 3 but since I use features like F-Strings it wont with python 2.x out of the box!**

 install
 --------

  - clone repo or download the zip archive

      ``` $ git clone https://github.com/rosjat/TracTicketMSTeamsDispatcherPlugin.git```

  - build a python egg

       ``` $ python setup.py bdist_egg ```

  - copy the egg file in you trac projects plugins folder

  - install it in site-packages with pip (you might use a venv when using this version). The example assumes that you are in the cloned directory.

      ``` $ pip install . ```

  - reload trac

trac.ini settings
-------------------

 the Plugin will create a section called  `[msteams-dispatcher]` and create  variables `web_hook_x.name`, `web_hook_x.url`, `web_hook_x.type` under it. Where name is a pretty name displayed in the admin panel, url is the web hook url and type will be an identifier for the future were it will be possible to send payloads to other services like discord. the x will be replaced by a number like `web_hook_1.name` this way we can store more then one web hook in th furture.

 Also created under `[ticket-custom]` will be:

 - tmsd = checkbox
 - ttmsd.label = Notify MS Teams
 - ttmsd.value = 1

 admin settings
 -------------------

 there will be a section under Plugins to enable/disable the plugin. If enabled you get a subsection `MS Teams Dispatcher` under section `Ticket`.

 In `MS Teams Dispatcher` you can set a Value for the `web_hook` and save it.

 TODO / Features
 ----------------
 - Editable Templates for the webhook payload (still no really clue how to do it in a usable way lol)
 - adding localization support for the payloads
 - making the ship off of payloads async (dont know if this is possible)
 - structure the package a little better
 - adding some typing
