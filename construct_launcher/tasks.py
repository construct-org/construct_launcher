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
from construct.utils import platform
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
from cpenv.utils import dict_to_env, env_to_dict, join_dicts


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
    os_env = env_to_dict(os.environ.data)
    app_env = env_to_dict(app.env)
    env = dict_to_env(join_dicts(os_env, app_env))

    run(cmd, env=env, cwd=cwd)


def run(*args, **kwargs):
    '''On Windows start a detached process in it's own process group.'''

    if platform == 'win':
        create_new_process_group = 0x00000200
        detached_process = 0x00000008
        creation_flags = detached_process | create_new_process_group
        kwargs.setdefault('creationflags', creation_flags)

    kwargs.setdefault('shell', True)
    subprocess.Popen(*args, **kwargs)
