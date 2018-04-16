# -*- coding: utf-8 -*-
from __future__ import absolute_import

__all__ = [
    'setup_app',
    'build_app_env',
    'launch_app'
]

import os
import subprocess
from construct import api
from construct.errors import Fail, Skip, Disable
from construct.types import Namespace
from construct.tasks import (
    task,
    pass_context,
    requires,
    success,
    returns,
    store,
    params,
    pass_args,
    available,
    artifact
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
        task=ctx.task,
        workspace=ctx.workspace,
        default_workspace=action.default_workspace,
    )
    return app


@task(priority=SETUP_LAUNCH)
@pass_context
@requires(success('setup_app'))
@params(store('app'))
@available(lambda ctx: ctx.task and not ctx.workspace)
@returns(artifact('workspace'))
def setup_workspace(ctx, app):
    '''Setup a workspace for the current task'''

    workspace = app.task.workspaces.name(app.host).one()
    if not workspace and not app.default_workspace:
        raise Disable('Could not find workspace for %s' % app.host)

    artifact = False
    if not workspace:
        path_template = api.get_path_template('workspace')
        template = api.get_template(app.default_workspace, 'workspace')

        path = path_template.format(dict(
            task=app.task.path,
            workspace=app.host
        ))

        if os.path.exists(path):
            import fsfs
            workspace = fsfs.get_entry(path)
            workspace.tag(*template.tags)
            workspace.write(**template.read())
        else:
            workspace = template.copy(path)

        artifact = True

    ctx.workspace = workspace
    app.cwd = workspace.path

    if artifact:
        return workspace


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
