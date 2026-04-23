
# My Schema (Schema)

`ogc.focal.mySchema` *v0.1*

An example schema defining the set of properties of any type of object.

[*Status*](http://www.opengis.net/def/status): Under development

## Description

## My Schema

Defines a set of properties that may be used in **any** JSON schema.

> Note these properties may be used in the "properties" sub-component of a GeoJSON object, as a simple object

## Examples

### This is an example with just a description and no code snippets.
This an example.

In **Markdown** format.
#### json
```json
{
  "LT": "2S1",
  "LES_OBL": 8,
  "LO_CAST": "a",
  "UDRZBA": 2022,
  "ZMENA": "Uveden\u00ed do souladu s KN",
  "ZADOST": "-",
  "CHS": 25,
  "PCHS": "25a",
  "OVER_T": "NE",
  "ROK_MAP": 2015,
  "ID1": 128301,
  "SLT": "2S",
  "PLOCHA": 1224.24963,
  "DS_OPRL": 2025
}
```

#### jsonld
```jsonld
{
  "@context": [
    {
      "mynamespace": "http://example.com/mythings/"
    },
    "https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/mySchema/context.jsonld"
  ],
  "LT": "2S1",
  "LES_OBL": 8,
  "LO_CAST": "a",
  "UDRZBA": 2022,
  "ZMENA": "Uveden\u00ed do souladu s KN",
  "ZADOST": "-",
  "CHS": 25,
  "PCHS": "25a",
  "OVER_T": "NE",
  "ROK_MAP": 2015,
  "ID1": 128301,
  "SLT": "2S",
  "PLOCHA": 1224.24963,
  "DS_OPRL": 2025
}
```

#### ttl
```ttl
@prefix focal-prop: <https://w3id.org/ogc/hosted/focal/properties/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

[] focal-prop:lesniCHS 25 ;
    focal-prop:lesniDSOPRL 2025 ;
    focal-prop:lesniID1 128301 ;
    focal-prop:lesniOVERT "NE" ;
    focal-prop:lesniOblast 8 ;
    focal-prop:lesniOblastCast "a" ;
    focal-prop:lesniPCHS "25a" ;
    focal-prop:lesniPLOCHA 1.22425e+03 ;
    focal-prop:lesniROKMAP 2015 ;
    focal-prop:lesniSLT "2S" ;
    focal-prop:lesniTyp <https://w3id.org/ogc/hosted/focal/lt/2S1> ;
    focal-prop:lesniUDRZBA 2022 ;
    focal-prop:lesniZADOST "-" ;
    focal-prop:lesniZMENA "Uvedení do souladu s KN" .


```

## Schema

```yaml
$schema: https://json-schema.org/draft/2020-12/schema
description: My example schema
type: object
properties:
  LT:
    type: string
    x-jsonld-id: https://w3id.org/ogc/hosted/focal/properties/lesniTyp
    x-jsonld-type: '@id'
    x-jsonld-base: https://w3id.org/ogc/hosted/focal/lt/
  LES_OBL:
    type: number
    x-jsonld-id: https://w3id.org/ogc/hosted/focal/properties/lesniOblast
  LO_CAST:
    type: string
    x-jsonld-id: https://w3id.org/ogc/hosted/focal/properties/lesniOblastCast
  UDRZBA:
    type: number
    x-jsonld-id: https://w3id.org/ogc/hosted/focal/properties/lesniUDRZBA
  ZMENA:
    type: string
    x-jsonld-id: https://w3id.org/ogc/hosted/focal/properties/lesniZMENA
  ZADOST:
    type: string
    x-jsonld-id: https://w3id.org/ogc/hosted/focal/properties/lesniZADOST
  CHS:
    type: number
    x-jsonld-id: https://w3id.org/ogc/hosted/focal/properties/lesniCHS
  PCHS:
    type: string
    x-jsonld-id: https://w3id.org/ogc/hosted/focal/properties/lesniPCHS
  OVER_T:
    type: string
    x-jsonld-id: https://w3id.org/ogc/hosted/focal/properties/lesniOVERT
  ROK_MAP:
    type: number
    x-jsonld-id: https://w3id.org/ogc/hosted/focal/properties/lesniROKMAP
  ID1:
    type: number
    x-jsonld-id: https://w3id.org/ogc/hosted/focal/properties/lesniID1
  SLT:
    type: string
    x-jsonld-id: https://w3id.org/ogc/hosted/focal/properties/lesniSLT
  PLOCHA:
    type: number
    x-jsonld-id: https://w3id.org/ogc/hosted/focal/properties/lesniPLOCHA
  DS_OPRL:
    type: number
    x-jsonld-id: https://w3id.org/ogc/hosted/focal/properties/lesniDSOPRL
required:
- LT
x-jsonld-prefixes:
  focal-prop: https://w3id.org/ogc/hosted/focal/properties/

```

Links to the schema:

* YAML version: [schema.yaml](https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/mySchema/schema.json)
* JSON version: [schema.json](https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/mySchema/schema.yaml)


# JSON-LD Context

```jsonld
{
  "@context": {
    "LT": {
      "@context": {
        "@base": "https://w3id.org/ogc/hosted/focal/lt/"
      },
      "@id": "focal-prop:lesniTyp",
      "@type": "@id"
    },
    "LES_OBL": "focal-prop:lesniOblast",
    "LO_CAST": "focal-prop:lesniOblastCast",
    "UDRZBA": "focal-prop:lesniUDRZBA",
    "ZMENA": "focal-prop:lesniZMENA",
    "ZADOST": "focal-prop:lesniZADOST",
    "CHS": "focal-prop:lesniCHS",
    "PCHS": "focal-prop:lesniPCHS",
    "OVER_T": "focal-prop:lesniOVERT",
    "ROK_MAP": "focal-prop:lesniROKMAP",
    "ID1": "focal-prop:lesniID1",
    "SLT": "focal-prop:lesniSLT",
    "PLOCHA": "focal-prop:lesniPLOCHA",
    "DS_OPRL": "focal-prop:lesniDSOPRL",
    "focal-prop": "https://w3id.org/ogc/hosted/focal/properties/",
    "@version": 1.1
  }
}
```

You can find the full JSON-LD context here:
[context.jsonld](https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/mySchema/context.jsonld)

## Sources

* [Sample source document](https://example.com/sources/1)

# For developers

The source code for this Building Block can be found in the following repository:

* URL: [https://github.com/ogcincubator/bblocks-focal](https://github.com/ogcincubator/bblocks-focal)
* Path: `_sources/mySchema`

