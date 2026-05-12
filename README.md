````markdown
# User Story

## Publishing Machine-Interpretable Forest Typology Data

As a Forest Data Provider (e.g. a forestry researcher), I want to provide my "normal GIS" data (e.g. typology derived by photogrammetry and remote sensing) in a way that my data conforms to my domain (multilingual) and can be integrated with data from another domain (e.g. climate projections) by defining clear input/output contracts.

As a platform operator who follows the OGC Smart concepts, I know that domain-specific profiles can be provided by public registers to ensure public consistency of distributed digital twins. Using those profiles turns the local typology data of the data provider into machine-interpretable knowledge that can be used to extend the distributed digital twin of forest typologies or can be automatically integrated into more complex distributed digital twins like climate-resilient reforestation simulations or processed by AI tools to generate climate-resilient reforestation recommendations.

---

# Context

This story illustrates the transition from "normal GIS" (manual overlays and scripts) to a standards-mediated geo-data supply chain.

By implementing the Forest Typology OGC Block, the data provider removes the need for bespoke engineering. Instead of rebuilding a pipeline for every new forest, the provider publishes the Forest Typology OGC Block definitions as the "input/output contract" of a consistent distributed digital twin for forest typologies, allowing AI agents to navigate semantic gaps automatically and provide validated decision support.

---

# Steps taken

1. Implemented a Forest Typology OGC Block for "Features with geometry and typology" with a suitable ontology.
2. Extended the ontology with the forest type code attribute (`LT`) which needs to be mapped to a URI that an AI agent (like JackDaw) can use to retrieve ecological properties in multiple languages.
   - *(Map View – displaying code description)*
3. Added an example GeoJSON `FeatureCollection` conform to the new Forest Site Assessment schema.
4. Added a transform to produce only CRS 5555 output data.
5. Added tests for validation purposes.

---

# Step in detail

Model the forest typology as a "Feature with geometry" that carries a well-defined domain model (the Forest Typology schema). This schema provides the "input/output contract" for your data and maps "normal GIS" attributes to standardized types.

Look at the provided Forest Typology OGC Block (Webpage).

---

# 1. OGC Block Composition

Look at the different folders in `_sources`:

- `focal-ontology`
  - Provides the semantics and gets automatically uploaded to the official register.

- `mySchema`
  - A Property Set with the domain-specific Forest Typology attributes mapped to the semantics.

- `myFeature`
  - A Feature OGC Block (inherited from Feature OGC Block) combining geometry with the domain-specific schema.

- `myFeatureCollection`
  - A FeatureCollection OGC Block (inherited from FeatureCollection OGC Block) describing the whole dataset.

## The Property Set (Czech meta-data description)

```txt
F_A_Lesni_typ
Název: Lesní typologie
Geometrie: polygon

Atributy:
LT: Lesní typ
LES_OBL: lesní oblast
LO_CAST: lesní oblast (část)
UDRZBA: Rok poslední změny dat
ZMENA: na žádost vlastníka/SLT-KN/na základě odsouhlaseného požadavku nebo projektu pro jiné subjekty
ZADOST: číselné zařazení žádosti
CHS: Cílový hospodářský soubor
PCHS: Podsoubor cílového hospodářského souboru
OVER_T: Ověřeno v terénu ANO/NE
ROK_MAP: Rok sběru dat
ID1: jednoznačný identifikátor
SLT: Soubor lesních typů
PLOCHA: v metrech čtverečních
DS_OPRL: 2025

Platnost dat k 1.1.2025
Souřadnicový systém: S-JTSK
```

## Important files

1. `ontology.ttl`
   - Semantics

2. `schema.yaml`
   - Typology type definitions

3. `context.jsonld`
   - Maps the type definitions to the URIs from the ontology

4. `schema.yaml`
   - Feature definition

5. `schema.yaml`
   - Feature collection definition

---

# 2. Forest Type Codes

Adds the forest type code definitions (Czech meta-data descriptions) to the ontology and makes them multilingual.

See within the `ontology.ttl` for the semantics:

```ttl
focal-lt:LT a skos:ConceptScheme, owl:Class ;
  skos:prefLabel "lesní typ"@cz, "forest type"@en, "Waldtyp"@de ;
  skos:hasTopConcept focal-lt:2S1 ;
.

focal-lt:2S1 a skos:Concept, focal-lt:LT ;
 skos:prefLabel "2S1 - Svěží buková doubrava modální"@cz,
 "2S1 - Fresh beech-oak forest (modal)"@en,
 "2S1 - Frische Buchen-Eichenwälder (typisch)"@de ;
 skos:definition "2S1 – svěží buková doubrava modální, lesní typ 2. lesního vegetačního stupně na živinami středně bohatých, svěžích stanovištích"@cz,
 "2S1 – Fresh beech-oak forest (modal), a forest type of the 2nd forest vegetation zone on moderately nutrient-rich, fresh sites"@en,
 "2S1 – Frische Buchen-Eichenwälder (typisch), ein Waldtyp der 2. forstlichen Vegetationsstufe auf mäßig nährstoffreichen, frischen Standorten"@de ;
 skos:notation "2S1" ;
 skos:topConceptOf focal-lt:LT ;
 skos:inScheme focal-lt:LT ;
.
```

---

# 3. Examples

Look at the example data for a feature collection. This example data has been created by QGIS as an export from a shapefile.

The example data for feature collections can be integrated by providing an `examples.yaml` within the `myFeatureCollection` definitions.

The example data for a feature can be defined by linking back to the feature collection using the `examples.yaml` within the `myFeature` definitions.

The first feature within the feature collection carries the coordinate reference system as an extra property. Without this definition, the example feature could not be viewed within the "map view" of the feature example.

The example data for the domain-specific schema can also be defined by linking to the feature collection example using its `examples.yaml` within the `mySchema` definitions.

---

# 4. Transform to Match CRS 5555

A transform can be added by creating a `transforms.yaml`.

It is possible to provide the code snippet directly within this file, but for reasons of clarity the code can be linked as shown in the `transforms.yaml`.

---

# 5. Validation

Validation and testing can be carried out using SHACL rules.

The example checks if the `focal-prop:lesniTyp` exists.

By providing failure examples (`FeatureCollection`, `Feature`), the SHACL rules can be tested further.
````


[General information on design and usage](https://github.com/opengeospatial/bblock-template/blob/master/USAGE.md)


