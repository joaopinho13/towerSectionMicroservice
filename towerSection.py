#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 17 16:09:38 2023

@author: joao
"""

class TowerSection:
    
    def __init__(self, section_id, length):
        self.section_id = section_id
        self.length = length
        self.shells = []

    def __str__(self):
        return 'Tower Section ID: {}, lenght = {}'.format(self.section_id, self.length)
    
    def add_shell(self, shell):
        self.shells.append(shell)
    
    def get_shell_information(self):
        return self.shells
    
    


if __name__ == '__main__':
    tower = TowerSection(3, 13)
    print(tower)