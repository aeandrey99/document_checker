#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Пакет общих компонентов интерфейса
"""

from .tooltips import create_tooltip, ToolTip
from .utils import UIUtils
from .panels import PanelsBuilder

__all__ = [
    'create_tooltip',
    'ToolTip',
    'UIUtils',
    'PanelsBuilder',
]