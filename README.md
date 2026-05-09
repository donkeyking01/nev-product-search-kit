<div align="center">

# NEV-Product-Research-Kit

[中文](README.zh-CN.md) | English

</div>

## Overview

`NEV-Product-Research-Kit` is a product research toolkit for the new energy passenger vehicle market. It combines an offline data pipeline, a decision-support dashboard, and an agent skill for evidence-based product research.

Inspired by the research framework behind [SCSI-SLM-EV-Design](https://github.com/DonkeyKing01/SCSI-SLM-EV-Design), this project focuses on engineering implementation, workflow reproducibility, and real research collaboration rather than staying at the level of a paper demo.

The repository currently contains three major modules:

- `offline-pipeline/`: offline workflows for data collection, processing, modeling, retrieval, and interactive research support
- `dashboard/`: a decision-support dashboard built from processed research snapshots
- `nev-product-research/`: an agent skill that turns raw evidence into traceable product research deliverables

## Modules

### 1. `offline-pipeline/`

The offline pipeline contains the core research workflow, including:

- **Data ingestion and normalization**: organize vehicle specs, user comments, competitor information, and public materials into cleaner, reusable inputs
- **User voice structuring**: transform unstructured comments into product dimensions, scenarios, sentiment, pain points, and need signals
- **Product-user mapping analysis**: connect product-side performance with user-side preferences through IPA, persona analysis, and product-dimension comparisons
- **Competitor and product-dimension analysis**: compare NEV products on price, range, charging, space, comfort, cockpit, and assisted driving dimensions
- **Evidence-chain outputs**: separate user quotes, product facts, model inferences, and analysis conclusions into traceable intermediate artifacts
- **Opportunity inputs**: prepare structured results for downstream dashboard views and product research reports

#### Architecture

<p align="center">
  <img src="./docs/images/architecture.png" alt="System architecture" width="75%">
</p>

See [offline-pipeline/README.md](offline-pipeline/README.md) for more details.

### 2. `dashboard/`

`dashboard/` is a data understanding and decision-support surface for EV product managers. It is designed for quickly browsing and interpreting key outputs from the offline pipeline.

#### Preview

<p align="center">
  <img src="./docs/images/dashboard-1.png" alt="Dashboard preview 1" width="75%">
</p>

<p align="center">
  <img src="./docs/images/dashboard-2.png" alt="Dashboard preview 2" width="75%">
</p>

### 3. `nev-product-research/`

`nev-product-research/` is a skill for NEV product and user research.

It follows an evidence-first workflow:

1. Define the research scope
2. Collect evidence from the web
3. Normalize the evidence structure
4. Build the product-side model
5. Build the user-side model
6. Diagnose opportunity areas
7. Generate deliverables

#### Example case

This project provides a sample case generated based on `nev-product-research`, intended to demonstrate how the skill can start from a relatively short product research question and gradually complete Scope definition, evidence organization, product-side modeling, user-side modeling, opportunity diagnosis, and final report generation.

The sample question is:

> What product opportunities exist in long-distance travel experiences for family users in the RMB 200k-300k new energy family SUV market?

The sample outputs are located in [docs/examples](./docs/examples/), showing the complete generated results from Research Scope, Evidence Collection, Product Model, User Model, and Opportunity Cards to Final Report.

This sample is used to illustrate the execution flow and deliverable format of the Skill, and does not represent the only possible research question or a fixed template.

## Repository Structure

```text
.
|-- dashboard/
|-- docs/
|   |-- examples/
|   `-- images/
|-- nev-product-research/
|   |-- agents/
|   |-- references/
|   |-- scripts/
|   `-- workflows/
|-- offline-pipeline/
|   |-- analysis/
|   |-- crawler/
|   |-- data/
|   |-- graph/
|   |-- process/
|   |-- rag/
|   `-- vector/
|-- README.md
`-- README.zh-CN.md
```

## Quick Start

### `offline-pipeline/`

See [offline-pipeline/README.md](offline-pipeline/README.md).

### `dashboard/`

Open `dashboard/index.html` directly in a browser.

### `nev-product-research/`

#### Codex

```bash
git clone https://github.com/DonkeyKing01/nev-product-search-kit.git
cp -r nev-product-search-kit/nev-product-research-skill ~/.codex/skills/nev-product-research-skill
```

#### Claude Code

```bash
git clone https://github.com/DonkeyKing01/nev-product-search-kit.git
cp -r nev-product-search-kit/nev-product-research-skill ~/.claude/skills/nev-product-research-skill
```

#### Manual install

Keep the following structure and copy `nev-product-research/` into the target agent's skills directory:

```text
nev-product-research/
  agents/
  references/
  scripts/
  workflows/
```

## License

MIT
