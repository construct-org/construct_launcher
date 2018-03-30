# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

__all__ = [
    'BaseLauncher',
    'new_launcher',
]

from construct import Action, types, config
from construct.utils import platform
from construct_launcher.constants import (
    SETUP_LAUNCH,
    BEFORE_LAUNCH,
    LAUNCH,
    AFTER_LAUNCH,
    DEFAULT_SOFTWARE_ICON
)


class BaseLauncher(Action):

    label = 'Base Launch'
    identifier = 'launch'
    description = 'Launch an application'
    priorities = [SETUP_LAUNCH, BEFORE_LAUNCH, LAUNCH, AFTER_LAUNCH]
    parameters = {}

    # These are set by new_launcher and used by launcher tasks to launch
    # the application
    icon = None
    path = None
    args = None
    env = None
    host = None

    @staticmethod
    def available(ctx):
        return ctx.project


def new_launcher(name, data):
    '''Create a new :class:`Action` type to launch an application'''

    label = data.get('label', 'Launch ' + name.title())

    identifier = data.get('identifier', None)
    if identifier and not identifier.startswith('launch'):
        identifier = 'launch.' + identifier
    else:
        identifier = 'launch.' + name

    cmd = data['cmd'][platform]
    action = type(
        'Launch' + name.title(),
        (BaseLauncher,),
        dict(
            label=label,
            name=name,
            identifier=identifier,
            description=data.get('description', label),
            icon=data.get('icon', DEFAULT_SOFTWARE_ICON),
            path=cmd['path'],
            args=cmd['args'],
            env=data.get('env', {}),
            host=data['host'],
        )
    )
    return action
