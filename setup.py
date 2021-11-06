from setuptools import find_packages, setup

PACKAGE = 'TracTicketMSTeamsDispatcher'
PACKAGE_SHORT = 'ttmsd'
VERSION = '0.1'

setup(
    name=PACKAGE,
    version=VERSION,
    packages=[PACKAGE_SHORT],
    package_data={PACKAGE_SHORT: ['templates/*.html']},
    author='Markus Rosjat',
    email='markus.rosjat@gmail.com',
    url='https://github.com/rosjat',
    license='GPLv2 or later',
    description='Send a message on ticket ceation to a MS Teams channel.',
    entry_points = """
        [trac.plugins] 
        %(pkg)s.admin = %(pkg_s)s.admin
        %(pkg)s.api = %(pkg_s)s.api
        """ % {'pkg': PACKAGE, 'pkg_s':PACKAGE_SHORT},
)