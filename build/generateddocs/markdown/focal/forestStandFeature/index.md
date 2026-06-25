
# FOCAL Forest Stand Feature (Schema)

`ogc.focal.forestStandFeature` *v1.0*

GeoJSON Feature representing a spatially delineated forest stand classified according to the FOCAL forest typology system, with properties describing forest type, region, management unit, area, and data provenance.

[*Status*](http://www.opengis.net/def/status): Under development

## Description

## Custom Feature Type 

This building block illustrates a typical "Feature Type" - where an object is modelled as a "Feature with geometry", but has its own "native schema" - or "domain model".

This is an **interoperable** approach to defining a Feature, allowing re-use of a well-defined domain model.

i.e. the attributes (properties) are managed independently of the packaging container (Feature) 

the **mySchema" building block is referenced by this container, complete with an example of semantic annotations for the domain model.  It may inherit reusable sub-components using the same mechanisms - after all there is usually a lot in common across a range of FeatureTypes in any environment.  

This building block **inherits** reusable semantic annotations from a common library, simplifying implementation. 




## Examples

### GeoJSON - specialisation example.
This examples shows how to define a customised schema based on an existing building block - in this case the *OGC API Features* basic GeoJSON Feature response
#### json
```json
{
  "type": "Feature",
  "crs": {
    "type": "name",
    "properties": {
      "name": "urn:ogc:def:crs:EPSG::5514"
    }
  },
  "properties": {
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
  },
  "geometry": {
    "type": "MultiPolygon",
    "coordinates": [
      [
        [
          [
            -785371.8095452676,
            -1062509.789513851
          ],
          [
            -785367.0195452989,
            -1062497.0295136066
          ],
          [
            -785331.7395455441,
            -1062484.7895138361
          ],
          [
            -785328.9995457674,
            -1062483.8395130674
          ],
          [
            -785327.3695456531,
            -1062483.2695133782
          ],
          [
            -785323.1095454189,
            -1062481.859513526
          ],
          [
            -785321.3095452319,
            -1062483.119513762
          ],
          [
            -785319.6595456105,
            -1062484.2795136091
          ],
          [
            -785312.5495449909,
            -1062481.649514441
          ],
          [
            -785304.0695454476,
            -1062478.5095131495
          ],
          [
            -785297.8597342281,
            -1062470.8605682855
          ],
          [
            -785292.4935223358,
            -1062477.384270917
          ],
          [
            -785282.5179010982,
            -1062488.6637585284
          ],
          [
            -785284.2195450471,
            -1062489.2795136191
          ],
          [
            -785339.9495455844,
            -1062502.819514532
          ],
          [
            -785371.8095452676,
            -1062509.789513851
          ]
        ]
      ]
    ]
  }
}
```

#### jsonld
```jsonld
{
  "@context": [
    {
      "mynamespace": "http://example.com/mythings/"
    },
    "https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/forestStandFeature/context.jsonld"
  ],
  "type": "Feature",
  "crs": {
    "type": "name",
    "properties": {
      "name": "urn:ogc:def:crs:EPSG::5514"
    }
  },
  "properties": {
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
  },
  "geometry": {
    "type": "MultiPolygon",
    "coordinates": [
      [
        [
          [
            -785371.8095452676,
            -1062509.789513851
          ],
          [
            -785367.0195452989,
            -1062497.0295136066
          ],
          [
            -785331.7395455441,
            -1062484.7895138361
          ],
          [
            -785328.9995457674,
            -1062483.8395130674
          ],
          [
            -785327.3695456531,
            -1062483.2695133782
          ],
          [
            -785323.1095454189,
            -1062481.859513526
          ],
          [
            -785321.3095452319,
            -1062483.119513762
          ],
          [
            -785319.6595456105,
            -1062484.2795136091
          ],
          [
            -785312.5495449909,
            -1062481.649514441
          ],
          [
            -785304.0695454476,
            -1062478.5095131495
          ],
          [
            -785297.8597342281,
            -1062470.8605682855
          ],
          [
            -785292.4935223358,
            -1062477.384270917
          ],
          [
            -785282.5179010982,
            -1062488.6637585284
          ],
          [
            -785284.2195450471,
            -1062489.2795136191
          ],
          [
            -785339.9495455844,
            -1062502.819514532
          ],
          [
            -785371.8095452676,
            -1062509.789513851
          ]
        ]
      ]
    ]
  }
}
```

#### ttl
```ttl
@prefix focal-prop: <https://w3id.org/ogc/hosted/focal/properties/> .
@prefix geojson: <https://purl.org/geojson/vocab#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

[] a geojson:Feature ;
    geojson:geometry [ a geojson:MultiPolygon ;
            geojson:coordinates ( ( ( ( -7.853718e+05 -1.06251e+06 ) ( -7.85367e+05 -1.062497e+06 ) ( -7.853317e+05 -1.062485e+06 ) ( -7.85329e+05 -1.062484e+06 ) ( -7.853274e+05 -1.062483e+06 ) ( -7.853231e+05 -1.062482e+06 ) ( -7.853213e+05 -1.062483e+06 ) ( -7.853197e+05 -1.062484e+06 ) ( -7.853125e+05 -1.062482e+06 ) ( -7.853041e+05 -1.062479e+06 ) ( -7.852979e+05 -1.062471e+06 ) ( -7.852925e+05 -1.062477e+06 ) ( -7.852825e+05 -1.062489e+06 ) ( -7.852842e+05 -1.062489e+06 ) ( -7.853399e+05 -1.062503e+06 ) ( -7.853718e+05 -1.06251e+06 ) ) ) ) ] ;
    focal-prop:lesniCHS 25 ;
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
description: Example of a simple GeoJSON Feature specialisation
$defs:
  MyFeature:
    allOf:
    - $ref: https://opengeospatial.github.io/bblocks/annotated-schemas/geo/features/feature/schema.yaml
    - properties:
        properties:
          $ref: https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/forestStandProperties/schema.yaml
anyOf:
- $ref: '#/$defs/MyFeature'

```

Links to the schema:

* YAML version: [schema.yaml](https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/forestStandFeature/schema.json)
* JSON version: [schema.json](https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/forestStandFeature/schema.yaml)


# JSON-LD Context

```jsonld
{
  "@context": {
    "Feature": "geojson:Feature",
    "FeatureCollection": "geojson:FeatureCollection",
    "GeometryCollection": "geojson:GeometryCollection",
    "LineString": "geojson:LineString",
    "MultiLineString": "geojson:MultiLineString",
    "MultiPoint": "geojson:MultiPoint",
    "MultiPolygon": "geojson:MultiPolygon",
    "Point": "geojson:Point",
    "Polygon": "geojson:Polygon",
    "features": {
      "@container": "@set",
      "@id": "geojson:features"
    },
    "type": "@type",
    "id": "@id",
    "properties": "@nest",
    "geometry": {
      "@context": {
        "coordinates": {
          "@container": "@list",
          "@id": "geojson:coordinates"
        }
      },
      "@id": "geojson:geometry"
    },
    "bbox": {
      "@container": "@list",
      "@id": "geojson:bbox"
    },
    "links": {
      "@context": {
        "href": {
          "@type": "@id",
          "@id": "oa:hasTarget"
        },
        "rel": {
          "@context": {
            "@base": "http://www.iana.org/assignments/relation/"
          },
          "@id": "http://www.iana.org/assignments/relation",
          "@type": "@id"
        },
        "type": "dct:type",
        "hreflang": "dct:language",
        "title": "rdfs:label",
        "length": "dct:extent"
      },
      "@id": "rdfs:seeAlso"
    },
    "geojson": "https://purl.org/geojson/vocab#",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "oa": "http://www.w3.org/ns/oa#",
    "dct": "http://purl.org/dc/terms/",
    "focal-prop": "https://w3id.org/ogc/hosted/focal/properties/",
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
    "@version": 1.1
  }
}
```

You can find the full JSON-LD context here:
[context.jsonld](https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/forestStandFeature/context.jsonld)

## Sources

* [OGC API - Features, Part 1, 7.16.2: Feature Response](https://docs.ogc.org/is/17-069r3/17-069r3.html#_response_7)

# For developers

The source code for this Building Block can be found in the following repository:

* URL: [https://github.com/ogcincubator/bblocks-focal](https://github.com/ogcincubator/bblocks-focal)
* Path: `_sources/forestStandFeature`

