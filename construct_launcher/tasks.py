# -*- coding: utf-8 -*-
from __future__ import absolute_import

__all__ = [
    'setup_app',
    'build_app_env',
    'launch_app'
]

import os
import subprocess
from construct.types import Namespace
from construct.tasks import (
    task,
    pass_context,
    requires,
    success,
    returns,
    store,
    params,
    kwarg,
    pass_args
)
from construct_launcher.constants import SETUP_LAUNCH, LAUNCH


@task(priority=SETUP_LAUNCH)
@pass_context
@pass_args
@returns(store('app'))
def setup_app(ctx, args):
    '''Setup application item to launch'''

    entry = ctx.get_deepest_entry()
    action = ctx.action
    app = Namespace(
        path=action.path,
        args=list(action.args) + list(args),
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
def build_app_env(ctx, app):
    '''Build application environment'''

    ctx_env = ctx.to_env_dict(exclude=['host'])
    ctx_env['CONSTRUCT_HOST'] = app.host
    app.env.update(ctx_env)


@task(priority=LAUNCH)
@requires(success('build_app_env'))
@params(store('app'))
def launch_app(app):
    '''Launch application'''

    cmd = [app.path] + app.args
    cwd = app.cwd
    env = dict(os.environ.data)
    env.update(app.env)

    subprocess.Popen(cmd, env=env, cwd=cwd)
