# -*- coding: utf-8 -*-
from __future__ import absolute_import

__all__ = ['Launcher']

from construct.utils import missing
from construct.extension import Extension, Config
from construct_launcher.tasks import (
    setup_app,
    setup_workspace,
    build_app_env,
    launch_app
)
from construct_launcher.actions import new_launcher


class Launcher(Extension):
    '''Launcher provides Actions configured through the key SOFTWARE in your
    configuration file. Launcher Actions are dynamically generated in
    get_actions, instead of adding them in load. By doing so we can provide
    Actions for the current context and configuration.

    To extend application launching behavior add a task of priority
    BEFORE_LAUNCH(1) or AFTER_LAUNCH(3) to the identifier 'launch.*'.

    Example extension setting an environment variable before launch:

        >>> @task(priority=1)
        ... @params(store('app'))
        ... def before_launch_task(app):
        ...     app.env['HELLO'] = 'WORLD!'

        >>> class MyLauncher(Extension):
        ...     name = 'MyLauncher'
        ...     attr_name = 'my_launcher'
        ...
        ...     def load(self):
        ...         self.add_task('launch.*', build_app_env)

    '''

    name = 'Launcher'
    attr_name = 'launcher'

    # Provides attribute access to construct.config['SOFTWARE']
    software = Config('SOFTWARE')

    def load(self):
        '''Adds tasks that respond to all launch actions.
        These are the core tasks used by the app luancher.'''

        self.add_task('launch.*', setup_app)
        self.add_task('launch.*', setup_workspace)
        self.add_task('launch.*', build_app_env)
        self.add_task('launch.*', launch_app)

    def get_actions(self, ctx=missing):
        '''Instead of adding launch actions in load, we implement get_actions
        to generate new Action instances every time actions are looked up.
        This way we can provide different launch actions per context.
        '''

        actions = {}
        for app_name, app_data in self.software.items():
            action = new_launcher(app_name, app_data)
            actions[action.identifier] = action
        return actions

    def available(self, ctx):
        return ctx.project
