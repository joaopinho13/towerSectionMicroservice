#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 17 16:42:26 2023

@author: joao
"""

from shell import Shell
from towerSection import TowerSection

catalog = []

def add_tower_section(catalog, section_id, shells):
    # Check if the section ID is unique
    for section in catalog:
        if section.section_id == section_id:
            print(f"A tower section with ID {section_id} already exists.")
            return None
    
    # Check if Shells ID is unique
    i = 0
    unique_codes = []
    duplicate_codes = []
    for shell in shells:
        code = shell.unique_id
        if code in unique_codes:
            duplicate_codes.append(code)
        else:
            unique_codes.append(code)
        if duplicate_codes:
            print(f"A Shell section with ID {shell.unique_id} already exists.")
            return None
        prev_unique_id = shells[i].unique_id
        i += 1
        for section in catalog:
            for shell in section.shells:
                if prev_unique_id == shell.unique_id:
                    print(f"A Shell section with ID {shell.unique_id} already exists.")
                    return None
    
    # Check if the section has at least one shell
    if len(shells) < 1:
        print("The tower section must have at least one shell.")
        return None
    
    # Check if the shell numbers are sequential, unique, and start with number 1
    shell_numbers = []
    for shell in shells:
        shell_numbers.append(shell.section_position)
    
    i = 1
    expected_numbers = []
    for pos in range(len(shells)):
        expected_numbers.append(i)
        i += 1
    if shell_numbers != expected_numbers:
        print("The shell numbers must be sequential, unique, and start with number 1.")
        return None
    
    # Check if the shell diameters are contiguous between adjacent shells
    prev_top_diameter = shells[0].top_diameter
    for shell in shells[1:]:
        if prev_top_diameter != shell.bot_diameter:
            print("The shell diameters are not contiguous between adjacent shells.")
            return None
        if shell.top_diameter > shell.bot_diameter:
            print("Top diameter bigger than Bottom diameter.")
            return None
        prev_top_diameter = shell.top_diameter

    # Calculate the total length of the section
    total_length = sum(shell.height for shell in shells)

    # Create the new tower section and add it to the catalog
    section = TowerSection(section_id)
    section.shells = shells
    section.length = total_length
    catalog.append(section)

    print("Tower section added successfully.")


# Create some shells
shell1 = Shell('S001', 1, 10, 7, 8, 2, 7.8)
shell2 = Shell('S002', 2, 15, 6, 7, 2, 7.8)
shell3 = Shell('S003', 3, 8, 5, 6, 2, 7.8)
shell4 = Shell('S004', 4, 8, 4, 5, 2, 7.8)

# Add a tower section to the catalog
add_tower_section(catalog, "A001", [shell1, shell2, shell3, shell4])

# Print the catalog
for section in catalog:
    print(section)
    for shell in section.shells:
        print(shell)









    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    