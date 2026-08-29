"""
Module: test_pcm.py
Description: Formal unit test suite validating SDDL parsing accuracy, graph weight 
calculations, and node capacity constraints for CI/CD pipeline execution.
"""

import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from pcm_graph_builder import PCMSecurityGraphBuilder

class TestPCMSecurityGraphBuilder(unittest.TestCase):
    def setUp(self):
        self.builder = PCMSecurityGraphBuilder(node_capacity=10)

    def test_node_capacity_limit(self):
        for i in range(10):
            self.builder.add_node(f"node_{i}", "Workstation", "Windows 10", "Medium")
        with self.assertRaises(ValueError):
            self.builder.add_node("node_overflow", "Workstation", "Windows 10", "Medium")

    def test_access_mask_parsing(self):
        rights = self.builder.parse_access_mask("0x001301BF")
        self.assertIn("GenericAll", rights)
        
        invalid_rights = self.builder.parse_access_mask("INVALID_HEX")
        self.assertEqual(invalid_rights, [])

    def test_edge_weight_computation(self):
        edge = self.builder.add_edge("node_0", "node_1", "(A;;GA;;;WD)", "Medium")
        self.assertIsNotNone(edge)
        self.assertGreater(edge["weight"], 0.0)
        self.assertIn("GenericAll", edge["permissions"])

if __name__ == "__main__":
    unittest.main()
