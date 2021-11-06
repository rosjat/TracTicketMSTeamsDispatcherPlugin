TracTicketMSTeamsDispatcher
============================

This is a work in progress, the plugin is in a state of development and is more or less a playground for myself to get an feeling for Trac Plugin Development.

If you are a someone who wants to help with this just send me a message.

 install
 --------

  - clone repo or download the zip archive
      
      ``` $ git clone https://github.com/rosjat/TracTicketMSTeamsDispatcherPlugin.git```
      
  - build a python egg
       
       ``` $ python setup.py bdist_egg ```

  - copy the egg file in you trac projects plugins folder 
  - reload trac

trac.ini settings
-------------------

 the Plugin will create a section called  `[msteams-dispatcher]` and create a variable `web_hook` under it.

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

 - Editable Templates for the webhook payload
 
