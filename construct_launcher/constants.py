# -*- coding: utf-8 -*-
from __future__ import absolute_import
__all__ = [
    'SETUP_LAUNCH',
    'BEFORE_LAUNCH',
    'LAUNCH',
    'AFTER_LAUNCH',
    'DEFAULT_SOFTWARE_ICON'
]
from construct import types


SETUP_LAUNCH = types.Priority(0, 'Setup Launch', 'Setup app')
BEFORE_LAUNCH = types.Priority(1, 'Before Launch', 'Before app launch')
LAUNCH = types.Priority(2, 'Launch', 'Launch app')
AFTER_LAUNCH = types.Priority(3, 'After Launch', 'After app launch')
DEFAULT_SOFTWARE_ICON = 'software_icon.svg'  # TODO: make this icon
