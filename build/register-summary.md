# FOCAL Forest Typology Czech OGC Blocks

This is an example which uses OGC Blocks to define the ontology for forest typology multilingual.


## About this Register: FOCAL Forest Typology Czech OGC Blocks

As a Forest Data Provider (e.g. a forestry researcher), I want to provide my "normal GIS" data (e.g. typology derived by photogrammetry and remote sensing) in a way that my data is conform to my domain (multilingual) and can be integrate with data from another domain (e.g. climate projections) by defining clear input/output contracts. As a platform operator who follows the OGC Smart concepts, I know that domain specific profiles can be provided by public registers to ensure public consistency of distributed digital twins. Using those profiles turns the local typology data of the data provider into machine-interpretable knowledge that can be used to extend the distributed digital twin of forest typologies or can be automatically integrated into more complex distributed digital twins like climate-resilient reforestation simulations or processed by AI tools to generate climate-resilient reforestation recommendations.

This story illustrates the transition from "normal GIS" (manual overlays and scripts) to a standards-mediated geo-data supply chain. By implementing the Forest Typology OGC Block, the data provider removes the need for bespoke engineering. Instead of rebuilding a pipeline for every new forest, the provider publishes the Forest Typology OGC Block definitions as the "input/output contract" of a consistent distributed digital twin for forest typologies, allowing AI agents to navigate semantic gaps automatically and provide validated decision support. 

This register provides the machine-readable foundation for the **FOCAL project**, establishing a standards-mediated pipeline to bridge the gap between global climate science and local decision-making. It implements the **OGC Blocks** framework to deliver a "system of systems" approach for **Distributed Digital Twins** in forestry and urban planning.

### **Who is this register for?**
This register supports a multi-actor ecosystem:
*   **Data Providers:** Forestry researchers and municipal GIS departments who need to transform **"normal GIS"** data (e.g., typology from photogrammetry) into machine-interpretable knowledge.
*   **Developers:** Engineers building climate services who require stable API contracts, versioned schemas, and reusable data models for **Digital Twins**.
*   **Domain Experts:** Foresters and urban planners, such as those in **Constance** or the **Czech Forestry Institute**, looking for validated, climate-resilient recommendations.
*   **AI Agents:** Automated systems like the **JackDaw** assistant that require explicit semantics to programmatically process data without human intervention.

### **What does this register contain?**
It hosts reusable **OGC Blocks** that move from document-centric descriptions to actionable components:
*   **Forest Site Assessment:** Schemas mapping management units to soil types (FAO World Reference Base) and growth records. It includes target mixtures for specific codes, such as **5K1** (Acidic fir-beech modal site).
*   **Urban Climate Vulnerability:** Models for urban morphology (building density, sealed surfaces) and demographics linked to heat and flood risk.
*   **focal-ontology:** A core module providing the machine-readable semantics (SKOS/OWL) for forest type codes (e.g., **2S1**) with **multi-lingual support** in Czech, English, and German.
*   **Custom Features:** Implementation of the **"Feature with geometry"** pattern, where attributes are managed in a standardized **Property Set** independently of the spatial packaging.

### **When should this register be used?**
*   **Standardized Ingestion:** During the conversion of static shapefiles or **CF-NetCDF** scientific data into planning-ready formats via the **CF-to-Planning Transform**.
*   **Data Validation:** To enforce **Integrity, Provenance, and Trust (IPT)** via **SHACL shapes**, ensuring data meets mandatory Coordinate Reference System (**S-JTSK / EPSG:5514**) and unit contracts.
*   **Workflow Composition:** When building containerized workflows in systems like **Steep** that require consistent input/output contracts between scientific and local domains.

### **Where does this register fit?**
*   **Federated Register Infrastructure:** It acts as a domain-specific node analogous to the Domain Name System (DNS), inheriting foundational patterns from the root OGC register.
*   **Domain Profiling:** It implements the **European Climate Assessment Profile**, binding global standards to regional conventions like **ETRS89** and the European forest inventory.
*   **Pilot Integration:** It connects scientific repositories (ESGF) with local implementation registers**.

### **Why does this register exist?**
*   **Closing the Semantic Gap:** It addresses the "semantic disconnection" where scientific variables (e.g., "tas" for temperature) are opaque to local planning software.
*   **Scalability:** It replaces bespoke data engineering for every city with a **"recipe-based" pipeline**, allowing new municipalities to onboard by creating a local profile rather than custom scripts.
*   **Trust and Reproducibility:** It provides an auditable framework where every recommendation is backed by a **machine-readable manifest (JSON)** recording lineage, code versions, and processing history.

### **How is this register structured and implemented?**
*   **Implementation:** Developed using the **GitHub bblock-template** with a test-driven CI/CD pipeline where every example must pass validation.
*   **Recursive Composition:** Each block aggregates a `schema.yaml` for structure, a `context.jsonld` for semantic uplift, and `shacl.ttl` for executable constraints.
*   **Profile Layering:** It utilizes hierarchical profiling, allowing local specializations to inherit and extend base standards without breaking interoperability. The forestStandFeature block inherits from the base OGC Feature block and aggregates the forestStandProperties property set.

### **For Developers**
*   **[GitHub Repository](https://github.com/ogcincubator/bblocks-focal)**
*   **[OGC Blocks Documentation](https://ogcincubator.github.io/bblocks-docs/)**
*   **[OGC Blocks Tutorials](https://ogcincubator.github.io/bblocks-tutorial/)**
*   **[OGC Blocks Examples](https://ogcincubator.github.io/bblocks-examples/)**


## Building Blocks

### `ogc.focal.focal-ontology` — FOCAL Ontology

**Type:** model

RDF contents for the FOCAL ontology

### `ogc.focal.forestStandProperties` — FOCAL Forest Stand Properties

**Type:** schema

Schema defining the properties of a FOCAL forest stand, including forest type classification, forest region, target management unit, field verification status, area, and data provenance.

### `ogc.focal.transferability.vocab` — FOCAL Transferability Vocabulary and Model Ontology

**Type:** model

The RDF vocabulary behind the FOCAL workflow transferability model: ten open SKOS concept schemes (actions, triggers, condition tests, envelope dimensions, envelope roles, artifact roles, scenario markers, computation types, maturity statuses, quality dimensions) plus the classes and properties FOCAL mints where no published vocabulary says the same thing.

### `ogc.focal.transferability.notes` — FOCAL Transferability Notes (mixin)

**Type:** schema

Reusable mixin adding a free-text escape hatch for transferability facts the controlled vocabularies cannot capture. Uplifts to rdfs:comment rather than a FOCAL-specific property.

### `ogc.focal.transferability.computationType` — FOCAL Computation Type (mixin)

**Type:** schema

Reusable mixin adding computationType, an open-vocabulary classification of how a workflow computes its results (statistical/ML, deterministic/rule-based, precomputed data delivery). Optional at the workflow level.

### `ogc.focal.transferability.maturityStatus` — FOCAL Workflow Maturity Status (mixin)

**Type:** schema

Reusable mixin adding maturityStatus, an open-vocabulary classification of a workflow's operational maturity (prototype, pre-operational, operational). Deliberately a separate vocabulary from a bblock's own authoring-lifecycle status field.

### `ogc.focal.transferability.qualityAnnotation` — FOCAL Quality Annotation

**Type:** schema

A single statement of uncertainty or confidence about a workflow's results, independent of its maturityStatus. Binds to the W3C Data Quality Vocabulary (DQV) directly, since no OGC Block wraps DQV.

### `ogc.focal.transferability.acceptanceCriteria` — FOCAL Artifact Acceptance Criteria

**Type:** schema

What a dataset must satisfy to serve as a given artifact - variable name, acceptable units (QUDT), required axes, acceptable grids, schemas it must conform to. What makes replace-with-local-equivalent actionable rather than merely stated.

### `ogc.focal.transferability.envelopeConstraint` — FOCAL Transferability Envelope Constraint

**Type:** schema

A single {role, dimension, value} statement bounding where a workflow's results are valid, addressable by id so rules can cite which boundary they are evaluated against. Spatial values are GeoSPARQL geometries and temporal values DCAT periods, so a consumer can evaluate them without knowing FOCAL.

### `ogc.focal.transferability.rule` — FOCAL Transferability Rule

**Type:** schema

What must happen, to which artifacts, under which envelope conditions. Conditions cite envelope constraints by id and are conjunctive; actions are an OR-set.

### `ogc.focal.forestStandFeature` — FOCAL Forest Stand Feature

**Type:** schema

GeoJSON Feature representing a spatially delineated forest stand classified according to the FOCAL forest typology system, with properties describing forest type, region, management unit, area, and data provenance.

### `ogc.focal.transferability.transferabilityStatement` — FOCAL Transferability Statement

**Type:** schema

Where something's results are valid (envelope), which reference/calibration artifacts it depends on (artifacts), and what must happen to each under which conditions (rules) - three id-addressable lists joined by reference rather than nesting.

### `ogc.focal.forestStandCollection` — FOCAL Forest Stand Feature Collection

**Type:** schema

GeoJSON FeatureCollection of FOCAL forest stands, providing a spatial dataset of forest units classified by forest type, region, and management unit.

### `ogc.focal.transferability.workflow` — FOCAL Transferability Workflow

**Type:** schema

Profile of a CWL Workflow adding FOCAL's machine-readable transferability facts: a transferability statement (validity envelope, reference/calibration-artifact adaptation rules), computation type, maturity status, and quality annotations.

