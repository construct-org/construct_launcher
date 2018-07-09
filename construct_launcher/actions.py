# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

__all__ = [
    'BaseLauncher',
    'new_launcher',
]

from construct import Action
from construct.utils import platform
from construct_launcher.constants import (
    SETUP_LAUNCH,
    BEFORE_LAUNCH,
    LAUNCH,
    AFTER_LAUNCH,
    DEFAULT_SOFTWARE_ICON
)
from cpenv.utils import preprocess_dict, dict_to_env


class BaseLauncher(Action):

    label = 'Base Launch'
    identifier = 'launch'
    description = 'Launch an application'
    priorities = [SETUP_LAUNCH, BEFORE_LAUNCH, LAUNCH, AFTER_LAUNCH]

    # These are set by new_launcher and used by launcher tasks to launch
    # the application
    icon = None
    default_workspace = None
    path = None
    args = None
    env = None
    host = None

    @staticmethod
    def available(ctx):
        return ctx.task


def new_launcher(name, data):
    '''Create a new :class:`Action` type to launch an application'''

    label = data.get('label', 'Launch ' + name.title())

    identifier = data.get('identifier', 'launch.' + name)
    if not identifier.startswith('launch'):
        identifier = 'launch.' + identifier

    # Preprocess env dict
    # expands variables
    # extracts platform specific env vars
    app_env = data.get('env', {})
    app_env = dict_to_env(preprocess_dict(app_env))

    cmd = data['cmd'][platform]
    action = type(
        'Launch' + name.title(),
        (BaseLauncher,),
        dict(
            label=label,
            name=name,
            default_workspace=data.get('default_workspace', None),
            identifier=identifier,
            description=data.get('description', label),
            icon=data.get('icon', DEFAULT_SOFTWARE_ICON),
            path=cmd['path'],
            args=cmd['args'],
            env=app_env,
            host=data['host'],
        )
    )
    return action
