#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 17 10:39:55 2023

@author: joao
"""

class Shell:
    
    def __init__(self, unique_id, shell_id, section_position, height, top_diameter,
                 bot_diameter, thickness, steel_density):
        self.unique_id = unique_id
        self.shell_id = shell_id
        self.section_position = section_position
        self.height = height
        self.top_diameter = top_diameter
        self.bot_diameter = bot_diameter
        self.thickness = thickness
        self.steel_density = steel_density
    
    def __str__(self):
        return'Shell number (ID): {}, section_id: {}, Position: {}, Height: {}, Top diameter: {},'\
               ' Bottom diameter: {}, Thickness: {}, Steel density: {}'.format(
               self.unique_id, self.shell_id, self.section_position, self.height,
               self.top_diameter, self.bot_diameter, self.thickness,
               self.steel_density)


if __name__ == '__main__':
    a = Shell('A01','S01', 2, 3, 4, 5, 6, 7)
    print(a)