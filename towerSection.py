#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 17 16:09:38 2023

@author: joao
"""

class TowerSection:
    def __init__(self, section_id):
        self.section_id = section_id
    
    def __str__(self):
        return 'Tower Section ID: {}'.format(self.section_id)


if __name__ == '__main__':
    tower = TowerSection(3)
    print(tower)