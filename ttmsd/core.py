# coding: utf-8

# Copyright (C) 2023 by Markus Rosjat<markus.rosjat@gmail.com>
# SPDX-FileCopyrightText: 2022 The TracTicketMSTeamsDispatcherPlugin Authors
#
# SPDX-License-Identifier: LGPL-2.1-or-later

from trac.core import Component, TracError, implements
from trac.db import Column, Table
from trac.db.api import DatabaseManager
from trac.env import IEnvironmentSetupParticipant


class TicketTeamDispatcher(Component):
    """This must be enabled for the plugin to work!"""

    implements(IEnvironmentSetupParticipant)

    required = True
    _section = "msteams-dispatcher"
    _db_schema_version = 1
    _db_plugin = "ttmsd_version"
    _db_schema = [
        Table("ttmsd_webhooks", key="id")[
            Column("id", type="int", auto_increment=True),
            Column("name", type="text"),
            Column("url", type="text"),
            Column("type", type="int"),
        ],
        Table("ttmsd_payloads", key=("id", "webhook_id"))[
            Column("id", type="int", auto_increment=True),
            Column("webhook_id", type="int"),
            Column("color", type="text"),
            Column("summary", type="int"),
            Column("type", type="int"),
        ],
        Table("ttmsd_sections", key=("id", "payload_id"))[
            Column("id", type="int", auto_increment=True),
            Column("payload_id", type="int"),
            Column("title", type="int"),
            Column("subtitle", type="int"),
            Column("image_url", type="text"),
        ],
        Table("ttmsd_facts", key=("id", "section_id"))[
            Column("id", type="int", auto_increment=True),
            Column("section_id", type="int"),
            Column("name", type="text"),
            Column("value", type="int"),
        ],
        Table("ttmsd_payload_types", key=("id"))[
            Column("id", type="int", auto_increment=True),
            Column("name", type="text"),
        ],
        Table("ttmsd_payload_values", key=("id"))[
            Column("id", type="int", auto_increment=True),
            Column("name", type="text"),
        ],
        Table("ttmsd_webhook_types", key=("id"))[
            Column("id", type="int", auto_increment=True),
            Column("name", type="text"),
        ],
    ]
    _db_default_table_data = (
        (
            "ttmsd_webhook_types",
            ["name"],
            (
                ("MS Teams",),
                ("Discord",),
            ),
        ),
        (
            "ttmsd_payload_types",
            ["name"],
            (
                ("create",),
                ("change",),
                ("delete",),
                ("comment_modify",),
                ("change_delete",),
            ),
        ),
        (
            "ttmsd_payload_values",
            ["name"],
            (
                ("TICKET_SUMMARY",),
                ("TICKET_REPORTER",),
                ("TICKET_OWNER",),
                ("TICKET_DESCRIPTION",),
                ("TICKET_TYPE",),
                ("TICKET_STATUS",),
                ("TICKET_PRIORITY",),
                ("TICKET_MILESTONE",),
                ("TICKET_COMPONENT",),
                ("TICKET_SEVERITY",),
                ("TICKET_RESOLUTION",),
                ("TICKET_KEYWORDS",),
                ("TICKET_CC",),
                ("TICKET_TIME",),
                ("TICKET_CHANGETIME",),
                ("TICKET_ESTIMATEDHOURS",),
                ("TICKET_TOTALHOURS",),
            ),
        ),
        ("ttmsd_webhooks", ("id", "name", "url", "type"), ((1, "", "", 1),)),
        (
            "ttmsd_payloads",
            ("webhook_id", "color", "summary", "type"),
            ((1, "000000", 1, 1),),
        ),
        (
            "ttmsd_sections",
            ("payload_id", "title", "subtitle", "image_url"),
            (
                (1, 4, 3, ""),
                (2, 4, 3, ""),
            ),
        ),
        (
            "ttmsd_facts",
            ("section_id", "name", "value"),
            (
                (1, "", 14),
                (1, "", 14),
                (2, "", 14),
                (2, "", 14),
            ),
        ),
    )

    def environment_created(self):
        pass

    def environment_needs_upgrade(self, db=None):
        schema_ver = self.get_schema_version()
        if schema_ver == self._db_schema_version:
            return False
        elif schema_ver > self._db_schema_version:
            raise TracError(
                _(
                    "A newer plugin version has been installed "
                    "before, but downgrading is unsupported."
                )
            )
        self.log.info(
            f"TracTicketMSTeamsDispatcher database schema version is {schema_ver}, should be {self._db_schema_version}"
        )
        return True

    def upgrade_environment(self, db=None):
        """Each schema version should have its own upgrade module, named
        upgrades/dbN.py, where 'N' is the version number (int).
        """
        dbm = DatabaseManager(self.env)
        schema_ver = self.get_schema_version()

        with self.env.db_transaction as db:
            if dbm.get_database_version(self._db_plugin) == 0:
                dbm.create_tables(self._db_schema)
                dbm.insert_into_tables(self._db_default_table_data)
                dbm.set_database_version(self._db_schema_version, self._db_plugin)
            else:
                dbm.upgrade(self._db_schema_version, self._db_plugin, "ttmsd.upgrades")

    def get_db_version(self):
        for (version,) in self.env.db_query(
            f"SELECT value FROM system WHERE name='{self._db_plugin}'"
        ):
            return int(version)

    def get_schema_version(self):
        """Return the current schema version for this plugin."""
        version = self.get_db_version()
        if not version:
            tables = self._get_tables()
            if self._db_plugin in tables:
                self.env.log.debug(
                    "TracTicketMSTeamsDispatcher needs to register schema version"
                )
                return 1
            return 0
        return version or 0

    # Internal methods

    def _get_tables(self):
        """Code from TracMigratePlugin by Jun Omae (see tracmigrate.admin)."""
        dburi = self.config.get("trac", "database")
        if dburi.startswith("sqlite:"):
            sql = """
                SELECT name FROM sqlite_master
                WHERE type='table' AND NOT name='sqlite_sequence'
                """
        elif dburi.startswith("postgres:"):
            sql = """
                SELECT tablename FROM pg_tables
                WHERE schemaname = ANY (current_schemas(false))
                """
        elif dburi.startswith("mysql:"):
            sql = "SHOW TABLES"
        else:
            raise TracError('Unsupported database type "%s"' % dburi.split(":")[0])
        with self.env.db_transaction as db:
            cursor = db.cursor()
            cursor.execute(sql)
            return sorted(name for name, in cursor.fetchall())
