# Highlights of this Repository

1. Howto publish vector data with a custom schema
2. Howto add CRS transformations
3. Howto validate vector data with a custom schema

# Steps

1. Read the [OGC Building Blocks Documentation](https://ogcincubator.github.io/bblocks-docs/)
2. Create the repo by following the [instructions](https://github.com/opengeospatial/bblock-template/blob/master/USAGE.md) from the [template](https://github.com/opengeospatial/bblock-template/)
3. Implement the Forest Typology OGC Blocks for "Features with geometry and typology" with a suitable [ontology](_sources/focal-ontology).
4. Extend the [`ontology.ttl`](_sources/focal-ontology/ontology.ttl) with the forest type code attribute (`LT`) which needs to be mapped to proper URIs which in turn can be used to retrieve ecological properties in multiple languages for the forest type code attribute (`LT`).
5. Add an example GeoJSON [`FeatureCollection`](_sources/myFeatureCollection/examples/feature.json) conform to the new Forest Site Assessment schema.
6. Add a [`transforms.yaml`](_sources/myFeatureCollection/transforms.yaml) to produce only CRS 5555 output data.
7. Add a test for validation purposes using [shacl shapes](_sources/myFeature/shapes.shacl).

---

# Steps in detail

## 1. Read the Docs

[OGC Building Blocks Documentation](https://ogcincubator.github.io/bblocks-docs/)

## 2. Create the Repo

See the [instructions](https://github.com/opengeospatial/bblock-template/blob/master/USAGE.md) to create this repo from the [template](https://github.com/opengeospatial/bblock-template/).

## 3. OGC Blocks Composition

### The folder structure 

Look at the different folders in [`_sources`](_sources). Each folder contains a [`bblock.json`](_sources/mySchema/bblock.json) to define a OGC Block.

- [`focal-ontology`](_sources/focal-ontology)
  - The ontology OGC Block provides the semantics and gets automatically uploaded to an official register.

- [`mySchema`](_sources/mySchema)
  - The domain-specific Forest Typology OGC Block which maps the attributes of the dataset to the semantics.

- [`myFeature`](_sources/myFeature)
  - A Feature OGC Block inherited from the Feature OGC Block combining geometry with the domain-specific schema.

- [`myFeatureCollection`](_sources/myFeatureCollection)
  - A FeatureCollection OGC Block inherited from the FeatureCollection OGC Block describing the whole dataset.

### The Property Set (Czech meta-data description)

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

### Important files

1. [`ontology.ttl`](_sources/focal-ontology/ontology.ttl)
   - Semantics

2. [`schema.yaml`](_sources/mySchema/schema.yaml) within [`mySchema`](_sources/mySchema)
   - Typology type definitions

3. [`context.jsonld`](_sources/mySchema/context.jsonld) within [`mySchema`](_sources/mySchema)
   - Maps the type definitions to the URIs from the ontology

4. [`schema.yaml`](_sources/myFeature/schema.yaml) within [`myFeature`](_sources/myFeature)
   - Feature definition

5. [`schema.yaml`](_sources/myFeatureCollection/schema.yaml) within [`myFeatureCollection`](_sources/myFeatureCollection)
   - Feature collection definition

---

## 4. Forest Type Codes

Adds the forest type code definitions (Czech meta-data descriptions) to the ontology and makes them multilingual.

See within the [`ontology.ttl`](_sources/focal-ontology/ontology.ttl) for the semantics:

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


## 5. Examples

Look at the example data for a feature collection. This example data has been created by QGIS as an export from a shapefile.

The example data for feature collections can be integrated by providing an [`GeoJSON`](_sources/myFeatureCollection/examples/feature.json) and an [`examples.yaml`](_sources/myFeatureCollection/examples.yaml) within the [`myFeatureCollection`](_sources/myFeatureCollection) definitions and a .

The example data for a feature can be defined by linking back to the feature collection using the [`examples.yaml`](_sources/myFeature/examples.yaml) within the [`myFeature`](_sources/myFeature) definitions.

The first feature within the feature collection carries the coordinate reference system as an extra property. Without this definition, the example feature could not be viewed within the ["map view"](https://ogcincubator.github.io/bblocks-focal/bblock/ogc.focal.myFeature/examples) of the feature example.

The example data for the domain-specific schema can also be defined by linking to the feature collection example using its [`examples.yaml`](_sources/mySchema/examples.yaml) within the [`mySchema`](_sources/mySchema) definitions.


## 6. Transform to Match CRS 5555

A transform can be added by creating a [`transforms.yaml`](_sources/myFeatureCollection/transforms.yaml). It is possible to provide the code snippet directly within this file, but for reasons of clarity the code has been outsourced to the [`transforms`](_sources/myFeatureCollection/transforms) folder can be linked as shown in the [`transforms.yaml`](_sources/myFeatureCollection/transforms.yaml).


## 7. Validation

Validation and testing can be carried out using [SHACL shapes](_sources/myFeature/shapes.shacl). The provided example checks if the `focal-prop:lesniTyp` exists for the given examples. By providing failure examples ([`FeatureCollection`](_sources/myFeatureCollection/tests/feature-fail.json), [`Feature`](_sources/myFeature/tests/feature-fail.json)), the SHACL shapes can be tested further.


