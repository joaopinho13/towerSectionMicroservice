#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 17 16:42:26 2023

@author: joao
"""

import sqlite3
from shell import Shell
from towerSection import TowerSection


# Create Shells
shell1 = Shell('S001', 1, 10, 7, 8, 2, 7.8)
shell2 = Shell('S002', 2, 15, 6, 7, 2, 7.8)
shell3 = Shell('S003', 3, 8, 5, 6, 2, 7.8)
shell4 = Shell('S004', 4, 8, 4, 5, 2, 7.8)


# Catalogue of Towers Sections
catalog = []



def add_tower_section(catalog, section_id, shells):
    conn = sqlite3.connect('catalogue.db')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS sections (
                        section_id TEXT PRIMARY KEY
                    )''')
    cur.execute('''CREATE TABLE IF NOT EXISTS shells (
                        unique_id TEXT PRIMARY KEY,
                        section_position INTEGER,
                        height REAL,
                        top_diameter REAL,
                        bot_diameter REAL,
                        thickness REAL,
                        steel_density REAL
                    )''')
    
    # Check if the section ID is unique
    for section in catalog:
        if section.section_id == section_id:
            print(f"A tower section with ID {section_id} already exists")
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
            print(f"A Shell section with ID {shell.unique_id} already exists")
            return None
        prev_unique_id = shells[i].unique_id
        i += 1
        for section in catalog:
            for shell in section.shells:
                if prev_unique_id == shell.unique_id:
                    print(f"A Shell section with ID {shell.unique_id} already exists")
                    return None
    
    # Check if the section has at least one shell
    if len(shells) < 1:
        print("The tower section must have at least one shell")
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
        print("The shell numbers must be sequential, unique, and start with number 1")
        return None
    
    # Check if the shell diameters are contiguous between adjacent shells
    prev_top_diameter = shells[0].top_diameter
    for shell in shells[1:]:
        if prev_top_diameter != shell.bot_diameter:
            print("The shell diameters are not contiguous between adjacent shells")
            return None
        if shell.top_diameter > shell.bot_diameter:
            print("Top diameter bigger than Bottom diameter")
            return None
        prev_top_diameter = shell.top_diameter

    # Calculate the total length of the section
    total_length = sum(shell.height for shell in shells)

    # Create the new tower section and add it to the catalog
    section = TowerSection(section_id)
    section.shells = shells
    section.length = total_length
    catalog.append(section)
    
    # Add to the SQLite DataBase
    cur.execute("INSERT INTO sections VALUES (?)", (section_id,))
    
    for shell in shells:
        cur.execute("INSERT INTO shells VALUES (?,?,?,?,?,?,?)", (
            shell.unique_id,
            shell.section_position,
            shell.height,
            shell.top_diameter,
            shell.bot_diameter,
            shell.thickness,
            shell.steel_density
    ))

    conn.commit()
    conn.close()
    print("Tower section added successfully")



def retrieve_tower_section_id(catalog, section_id):
    for section in catalog:
        if section.section_id == section_id:
            print(f"Tower Section ID: {section.section_id}")
            print("Shells:")
            for shell in section.shells:
                print("----------")
                print(f"Shell number (ID): {shell.unique_id}")
                print(f"Position: {shell.section_position}")
                print(f"Height: {shell.height}")
                print(f"Top diameter: {shell.top_diameter}")
                print(f"Bottom diameter: {shell.bot_diameter}")
                print(f"Thickness: {shell.thickness}")
                print(f"Steel density: {shell.steel_density}")
            return None
    print(f"A tower section with ID {section_id} was not found in the catalog")



def delete_tower_section(catalog, section_id):
    for i, section in enumerate(catalog):
        if section.section_id == section_id:
            del catalog[i]
            print(f"Tower section with ID {section_id} deleted successfully")
            return None
        
    conn = sqlite3.connect('catalogue.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM sections WHERE section_id=?", (section_id,))
    conn.commit()
    conn.close()
    print(f"A tower section with ID {section_id} was not found in the catalog")



def modify_tower_section_properties(catalog, section_id, properties):
    conn = sqlite3.connect('catalogue.db')
    cur = conn.cursor()
    # Find the tower section with the specified ID
    for section in catalog:
        if section.section_id == section_id:
            # Modify the properties of the shells
            for prop in properties:
                shell_id = prop['unique_id']
                property_name = prop['property']
                new_value = prop['value']

                # Find the shell with the specified ID
                for shell in section.shells:
                    if shell.unique_id == shell_id:
                        # Modify the specified property
                        if property_name == 'height':
                            shell.height = new_value
                            cur.execute("UPDATE shells SET height = ? WHERE unique_id = ?", (new_value, shell_id)) 
                        elif property_name == 'top_diameter':
                            shell.top_diameter = new_value
                            cur.execute("UPDATE shells SET top_diameter = ? WHERE unique_id = ?", (new_value, shell_id)) 
                        elif property_name == 'bot_diameter':
                            shell.bot_diameter = new_value
                            cur.execute("UPDATE shells SET bot_diameter = ? WHERE unique_id = ?", (new_value, shell_id)) 
                        elif property_name == 'thickness':
                            shell.thickness = new_value
                            cur.execute("UPDATE shells SET thickness = ? WHERE unique_id = ?", (new_value, shell_id)) 
                        elif property_name == 'steel_density':
                            shell.steel_density = new_value
                            cur.execute("UPDATE shells SET stell_density = ? WHERE unique_id = ?", (new_value, shell_id)) 
                        else:
                            print(f"Invalid property name: {property_name}")
                            return

                        print(f"Modified property '{property_name}' of shell with ID '{shell_id}'")
                        break  # Exit the loop once the shell is found

                else:
                    print(f"No shell found with ID '{shell_id}' in the tower section")
                    return

            break  # Exit the loop once the tower section is found

    else:
        print(f"No tower section found with ID '{section_id}' in the catalog")  
    conn.commit()
    conn.close()     



def retrieve_tower_section_diameter(catalog, bot_diameter_range, top_diameter_range):
    conn = sqlite3.connect('catalogue.db')
    cur = conn.cursor()
    matching_sections = []
    for section in catalog:
        for shell in section.shells:
            if bot_diameter_range >= shell.bot_diameter \
                    and top_diameter_range <= shell.top_diameter:
                matching_sections.append(shell)
                cur.execute("SELECT * FROM shells WHERE unique_id = ?", (shell.unique_id,))
                row = cur.fetchone()
    conn.commit()
    conn.close()   
    return matching_sections


# Add a tower section to the catalog
add_tower_section(catalog, 'A001', [shell1, shell2, shell3])

# Exemple of the function retrieve_tower_section:
#retrieve_tower_section_id(catalog, 'A001')

# Exemple of the function delete_tower_section:
#delete_tower_section(catalog, "A001")

# Example usage:
# properties_to_modify = [
#     {'unique_id': 'S001', 'property': 'height', 'value': 11},
#     {'unique_id': 'S002', 'property': 'top_diameter', 'value': 6},
#     {'unique_id': 'S003', 'property': 'bot_diameter', 'value': 6}
# ]
#modify_tower_section_properties(catalog, "A001", properties_to_modify)


# Print the details of the matching tower sections
matching_sections = retrieve_tower_section_diameter(catalog, 7, 5)

for shell in matching_sections:
    print(shell)










    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    