# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

__all__ = [
    'SETUP_LAUNCH',
    'BEFORE_LAUNCH',
    'LAUNCH',
    'AFTER_LAUNCH',
    'new_launch_action',
    'setup_app',
    'launch_app',
]

import os
import subprocess
from construct import (
    Action,
    types,
    to_env_dict,
    task,
    requires,
    success,
    store,
    pass_context,
    params,
    returns
)


SETUP_LAUNCH = types.Priority(0, 'Setup Launch', 'Setup app')
BEFORE_LAUNCH = types.Priority(1, 'Before Launch', 'Before app launch')
LAUNCH = types.Priority(2, 'Launch', 'Launch app')
AFTER_LAUNCH = types.Priority(3, 'After Launch', 'After app launch')


class BaseLauncher(Action):

    label = 'Base Launch'
    identifier = 'launch'
    description = 'Launch an application'
    project_key = 'apps'
    app_key = None
    priorities = [SETUP_LAUNCH, BEFORE_LAUNCH, LAUNCH, AFTER_LAUNCH]
    parameters = {}

    @staticmethod
    def available(ctx):
        return ctx.project is not None

    @classmethod
    def register(cls, cons):
        cons.action_hub.register(cls)
        cons.action_hub.connect(cls.identifier, setup_app)
        cons.action_hub.connect(cls.identifier, build_app_env)
        cons.action_hub.connect(cls.identifier, launch_app)

    @classmethod
    def unregister(cls, cons):
        cons.action_hub.disconnect(cls.identifier, launch_app)
        cons.action_hub.disconnect(cls.identifier, build_app_env)
        cons.action_hub.disconnect(cls.identifier, setup_app)
        cons.action_hub.unregister(cls)


def new_launch_action(ctx, name, data):
    '''Create a new :class:`Action` type to launch an application'''

    cmd = data['cmd'][ctx.platform]
    icon = data.get('icon', None)
    if icon and icon.startswith('.'):
        icon = os.path.join(ctx.project.path, icon.lstrip('./\\'))

    action = type(
        'Launch' + name.title(),
        (BaseLauncher,),
        dict(
            label='Launch ' + name.title(),
            name=name,
            identifier=data.get('identifier', 'launch.' + name),
            description=data.get('description', 'Launch ' + name.title()),
            icon=icon,
            path=cmd['path'],
            args=cmd['args'],
            env=data.get('env', {}),
            host=data['host'],
        )
    )
    return action


@task(priority=SETUP_LAUNCH)
@pass_context
@returns(store('app'))
def setup_app(ctx):
    '''Setup application item to launch'''

    entry = ctx.get_deepest_entry()
    action = ctx.action_type
    app = dict(
        path=action.path,
        args=list(action.args),
        name=action.name,
        env=dict(action.env),
        cwd=entry.path,
        host=action.host,
    )
    return app


@task(priority=SETUP_LAUNCH)
@requires(success('setup_app'))
@pass_context
@params(store('app'))
@returns(store('app'))
def build_app_env(ctx, app):
    '''Build application environment'''

    ctx_env = to_env_dict(ctx)
    ctx_env['CONSTRUCT_HOST'] = app['host']
    app['env'].update(ctx_env)
    return app


@task(priority=LAUNCH)
@requires(success('build_app_env'))
@params(store('app'))
def launch_app(app):

    cmd = [app['path']] + app['args']
    cwd = app['cwd']
    env = dict(os.environ.data)
    env.update(app['env'])

    subprocess.Popen(cmd, env=env, cwd=cwd)
