from trac.admin import IAdminPanelProvider
from trac.core import Component, implements
from trac.env import IEnvironmentSetupParticipant
from trac.util.translation import _
from trac.web.chrome import ITemplateProvider, add_warning


class TicketTeamDispatcherAdmin(Component):
    """Provides functions related to registration
    """
    implements(IAdminPanelProvider, IEnvironmentSetupParticipant,
               ITemplateProvider)

    # IEnvironmentSetupParticipant methods

    def environment_created(self):
        self.upgrade_environment()

    def environment_needs_upgrade(self, db=None):
        return 'ttmsd' not in self.config['ticket-custom']

    def upgrade_environment(self, db=None):
        self.config.set('ticket-custom', 'ttmsd', 'checkbox')
        self.config.set('ticket-custom', 'ttmsd.label', 'Notify MS Teams')
        self.config.set('ticket-custom', 'ttmsd.value', 1)
        self.config.save()

    # IAdminPanelProvider methods

    def get_admin_panels(self, req):
        #if 'TICKET_ADMIN' in req.perm:
        yield 'ticket', 'Ticket System', 'ttmsd', 'MS Teams Dispatcher'

    def render_admin_panel(self, req, category, page, path_info):
        #req.perm.require('TICKET_ADMIN')

        #users = UserManager(self.env).get_active_users()
        web_hook = self.get_web_hook()


        return 'msteams_dispatcher_admin.html', {
            'web_hook': web_hook,
        }

    # INavigationContributor methods

    def get_templates_dirs(self):
        from pkg_resources import resource_filename
        return [resource_filename(__name__, 'templates')]

    def get_htdocs_dirs(self):
        return []

    # Internal methods

    def get_web_hook(self):
        return self.config.get('msteams-dispatcher', 'web_hook')
