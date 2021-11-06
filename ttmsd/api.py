from trac.config import Option, BoolOption
from trac.core import Component, implements
from trac.ticket.api import ITicketChangeListener
from trac.wiki.model import WikiPage
import requests
import json


def create_payload(ticket_id, values):
    title = "Ticket #%s" % str(ticket_id)
    payload = {
        "@type": "MessageCard",

        "@context": "http://schema.org/extensions",

        "themeColor": "007600",

        "summary": values['summary'],

        "sections": [{
            "activityTitle": title,
            "activitySubtitle": values['component'],
            "activityImage": "https://teamsnodesample.azurewebsites.net/static/img/image5.png",
            "facts": [{
                "name": "Status:",
                "value": values['status']
            }, {
                "name": "Erstellt:",
                "value": values['time'].strftime('%d.%m.%Y %H:%M')
            }, {
                "name": "Kunde:",
                "value": values['component']
            }, {
                "name": "Priority:",
                "value": values['priority']
            }, {
                "name": "Beschreibung:",
                "value": values['description']
            }],
            "markdown": True
        }]
    }
    return json.dumps(payload, indent=4)

def change_payload(ticket_id, values):
    title = "Ticket #%s" % str(ticket_id)
    payload = {
        "@type": "MessageCard",

        "@context": "http://schema.org/extensions",

        "themeColor": "007600",

        "summary": values['summary'],

        "sections": [{
            "activityTitle": title,
            "activitySubtitle": values['component'],
            "activityImage": "https://teamsnodesample.azurewebsites.net/static/img/image5.png",
            "facts": [{
                "name": "Status:",
                "value": values['status']
            }, {
                "name": "Bearbeitet am:",
                "value": values['time'].strftime('%d.%m.%Y %H:%M')
            }, {
                "name": "Kunde:",
                "value": values['component']
            }, {
                "name": "Priority:",
                "value": values['priority']
            }, {
                "name": "Eintrag:",
                "value": values['description']
            }, {
                "name": "Bearbeiter:",
                "value": values['owner']
            }],
            "markdown": True
        }]
    }
    return json.dumps(payload, indent=4)

class TicketMsTeamsNotification(Component):
    implements(ITicketChangeListener)

    web_hook = Option('msteams-dispatcher',
                      'web_hook',
                      doc= 'The URL for a MS Teams Connector')
    def ticket_created(self, ticket):
        notify_ms_teams = ticket.values['ttmsd']
        if notify_ms_teams:
            requests.post(self.web_hook, create_payload(ticket.id, ticket.values))

    def ticket_changed(self, ticket, comment, author, old_values):
        notify_ms_teams = ticket.values['ttmsd']
        if notify_ms_teams:
            requests.post(whook, change_payload(ticket.id, ticket.values))

    def ticket_deleted(self, ticket):
        pass

    def ticket_comment_modified(self, ticket, cdate, author, comment, old_comment):
        pass

    def ticket_change_deleted(self, ticket, cdate, changes):
        pass