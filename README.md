<!--
SPDX-FileCopyrightText: 2022 The TracTicketMSTeamsDispatcherPlugin Authors

SPDX-License-Identifier: LGPL-2.1-or-later
-->

# TracTicketMSTeamsDispatcher


**_NOTE:_ the code is tested on a Trac 1.5.x so it will work with python 3 but since I use features like F-Strings it wont with python 2.x out of the box!**

The plugin has the intention to provide a way to send information about the creation or the change of a ticket to a service like MS Teams via a webhook.
That said the name points out it's meant to work only for ms teams but that's not entirely true since we can send off information to any kind of webhook that expects a payload.
Of course we need to define a well-formed payload for every service and so we started out with ms teams. In the future it might be possible to send a payload to discord or some other fanzy web api.

**_HINT:_** a proof of concept payload for discord is already in the code but not really useful at this stage.

Lets get back to what we can do at this point. After the installation of the plugin you should get a new plugin under the plugins section of the trac adminstration. If we enable the plugin we get a new administration section called `Webhook Dispatcher`. There we can define our first webhook and save it. As soon as we got this we can use the checkbox `Notify MS Teams` in the ticket properties to send off a payload when a ticket is created or changed. To see what values are set in the trac.ini and the admin page read the sections further down in this document. The plugin also adds some new database tables to provide a way to add, edit or delete payloads and payload details.



 ## install
 -------------

  - clone repo or download the zip archive

      ``` $ git clone https://github.com/rosjat/TracTicketMSTeamsDispatcherPlugin.git```

  - build a python egg

       ``` $ python setup.py bdist_egg ```

  - copy the egg file in you trac projects plugins folder

  - install it in site-packages with pip (you might use a venv when using this version). The example assumes that you are in the cloned directory.

      ``` $ pip install . ``` or from pypi ``` $ pip install TracTicketMSTeamsDispatcher ```


  - reload trac

## trac.ini settings
---------------------
 the Plugin will create under `[ticket-custom]`:

 - tmsd = checkbox
 - ttmsd.label = Notify MS Teams
 - ttmsd.value = 1

## Plugin Settings
-----------------
 there will be a section under Plugins to enable/disable the plugin. If enabled you get a section `Webhook Dispatcher` and under this section you will have `Payloads` and `Webhooks` if enabled.


## Webhook Dispatcher Section
------------------------------

### Payloads

 In `Payloads` you can set a values for a various types of payloads and save it. You can also add or delete some `Facts` to a payload.
 For now the plugin only provides payloads for MS Teams but might add payloads for other kinds of services like discord.

 A MS Teams Payload consists of payload values itself, sections that itself have facts. In the frontend you will be able to edit the following values (for now).

 - 2 payloads, one for Ticket create annd one for Ticket change
   - **NOTE:** if you change the payload type of the predefined payloads you might end up not sending payloads on the desired ticket event!!!
 - A paload template consists of
   - a Section(for now)
     - and facts in this section, you could add, delete, change them.
   - payload values can be ticket values or some text values set by the user. All values that need to come from the ticket will be set from a dropdown.

### Webhooks

 In `Webhooks` you can add, edit or delete webhooks. For now we only provide a way to send MS Teams payloads but we can define discord webhooks here too.


 ## TODO / Features
 --------------------
 - more sane documentation in the code
 - adding localization support for the payloads
 - making the ship off of payloads async (dont know if this is possible)
 - structure the package better and code cleanup, there is space for inprovment for sure!
 - adding some typing
