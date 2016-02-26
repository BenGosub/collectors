# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import subprocess


for name in os.listdir(os.path.dirname(__file__)):
    name, ext = name.split('.')
    if ext != 'yml':
        continue
    command = ''
    command += 'tutum stack inspect scraper-{name} || '
    command += 'tutum stack create --sync -f stacks/{name}.yml -n scraper-{name} && '
    command += 'tutum stack update --sync -f stacks/{name}.yml scraper-{name}'
    command = command.format(name=name)
    subprocess.call(command, shell=True)
