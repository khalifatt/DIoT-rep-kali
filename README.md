PCM-Framework-Data-Validation/
├── README.md
├── requirements.txt
├── docker-compose.yml
├── run_evaluation.sh
├── CITATION.cff
├── .github/
│   └── workflows/
│       └── test.yml
├── src/
│   ├── __init__.py
│   ├── pcm_graph_builder.py
│   └── eval_metrics.py
├── tests/
│   └── test_pcm.py
├── data/
│   └── pcm_testbed_schema_500.json
└── configs/
    ├── sddl_mappings.json
    └── escalation_graph.dot

# PCM-Framework-Data-Validation

This repository contains the configuration scripts, SDDL parsing modules, test suites, and dataset schemas utilized to seed and validate the Privilege Chain Modeling (PCM) framework across a heterogeneous 500-node enterprise testbed.

## Testbed Architecture
The testbed environment consists of exactly 500 security-relevant nodes distributed across:
- **Domain Controllers**: 3 instances (Windows Server 2022 Standard)
- **Workstations (Windows 10)**: 211 instances
- **Workstations (Windows 11)**: 245 instances
- **Legacy Workstations (Windows 8)**: 5 instances
- **Legacy Workstations (Windows 7)**: 2 instances
- **Application Servers (Ubuntu 20.04 LTS)**: 34 instances

## Repository Structure
- `src/pcm_graph_builder.py`: Automated generator script parsing Windows SDDL matrices and programmatically constructing the weighted directed graph $G = (V_{spr}, E_{are}, W)$ for all 500 nodes.
- `src/eval_metrics.py`: Automated performance evaluator computing TPR, FPR, F1-score, and AUC metrics.
- `tests/test_pcm.py`: Unit test suite verifying graph capacity limits and SDDL parsing.
- `data/pcm_testbed_schema_500.json`: Complete dataset schema containing node states and Access Control Entries (NACLs) across the 500 infrastructure nodes.
- `configs/sddl_mappings.json`: Hex-encoded access mask mappings and baseline scaling parameters.
- `configs/escalation_graph.dot`: Graphviz structural configuration for path visualization.
- run_evaluation.sh: Automated execution script for end-to-end replication.
  
**Tools:**
- BloodHound (https://github.com/SpecterOps/BloodHound-Legacy)
- https://github.com/PowerShellMafia/PowerSploit/blob/master/Recon/PowerView.ps1
