#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 17 16:42:26 2023

@author: joao
"""

import sqlite3
import random
from shell import Shell
from towerSection import TowerSection


def getNewId():
    return random.getrandbits(28)


# Create Shells
shells = [
    {
     'position': 1, 
     'height': 10, 
     'top_diameter': 8, 
     'bot_diameter': 9, 
     'thickness': 1, 
     'steel_density': 7.85
     },
    {
     'position': 2, 
     'height': 15, 
     'top_diameter': 7, 
     'bot_diameter': 8, 
     'thickness': 1, 
     'steel_density': 7.85
     },
    {
     'position': 3, 
     'height': 20, 
     'top_diameter': 6, 
     'bot_diameter': 7, 
     'thickness': 1, 
     'steel_density': 7.85}
]


conn = sqlite3.connect('catalogue.db')
cur = conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS sections (
                    section_id TEXT PRIMARY KEY,
                    length REAL
                )''')
cur.execute('''CREATE TABLE IF NOT EXISTS shells (
                    unique_id TEXT PRIMARY KEY,
                    shell_id TEXT,
                    section_position INTEGER,
                    height REAL,
                    top_diameter REAL,
                    bot_diameter REAL,
                    thickness REAL,
                    steel_density REAL
                )''')
conn.commit()
conn.close()

def add_tower_section(section_id, shells):
    conn = sqlite3.connect('catalogue.db')
    cur = conn.cursor()
    
    # Check if the section code already exists in the database
    cur.execute('SELECT * FROM sections WHERE section_id=?', (section_id,))
    if cur.fetchone():
        print('Section code already exists. Please choose a different code')
        conn.close()
        return None
    
    # Check if the tower section has at least one shell
    if len(shells) == 0:
        print('A tower section must have at least one shell')
        conn.close()
        return
    
    # Check if shell numbers are sequential, unique, and start with number 1
    shell_numbers = [shell['position'] for shell in shells]
    if shell_numbers != list(range(1, len(shell_numbers) + 1)):
        print('Invalid shell numbers. Shell numbers must be sequential, unique, and start with number 1')
        conn.close()
        return
        
    # Check if shell diameters are contiguous
    for i in range(len(shells) - 1):
        if shells[i]['top_diameter'] != shells[i + 1]['bot_diameter']:
            print('Invalid shell diameters. Diameters must be contiguous between adjacent shells')
            conn.close()
            return

    # Calculate the length of the tower section
    length = sum(shell['height'] for shell in shells)
    
    tower = TowerSection(section_id, length)
    cur.execute("INSERT INTO sections VALUES (?,?)", (
        tower.section_id,
        tower.length))
    
    for shell in shells:
        unique_id = getNewId()
        s = Shell(unique_id, section_id, shell['position'],
                  shell['height'], shell['top_diameter'], shell['bot_diameter'], 
                  shell['thickness'], shell['steel_density'])
        tower.add_shell(s)
        
        # Add to the SQLite DataBase
        cur.execute("INSERT INTO shells VALUES (?,?,?,?,?,?,?,?)", (
            s.unique_id,
            s.shell_id,
            s.section_position,
            s.height,
            s.top_diameter,
            s.bot_diameter,
            s.thickness,
            s.steel_density
    ))
    conn.commit()
    conn.close()
    print("Tower section added successfully")



def retrieve_tower_section_id(section_id):
    conn = sqlite3.connect('catalogue.db')
    cur = conn.cursor()
    
    # Check if the section code exists in the database
    cur.execute('SELECT * FROM sections WHERE section_id=?', (section_id,))
    section_row = cur.fetchone()

    if section_row is None:
        print(f'A tower section with ID {section_id} was not found in the catalog')
        conn.close()
        return None

    # Search for the shells
    cur.execute("SELECT * FROM shells WHERE shell_id=?", (section_id,))
    shell_rows = cur.fetchall()

    # Add shells to tower_section
    list_shells = []
    for shell_row in shell_rows:
        list_shells.append(shell_row)

    conn.close()
    
    return list_shells




def delete_tower_section(section_id):
    conn = sqlite3.connect('catalogue.db')
    cur = conn.cursor()
    # Check if the section code exists in the database
    cur.execute('SELECT * FROM sections WHERE section_id=?', (section_id,))
    if cur.fetchone():
        cur.execute("DELETE FROM sections WHERE section_id=?", (section_id,))
        conn.commit()
        conn.close()
        print(f"Tower section with ID {section_id} deleted successfully")
        return None
    
    print(f"A tower section with ID {section_id} was not found in the catalog")


# The two following functions are not up to date
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
#add_tower_section("TS001", shells)

section_id = "TS001"  # ID da seção da torre que deseja recuperar

shells = retrieve_tower_section_id(section_id)
if shells is not None:
    # A seção da torre foi encontrada no catálogo
    print(f"Shells for tower section ID {section_id}:")
    for shell in shells:
        print(shell)

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
# matching_sections = retrieve_tower_section_diameter(catalog, 7, 5)

# for shell in matching_sections:
#     print(shell)










    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    