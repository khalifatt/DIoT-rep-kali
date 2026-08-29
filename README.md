PCM-Framework-Data-Validation/
├── README.md
├── src/
│   ├── __init__.py
│   └── pcm_graph_builder.py
├── data/
│   └── pcm_testbed_schema.json
└── configs/
    └── sddl_mappings.json

# PCM-Framework-Data-Validation

This repository contains the configuration scripts, SDDL parsing modules, and dataset schemas utilized to seed and validate the Privilege Chain Modeling (PCM) framework across a heterogeneous 500-node enterprise testbed.

## Testbed Architecture
The testbed environment consists of 500 security-relevant nodes distributed across:
- **Domain Controllers**: 3 instances (Windows Server 2022 Standard)
- **Workstations (Windows 10)**: 211 instances
- **Workstations (Windows 11)**: 245 instances
- **Legacy Workstations (Windows 8)**: 5 instances
- **Legacy Workstations (Windows 7)**: 2 instances
- **Application Servers (Ubuntu 20.04 LTS)**: 34 instances

## Repository Structure
- `src/pcm_graph_builder.py`: Automated generator script parsing Windows SDDL matrices and constructing the weighted directed graph $G = (V_{spr}, E_{are}, W)$.
- `data/pcm_testbed_schema_500.json`: Complete dataset schema containing node states and Access Control Entries (NACLs) across the 500 nodes.
- `configs/sddl_mappings.json`: Hex-encoded access mask mappings and baseline scaling parameters.
