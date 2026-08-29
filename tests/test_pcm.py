"""
Module: test_pcm.py
Description: Formal unit test suite validating SDDL parsing accuracy, graph weight 
calculations, node capacity limits, and heterogeneous OS allocations for CI/CD execution.
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
        # Testing node addition across mixed operating systems to match testbed diversity
        os_list = ["Windows Server 2022", "Windows 10", "Windows 11", "Windows 8", "Windows 7", "Ubuntu 20.04 LTS"]
        for i in range(10):
            target_os = os_list[i % len(os_list)]
            self.builder.add_node(f"node_{i}", "Workstation", target_os, "Medium")
            
        with self.assertRaises(ValueError):
            self.builder.add_node("node_overflow", "Workstation", "Windows 11", "High")

    def test_access_mask_parsing(self):
        rights = self.builder.parse_access_mask("0x001301BF")
        self.assertIn("GenericAll", rights)
        
        invalid_rights = self.builder.parse_access_mask("INVALID_HEX")
        self.assertEqual(invalid_rights, [])

    def test_edge_weight_computation(self):
        edge = self.builder.add_edge("node_0", "node_1", "(A;;GA;;;WD)", "High")
        self.assertIsNotNone(edge)
        self.assertGreater(edge["weight"], 0.0)
        self.assertIn("GenericAll", edge["permissions"])

if __name__ == "__main__":
    unittest.main()
