#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created by caio on 05/01/16.
"""

import os
import glob

# Allow "import services.models.*"
services = glob.glob(os.path.dirname(__file__)+"/*.py")
__all__ = [ os.path.basename(f)[:-3] for f in services]