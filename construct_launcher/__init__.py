# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

__title__ = 'construct_launcher'
__description__ = 'Construct Launcher Actions'
__version__ = '0.0.1'
__author__ = 'Dan Bradham'
__email__ = 'danielbradham@gmail.com'
__license__ = 'MIT'
__url__ = 'https://github.com/danbradham/construct_launcher'

from construct_launcher.actions import *


def available(ctx):
    return True


def register(cons):
    '''Register Launch Actions from Project Configuration'''

    ctx = cons.get_context()
    project = ctx.project
    if not project:
        return

    try:
        apps = project.read('apps')
    except KeyError:
        apps = {}

    for name, data in apps.items():
        launch_action = actions.new_launch_action(ctx, name, data)
        launch_action.register(cons)


def unregister(cons):
    '''Unregister Launch Actions'''

    for action in cons.action_hub._actions.values():
        if isinstance(action, BaseLauncher):
            action.unregister(cons)
