#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 18 21:52:22 2023

@author: joao
"""

import towerSectionFinderMicroservice
import os
from flask import Flask

app = Flask(__name__)

if not os.path.isfile('catalogue.db'):
    towerSectionFinderMicroservice.add_tower_section(catalog, section_id, shells)

@app.route('/sections', methods=['POST'])
def hello_world():
    return('Hello World!')

if __name__ == '__main__':
    app.run()