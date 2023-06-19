#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 18 21:52:22 2023

@author: joao
"""

import unittest
import towerSectionFinderMicroservice
import random
from flask import Flask, jsonify, request


app = Flask(__name__)


def getNewId():
    return random.getrandbits(28)

# Add your existing code here

# Add Tower Section endpoint
@app.route('/tower_section', methods=['POST'])
def add_tower_section_endpoint():
    data = request.json
    section_id = data.get('section_id')
    shells = data.get('shells')

    if section_id is None or shells is None:
        return jsonify({'error': 'Invalid request payload'}), 400

    add_tower_section(section_id, shells)
    return jsonify({'message': 'Tower section added successfully'})

# Retrieve Tower Section endpoint
@app.route('/tower_section/<section_id>', methods=['GET'])
def retrieve_tower_section_endpoint(section_id):
    shells = retrieve_tower_section_id(section_id)
    if shells is None:
        return jsonify({'error': f'Tower section with ID {section_id} not found'}), 404

    return jsonify({'shells': shells})

# Delete Tower Section endpoint
@app.route('/tower_section/<section_id>', methods=['DELETE'])
def delete_tower_section_endpoint(section_id):
    delete_tower_section(section_id)
    return jsonify({'message': f'Tower section with ID {section_id} deleted successfully'})

# Unit tests for endpoints
class TowerSectionTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_add_tower_section_endpoint(self):
        # Test valid request
        response = self.app.post('/tower_section', json={
            'section_id': 'TS001',
            'shells': [
                {
                    'position': 1,
                    'height': 10,
                    'top_diameter': 8,
                    'bot_diameter': 9,
                    'thickness': 1,
                    'steel_density': 7.85
                }
            ]
        })
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['message'], 'Tower section added successfully')

        # Test invalid request (missing section_id)
        response = self.app.post('/tower_section', json={
            'shells': [
                {
                    'position': 1,
                    'height': 10,
                    'top_diameter': 8,
                    'bot_diameter': 9,
                    'thickness': 1,
                    'steel_density': 7.85
                }
            ]
        })
        self.assertEqual(response.status_code, 400)

    def test_retrieve_tower_section_endpoint(self):
        # Test existing tower section
        response = self.app.get('/tower_section/TS001')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(data['shells'])

        # Test non-existing tower section
        response = self.app.get('/tower_section/TS002')
        self.assertEqual(response.status_code, 404)

    def test_delete_tower_section_endpoint(self):
        # Test existing tower section
        response = self.app.delete('/tower_section/TS001')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['message'], 'Tower section with ID TS001 deleted successfully')

        # Test non-existing tower section
        response = self.app.delete('/tower_section/TS002')
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
