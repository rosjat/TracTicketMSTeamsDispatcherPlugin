<!--
SPDX-FileCopyrightText: 2022 The TracTicketMSTeamsDispatcherPlugin Authors

SPDX-License-Identifier: LGPL-2.1-or-later
-->

TracTicketMSTeamsDispatcher
============================

**_NOTE:_ the code is tested on a Trac 1.5.x so it will work with python 3 but since I use features like F-Strings it wont with python 2.x out of the box!**

The plugin has the intention to provide a way to send information about the creation or the change of a ticket to a service like MS Teams via a webhook.
That said the name points out it's meant to work only for ms teams but that's not entirely true since we can send off information to any kind of webhook that expects a payload.
Of course we need to define a well-formed payload for every service and so we started out with ms teams. In the future it might be possible to send a payload to discord or some other fanzy web api.

**_HINT:_** a proof of concept payload for discord is already in the code but not really useful at this stage.

Lets get back to what we can do at this point. After the installation of the plugin you should get a new plugin under the plugins section of the trac adminstration. If we enable the plugin we get a new administration page under the ticket system section called `MS Teams Dispatcher`. There we can define our first webhook and save it. As soon as we got this we can use the checkbox `Notify MS Teams` in the ticket properties to send off a payload when a ticket is created or changed. To see what values are set in the trac.ini and the admin page read the sections further down in this document.



 install
 --------

  - clone repo or download the zip archive

      ``` $ git clone https://github.com/rosjat/TracTicketMSTeamsDispatcherPlugin.git```

  - build a python egg

       ``` $ python setup.py bdist_egg ```

  - copy the egg file in you trac projects plugins folder

  - install it in site-packages with pip (you might use a venv when using this version). The example assumes that you are in the cloned directory.

      ``` $ pip install . ``` or from pypi ``` $ pip install TracTicketMSTeamsDispatcher ```


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

 In `MS Teams Dispatcher` you can set a values for a web hook and save it. You can also add or delete a webhook if you dont want to send payloads to it.

 TODO / Features
 ----------------
 - Editable Templates for the webhook payload (still no really clue how to do it in a usable way lol)
 - adding localization support for the payloads
 - making the ship off of payloads async (dont know if this is possible)
 - structure the package a little better
 - adding some typing
