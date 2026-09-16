# FOCAL OGC Blocks

OGC Blocks for the FOCAL project. The main content is a machine-readable model for the
transferability of climate-service workflows - where a workflow's results are valid, what reference
and calibration artifacts it depends on, and what must happen to them before the workflow can be
reused elsewhere. The register also carries a forest-typology ontology and data model, originally
built as a worked demonstrator of bblocks' semantic-binding and JSON-LD-enhanced map-view
capabilities applied to a real domain.


## About this Register: FOCAL OGC Blocks

This register is the machine-readable foundation for the **[FOCAL project](https://www.focal-euproject.eu/)**, a standards-mediated
pipeline bridging global climate science and local decision-making. It implements the **OGC Blocks**
framework to deliver a "system of systems" approach for **Distributed Digital Twins**, and covers two
related concerns:

*   **Workflow transferability:** a model for stating, in machine-readable form, where a workflow's
    results hold, what reference/calibration artifacts they depend on, and what must happen to those
    artifacts (recalibrate, substitute, flag as unsupported, ...) before the workflow can be run
    somewhere else. This lets a consumer - human or automated - decide whether a workflow built for
    one region, dataset, or scenario can be trusted, adapted, or must be rejected for another.
*   **A worked demonstrator:** an ontology and a Czech forest-typology data model (forest stand
    features, properties, and feature collections) built to show bblocks' semantic-binding and
    JSON-LD-enhanced map-view capabilities applied to a real domain, ahead of applying the same
    capabilities to the transferability model itself.

### **Who is this register for?**
This register supports a multi-actor ecosystem:
*   **Workflow Owners:** Scientists and engineers who build climate-service workflows and need a
    standard way to say where those workflows are valid and what they depend on.
*   **Developers:** Engineers building climate services who require stable API contracts, versioned
    schemas, and reusable data models for **Digital Twins**.
*   **Bblocks Authors:** Anyone evaluating OGC Blocks' semantic-binding and JSON-LD map-view
    capabilities can use the forest-typology demonstrator as a worked reference.
*   **AI Agents:** Automated systems that require explicit semantics to programmatically process data
    and evaluate workflow transferability without human intervention.

### **What does this register contain?**
It hosts reusable **OGC Blocks** that move from document-centric descriptions to actionable components:
*   **Transferability model** (`_sources/transferability`): a profile of a CWL Workflow adding a
    transferability statement (validity envelope, artifact acceptance criteria, adaptation rules),
    computation type, maturity status, quality annotations, and the open SKOS vocabularies these
    blocks are built on.
*   **focal-ontology:** A core module providing the machine-readable semantics (SKOS/OWL) for forest
    type codes with **multi-lingual support** in Czech, English, and German - the demonstrator's
    vocabulary.
*   **Forest Stand data model:** `forestStandProperties`, `forestStandFeature`, and
    `forestStandCollection` - a Feature/FeatureCollection profile for forest stands classified by the
    FOCAL forest typology, showing how a schema binds to that vocabulary and renders in the
    JSON-LD-enhanced map view.

### **When should this register be used?**
*   **Standardized Ingestion:** When converting shapefiles or other scientific data into
    planning-ready formats that need explicit semantics.
*   **Data Validation:** To enforce data quality and consistency via **SHACL shapes**, ensuring data
    meets mandatory Coordinate Reference System and unit contracts.
*   **Workflow Composition and Reuse:** When building or reusing containerized workflows (e.g. in
    **CWL**, or execution systems such as **Steep**) that need a machine-readable statement of where
    they are valid and what must happen before they are transferred to a new region, dataset, or
    scenario.

### **Where does this register fit?**
*   **Federated Register Infrastructure:** It acts as a domain-specific node analogous to the Domain
    Name System (DNS), inheriting foundational patterns from the root OGC register, and importing the
    [bblocks-cwl](https://github.com/ogcincubator/bblocks-cwl) and
    [cross-domain-model](https://github.com/ogcincubator/cross-domain-model) registers.

### **Why does this register exist?**
*   **Closing the Semantic Gap:** It addresses the "semantic disconnection" where scientific data and
    workflows are opaque to the local systems meant to reuse them.
*   **Transferability, not just interoperability:** Format and schema compatibility do not tell a
    consumer whether a workflow's *results* still hold outside the context it was built for; this
    register adds that missing, machine-readable layer.
*   **Trust and Reproducibility:** It provides an auditable framework where every recommendation is
    backed by a machine-readable manifest recording lineage, code versions, and processing history.

### **How is this register structured and implemented?**
*   **Implementation:** Developed using the **GitHub bblock-template** with a test-driven CI/CD
    pipeline where every example must pass validation.
*   **Recursive Composition:** Each block aggregates a `schema.yaml` for structure, a
    `context.jsonld` for semantic uplift, and SHACL shapes for executable constraints.
*   **Profile Layering:** It utilizes hierarchical profiling, allowing local specializations to
    inherit and extend base standards without breaking interoperability - e.g. the transferability
    `workflow` block profiles a CWL Workflow, and `forestStandFeature` inherits from the base OGC
    Feature block.

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

### `ogc.focal.transferability.notes` — FOCAL Transferability Notes (mixin)

**Type:** schema

Reusable mixin adding a free-text escape hatch for transferability facts the controlled vocabularies cannot capture. Uplifts to rdfs:comment rather than a FOCAL-specific property.

### `ogc.focal.transferability.vocab` — FOCAL Transferability Vocabulary and Model Ontology

**Type:** model

The RDF vocabulary behind the FOCAL workflow transferability model: ten open SKOS concept schemes (actions, triggers, condition tests, envelope dimensions, envelope roles, artifact roles, scenario markers, computation types, maturity statuses, quality dimensions) plus the classes and properties FOCAL mints where no published vocabulary says the same thing.

### `ogc.focal.transferability.acceptanceCriteria` — FOCAL Artifact Acceptance Criteria

**Type:** schema

What a dataset must satisfy to serve as a given artifact - variable name, acceptable units (QUDT), required axes, acceptable grids, schemas it must conform to. What makes replace-with-local-equivalent actionable rather than merely stated.

### `ogc.focal.transferability.computationType` — FOCAL Computation Type (mixin)

**Type:** schema

Reusable mixin adding computationType, an open-vocabulary classification of how a workflow computes its results (statistical/ML, deterministic/rule-based, precomputed data delivery). Optional at the workflow level.

### `ogc.focal.transferability.envelopeConstraint` — FOCAL Transferability Envelope Constraint

**Type:** schema

A single {role, dimension, value} statement bounding where a workflow's results are valid, addressable by id so rules can cite which boundary they are evaluated against. Spatial values are GeoSPARQL geometries and temporal values DCAT periods, so a consumer can evaluate them without knowing FOCAL.

### `ogc.focal.transferability.maturityStatus` — FOCAL Workflow Maturity Status (mixin)

**Type:** schema

Reusable mixin adding maturityStatus, an open-vocabulary classification of a workflow's operational maturity (prototype, pre-operational, operational). Deliberately a separate vocabulary from a bblock's own authoring-lifecycle status field.

### `ogc.focal.transferability.qualityAnnotation` — FOCAL Quality Annotation

**Type:** schema

A single statement of uncertainty or confidence about a workflow's results, independent of its maturityStatus. Binds to the W3C Data Quality Vocabulary (DQV) directly, since no OGC Block wraps DQV.

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

