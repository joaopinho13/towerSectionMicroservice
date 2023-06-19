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
        s = Shell(getNewId(), section_id, shell['position'],
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

    for shell_row in shell_rows:
        shell_info = {
        'ID': shell_row[0],
        'position': shell_row[2],
        'height': shell_row[3],
        'top_diameter': shell_row[4],
        'bot_diameter': shell_row[5],
        'thickness': shell_row[6],
        'steel_density': shell_row[7],
        }
        print(shell_info)

    conn.close()
    
    return



def delete_tower_section(section_id):
    conn = sqlite3.connect('catalogue.db')
    cur = conn.cursor()
    # Check if the section code exists in the database
    cur.execute('SELECT * FROM sections WHERE section_id=?', (section_id,))
    if cur.fetchone():
        cur.execute("DELETE FROM sections WHERE section_id=?", (section_id,))
        cur.execute('DELETE FROM shells WHERE shell_id=?', (section_id,))
        conn.commit()
        conn.close()
        print(f"Tower section with ID {section_id} deleted successfully")
        return None
    
    print(f"A tower section with ID {section_id} was not found in the catalog")


# Function doing well but missing the restristions
def modify_tower_section_properties(section_id, new_shell):
    conn = sqlite3.connect('catalogue.db')
    cur = conn.cursor()

    # Check if the tower section exists in the database
    cur.execute('SELECT * FROM sections WHERE section_id=?', (section_id,))
    section_row = cur.fetchone()

    if section_row is None:
        print(f'A tower section with ID {section_id} was not found in the catalog')
        conn.close()
        return None

    # Check if the shell exists in the tower section
    cur.execute('SELECT * FROM shells WHERE shell_id=?', (section_id,))
    shell_row = cur.fetchone()

    if shell_row is None:
        print(f'A shell with ID {section_id} was not found in the tower section')
        conn.close()
        return None
    
    # Update the dimensions and steel density of the shell
    cur.execute('UPDATE shells SET height=?, top_diameter=?, bot_diameter=?, thickness=?, steel_density=? WHERE shell_id=?',
                (new_shell.height, new_shell.top_diameter, new_shell.bot_diameter,
                 new_shell.thickness, new_shell.steel_density, section_id))

    conn.commit()
    conn.close()
    print(f'Shell with ID {section_id} in tower section {section_id} modified successfully')


# Only returns if the bot and top diameter are equals to the shell
def retrieve_shells_diameter(bottom_diameter, top_diameter):
    conn = sqlite3.connect('catalogue.db')
    cur = conn.cursor()

    cur.execute('''SELECT * FROM shells
                    WHERE bot_diameter = ? AND top_diameter = ?''',
                (bottom_diameter, top_diameter))
    shell_rows = cur.fetchall()
    
    for shell_row in shell_rows:
        shell_info = {
        'ID': shell_row[0],
        'position': shell_row[2],
        'height': shell_row[3],
        'top_diameter': shell_row[4],
        'bot_diameter': shell_row[5],
        'thickness': shell_row[6],
        'steel_density': shell_row[7],
        }
        print(shell_info)

    conn.close()
    return


section_id = "TS001"

# Add a tower section to the catalog
#add_tower_section("TS001", shells)


# Retrieve a tower section by id
#shells = retrieve_tower_section_id(section_id)


# Exemple of the function delete_tower_section
#delete_tower_section(section_id)

# Example
#new_shell = Shell(getNewId(), section_id, 3, 5, 3, 4,0.7, 2)
#modify_tower_section_properties("TS001", new_shell)


# Print the details
#shells = retrieve_shells_diameter(8, 7)





    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    