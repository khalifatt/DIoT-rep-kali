"""
Module: pcm_graph_builder.py
Description: Automated generator for the 500-node heterogeneous enterprise testbed,
incorporating exact node distribution across Windows Server, Windows 10/11/8/7, and Ubuntu 20.04.
"""

import json
import logging
from typing import Dict, List, Optional

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

class PCMSecurityGraphBuilder:
    def __init__(self, node_capacity: int = 500):
        self.node_capacity = node_capacity
        self.nodes: List[Dict] = []
        self.edges: List[Dict] = []

    def seed_testbed_inventory(self) -> None:
        """
        Programmatically populates the 500 nodes matching the exact testbed architecture:
        - 3 Domain Controllers (Windows Server 2022)
        - 211 Windows 10 Workstations
        - 245 Windows 11 Workstations
        - 5 Windows 8 Workstations
        - 2 Windows 7 Workstations
        - 34 Ubuntu 20.04 Server/Application Nodes
        """
        inventory_spec = [
            ("DomainController", "Windows Server 2022 Standard", "High", 3),
            ("Workstation", "Windows 10 Build 19041", "Medium", 211),
            ("Workstation", "Windows 11 Build 22000", "High", 245),
            ("Workstation", "Windows 8 Build 9200", "Low", 5),
            ("Workstation", "Windows 7 Build 7601", "Low", 2),
            ("ApplicationServer", "Ubuntu 20.04 LTS", "Medium", 34)
        ]

        node_counter = 1
        for node_type, os_version, baseline, count in inventory_spec:
            for i in range(1, count + 1):
                if len(self.nodes) >= self.node_capacity:
                    break
                node_id = f"v_spr_{node_type.lower()}_{node_counter:03d}"
                
                # Assign state vector based on role
                state_vector = [1.0 if i == 1 and node_type == "DomainController" else 0.0] * 10
                
                node_entry = {
                    "id": node_id,
                    "type": node_type,
                    "os_version": os_version,
                    "baseline": baseline,
                    "state_vector": state_vector
                }
                self.nodes.append(node_entry)
                node_counter += 1
                
        logging.info(f"Successfully initialized testbed inventory with {len(self.nodes)} nodes.")

    def parse_access_mask(self, mask_hex: str) -> List[str]:
        try:
            mask_val = int(mask_hex, 16)
        except ValueError:
            return []
            
        rights = []
        if mask_val & 0x00020000:
            rights.append("WriteDacl")
        if mask_val & 0x00040000:
            rights.append("WriteOwner")
        if mask_val & 0x00120196:
            rights.append("GenericRead")
        if mask_val & 0x001301BF:
            rights.append("GenericAll")
            
        return rights

    def add_edge(self, source_id: str, target_id: str, sddl_dacl: str, os_baseline: str) -> Optional[Dict]:
        permissions = self.parse_access_mask("0x001301BF" if "GA" in sddl_dacl else "0x00120196")
        if not permissions:
            return None
            
        c_exploit = 2.1 if "GenericAll" in permissions else 4.0
        multiplier_map = {"High": 1.5, "Medium": 1.2, "Low": 0.8}
        c_exploit = round(c_exploit * multiplier_map.get(os_baseline, 1.0), 3)
        
        delta_priv = 0.45 if "GenericAll" in permissions else 0.20
        weight = round(delta_priv / (c_exploit + 0.1), 4)
        
        edge_entry = {
            "source": source_id,
            "target": target_id,
            "permissions": permissions,
            "c_exploit": c_exploit,
            "delta_priv": delta_priv,
            "weight": weight
        }
        self.edges.append(edge_entry)
        return edge_entry

    def export_dataset_schema(self, filepath: str) -> None:
        dataset = {
            "metadata": {
                "framework": "PCM-Full",
                "total_nodes": len(self.nodes),
                "total_edges": len(self.edges),
                "description": "Complete 500-node heterogeneous enterprise testbed schema."
            },
            "nodes": self.nodes,
            "edges": self.edges
        }
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(dataset, f, indent=2)
        logging.info(f"Successfully exported full dataset schema to {filepath}")

if __name__ == "__main__":
    builder = PCMSecurityGraphBuilder(node_capacity=500)
    builder.seed_testbed_inventory()
    
    # Example cross-node escalation path mapping
    builder.add_edge("v_spr_workstation_004", "v_spr_domaincontroller_001", "(A;;GA;;;WD)", "Medium")
    
    builder.export_dataset_schema("data/pcm_testbed_schema_500.json")
