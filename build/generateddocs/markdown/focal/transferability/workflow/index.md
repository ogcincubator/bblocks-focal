
# FOCAL Transferability Workflow (Schema)

`ogc.focal.transferability.workflow` *v0.18*

Profile of a CWL Workflow adding FOCAL's machine-readable transferability facts: a transferability statement (validity envelope, reference/calibration-artifact adaptation rules), computation type, maturity status, and quality annotations.

[*Status*](http://www.opengis.net/def/status): Under development

## Description

## FOCAL Transferability Workflow

The workflow-level aggregator: profiles a CWL Workflow
([`ogc.cwl.v1_2_1.CWLWorkflow`](bblocks://ogc.cwl.v1_2_1.CWLWorkflow)) with FOCAL's transferability
model.

| Property | Cardinality | Source block |
|---|---|---|
| `transferability` | required (single object) | [`transferabilityStatement`](bblocks://ogc.focal.transferability.transferabilityStatement) |
| `computationType` | optional | [`computationType`](bblocks://ogc.focal.transferability.computationType) |
| `maturityStatus` | required | [`maturityStatus`](bblocks://ogc.focal.transferability.maturityStatus) |
| `qualityAnnotation` | optional, repeatable | [`qualityAnnotation`](bblocks://ogc.focal.transferability.qualityAnnotation) |

**Why `transferability` is its own nested object, not flattened here.** `envelope`, `artifacts`
and `rules` — the actual portability boundary — live in
[`transferabilityStatement`](bblocks://ogc.focal.transferability.transferabilityStatement), a
standalone bundle this block attaches under one `transferability` property, rather than merging
those properties directly onto the CWL Workflow profile. `computationType`, `maturityStatus`, and
`qualityAnnotation` describe the workflow's implementation and result quality generally, not its
portability boundary, so they stay outside that bundle and attach here directly instead.

**Status: draft/WIP**, seven worked examples covering seven of FOCAL's eight pilot workflows (the eighth is in `observingSystem`)
(FP-WF1, FP-WF2, FP-WF3, FP-WF5, UP-WF1, UP-WF2, UP-WF3). Between them they exercise every branch
point in the model: multiple simultaneous envelope roles, OR-set actions, an optional/degrading
rule (`mandatory: false`), the `component-not-executable` terminal outcome with `affects`, one rule
shared across several artifacts, a two-rule cascade over a single constraint, an evidenced temporal
envelope entry, the `grid-structure` dimension, an artifact-level `acceptanceCriteria` contract,
a positive statement that
no training or calibration data is needed (`trainingRequired: false`), and caveats about results
that are neither maturity nor a boundary (`qualityAnnotation`).

**FP-WF1, FP-WF2 and FP-WF5 are converted from the owners' own records** of 2026-11-18. They
declare CWL inputs (user choices, supplied data, shipped defaults) that `artifactRef` and
`inputRef` point at; those declarations await the owners' confirmation.

**Extents the owners did not state are assumed, not left empty.** Where a questionnaire names a
place without giving its boundary (for example the historical labels or the DWD stations), the example
uses a coarse polygon, usually the country's simplified border, and treats it as a hard boundary.
There is no fuzzy or confidence value on a geometry: a consumer that wants a wider margin widens the
polygon. Each assumed polygon says what it stands in for in its note, and the workflow owners are
asked to correct any that is wrong and to supply a better polygon.

**The eighth, FP-WF4, is not a CWL Workflow at all** but a SensLog observation store, so it cannot
profile `ogc.cwl.v1_2_1.CWLWorkflow`. It is modeled with the sibling block
[`observingSystem`](bblocks://ogc.focal.transferability.observingSystem), which carries the same
`transferabilityStatement` and deliberately no `computationType` and no `maturityStatus`.

Circulated to the pilot workflow owners for review in September 2026; nothing here is locked.

## Examples

### FP-WF1 — Tree growth prediction (training domain, species, shipped model)
A trained model with its training area, the value ranges it was trained on (`input-domain`) and the species it covers. The CWL inputs say what the user chooses, what data is supplied and what ships with the workflow as a default; `artifactRef` and `inputRef` point at them. Converted from the owners' record of 2026-11-18; input declarations are pending the owners' confirmation.

#### json
```json
{
  "class": "Workflow",
  "cwlVersion": "v1.2",
  "id": "",
  "label": "FWF1 - Tree growth prediction (FOCAL Forest Pilot)",
  "doc": [
    "Projects the yearly height growth of an existing forest stand to its rotation age under a chosen climate source, with bootstrap uncertainty and a yearly stress index against the 1991-2020 climate. The growth model was trained on Czech National Forest Inventory stands.",
    "Transferability record of workflow FP-WF1 (FWF1), record date 2026-11-18. Record basis: FWF1 API, focal_predict.py, wf1 climate/soil/terrain input functions, Rasdaman registry 1.1.8, focal_tree_growth repository (final downscaled model, feature documentation, report). Converted from the delivered record on 2026-11-25. Descriptive CWL profile: no steps are declared and the input and output identifiers are not yet those of an executable Application Package."
  ],
  "$namespaces": {
    "s": "https://schema.org/"
  },
  "s:identifier": "FP-WF1",
  "s:alternateName": "FWF1",
  "s:dateCreated": "2026-11-18",
  "requirements": {
    "SoftwareRequirement": {
      "packages": [
        {
          "package": "python"
        },
        {
          "package": "scikit-learn",
          "version": [
            "1.9.1"
          ]
        },
        {
          "package": "lightgbm",
          "version": [
            "4.7.0"
          ]
        },
        {
          "package": "flask"
        }
      ]
    },
    "NetworkAccess": {
      "networkAccess": true
    }
  },
  "inputs": {
    "latitude": {
      "type": "double",
      "label": "Latitude of the stand",
      "doc": "Latitude of the forest stand in decimal degrees (WGS 84). Soil, terrain and climate features are derived for this point. The Copernicus DEM reaches 89 degrees."
    },
    "longitude": {
      "type": "double",
      "label": "Longitude of the stand",
      "doc": "Longitude of the forest stand in decimal degrees (WGS 84)."
    },
    "species": {
      "type": {
        "type": "enum",
        "symbols": [
          "smrk",
          "borovice",
          "dub",
          "buk"
        ]
      },
      "label": "Tree species",
      "doc": "Species of the stand. Only these four are accepted: smrk = Norway spruce (Picea abies), borovice = Scots pine (Pinus sylvestris), dub = pedunculate oak (Quercus robur), buk = European beech (Fagus sylvatica)."
    },
    "age": {
      "type": "int",
      "label": "Stand age (years)",
      "doc": "Current age of the stand. Accepted from 16 years up to the rotation age of the species minus one."
    },
    "current_height": {
      "type": "float?",
      "label": "Current stand height (m)",
      "doc": "Current mean height of the stand in metres. If omitted, a typical height for the species and age is taken from the reference growth curves."
    },
    "rasdaman_connection": {
      "type": "string",
      "label": "Data cube connection",
      "doc": "How to reach the Rasdaman instance that holds the climate data (queried with rasql over SSH). The connection variables are not named in the delivered material, so one string stands for them; we assume credentials are supplied by the execution environment."
    },
    "rasdaman_registry": {
      "type": "File",
      "label": "Data cube registry",
      "doc": "rasdaman_registry.json for that instance. The FOCAL registry is not transferable as is."
    },
    "stress_threshold": {
      "type": "float?",
      "label": "Stress index threshold",
      "doc": "Manual threshold on the stress index SI for flagging stress years. If omitted, the species- and age-specific thresholds shipped with the workflow are used."
    },
    "rotation_age_spruce": {
      "type": "int",
      "label": "Rotation age of Norway spruce (years)",
      "doc": "Age up to which growth of Norway spruce is projected. The default is the Czech forest management convention; set it for the country of the stand.",
      "default": 110
    },
    "rotation_age_pine": {
      "type": "int",
      "label": "Rotation age of Scots pine (years)",
      "doc": "Age up to which growth of Scots pine is projected. The default is the Czech forest management convention; set it for the country of the stand.",
      "default": 110
    },
    "rotation_age_oak": {
      "type": "int",
      "label": "Rotation age of pedunculate oak (years)",
      "doc": "Age up to which growth of pedunculate oak is projected. The default is the Czech forest management convention; set it for the country of the stand.",
      "default": 140
    },
    "rotation_age_beech": {
      "type": "int",
      "label": "Rotation age of European beech (years)",
      "doc": "Age up to which growth of European beech is projected. The default is the Czech forest management convention; set it for the country of the stand.",
      "default": 130
    },
    "growth_model": {
      "type": "Directory",
      "label": "Trained growth model",
      "doc": "LightGBM pipeline (central model and bootstrap ensemble) fitted to Czech National Forest Inventory data. Ships with the workflow.",
      "default": {
        "class": "Directory",
        "location": "growth_model"
      }
    },
    "reference_increment": {
      "type": "File",
      "label": "Reference growth curves",
      "doc": "Typical height and increment per species and age (Czech NFI medians). Ships with the workflow.",
      "default": {
        "class": "File",
        "location": "reference_increment_d.csv"
      }
    },
    "stress_thresholds": {
      "type": "File",
      "label": "Stress thresholds table",
      "doc": "Stress index threshold per species and age (90th percentile of SI, 1991-2020, Czech NFI sites). Ships with the workflow.",
      "default": {
        "class": "File",
        "location": "stress_thresholds_d.csv"
      }
    }
  },
  "outputs": {
    "growth_projection": {
      "type": "File",
      "label": "Growth projection",
      "doc": "Yearly height and increment with 2.5-97.5 % bootstrap bands."
    },
    "stress_assessment": {
      "type": "File",
      "label": "Stress assessment",
      "doc": "Stress index SI = 1 - I / I_ref against the 1991-2020 climate, stress years and their share across bootstrap members."
    },
    "typical_growth": {
      "type": "File",
      "label": "Typical growth",
      "doc": "Typical height and increment of the species."
    },
    "period_summary": {
      "type": "File",
      "label": "Period summary",
      "doc": "Summary over the projected period."
    }
  },
  "steps": {},
  "transferability": {
    "trainingRequired": true,
    "transferabilityNotes": "Envelope entries and rules that only described which data FOCAL currently holds, or its platform, are not part of this statement; what they said is kept in the notes of the artifacts concerned. An area or period for which no data is at hand is a matter of providing data (as delivered, in the data cube) that meets the artifact's criteria. The delivered record also notes: temporal extent is the year range of each collection, read from Rasdaman at runtime. Delivered coverage fact: SoilGrids and Copernicus DEM are global; the API runs wherever the climate collections cover the point and does not restrict to Czechia or to forest land.",
    "envelope": [
      {
        "id": "czech-nfi-plots",
        "role": "trained-on",
        "dimension": "spatial",
        "value": {
          "asWKT": "POLYGON((12.2444 48.6232, 18.815 48.6232, 18.815 51.0198, 12.2444 51.0198, 12.2444 48.6232))"
        },
        "inputRef": [
          "/inputs/latitude",
          "/inputs/longitude"
        ],
        "transferabilityNotes": "Bounding box of the 1,756 Czech NFI (UHUL) monitoring stands used for training (1964-2025). Validation: spatial hold-out of 160 Czech stands, 2015-2025."
      },
      {
        "id": "czech-nfi-period",
        "role": "trained-on",
        "dimension": "temporal",
        "value": {
          "startDate": "1964",
          "endDate": "2025"
        },
        "transferabilityNotes": "Training rows before 2015, test rows 2015-2025."
      },
      {
        "id": "training-feature-domain",
        "role": "valid-for",
        "dimension": "input-domain",
        "value": {
          "variables": [
            {
              "name": "age",
              "unit": "years",
              "min": 24.0,
              "max": 144.0
            },
            {
              "name": "elevation",
              "unit": "m a.s.l.",
              "min": 175.0,
              "max": 1150.0
            },
            {
              "name": "slope",
              "unit": "degrees",
              "min": 0.4369,
              "max": 27.0
            },
            {
              "name": "avg_h_lag",
              "unit": "m",
              "min": 9.99,
              "max": 37.67
            },
            {
              "name": "N_0_5",
              "unit": "cg/kg",
              "min": 518.0,
              "max": 1096.0
            },
            {
              "name": "N_5_15",
              "unit": "cg/kg",
              "min": 161.0,
              "max": 673.0
            },
            {
              "name": "N_15_30",
              "unit": "cg/kg",
              "min": 115.0,
              "max": 411.0
            },
            {
              "name": "N_30_60",
              "unit": "cg/kg",
              "min": 72.0,
              "max": 296.0
            },
            {
              "name": "C",
              "unit": "dg/kg",
              "min": 193.2,
              "max": 825.5
            },
            {
              "name": "pH",
              "unit": "pH × 10",
              "min": 47.75,
              "max": 65.0
            },
            {
              "name": "clay",
              "unit": "g/kg",
              "min": 142.5,
              "max": 339.2
            },
            {
              "name": "T_year",
              "unit": "°C",
              "min": 3.705,
              "max": 10.17
            },
            {
              "name": "T_autumn",
              "unit": "°C",
              "min": 4.207,
              "max": 11.06
            },
            {
              "name": "T_min_month",
              "unit": "°C",
              "min": -10.54,
              "max": 1.298
            },
            {
              "name": "T_amplitude",
              "unit": "°C",
              "min": 16.26,
              "max": 27.91
            },
            {
              "name": "T_veg_lag_1",
              "unit": "°C",
              "min": 9.507,
              "max": 16.53
            },
            {
              "name": "T_autumn_lag_1",
              "unit": "°C",
              "min": 4.183,
              "max": 10.92
            },
            {
              "name": "T_min_month_lag_1",
              "unit": "°C",
              "min": -10.54,
              "max": 1.249
            },
            {
              "name": "T_amplitude_lag_1",
              "unit": "°C",
              "min": 16.25,
              "max": 27.92
            },
            {
              "name": "SR_veg",
              "unit": "W/m²",
              "min": 136.8,
              "max": 181.5
            },
            {
              "name": "SR_spring",
              "unit": "W/m²",
              "min": 112.5,
              "max": 166.3
            },
            {
              "name": "SR_veg_lag_1",
              "unit": "W/m²",
              "min": 136.4,
              "max": 181.4
            },
            {
              "name": "SR_spring_lag_1",
              "unit": "W/m²",
              "min": 112.0,
              "max": 166.3
            },
            {
              "name": "P_spring",
              "unit": "mm",
              "min": 97.33,
              "max": 371.2
            },
            {
              "name": "P_summer",
              "unit": "mm",
              "min": 136.4,
              "max": 549.6
            },
            {
              "name": "P_prev_late",
              "unit": "mm",
              "min": 97.56,
              "max": 412.0
            },
            {
              "name": "P_spring_lag_1",
              "unit": "mm",
              "min": 99.11,
              "max": 370.3
            },
            {
              "name": "P_summer_lag_1",
              "unit": "mm",
              "min": 137.4,
              "max": 550.9
            },
            {
              "name": "P_prev_late_lag_1",
              "unit": "mm",
              "min": 98.32,
              "max": 413.7
            },
            {
              "name": "SPI_3_summer",
              "unit": "z-score",
              "min": -2.008,
              "max": 2.483
            },
            {
              "name": "SPI_3_summer_lag_1",
              "unit": "z-score",
              "min": -2.009,
              "max": 2.515
            },
            {
              "name": "Tmax_Jul",
              "unit": "°C",
              "min": 15.65,
              "max": 26.7
            },
            {
              "name": "Tmax_Jul_lag_1",
              "unit": "°C",
              "min": 15.63,
              "max": 26.67
            },
            {
              "name": "Tmax_Aug",
              "unit": "°C",
              "min": 15.88,
              "max": 26.73
            },
            {
              "name": "Tmax_Aug_lag_1",
              "unit": "°C",
              "min": 15.88,
              "max": 26.59
            },
            {
              "name": "HD30_veg",
              "unit": "days",
              "min": 0.0,
              "max": 12.0
            },
            {
              "name": "HD30_veg_lag_1",
              "unit": "days",
              "min": 0.0,
              "max": 12.0
            },
            {
              "name": "FD_AprMay",
              "unit": "days",
              "min": 0.0,
              "max": 28.0
            },
            {
              "name": "FD_AprMay_lag_1",
              "unit": "days",
              "min": 0.0,
              "max": 29.0
            },
            {
              "name": "FD_winter_std",
              "unit": "days",
              "min": 45.0,
              "max": 90.0
            },
            {
              "name": "FD_winter_std_lag_1",
              "unit": "days",
              "min": 44.0,
              "max": 90.0
            },
            {
              "name": "R10mm_veg",
              "unit": "days",
              "min": 3.0,
              "max": 31.0
            },
            {
              "name": "R10mm_veg_lag_1",
              "unit": "days",
              "min": 3.0,
              "max": 31.0
            }
          ]
        },
        "inputRef": [
          "/inputs/latitude",
          "/inputs/longitude",
          "/inputs/age",
          "/inputs/current_height"
        ],
        "transferabilityNotes": "1st-99th percentile of 30,883 training stand-years (final model). Outside, the tree-based model repeats edge behaviour; predictions are extrapolation. A per-species area-of-applicability check exists in the modelling code but is not run by the API. Bounds are the 1st and 99th percentiles. The categorical variable aspect (NFI code) is not a range and is not listed in the value; the delivered 1st-99th percentile codes were 100 to 900."
      },
      {
        "id": "trained-species",
        "role": "valid-for",
        "dimension": "ecological",
        "value": {
          "scheme": "gbif-backbone",
          "classes": [
            "Picea abies",
            "Pinus sylvestris",
            "Quercus robur",
            "Fagus sylvatica"
          ]
        },
        "inputRef": "/inputs/species",
        "transferabilityNotes": "Only these four species are accepted by the API."
      },
      {
        "id": "dem-coverage",
        "role": "can-run-on",
        "dimension": "spatial",
        "value": {
          "asWKT": "POLYGON((-180 -89, 180 -89, 180 89, -180 89, -180 -89))"
        },
        "transferabilityNotes": "Coverage of the Copernicus DEM (artifact copernicus-dem), up to 89 degrees latitude."
      },
      {
        "id": "czech-jurisdiction",
        "role": "valid-for",
        "dimension": "jurisdictional",
        "value": {
          "asWKT": "POLYGON((12.07 48.48, 18.97 48.48, 18.97 51.08, 12.07 51.08, 12.07 48.48))"
        },
        "inputRef": [
          "/inputs/latitude",
          "/inputs/longitude"
        ],
        "transferabilityNotes": "Where the Czech forest management convention for rotation ages applies. The box is the FOCAL Czechia box, an approximation of the national territory."
      }
    ],
    "artifacts": [
      {
        "id": "growth-model",
        "artifact": "LightGBM pipeline (central model + bootstrap ensemble), 45 inputs (training_feature_set_d.txt)",
        "artifactRole": "workflow-input",
        "artifactRef": "/inputs/growth_model",
        "transferabilityNotes": "A replacement model takes 45 inputs in fixed order (training_feature_set_d.txt): age, elevation, aspect, slope, avg_h_lag, N_0_5, N_5_15, N_15_30, N_30_60, C, pH, clay, T_year, T_autumn, T_min_month, T_amplitude, T_veg_lag_1, T_autumn_lag_1, T_min_month_lag_1, T_amplitude_lag_1, SR_veg, SR_spring, SR_veg_lag_1, SR_spring_lag_1, P_spring, P_summer, P_prev_late, P_spring_lag_1, P_summer_lag_1, P_prev_late_lag_1, SPI_3_summer, SPI_3_summer_lag_1, Tmax_Jul, Tmax_Jul_lag_1, Tmax_Aug, Tmax_Aug_lag_1, HD30_veg, HD30_veg_lag_1, FD_AprMay, FD_AprMay_lag_1, FD_winter_std, FD_winter_std_lag_1, R10mm_veg, R10mm_veg_lag_1, species. Software: scikit-learn 1.9.1, LightGBM 4.7.0. Used by (delivered step names): growth-simulation, stress-index."
      },
      {
        "id": "reference-increment",
        "artifact": "reference_increment_d.csv: typical height and increment per species and age (Czech NFI medians)",
        "artifactRole": "workflow-input",
        "artifactRef": "/inputs/reference_increment",
        "transferabilityNotes": "Per species and age; regenerated by the same pipeline together with the model. Used by (delivered step names): typical-growth, default-initial-height."
      },
      {
        "id": "stress-thresholds",
        "artifact": "stress_thresholds_d.csv: SI threshold per species and age (90th percentile of SI, 1991-2020, Czech NFI sites)",
        "artifactRole": "workflow-input",
        "artifactRef": [
          "/inputs/stress_thresholds",
          "/inputs/stress_threshold"
        ],
        "transferabilityNotes": "Per species and age; regenerated by the same pipeline together with the model. Used by (delivered step names): stress-years."
      },
      {
        "id": "nfi-training-data",
        "artifact": "Czech NFI stand measurements (species, age, mean height, site), 1964-2025",
        "artifactRole": "external-resource",
        "transferabilityNotes": "Not read at inference; needed to retrain. A replacement must give, per stand: species (the species to be modelled), stand age, mean height, coordinates and measurement year, with at least two measurements per stand. The intervals between the Czech measurements were mostly five years. Used by (delivered step names): training.",
        "acceptanceCriteria": {
          "variables": [
            {
              "name": "species"
            },
            {
              "name": "stand age"
            },
            {
              "name": "mean height"
            },
            {
              "name": "coordinates"
            },
            {
              "name": "measurement year"
            }
          ]
        }
      },
      {
        "id": "soilgrids",
        "artifact": "ISRIC SoilGrids 2.0 (Q0.5), nitrogen 4 depths, SOC, pH, clay 0-60 cm, 250 m",
        "artifactRole": "external-resource",
        "acceptanceCriteria": {
          "variables": [
            {
              "name": "nitrogen"
            },
            {
              "name": "soc"
            },
            {
              "name": "phh2o"
            },
            {
              "name": "clay",
              "units": [
                "GM-PER-KiloGM"
              ]
            }
          ],
          "transferabilityNotes": "Same product required; raw SoilGrids units are part of the model contract: nitrogen in cg/kg, soc in dg/kg, phh2o as pH x 10, clay in g/kg. Depths: nitrogen at 0-5, 5-15, 15-30 and 30-60 cm; soc, pH and clay 0-60 cm."
        },
        "transferabilityNotes": "Global; fetched live from ISRIC (WCS or WebDAV) with a local cache, so nothing has to be prepared or supplied. Used by (delivered step names): site-features."
      },
      {
        "id": "copernicus-dem",
        "artifact": "Copernicus DEM GLO-30, elevation and 11 x 11 plane-fit slope/aspect",
        "artifactRole": "external-resource",
        "transferabilityNotes": "Same product only; the slope method is calibrated to it. Resolution 1 arc-second, vertical datum EGM2008. Aspect coding: 100 flat (slope <= 5 deg), 200-900 N..NW. Global (up to 89 degrees latitude); fetched live from AWS with a local cache, so nothing has to be prepared or supplied. Used by (delivered step names): site-features."
      },
      {
        "id": "historical-climate",
        "artifact": "ERA5-Land daily temperature (min/mean/max), precipitation, net SSR",
        "artifactRole": "workflow-input",
        "acceptanceCriteria": {
          "variables": [
            {
              "name": "tmin",
              "units": [
                "DEG_C"
              ],
              "standardName": "air_temperature"
            },
            {
              "name": "tmean",
              "units": [
                "DEG_C"
              ],
              "standardName": "air_temperature"
            },
            {
              "name": "tmax",
              "units": [
                "DEG_C"
              ],
              "standardName": "air_temperature"
            },
            {
              "name": "pr",
              "units": [
                "MilliM-PER-DAY"
              ]
            },
            {
              "name": "ssr",
              "units": [
                "J-PER-M2",
                "W-PER-M2"
              ],
              "standardName": [
                "surface_net_downward_shortwave_flux",
                "integral_wrt_time_of_surface_net_downward_shortwave_flux"
              ]
            }
          ],
          "temporal": {
            "resolution": "P1D",
            "calendar": [
              "standard",
              "gregorian",
              "proleptic_gregorian"
            ],
            "complete": true,
            "startDate": "1991"
          },
          "axes": [
            "time"
          ],
          "gridTypes": [
            "regular-latlon",
            "rotated-pole",
            "curvilinear"
          ],
          "transferabilityNotes": "Structure: daily [day, y, x]; temperature as a struct cell (min/mean/max). Curvilinear grids need 2D latitude/longitude. ssr is net shortwave radiation, either in J/m2 per day (24-h accumulation assigned to UTC day D) or in W/m2; downward rsds/ssrd is not accepted. Non-Gregorian calendars must be harmonised before ingestion (they are rejected by the climate function). No-data is NaN; no gaps are allowed in required windows."
        },
        "transferabilityNotes": "As delivered, the workflow does not take these data as a file: it reads them from the Rasdaman data cube (artifact rasdaman), for the requested area and the years it needs. The delivered material gives no specification of the layout the code expects. Must be on a frame consistent with the training climate (FOCAL downscaled ERA5-Land, about 350 m, elevation-corrected, for temperature and precipitation; ERA5-Land net solar radiation). Within FOCAL: ERA5-Land temperature and precipitation are held for Czechia, Spain and Finland, and daily net SSR is registered for the Czechia grid (delivered box: 12.07-18.97 E, 48.48-51.08 N); elsewhere a routine ERA5-Land run, including net SSR from 1991. Outside FOCAL: Copernicus Climate Data Store. Used by (delivered step names): climate-features, spi-baseline, stress-reference, lag-context."
      },
      {
        "id": "projection-climate",
        "artifact": "Daily projected temperature (min/mean/max), precipitation and net SSR, bias-corrected to the training climate frame",
        "artifactRole": "workflow-input",
        "acceptanceCriteria": {
          "variables": [
            {
              "name": "tmin",
              "units": [
                "DEG_C"
              ],
              "standardName": "air_temperature"
            },
            {
              "name": "tmean",
              "units": [
                "DEG_C"
              ],
              "standardName": "air_temperature"
            },
            {
              "name": "tmax",
              "units": [
                "DEG_C"
              ],
              "standardName": "air_temperature"
            },
            {
              "name": "pr",
              "units": [
                "MilliM-PER-DAY"
              ]
            },
            {
              "name": "ssr",
              "units": [
                "J-PER-M2",
                "W-PER-M2"
              ],
              "standardName": [
                "surface_net_downward_shortwave_flux",
                "integral_wrt_time_of_surface_net_downward_shortwave_flux"
              ]
            }
          ],
          "temporal": {
            "resolution": "P1D",
            "calendar": [
              "standard",
              "gregorian",
              "proleptic_gregorian"
            ],
            "complete": true
          },
          "axes": [
            "time"
          ],
          "gridTypes": [
            "regular-latlon",
            "rotated-pole",
            "curvilinear"
          ],
          "transferabilityNotes": "Structure: daily [day, y, x]; temperature as a struct cell (min/mean/max). Curvilinear grids need 2D latitude/longitude. ssr is net shortwave radiation, either in J/m2 per day (24-h accumulation assigned to UTC day D) or in W/m2; downward rsds/ssrd is not accepted. Non-Gregorian calendars must be harmonised before ingestion (they are rejected by the climate function). No-data is NaN; no gaps are allowed in required windows."
        },
        "transferabilityNotes": "As delivered, the workflow does not take these data as a file: it reads them from the Rasdaman data cube (artifact rasdaman), for the requested area and the years it needs. The delivered material gives no specification of the layout the code expects. Must be bias-corrected to the training climate frame. A projection set with net SSR, corrected to that frame, is required everywhere, including Czechia. FOCAL EUR-11 REMO2020 collections hold temperature and precipitation only. Model development used NEX-GDDP-CMIP6 with rsds x (1 - 0.15) and per-point monthly bias correction (1991-2014). FOCAL downscaled projections are expected in early 2027. Outside FOCAL: CORDEX or NEX-GDDP-CMIP6, including net shortwave radiation. Used by (delivered step names): climate-features. Needed only to project years beyond the historical data (our reading; to be confirmed)."
      },
      {
        "id": "rotation-age-spruce",
        "artifact": "Rotation age of Norway spruce (110 years, Czech convention)",
        "artifactRole": "workflow-input",
        "artifactRef": "/inputs/rotation_age_spruce",
        "transferabilityNotes": "Czech forest management convention. Reported by the delivery as hard-coded in the current API; to be set per country."
      },
      {
        "id": "rotation-age-pine",
        "artifact": "Rotation age of Scots pine (110 years, Czech convention)",
        "artifactRole": "workflow-input",
        "artifactRef": "/inputs/rotation_age_pine",
        "transferabilityNotes": "Czech forest management convention. Reported by the delivery as hard-coded in the current API; to be set per country."
      },
      {
        "id": "rotation-age-oak",
        "artifact": "Rotation age of pedunculate oak (140 years, Czech convention)",
        "artifactRole": "workflow-input",
        "artifactRef": "/inputs/rotation_age_oak",
        "transferabilityNotes": "Czech forest management convention. Reported by the delivery as hard-coded in the current API; to be set per country."
      },
      {
        "id": "rotation-age-beech",
        "artifact": "Rotation age of European beech (130 years, Czech convention)",
        "artifactRole": "workflow-input",
        "artifactRef": "/inputs/rotation_age_beech",
        "transferabilityNotes": "Czech forest management convention. Reported by the delivery as hard-coded in the current API; to be set per country."
      },
      {
        "id": "rasdaman",
        "artifact": "FOCAL Rasdaman data cube (rasql over SSH) and its registry (rasdaman_registry.json)",
        "artifactRole": "infrastructure",
        "artifactRef": [
          "/inputs/rasdaman_connection",
          "/inputs/rasdaman_registry"
        ],
        "transferabilityNotes": "The delivered workflow reads climate data from a Rasdaman instance queried with rasql over SSH, located through rasdaman_registry.json. Another platform needs Rasdaman with the same layout and its own registry, or a custom climate loader returning the 32 annual features (the predictor accepts one). Within FOCAL new collections are configuration entries; the FOCAL registry is not transferable as is. Used by (delivered step names): data-access."
      }
    ],
    "rules": [
      {
        "appliesTo": [
          "growth-model",
          "reference-increment"
        ],
        "when": [
          {
            "constraint": "czech-nfi-plots",
            "test": "outside"
          }
        ],
        "actions": [
          "retrain"
        ],
        "mandatory": true,
        "transferabilityNotes": "Retrain the pipeline on national stand data; regenerate reference curves, stress thresholds and species support."
      },
      {
        "appliesTo": [
          "stress-thresholds"
        ],
        "when": [
          {
            "constraint": "czech-nfi-plots",
            "test": "outside"
          }
        ],
        "actions": [
          "retrain",
          "replace-with-local-equivalent"
        ],
        "mandatory": true,
        "transferabilityNotes": "A manual threshold can be passed per request (input stress_threshold)."
      },
      {
        "appliesTo": [
          "growth-model"
        ],
        "when": [
          {
            "constraint": "training-feature-domain",
            "test": "outside"
          }
        ],
        "actions": [
          "retrain"
        ],
        "mandatory": false,
        "transferabilityNotes": "Inside Czechia, inputs outside the range (e.g. late-century heat days) are extrapolation; flag rather than block."
      },
      {
        "appliesTo": [
          "nfi-training-data"
        ],
        "when": [
          {
            "constraint": "czech-nfi-plots",
            "test": "outside"
          }
        ],
        "actions": [
          "replace-with-local-equivalent"
        ],
        "mandatory": true,
        "transferabilityNotes": "National forest inventory with remeasured plots."
      },
      {
        "appliesTo": [
          "rotation-age-spruce",
          "rotation-age-pine",
          "rotation-age-oak",
          "rotation-age-beech"
        ],
        "when": [
          {
            "constraint": "czech-jurisdiction",
            "test": "outside"
          }
        ],
        "actions": [
          "replace-with-local-equivalent"
        ],
        "mandatory": false,
        "transferabilityNotes": "The defaults follow Czech forest management conventions. If they are not set for the country, projections end at an age, and accept stand ages, that may not match local practice."
      },
      {
        "appliesTo": [
          "rasdaman"
        ],
        "triggeredBy": "service-unavailable",
        "actions": [
          "replace-with-local-equivalent"
        ],
        "mandatory": true,
        "transferabilityNotes": "Applies where no Rasdaman instance is available to the workflow: set one up with the same layout and its own registry, or change the code that reads the data (see the rasdaman artifact). On the FOCAL instance, a missing area is instead added as new collections and entries."
      }
    ]
  },
  "computationType": "statistical-ml",
  "maturityStatus": "operational",
  "qualityAnnotation": [
    {
      "dimension": "accuracy",
      "note": "Hold-out test (160 Czech stands, 2015-2025): total-height MAPE 3.15 % (2.7-3.6 % per species)."
    },
    {
      "dimension": "method-limitation",
      "note": "Bands are bootstrap model uncertainty for one climate source; no climate-model spread, no initial-height or stand-specific variability."
    },
    {
      "dimension": "method-limitation",
      "note": "Stands younger than about 16 years and late-century heat extremes lie outside the training data."
    },
    {
      "dimension": "method-limitation",
      "note": "Disturbances, mortality and management are not modelled; projections describe undisturbed growth."
    },
    {
      "dimension": "method-limitation",
      "note": "stress_probability is the share of bootstrap members flagging a stress year, not a calibrated probability."
    },
    {
      "dimension": "method-limitation",
      "note": "Slope, aspect and soil come from global maps, not field measurements (slope MAE 2.7 deg on 1,033 Czech plots)."
    },
    {
      "dimension": "method-limitation",
      "note": "Final model trained on FOCAL downscaled ERA5-Land (elevation correction fitted on Czech CHMI stations); inference collections must be on a consistent frame."
    }
  ]
}

```

#### jsonld
```jsonld
{
  "@context": "https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/workflow/context.jsonld",
  "class": "Workflow",
  "cwlVersion": "v1.2",
  "id": "",
  "label": "FWF1 - Tree growth prediction (FOCAL Forest Pilot)",
  "doc": [
    "Projects the yearly height growth of an existing forest stand to its rotation age under a chosen climate source, with bootstrap uncertainty and a yearly stress index against the 1991-2020 climate. The growth model was trained on Czech National Forest Inventory stands.",
    "Transferability record of workflow FP-WF1 (FWF1), record date 2026-11-18. Record basis: FWF1 API, focal_predict.py, wf1 climate/soil/terrain input functions, Rasdaman registry 1.1.8, focal_tree_growth repository (final downscaled model, feature documentation, report). Converted from the delivered record on 2026-11-25. Descriptive CWL profile: no steps are declared and the input and output identifiers are not yet those of an executable Application Package."
  ],
  "$namespaces": {
    "s": "https://schema.org/"
  },
  "s:identifier": "FP-WF1",
  "s:alternateName": "FWF1",
  "s:dateCreated": "2026-11-18",
  "requirements": {
    "SoftwareRequirement": {
      "packages": [
        {
          "package": "python"
        },
        {
          "package": "scikit-learn",
          "version": [
            "1.9.1"
          ]
        },
        {
          "package": "lightgbm",
          "version": [
            "4.7.0"
          ]
        },
        {
          "package": "flask"
        }
      ]
    },
    "NetworkAccess": {
      "networkAccess": true
    }
  },
  "inputs": {
    "latitude": {
      "type": "double",
      "label": "Latitude of the stand",
      "doc": "Latitude of the forest stand in decimal degrees (WGS 84). Soil, terrain and climate features are derived for this point. The Copernicus DEM reaches 89 degrees."
    },
    "longitude": {
      "type": "double",
      "label": "Longitude of the stand",
      "doc": "Longitude of the forest stand in decimal degrees (WGS 84)."
    },
    "species": {
      "type": {
        "type": "enum",
        "symbols": [
          "smrk",
          "borovice",
          "dub",
          "buk"
        ]
      },
      "label": "Tree species",
      "doc": "Species of the stand. Only these four are accepted: smrk = Norway spruce (Picea abies), borovice = Scots pine (Pinus sylvestris), dub = pedunculate oak (Quercus robur), buk = European beech (Fagus sylvatica)."
    },
    "age": {
      "type": "int",
      "label": "Stand age (years)",
      "doc": "Current age of the stand. Accepted from 16 years up to the rotation age of the species minus one."
    },
    "current_height": {
      "type": "float?",
      "label": "Current stand height (m)",
      "doc": "Current mean height of the stand in metres. If omitted, a typical height for the species and age is taken from the reference growth curves."
    },
    "rasdaman_connection": {
      "type": "string",
      "label": "Data cube connection",
      "doc": "How to reach the Rasdaman instance that holds the climate data (queried with rasql over SSH). The connection variables are not named in the delivered material, so one string stands for them; we assume credentials are supplied by the execution environment."
    },
    "rasdaman_registry": {
      "type": "File",
      "label": "Data cube registry",
      "doc": "rasdaman_registry.json for that instance. The FOCAL registry is not transferable as is."
    },
    "stress_threshold": {
      "type": "float?",
      "label": "Stress index threshold",
      "doc": "Manual threshold on the stress index SI for flagging stress years. If omitted, the species- and age-specific thresholds shipped with the workflow are used."
    },
    "rotation_age_spruce": {
      "type": "int",
      "label": "Rotation age of Norway spruce (years)",
      "doc": "Age up to which growth of Norway spruce is projected. The default is the Czech forest management convention; set it for the country of the stand.",
      "default": 110
    },
    "rotation_age_pine": {
      "type": "int",
      "label": "Rotation age of Scots pine (years)",
      "doc": "Age up to which growth of Scots pine is projected. The default is the Czech forest management convention; set it for the country of the stand.",
      "default": 110
    },
    "rotation_age_oak": {
      "type": "int",
      "label": "Rotation age of pedunculate oak (years)",
      "doc": "Age up to which growth of pedunculate oak is projected. The default is the Czech forest management convention; set it for the country of the stand.",
      "default": 140
    },
    "rotation_age_beech": {
      "type": "int",
      "label": "Rotation age of European beech (years)",
      "doc": "Age up to which growth of European beech is projected. The default is the Czech forest management convention; set it for the country of the stand.",
      "default": 130
    },
    "growth_model": {
      "type": "Directory",
      "label": "Trained growth model",
      "doc": "LightGBM pipeline (central model and bootstrap ensemble) fitted to Czech National Forest Inventory data. Ships with the workflow.",
      "default": {
        "class": "Directory",
        "location": "growth_model"
      }
    },
    "reference_increment": {
      "type": "File",
      "label": "Reference growth curves",
      "doc": "Typical height and increment per species and age (Czech NFI medians). Ships with the workflow.",
      "default": {
        "class": "File",
        "location": "reference_increment_d.csv"
      }
    },
    "stress_thresholds": {
      "type": "File",
      "label": "Stress thresholds table",
      "doc": "Stress index threshold per species and age (90th percentile of SI, 1991-2020, Czech NFI sites). Ships with the workflow.",
      "default": {
        "class": "File",
        "location": "stress_thresholds_d.csv"
      }
    }
  },
  "outputs": {
    "growth_projection": {
      "type": "File",
      "label": "Growth projection",
      "doc": "Yearly height and increment with 2.5-97.5 % bootstrap bands."
    },
    "stress_assessment": {
      "type": "File",
      "label": "Stress assessment",
      "doc": "Stress index SI = 1 - I / I_ref against the 1991-2020 climate, stress years and their share across bootstrap members."
    },
    "typical_growth": {
      "type": "File",
      "label": "Typical growth",
      "doc": "Typical height and increment of the species."
    },
    "period_summary": {
      "type": "File",
      "label": "Period summary",
      "doc": "Summary over the projected period."
    }
  },
  "steps": {},
  "transferability": {
    "trainingRequired": true,
    "transferabilityNotes": "Envelope entries and rules that only described which data FOCAL currently holds, or its platform, are not part of this statement; what they said is kept in the notes of the artifacts concerned. An area or period for which no data is at hand is a matter of providing data (as delivered, in the data cube) that meets the artifact's criteria. The delivered record also notes: temporal extent is the year range of each collection, read from Rasdaman at runtime. Delivered coverage fact: SoilGrids and Copernicus DEM are global; the API runs wherever the climate collections cover the point and does not restrict to Czechia or to forest land.",
    "envelope": [
      {
        "id": "czech-nfi-plots",
        "role": "trained-on",
        "dimension": "spatial",
        "value": {
          "asWKT": "POLYGON((12.2444 48.6232, 18.815 48.6232, 18.815 51.0198, 12.2444 51.0198, 12.2444 48.6232))"
        },
        "inputRef": [
          "/inputs/latitude",
          "/inputs/longitude"
        ],
        "transferabilityNotes": "Bounding box of the 1,756 Czech NFI (UHUL) monitoring stands used for training (1964-2025). Validation: spatial hold-out of 160 Czech stands, 2015-2025."
      },
      {
        "id": "czech-nfi-period",
        "role": "trained-on",
        "dimension": "temporal",
        "value": {
          "startDate": "1964",
          "endDate": "2025"
        },
        "transferabilityNotes": "Training rows before 2015, test rows 2015-2025."
      },
      {
        "id": "training-feature-domain",
        "role": "valid-for",
        "dimension": "input-domain",
        "value": {
          "variables": [
            {
              "name": "age",
              "unit": "years",
              "min": 24.0,
              "max": 144.0
            },
            {
              "name": "elevation",
              "unit": "m a.s.l.",
              "min": 175.0,
              "max": 1150.0
            },
            {
              "name": "slope",
              "unit": "degrees",
              "min": 0.4369,
              "max": 27.0
            },
            {
              "name": "avg_h_lag",
              "unit": "m",
              "min": 9.99,
              "max": 37.67
            },
            {
              "name": "N_0_5",
              "unit": "cg/kg",
              "min": 518.0,
              "max": 1096.0
            },
            {
              "name": "N_5_15",
              "unit": "cg/kg",
              "min": 161.0,
              "max": 673.0
            },
            {
              "name": "N_15_30",
              "unit": "cg/kg",
              "min": 115.0,
              "max": 411.0
            },
            {
              "name": "N_30_60",
              "unit": "cg/kg",
              "min": 72.0,
              "max": 296.0
            },
            {
              "name": "C",
              "unit": "dg/kg",
              "min": 193.2,
              "max": 825.5
            },
            {
              "name": "pH",
              "unit": "pH \u00d7 10",
              "min": 47.75,
              "max": 65.0
            },
            {
              "name": "clay",
              "unit": "g/kg",
              "min": 142.5,
              "max": 339.2
            },
            {
              "name": "T_year",
              "unit": "\u00b0C",
              "min": 3.705,
              "max": 10.17
            },
            {
              "name": "T_autumn",
              "unit": "\u00b0C",
              "min": 4.207,
              "max": 11.06
            },
            {
              "name": "T_min_month",
              "unit": "\u00b0C",
              "min": -10.54,
              "max": 1.298
            },
            {
              "name": "T_amplitude",
              "unit": "\u00b0C",
              "min": 16.26,
              "max": 27.91
            },
            {
              "name": "T_veg_lag_1",
              "unit": "\u00b0C",
              "min": 9.507,
              "max": 16.53
            },
            {
              "name": "T_autumn_lag_1",
              "unit": "\u00b0C",
              "min": 4.183,
              "max": 10.92
            },
            {
              "name": "T_min_month_lag_1",
              "unit": "\u00b0C",
              "min": -10.54,
              "max": 1.249
            },
            {
              "name": "T_amplitude_lag_1",
              "unit": "\u00b0C",
              "min": 16.25,
              "max": 27.92
            },
            {
              "name": "SR_veg",
              "unit": "W/m\u00b2",
              "min": 136.8,
              "max": 181.5
            },
            {
              "name": "SR_spring",
              "unit": "W/m\u00b2",
              "min": 112.5,
              "max": 166.3
            },
            {
              "name": "SR_veg_lag_1",
              "unit": "W/m\u00b2",
              "min": 136.4,
              "max": 181.4
            },
            {
              "name": "SR_spring_lag_1",
              "unit": "W/m\u00b2",
              "min": 112.0,
              "max": 166.3
            },
            {
              "name": "P_spring",
              "unit": "mm",
              "min": 97.33,
              "max": 371.2
            },
            {
              "name": "P_summer",
              "unit": "mm",
              "min": 136.4,
              "max": 549.6
            },
            {
              "name": "P_prev_late",
              "unit": "mm",
              "min": 97.56,
              "max": 412.0
            },
            {
              "name": "P_spring_lag_1",
              "unit": "mm",
              "min": 99.11,
              "max": 370.3
            },
            {
              "name": "P_summer_lag_1",
              "unit": "mm",
              "min": 137.4,
              "max": 550.9
            },
            {
              "name": "P_prev_late_lag_1",
              "unit": "mm",
              "min": 98.32,
              "max": 413.7
            },
            {
              "name": "SPI_3_summer",
              "unit": "z-score",
              "min": -2.008,
              "max": 2.483
            },
            {
              "name": "SPI_3_summer_lag_1",
              "unit": "z-score",
              "min": -2.009,
              "max": 2.515
            },
            {
              "name": "Tmax_Jul",
              "unit": "\u00b0C",
              "min": 15.65,
              "max": 26.7
            },
            {
              "name": "Tmax_Jul_lag_1",
              "unit": "\u00b0C",
              "min": 15.63,
              "max": 26.67
            },
            {
              "name": "Tmax_Aug",
              "unit": "\u00b0C",
              "min": 15.88,
              "max": 26.73
            },
            {
              "name": "Tmax_Aug_lag_1",
              "unit": "\u00b0C",
              "min": 15.88,
              "max": 26.59
            },
            {
              "name": "HD30_veg",
              "unit": "days",
              "min": 0.0,
              "max": 12.0
            },
            {
              "name": "HD30_veg_lag_1",
              "unit": "days",
              "min": 0.0,
              "max": 12.0
            },
            {
              "name": "FD_AprMay",
              "unit": "days",
              "min": 0.0,
              "max": 28.0
            },
            {
              "name": "FD_AprMay_lag_1",
              "unit": "days",
              "min": 0.0,
              "max": 29.0
            },
            {
              "name": "FD_winter_std",
              "unit": "days",
              "min": 45.0,
              "max": 90.0
            },
            {
              "name": "FD_winter_std_lag_1",
              "unit": "days",
              "min": 44.0,
              "max": 90.0
            },
            {
              "name": "R10mm_veg",
              "unit": "days",
              "min": 3.0,
              "max": 31.0
            },
            {
              "name": "R10mm_veg_lag_1",
              "unit": "days",
              "min": 3.0,
              "max": 31.0
            }
          ]
        },
        "inputRef": [
          "/inputs/latitude",
          "/inputs/longitude",
          "/inputs/age",
          "/inputs/current_height"
        ],
        "transferabilityNotes": "1st-99th percentile of 30,883 training stand-years (final model). Outside, the tree-based model repeats edge behaviour; predictions are extrapolation. A per-species area-of-applicability check exists in the modelling code but is not run by the API. Bounds are the 1st and 99th percentiles. The categorical variable aspect (NFI code) is not a range and is not listed in the value; the delivered 1st-99th percentile codes were 100 to 900."
      },
      {
        "id": "trained-species",
        "role": "valid-for",
        "dimension": "ecological",
        "value": {
          "scheme": "gbif-backbone",
          "classes": [
            "Picea abies",
            "Pinus sylvestris",
            "Quercus robur",
            "Fagus sylvatica"
          ]
        },
        "inputRef": "/inputs/species",
        "transferabilityNotes": "Only these four species are accepted by the API."
      },
      {
        "id": "dem-coverage",
        "role": "can-run-on",
        "dimension": "spatial",
        "value": {
          "asWKT": "POLYGON((-180 -89, 180 -89, 180 89, -180 89, -180 -89))"
        },
        "transferabilityNotes": "Coverage of the Copernicus DEM (artifact copernicus-dem), up to 89 degrees latitude."
      },
      {
        "id": "czech-jurisdiction",
        "role": "valid-for",
        "dimension": "jurisdictional",
        "value": {
          "asWKT": "POLYGON((12.07 48.48, 18.97 48.48, 18.97 51.08, 12.07 51.08, 12.07 48.48))"
        },
        "inputRef": [
          "/inputs/latitude",
          "/inputs/longitude"
        ],
        "transferabilityNotes": "Where the Czech forest management convention for rotation ages applies. The box is the FOCAL Czechia box, an approximation of the national territory."
      }
    ],
    "artifacts": [
      {
        "id": "growth-model",
        "artifact": "LightGBM pipeline (central model + bootstrap ensemble), 45 inputs (training_feature_set_d.txt)",
        "artifactRole": "workflow-input",
        "artifactRef": "/inputs/growth_model",
        "transferabilityNotes": "A replacement model takes 45 inputs in fixed order (training_feature_set_d.txt): age, elevation, aspect, slope, avg_h_lag, N_0_5, N_5_15, N_15_30, N_30_60, C, pH, clay, T_year, T_autumn, T_min_month, T_amplitude, T_veg_lag_1, T_autumn_lag_1, T_min_month_lag_1, T_amplitude_lag_1, SR_veg, SR_spring, SR_veg_lag_1, SR_spring_lag_1, P_spring, P_summer, P_prev_late, P_spring_lag_1, P_summer_lag_1, P_prev_late_lag_1, SPI_3_summer, SPI_3_summer_lag_1, Tmax_Jul, Tmax_Jul_lag_1, Tmax_Aug, Tmax_Aug_lag_1, HD30_veg, HD30_veg_lag_1, FD_AprMay, FD_AprMay_lag_1, FD_winter_std, FD_winter_std_lag_1, R10mm_veg, R10mm_veg_lag_1, species. Software: scikit-learn 1.9.1, LightGBM 4.7.0. Used by (delivered step names): growth-simulation, stress-index."
      },
      {
        "id": "reference-increment",
        "artifact": "reference_increment_d.csv: typical height and increment per species and age (Czech NFI medians)",
        "artifactRole": "workflow-input",
        "artifactRef": "/inputs/reference_increment",
        "transferabilityNotes": "Per species and age; regenerated by the same pipeline together with the model. Used by (delivered step names): typical-growth, default-initial-height."
      },
      {
        "id": "stress-thresholds",
        "artifact": "stress_thresholds_d.csv: SI threshold per species and age (90th percentile of SI, 1991-2020, Czech NFI sites)",
        "artifactRole": "workflow-input",
        "artifactRef": [
          "/inputs/stress_thresholds",
          "/inputs/stress_threshold"
        ],
        "transferabilityNotes": "Per species and age; regenerated by the same pipeline together with the model. Used by (delivered step names): stress-years."
      },
      {
        "id": "nfi-training-data",
        "artifact": "Czech NFI stand measurements (species, age, mean height, site), 1964-2025",
        "artifactRole": "external-resource",
        "transferabilityNotes": "Not read at inference; needed to retrain. A replacement must give, per stand: species (the species to be modelled), stand age, mean height, coordinates and measurement year, with at least two measurements per stand. The intervals between the Czech measurements were mostly five years. Used by (delivered step names): training.",
        "acceptanceCriteria": {
          "variables": [
            {
              "name": "species"
            },
            {
              "name": "stand age"
            },
            {
              "name": "mean height"
            },
            {
              "name": "coordinates"
            },
            {
              "name": "measurement year"
            }
          ]
        }
      },
      {
        "id": "soilgrids",
        "artifact": "ISRIC SoilGrids 2.0 (Q0.5), nitrogen 4 depths, SOC, pH, clay 0-60 cm, 250 m",
        "artifactRole": "external-resource",
        "acceptanceCriteria": {
          "variables": [
            {
              "name": "nitrogen"
            },
            {
              "name": "soc"
            },
            {
              "name": "phh2o"
            },
            {
              "name": "clay",
              "units": [
                "GM-PER-KiloGM"
              ]
            }
          ],
          "transferabilityNotes": "Same product required; raw SoilGrids units are part of the model contract: nitrogen in cg/kg, soc in dg/kg, phh2o as pH x 10, clay in g/kg. Depths: nitrogen at 0-5, 5-15, 15-30 and 30-60 cm; soc, pH and clay 0-60 cm."
        },
        "transferabilityNotes": "Global; fetched live from ISRIC (WCS or WebDAV) with a local cache, so nothing has to be prepared or supplied. Used by (delivered step names): site-features."
      },
      {
        "id": "copernicus-dem",
        "artifact": "Copernicus DEM GLO-30, elevation and 11 x 11 plane-fit slope/aspect",
        "artifactRole": "external-resource",
        "transferabilityNotes": "Same product only; the slope method is calibrated to it. Resolution 1 arc-second, vertical datum EGM2008. Aspect coding: 100 flat (slope <= 5 deg), 200-900 N..NW. Global (up to 89 degrees latitude); fetched live from AWS with a local cache, so nothing has to be prepared or supplied. Used by (delivered step names): site-features."
      },
      {
        "id": "historical-climate",
        "artifact": "ERA5-Land daily temperature (min/mean/max), precipitation, net SSR",
        "artifactRole": "workflow-input",
        "acceptanceCriteria": {
          "variables": [
            {
              "name": "tmin",
              "units": [
                "DEG_C"
              ],
              "standardName": "air_temperature"
            },
            {
              "name": "tmean",
              "units": [
                "DEG_C"
              ],
              "standardName": "air_temperature"
            },
            {
              "name": "tmax",
              "units": [
                "DEG_C"
              ],
              "standardName": "air_temperature"
            },
            {
              "name": "pr",
              "units": [
                "MilliM-PER-DAY"
              ]
            },
            {
              "name": "ssr",
              "units": [
                "J-PER-M2",
                "W-PER-M2"
              ],
              "standardName": [
                "surface_net_downward_shortwave_flux",
                "integral_wrt_time_of_surface_net_downward_shortwave_flux"
              ]
            }
          ],
          "temporal": {
            "resolution": "P1D",
            "calendar": [
              "standard",
              "gregorian",
              "proleptic_gregorian"
            ],
            "complete": true,
            "startDate": "1991"
          },
          "axes": [
            "time"
          ],
          "gridTypes": [
            "regular-latlon",
            "rotated-pole",
            "curvilinear"
          ],
          "transferabilityNotes": "Structure: daily [day, y, x]; temperature as a struct cell (min/mean/max). Curvilinear grids need 2D latitude/longitude. ssr is net shortwave radiation, either in J/m2 per day (24-h accumulation assigned to UTC day D) or in W/m2; downward rsds/ssrd is not accepted. Non-Gregorian calendars must be harmonised before ingestion (they are rejected by the climate function). No-data is NaN; no gaps are allowed in required windows."
        },
        "transferabilityNotes": "As delivered, the workflow does not take these data as a file: it reads them from the Rasdaman data cube (artifact rasdaman), for the requested area and the years it needs. The delivered material gives no specification of the layout the code expects. Must be on a frame consistent with the training climate (FOCAL downscaled ERA5-Land, about 350 m, elevation-corrected, for temperature and precipitation; ERA5-Land net solar radiation). Within FOCAL: ERA5-Land temperature and precipitation are held for Czechia, Spain and Finland, and daily net SSR is registered for the Czechia grid (delivered box: 12.07-18.97 E, 48.48-51.08 N); elsewhere a routine ERA5-Land run, including net SSR from 1991. Outside FOCAL: Copernicus Climate Data Store. Used by (delivered step names): climate-features, spi-baseline, stress-reference, lag-context."
      },
      {
        "id": "projection-climate",
        "artifact": "Daily projected temperature (min/mean/max), precipitation and net SSR, bias-corrected to the training climate frame",
        "artifactRole": "workflow-input",
        "acceptanceCriteria": {
          "variables": [
            {
              "name": "tmin",
              "units": [
                "DEG_C"
              ],
              "standardName": "air_temperature"
            },
            {
              "name": "tmean",
              "units": [
                "DEG_C"
              ],
              "standardName": "air_temperature"
            },
            {
              "name": "tmax",
              "units": [
                "DEG_C"
              ],
              "standardName": "air_temperature"
            },
            {
              "name": "pr",
              "units": [
                "MilliM-PER-DAY"
              ]
            },
            {
              "name": "ssr",
              "units": [
                "J-PER-M2",
                "W-PER-M2"
              ],
              "standardName": [
                "surface_net_downward_shortwave_flux",
                "integral_wrt_time_of_surface_net_downward_shortwave_flux"
              ]
            }
          ],
          "temporal": {
            "resolution": "P1D",
            "calendar": [
              "standard",
              "gregorian",
              "proleptic_gregorian"
            ],
            "complete": true
          },
          "axes": [
            "time"
          ],
          "gridTypes": [
            "regular-latlon",
            "rotated-pole",
            "curvilinear"
          ],
          "transferabilityNotes": "Structure: daily [day, y, x]; temperature as a struct cell (min/mean/max). Curvilinear grids need 2D latitude/longitude. ssr is net shortwave radiation, either in J/m2 per day (24-h accumulation assigned to UTC day D) or in W/m2; downward rsds/ssrd is not accepted. Non-Gregorian calendars must be harmonised before ingestion (they are rejected by the climate function). No-data is NaN; no gaps are allowed in required windows."
        },
        "transferabilityNotes": "As delivered, the workflow does not take these data as a file: it reads them from the Rasdaman data cube (artifact rasdaman), for the requested area and the years it needs. The delivered material gives no specification of the layout the code expects. Must be bias-corrected to the training climate frame. A projection set with net SSR, corrected to that frame, is required everywhere, including Czechia. FOCAL EUR-11 REMO2020 collections hold temperature and precipitation only. Model development used NEX-GDDP-CMIP6 with rsds x (1 - 0.15) and per-point monthly bias correction (1991-2014). FOCAL downscaled projections are expected in early 2027. Outside FOCAL: CORDEX or NEX-GDDP-CMIP6, including net shortwave radiation. Used by (delivered step names): climate-features. Needed only to project years beyond the historical data (our reading; to be confirmed)."
      },
      {
        "id": "rotation-age-spruce",
        "artifact": "Rotation age of Norway spruce (110 years, Czech convention)",
        "artifactRole": "workflow-input",
        "artifactRef": "/inputs/rotation_age_spruce",
        "transferabilityNotes": "Czech forest management convention. Reported by the delivery as hard-coded in the current API; to be set per country."
      },
      {
        "id": "rotation-age-pine",
        "artifact": "Rotation age of Scots pine (110 years, Czech convention)",
        "artifactRole": "workflow-input",
        "artifactRef": "/inputs/rotation_age_pine",
        "transferabilityNotes": "Czech forest management convention. Reported by the delivery as hard-coded in the current API; to be set per country."
      },
      {
        "id": "rotation-age-oak",
        "artifact": "Rotation age of pedunculate oak (140 years, Czech convention)",
        "artifactRole": "workflow-input",
        "artifactRef": "/inputs/rotation_age_oak",
        "transferabilityNotes": "Czech forest management convention. Reported by the delivery as hard-coded in the current API; to be set per country."
      },
      {
        "id": "rotation-age-beech",
        "artifact": "Rotation age of European beech (130 years, Czech convention)",
        "artifactRole": "workflow-input",
        "artifactRef": "/inputs/rotation_age_beech",
        "transferabilityNotes": "Czech forest management convention. Reported by the delivery as hard-coded in the current API; to be set per country."
      },
      {
        "id": "rasdaman",
        "artifact": "FOCAL Rasdaman data cube (rasql over SSH) and its registry (rasdaman_registry.json)",
        "artifactRole": "infrastructure",
        "artifactRef": [
          "/inputs/rasdaman_connection",
          "/inputs/rasdaman_registry"
        ],
        "transferabilityNotes": "The delivered workflow reads climate data from a Rasdaman instance queried with rasql over SSH, located through rasdaman_registry.json. Another platform needs Rasdaman with the same layout and its own registry, or a custom climate loader returning the 32 annual features (the predictor accepts one). Within FOCAL new collections are configuration entries; the FOCAL registry is not transferable as is. Used by (delivered step names): data-access."
      }
    ],
    "rules": [
      {
        "appliesTo": [
          "growth-model",
          "reference-increment"
        ],
        "when": [
          {
            "constraint": "czech-nfi-plots",
            "test": "outside"
          }
        ],
        "actions": [
          "retrain"
        ],
        "mandatory": true,
        "transferabilityNotes": "Retrain the pipeline on national stand data; regenerate reference curves, stress thresholds and species support."
      },
      {
        "appliesTo": [
          "stress-thresholds"
        ],
        "when": [
          {
            "constraint": "czech-nfi-plots",
            "test": "outside"
          }
        ],
        "actions": [
          "retrain",
          "replace-with-local-equivalent"
        ],
        "mandatory": true,
        "transferabilityNotes": "A manual threshold can be passed per request (input stress_threshold)."
      },
      {
        "appliesTo": [
          "growth-model"
        ],
        "when": [
          {
            "constraint": "training-feature-domain",
            "test": "outside"
          }
        ],
        "actions": [
          "retrain"
        ],
        "mandatory": false,
        "transferabilityNotes": "Inside Czechia, inputs outside the range (e.g. late-century heat days) are extrapolation; flag rather than block."
      },
      {
        "appliesTo": [
          "nfi-training-data"
        ],
        "when": [
          {
            "constraint": "czech-nfi-plots",
            "test": "outside"
          }
        ],
        "actions": [
          "replace-with-local-equivalent"
        ],
        "mandatory": true,
        "transferabilityNotes": "National forest inventory with remeasured plots."
      },
      {
        "appliesTo": [
          "rotation-age-spruce",
          "rotation-age-pine",
          "rotation-age-oak",
          "rotation-age-beech"
        ],
        "when": [
          {
            "constraint": "czech-jurisdiction",
            "test": "outside"
          }
        ],
        "actions": [
          "replace-with-local-equivalent"
        ],
        "mandatory": false,
        "transferabilityNotes": "The defaults follow Czech forest management conventions. If they are not set for the country, projections end at an age, and accept stand ages, that may not match local practice."
      },
      {
        "appliesTo": [
          "rasdaman"
        ],
        "triggeredBy": "service-unavailable",
        "actions": [
          "replace-with-local-equivalent"
        ],
        "mandatory": true,
        "transferabilityNotes": "Applies where no Rasdaman instance is available to the workflow: set one up with the same layout and its own registry, or change the code that reads the data (see the rasdaman artifact). On the FOCAL instance, a missing area is instead added as new collections and entries."
      }
    ]
  },
  "computationType": "statistical-ml",
  "maturityStatus": "operational",
  "qualityAnnotation": [
    {
      "dimension": "accuracy",
      "note": "Hold-out test (160 Czech stands, 2015-2025): total-height MAPE 3.15 % (2.7-3.6 % per species)."
    },
    {
      "dimension": "method-limitation",
      "note": "Bands are bootstrap model uncertainty for one climate source; no climate-model spread, no initial-height or stand-specific variability."
    },
    {
      "dimension": "method-limitation",
      "note": "Stands younger than about 16 years and late-century heat extremes lie outside the training data."
    },
    {
      "dimension": "method-limitation",
      "note": "Disturbances, mortality and management are not modelled; projections describe undisturbed growth."
    },
    {
      "dimension": "method-limitation",
      "note": "stress_probability is the share of bootstrap members flagging a stress year, not a calibrated probability."
    },
    {
      "dimension": "method-limitation",
      "note": "Slope, aspect and soil come from global maps, not field measurements (slope MAE 2.7 deg on 1,033 Czech plots)."
    },
    {
      "dimension": "method-limitation",
      "note": "Final model trained on FOCAL downscaled ERA5-Land (elevation correction fitted on Czech CHMI stations); inference collections must be on a consistent frame."
    }
  ]
}
```

#### ttl
```ttl
@prefix cwl: <https://w3id.org/cwl/cwl#> .
@prefix dcat: <http://www.w3.org/ns/dcat#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix dqv: <http://www.w3.org/ns/dqv#> .
@prefix focal-transf-prop: <https://w3id.org/ogc/hosted/focal/transferability/properties/> .
@prefix geo: <http://www.opengis.net/ont/geosparql#> .
@prefix ns1: <https://w3id.org/cwl/cwl#SoftwarePackage/> .
@prefix ns2: <https://w3id.org/cwl/cwl#SoftwareRequirement/> .
@prefix ns3: <https://w3id.org/cwl/cwl#NetworkAccess/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix schema: <https://schema.org/> .
@prefix sld: <https://w3id.org/cwl/salad#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/> a cwl:Workflow ;
    rdfs:label "FWF1 - Tree growth prediction (FOCAL Forest Pilot)" ;
    rdfs:comment "Projects the yearly height growth of an existing forest stand to its rotation age under a chosen climate source, with bootstrap uncertainty and a yearly stress index against the 1991-2020 climate. The growth model was trained on Czech National Forest Inventory stands.",
        "Transferability record of workflow FP-WF1 (FWF1), record date 2026-11-18. Record basis: FWF1 API, focal_predict.py, wf1 climate/soil/terrain input functions, Rasdaman registry 1.1.8, focal_tree_growth repository (final downscaled model, feature documentation, report). Converted from the delivered record on 2026-11-25. Descriptive CWL profile: no steps are declared and the input and output identifiers are not yet those of an executable Application Package." ;
    schema:alternateName "FWF1" ;
    schema:dateCreated "2026-11-18" ;
    schema:identifier "FP-WF1" ;
    cwl:inputs <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/age>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/current_height>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/growth_model>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/latitude>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/longitude>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/rasdaman_connection>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/rasdaman_registry>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/reference_increment>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/rotation_age_beech>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/rotation_age_oak>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/rotation_age_pine>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/rotation_age_spruce>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/species>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/stress_threshold>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/stress_thresholds> ;
    cwl:outputs <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/growth_projection>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/period_summary>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/stress_assessment>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/typical_growth> ;
    cwl:requirements [ a cwl:SoftwareRequirement ;
            ns2:packages [ ns1:package "python" ],
                [ ns1:package "flask" ],
                [ ns1:package "scikit-learn" ;
                    ns1:version "1.9.1" ],
                [ ns1:package "lightgbm" ;
                    ns1:version "4.7.0" ] ],
        [ a cwl:NetworkAccess ;
            ns3:networkAccess true ] ;
    focal-transf-prop:computationType <https://w3id.org/ogc/hosted/focal/transferability/computation-types/statistical-ml> ;
    focal-transf-prop:maturityStatus <https://w3id.org/ogc/hosted/focal/transferability/maturity-statuses/operational> ;
    focal-transf-prop:qualityAnnotation [ dqv:inDimension <https://w3id.org/ogc/hosted/focal/transferability/quality-dimensions/method-limitation> ;
            focal-transf-prop:note "Slope, aspect and soil come from global maps, not field measurements (slope MAE 2.7 deg on 1,033 Czech plots)." ],
        [ dqv:inDimension <https://w3id.org/ogc/hosted/focal/transferability/quality-dimensions/method-limitation> ;
            focal-transf-prop:note "stress_probability is the share of bootstrap members flagging a stress year, not a calibrated probability." ],
        [ dqv:inDimension <https://w3id.org/ogc/hosted/focal/transferability/quality-dimensions/method-limitation> ;
            focal-transf-prop:note "Final model trained on FOCAL downscaled ERA5-Land (elevation correction fitted on Czech CHMI stations); inference collections must be on a consistent frame." ],
        [ dqv:inDimension <https://w3id.org/ogc/hosted/focal/transferability/quality-dimensions/accuracy> ;
            focal-transf-prop:note "Hold-out test (160 Czech stands, 2015-2025): total-height MAPE 3.15 % (2.7-3.6 % per species)." ],
        [ dqv:inDimension <https://w3id.org/ogc/hosted/focal/transferability/quality-dimensions/method-limitation> ;
            focal-transf-prop:note "Bands are bootstrap model uncertainty for one climate source; no climate-model spread, no initial-height or stand-specific variability." ],
        [ dqv:inDimension <https://w3id.org/ogc/hosted/focal/transferability/quality-dimensions/method-limitation> ;
            focal-transf-prop:note "Stands younger than about 16 years and late-century heat extremes lie outside the training data." ],
        [ dqv:inDimension <https://w3id.org/ogc/hosted/focal/transferability/quality-dimensions/method-limitation> ;
            focal-transf-prop:note "Disturbances, mortality and management are not modelled; projections describe undisturbed growth." ] ;
    focal-transf-prop:transferability [ rdfs:comment "Envelope entries and rules that only described which data FOCAL currently holds, or its platform, are not part of this statement; what they said is kept in the notes of the artifacts concerned. An area or period for which no data is at hand is a matter of providing data (as delivered, in the data cube) that meets the artifact's criteria. The delivered record also notes: temporal extent is the year range of each collection, read from Rasdaman at runtime. Delivered coverage fact: SoilGrids and Copernicus DEM are global; the API runs wherever the climate collections cover the point and does not restrict to Czechia or to forest land." ;
            focal-transf-prop:artifacts <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/copernicus-dem>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/growth-model>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/historical-climate>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/nfi-training-data>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/projection-climate>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/rasdaman>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/reference-increment>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/rotation-age-beech>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/rotation-age-oak>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/rotation-age-pine>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/rotation-age-spruce>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/soilgrids>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/stress-thresholds> ;
            focal-transf-prop:envelope <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/czech-jurisdiction>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/czech-nfi-period>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/czech-nfi-plots>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/dem-coverage>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/trained-species>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/training-feature-domain> ;
            focal-transf-prop:rules [ rdfs:comment "A manual threshold can be passed per request (input stress_threshold)." ;
                    focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/replace-with-local-equivalent>,
                        <https://w3id.org/ogc/hosted/focal/transferability/actions/retrain> ;
                    focal-transf-prop:appliesTo <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/stress-thresholds> ;
                    focal-transf-prop:mandatory true ;
                    focal-transf-prop:when [ focal-transf-prop:constraint <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/czech-nfi-plots> ;
                            focal-transf-prop:test <https://w3id.org/ogc/hosted/focal/transferability/tests/outside> ] ],
                [ rdfs:comment "Applies where no Rasdaman instance is available to the workflow: set one up with the same layout and its own registry, or change the code that reads the data (see the rasdaman artifact). On the FOCAL instance, a missing area is instead added as new collections and entries." ;
                    focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/replace-with-local-equivalent> ;
                    focal-transf-prop:appliesTo <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/rasdaman> ;
                    focal-transf-prop:mandatory true ;
                    focal-transf-prop:triggeredBy <https://w3id.org/ogc/hosted/focal/transferability/triggers/service-unavailable> ],
                [ rdfs:comment "The defaults follow Czech forest management conventions. If they are not set for the country, projections end at an age, and accept stand ages, that may not match local practice." ;
                    focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/replace-with-local-equivalent> ;
                    focal-transf-prop:appliesTo <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/rotation-age-beech>,
                        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/rotation-age-oak>,
                        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/rotation-age-pine>,
                        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/rotation-age-spruce> ;
                    focal-transf-prop:mandatory false ;
                    focal-transf-prop:when [ focal-transf-prop:constraint <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/czech-jurisdiction> ;
                            focal-transf-prop:test <https://w3id.org/ogc/hosted/focal/transferability/tests/outside> ] ],
                [ rdfs:comment "National forest inventory with remeasured plots." ;
                    focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/replace-with-local-equivalent> ;
                    focal-transf-prop:appliesTo <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/nfi-training-data> ;
                    focal-transf-prop:mandatory true ;
                    focal-transf-prop:when [ focal-transf-prop:constraint <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/czech-nfi-plots> ;
                            focal-transf-prop:test <https://w3id.org/ogc/hosted/focal/transferability/tests/outside> ] ],
                [ rdfs:comment "Inside Czechia, inputs outside the range (e.g. late-century heat days) are extrapolation; flag rather than block." ;
                    focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/retrain> ;
                    focal-transf-prop:appliesTo <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/growth-model> ;
                    focal-transf-prop:mandatory false ;
                    focal-transf-prop:when [ focal-transf-prop:constraint <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/training-feature-domain> ;
                            focal-transf-prop:test <https://w3id.org/ogc/hosted/focal/transferability/tests/outside> ] ],
                [ rdfs:comment "Retrain the pipeline on national stand data; regenerate reference curves, stress thresholds and species support." ;
                    focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/retrain> ;
                    focal-transf-prop:appliesTo <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/growth-model>,
                        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/reference-increment> ;
                    focal-transf-prop:mandatory true ;
                    focal-transf-prop:when [ focal-transf-prop:constraint <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/czech-nfi-plots> ;
                            focal-transf-prop:test <https://w3id.org/ogc/hosted/focal/transferability/tests/outside> ] ] ;
            focal-transf-prop:trainingRequired true ] .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/age> rdfs:label "Stand age (years)" ;
    rdfs:comment "Current age of the stand. Accepted from 16 years up to the rotation age of the species minus one." ;
    sld:type xsd:int .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/copernicus-dem> dcterms:title "Copernicus DEM GLO-30, elevation and 11 x 11 plane-fit slope/aspect" ;
    rdfs:comment "Same product only; the slope method is calibrated to it. Resolution 1 arc-second, vertical datum EGM2008. Aspect coding: 100 flat (slope <= 5 deg), 200-900 N..NW. Global (up to 89 degrees latitude); fetched live from AWS with a local cache, so nothing has to be prepared or supplied. Used by (delivered step names): site-features." ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/external-resource> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/current_height> rdfs:label "Current stand height (m)" ;
    rdfs:comment "Current mean height of the stand in metres. If omitted, a typical height for the species and age is taken from the reference growth curves." ;
    sld:type <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/float> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/czech-nfi-period> rdfs:comment "Training rows before 2015, test rows 2015-2025." ;
    focal-transf-prop:dimension <https://w3id.org/ogc/hosted/focal/transferability/dimensions/temporal> ;
    focal-transf-prop:role <https://w3id.org/ogc/hosted/focal/transferability/roles/trained-on> ;
    focal-transf-prop:value [ dcat:endDate "2025" ;
            dcat:startDate "1964" ] .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/dem-coverage> rdfs:comment "Coverage of the Copernicus DEM (artifact copernicus-dem), up to 89 degrees latitude." ;
    focal-transf-prop:dimension <https://w3id.org/ogc/hosted/focal/transferability/dimensions/spatial> ;
    focal-transf-prop:role <https://w3id.org/ogc/hosted/focal/transferability/roles/can-run-on> ;
    focal-transf-prop:value [ geo:asWKT "POLYGON((-180 -89, 180 -89, 180 89, -180 89, -180 -89))"^^geo:wktLiteral ] .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/growth_projection> rdfs:label "Growth projection" ;
    rdfs:comment "Yearly height and increment with 2.5-97.5 % bootstrap bands." ;
    sld:type cwl:File .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/historical-climate> dcterms:title "ERA5-Land daily temperature (min/mean/max), precipitation, net SSR" ;
    rdfs:comment "As delivered, the workflow does not take these data as a file: it reads them from the Rasdaman data cube (artifact rasdaman), for the requested area and the years it needs. The delivered material gives no specification of the layout the code expects. Must be on a frame consistent with the training climate (FOCAL downscaled ERA5-Land, about 350 m, elevation-corrected, for temperature and precipitation; ERA5-Land net solar radiation). Within FOCAL: ERA5-Land temperature and precipitation are held for Czechia, Spain and Finland, and daily net SSR is registered for the Czechia grid (delivered box: 12.07-18.97 E, 48.48-51.08 N); elsewhere a routine ERA5-Land run, including net SSR from 1991. Outside FOCAL: Copernicus Climate Data Store. Used by (delivered step names): climate-features, spi-baseline, stress-reference, lag-context." ;
    focal-transf-prop:acceptanceCriteria [ rdfs:comment "Structure: daily [day, y, x]; temperature as a struct cell (min/mean/max). Curvilinear grids need 2D latitude/longitude. ssr is net shortwave radiation, either in J/m2 per day (24-h accumulation assigned to UTC day D) or in W/m2; downward rsds/ssrd is not accepted. Non-Gregorian calendars must be harmonised before ingestion (they are rejected by the climate function). No-data is NaN; no gaps are allowed in required windows." ;
            focal-transf-prop:axis <https://w3id.org/ogc/hosted/focal/transferability/axes/time> ;
            focal-transf-prop:gridType <https://w3id.org/ogc/hosted/focal/transferability/grid-types/curvilinear>,
                <https://w3id.org/ogc/hosted/focal/transferability/grid-types/regular-latlon>,
                <https://w3id.org/ogc/hosted/focal/transferability/grid-types/rotated-pole> ;
            focal-transf-prop:temporalRequirement [ dcat:startDate "1991" ;
                    dcat:temporalResolution "P1D"^^xsd:duration ;
                    focal-transf-prop:calendar "gregorian",
                        "proleptic_gregorian",
                        "standard" ;
                    focal-transf-prop:temporalComplete true ] ;
            focal-transf-prop:variable [ focal-transf-prop:standardName "integral_wrt_time_of_surface_net_downward_shortwave_flux",
                        "surface_net_downward_shortwave_flux" ;
                    focal-transf-prop:unit <http://qudt.org/vocab/unit/J-PER-M2>,
                        <http://qudt.org/vocab/unit/W-PER-M2> ;
                    focal-transf-prop:variableName "ssr" ],
                [ focal-transf-prop:standardName "air_temperature" ;
                    focal-transf-prop:unit <http://qudt.org/vocab/unit/DEG_C> ;
                    focal-transf-prop:variableName "tmax" ],
                [ focal-transf-prop:standardName "air_temperature" ;
                    focal-transf-prop:unit <http://qudt.org/vocab/unit/DEG_C> ;
                    focal-transf-prop:variableName "tmean" ],
                [ focal-transf-prop:standardName "air_temperature" ;
                    focal-transf-prop:unit <http://qudt.org/vocab/unit/DEG_C> ;
                    focal-transf-prop:variableName "tmin" ],
                [ focal-transf-prop:unit <http://qudt.org/vocab/unit/MilliM-PER-DAY> ;
                    focal-transf-prop:variableName "pr" ] ] ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/workflow-input> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/latitude> rdfs:label "Latitude of the stand" ;
    rdfs:comment "Latitude of the forest stand in decimal degrees (WGS 84). Soil, terrain and climate features are derived for this point. The Copernicus DEM reaches 89 degrees." ;
    sld:type xsd:double .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/longitude> rdfs:label "Longitude of the stand" ;
    rdfs:comment "Longitude of the forest stand in decimal degrees (WGS 84)." ;
    sld:type xsd:double .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/period_summary> rdfs:label "Period summary" ;
    rdfs:comment "Summary over the projected period." ;
    sld:type cwl:File .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/projection-climate> dcterms:title "Daily projected temperature (min/mean/max), precipitation and net SSR, bias-corrected to the training climate frame" ;
    rdfs:comment "As delivered, the workflow does not take these data as a file: it reads them from the Rasdaman data cube (artifact rasdaman), for the requested area and the years it needs. The delivered material gives no specification of the layout the code expects. Must be bias-corrected to the training climate frame. A projection set with net SSR, corrected to that frame, is required everywhere, including Czechia. FOCAL EUR-11 REMO2020 collections hold temperature and precipitation only. Model development used NEX-GDDP-CMIP6 with rsds x (1 - 0.15) and per-point monthly bias correction (1991-2014). FOCAL downscaled projections are expected in early 2027. Outside FOCAL: CORDEX or NEX-GDDP-CMIP6, including net shortwave radiation. Used by (delivered step names): climate-features. Needed only to project years beyond the historical data (our reading; to be confirmed)." ;
    focal-transf-prop:acceptanceCriteria [ rdfs:comment "Structure: daily [day, y, x]; temperature as a struct cell (min/mean/max). Curvilinear grids need 2D latitude/longitude. ssr is net shortwave radiation, either in J/m2 per day (24-h accumulation assigned to UTC day D) or in W/m2; downward rsds/ssrd is not accepted. Non-Gregorian calendars must be harmonised before ingestion (they are rejected by the climate function). No-data is NaN; no gaps are allowed in required windows." ;
            focal-transf-prop:axis <https://w3id.org/ogc/hosted/focal/transferability/axes/time> ;
            focal-transf-prop:gridType <https://w3id.org/ogc/hosted/focal/transferability/grid-types/curvilinear>,
                <https://w3id.org/ogc/hosted/focal/transferability/grid-types/regular-latlon>,
                <https://w3id.org/ogc/hosted/focal/transferability/grid-types/rotated-pole> ;
            focal-transf-prop:temporalRequirement [ dcat:temporalResolution "P1D"^^xsd:duration ;
                    focal-transf-prop:calendar "gregorian",
                        "proleptic_gregorian",
                        "standard" ;
                    focal-transf-prop:temporalComplete true ] ;
            focal-transf-prop:variable [ focal-transf-prop:unit <http://qudt.org/vocab/unit/MilliM-PER-DAY> ;
                    focal-transf-prop:variableName "pr" ],
                [ focal-transf-prop:standardName "integral_wrt_time_of_surface_net_downward_shortwave_flux",
                        "surface_net_downward_shortwave_flux" ;
                    focal-transf-prop:unit <http://qudt.org/vocab/unit/J-PER-M2>,
                        <http://qudt.org/vocab/unit/W-PER-M2> ;
                    focal-transf-prop:variableName "ssr" ],
                [ focal-transf-prop:standardName "air_temperature" ;
                    focal-transf-prop:unit <http://qudt.org/vocab/unit/DEG_C> ;
                    focal-transf-prop:variableName "tmax" ],
                [ focal-transf-prop:standardName "air_temperature" ;
                    focal-transf-prop:unit <http://qudt.org/vocab/unit/DEG_C> ;
                    focal-transf-prop:variableName "tmean" ],
                [ focal-transf-prop:standardName "air_temperature" ;
                    focal-transf-prop:unit <http://qudt.org/vocab/unit/DEG_C> ;
                    focal-transf-prop:variableName "tmin" ] ] ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/workflow-input> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/rasdaman_connection> rdfs:label "Data cube connection" ;
    rdfs:comment "How to reach the Rasdaman instance that holds the climate data (queried with rasql over SSH). The connection variables are not named in the delivered material, so one string stands for them; we assume credentials are supplied by the execution environment." ;
    sld:type xsd:string .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/rasdaman_registry> rdfs:label "Data cube registry" ;
    rdfs:comment "rasdaman_registry.json for that instance. The FOCAL registry is not transferable as is." ;
    sld:type cwl:File .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/reference_increment> rdfs:label "Reference growth curves" ;
    rdfs:comment "Typical height and increment per species and age (Czech NFI medians). Ships with the workflow." ;
    sld:default <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/reference_increment_d.csv> ;
    sld:type cwl:File .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/reference_increment_d.csv> a cwl:File .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/rotation_age_beech> rdfs:label "Rotation age of European beech (years)" ;
    rdfs:comment "Age up to which growth of European beech is projected. The default is the Czech forest management convention; set it for the country of the stand." ;
    sld:default 130 ;
    sld:type xsd:int .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/rotation_age_oak> rdfs:label "Rotation age of pedunculate oak (years)" ;
    rdfs:comment "Age up to which growth of pedunculate oak is projected. The default is the Czech forest management convention; set it for the country of the stand." ;
    sld:default 140 ;
    sld:type xsd:int .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/rotation_age_pine> rdfs:label "Rotation age of Scots pine (years)" ;
    rdfs:comment "Age up to which growth of Scots pine is projected. The default is the Czech forest management convention; set it for the country of the stand." ;
    sld:default 110 ;
    sld:type xsd:int .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/rotation_age_spruce> rdfs:label "Rotation age of Norway spruce (years)" ;
    rdfs:comment "Age up to which growth of Norway spruce is projected. The default is the Czech forest management convention; set it for the country of the stand." ;
    sld:default 110 ;
    sld:type xsd:int .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/soilgrids> dcterms:title "ISRIC SoilGrids 2.0 (Q0.5), nitrogen 4 depths, SOC, pH, clay 0-60 cm, 250 m" ;
    rdfs:comment "Global; fetched live from ISRIC (WCS or WebDAV) with a local cache, so nothing has to be prepared or supplied. Used by (delivered step names): site-features." ;
    focal-transf-prop:acceptanceCriteria [ rdfs:comment "Same product required; raw SoilGrids units are part of the model contract: nitrogen in cg/kg, soc in dg/kg, phh2o as pH x 10, clay in g/kg. Depths: nitrogen at 0-5, 5-15, 15-30 and 30-60 cm; soc, pH and clay 0-60 cm." ;
            focal-transf-prop:variable [ focal-transf-prop:variableName "phh2o" ],
                [ focal-transf-prop:variableName "nitrogen" ],
                [ focal-transf-prop:unit <http://qudt.org/vocab/unit/GM-PER-KiloGM> ;
                    focal-transf-prop:variableName "clay" ],
                [ focal-transf-prop:variableName "soc" ] ] ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/external-resource> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/species> rdfs:label "Tree species" ;
    rdfs:comment "Species of the stand. Only these four are accepted: smrk = Norway spruce (Picea abies), borovice = Scots pine (Pinus sylvestris), dub = pedunculate oak (Quercus robur), buk = European beech (Fagus sylvatica)." ;
    sld:type [ sld:type <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/enum> ] .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/stress_assessment> rdfs:label "Stress assessment" ;
    rdfs:comment "Stress index SI = 1 - I / I_ref against the 1991-2020 climate, stress years and their share across bootstrap members." ;
    sld:type cwl:File .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/stress_threshold> rdfs:label "Stress index threshold" ;
    rdfs:comment "Manual threshold on the stress index SI for flagging stress years. If omitted, the species- and age-specific thresholds shipped with the workflow are used." ;
    sld:type <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/float> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/stress_thresholds> rdfs:label "Stress thresholds table" ;
    rdfs:comment "Stress index threshold per species and age (90th percentile of SI, 1991-2020, Czech NFI sites). Ships with the workflow." ;
    sld:default <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/stress_thresholds_d.csv> ;
    sld:type cwl:File .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/stress_thresholds_d.csv> a cwl:File .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/trained-species> rdfs:comment "Only these four species are accepted by the API." ;
    focal-transf-prop:dimension <https://w3id.org/ogc/hosted/focal/transferability/dimensions/ecological> ;
    focal-transf-prop:inputRef "/inputs/species" ;
    focal-transf-prop:role <https://w3id.org/ogc/hosted/focal/transferability/roles/valid-for> ;
    focal-transf-prop:value [ focal-transf-prop:class "Fagus sylvatica",
                "Picea abies",
                "Pinus sylvestris",
                "Quercus robur" ;
            focal-transf-prop:classificationScheme <https://w3id.org/ogc/hosted/focal/transferability/classification-schemes/gbif-backbone> ] .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/typical_growth> rdfs:label "Typical growth" ;
    rdfs:comment "Typical height and increment of the species." ;
    sld:type cwl:File .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/czech-jurisdiction> rdfs:comment "Where the Czech forest management convention for rotation ages applies. The box is the FOCAL Czechia box, an approximation of the national territory." ;
    focal-transf-prop:dimension <https://w3id.org/ogc/hosted/focal/transferability/dimensions/jurisdictional> ;
    focal-transf-prop:inputRef "/inputs/latitude",
        "/inputs/longitude" ;
    focal-transf-prop:role <https://w3id.org/ogc/hosted/focal/transferability/roles/valid-for> ;
    focal-transf-prop:value [ geo:asWKT "POLYGON((12.07 48.48, 18.97 48.48, 18.97 51.08, 12.07 51.08, 12.07 48.48))"^^geo:wktLiteral ] .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/growth_model> a cwl:Directory ;
    rdfs:label "Trained growth model" ;
    rdfs:comment "LightGBM pipeline (central model and bootstrap ensemble) fitted to Czech National Forest Inventory data. Ships with the workflow." ;
    sld:default <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/growth_model> ;
    sld:type cwl:Directory .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/nfi-training-data> dcterms:title "Czech NFI stand measurements (species, age, mean height, site), 1964-2025" ;
    rdfs:comment "Not read at inference; needed to retrain. A replacement must give, per stand: species (the species to be modelled), stand age, mean height, coordinates and measurement year, with at least two measurements per stand. The intervals between the Czech measurements were mostly five years. Used by (delivered step names): training." ;
    focal-transf-prop:acceptanceCriteria [ focal-transf-prop:variable [ focal-transf-prop:variableName "species" ],
                [ focal-transf-prop:variableName "coordinates" ],
                [ focal-transf-prop:variableName "measurement year" ],
                [ focal-transf-prop:variableName "mean height" ],
                [ focal-transf-prop:variableName "stand age" ] ] ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/external-resource> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/rasdaman> dcterms:title "FOCAL Rasdaman data cube (rasql over SSH) and its registry (rasdaman_registry.json)" ;
    rdfs:comment "The delivered workflow reads climate data from a Rasdaman instance queried with rasql over SSH, located through rasdaman_registry.json. Another platform needs Rasdaman with the same layout and its own registry, or a custom climate loader returning the 32 annual features (the predictor accepts one). Within FOCAL new collections are configuration entries; the FOCAL registry is not transferable as is. Used by (delivered step names): data-access." ;
    focal-transf-prop:artifactRef "/inputs/rasdaman_connection",
        "/inputs/rasdaman_registry" ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/infrastructure> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/reference-increment> dcterms:title "reference_increment_d.csv: typical height and increment per species and age (Czech NFI medians)" ;
    rdfs:comment "Per species and age; regenerated by the same pipeline together with the model. Used by (delivered step names): typical-growth, default-initial-height." ;
    focal-transf-prop:artifactRef "/inputs/reference_increment" ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/workflow-input> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/rotation-age-beech> dcterms:title "Rotation age of European beech (130 years, Czech convention)" ;
    rdfs:comment "Czech forest management convention. Reported by the delivery as hard-coded in the current API; to be set per country." ;
    focal-transf-prop:artifactRef "/inputs/rotation_age_beech" ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/workflow-input> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/rotation-age-oak> dcterms:title "Rotation age of pedunculate oak (140 years, Czech convention)" ;
    rdfs:comment "Czech forest management convention. Reported by the delivery as hard-coded in the current API; to be set per country." ;
    focal-transf-prop:artifactRef "/inputs/rotation_age_oak" ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/workflow-input> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/rotation-age-pine> dcterms:title "Rotation age of Scots pine (110 years, Czech convention)" ;
    rdfs:comment "Czech forest management convention. Reported by the delivery as hard-coded in the current API; to be set per country." ;
    focal-transf-prop:artifactRef "/inputs/rotation_age_pine" ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/workflow-input> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/rotation-age-spruce> dcterms:title "Rotation age of Norway spruce (110 years, Czech convention)" ;
    rdfs:comment "Czech forest management convention. Reported by the delivery as hard-coded in the current API; to be set per country." ;
    focal-transf-prop:artifactRef "/inputs/rotation_age_spruce" ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/workflow-input> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/stress-thresholds> dcterms:title "stress_thresholds_d.csv: SI threshold per species and age (90th percentile of SI, 1991-2020, Czech NFI sites)" ;
    rdfs:comment "Per species and age; regenerated by the same pipeline together with the model. Used by (delivered step names): stress-years." ;
    focal-transf-prop:artifactRef "/inputs/stress_threshold",
        "/inputs/stress_thresholds" ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/workflow-input> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/training-feature-domain> rdfs:comment "1st-99th percentile of 30,883 training stand-years (final model). Outside, the tree-based model repeats edge behaviour; predictions are extrapolation. A per-species area-of-applicability check exists in the modelling code but is not run by the API. Bounds are the 1st and 99th percentiles. The categorical variable aspect (NFI code) is not a range and is not listed in the value; the delivered 1st-99th percentile codes were 100 to 900." ;
    focal-transf-prop:dimension <https://w3id.org/ogc/hosted/focal/transferability/dimensions/input-domain> ;
    focal-transf-prop:inputRef "/inputs/age",
        "/inputs/current_height",
        "/inputs/latitude",
        "/inputs/longitude" ;
    focal-transf-prop:role <https://w3id.org/ogc/hosted/focal/transferability/roles/valid-for> ;
    focal-transf-prop:value [ focal-transf-prop:variableRange [ focal-transf-prop:maximum 3.703e+02 ;
                    focal-transf-prop:minimum 9.911e+01 ;
                    focal-transf-prop:unitLabel "mm" ;
                    focal-transf-prop:variableName "P_spring_lag_1" ],
                [ focal-transf-prop:maximum 2.792e+01 ;
                    focal-transf-prop:minimum 1.625e+01 ;
                    focal-transf-prop:unitLabel "°C" ;
                    focal-transf-prop:variableName "T_amplitude_lag_1" ],
                [ focal-transf-prop:maximum 2.7e+01 ;
                    focal-transf-prop:minimum 4.369e-01 ;
                    focal-transf-prop:unitLabel "degrees" ;
                    focal-transf-prop:variableName "slope" ],
                [ focal-transf-prop:maximum 5.496e+02 ;
                    focal-transf-prop:minimum 1.364e+02 ;
                    focal-transf-prop:unitLabel "mm" ;
                    focal-transf-prop:variableName "P_summer" ],
                [ focal-transf-prop:maximum 1.017e+01 ;
                    focal-transf-prop:minimum 3.705e+00 ;
                    focal-transf-prop:unitLabel "°C" ;
                    focal-transf-prop:variableName "T_year" ],
                [ focal-transf-prop:maximum 1.653e+01 ;
                    focal-transf-prop:minimum 9.507e+00 ;
                    focal-transf-prop:unitLabel "°C" ;
                    focal-transf-prop:variableName "T_veg_lag_1" ],
                [ focal-transf-prop:maximum 1.2e+01 ;
                    focal-transf-prop:minimum 0e+00 ;
                    focal-transf-prop:unitLabel "days" ;
                    focal-transf-prop:variableName "HD30_veg_lag_1" ],
                [ focal-transf-prop:maximum 4.137e+02 ;
                    focal-transf-prop:minimum 9.832e+01 ;
                    focal-transf-prop:unitLabel "mm" ;
                    focal-transf-prop:variableName "P_prev_late_lag_1" ],
                [ focal-transf-prop:maximum 2.96e+02 ;
                    focal-transf-prop:minimum 7.2e+01 ;
                    focal-transf-prop:unitLabel "cg/kg" ;
                    focal-transf-prop:variableName "N_30_60" ],
                [ focal-transf-prop:maximum 3.712e+02 ;
                    focal-transf-prop:minimum 9.733e+01 ;
                    focal-transf-prop:unitLabel "mm" ;
                    focal-transf-prop:variableName "P_spring" ],
                [ focal-transf-prop:maximum 1.663e+02 ;
                    focal-transf-prop:minimum 1.125e+02 ;
                    focal-transf-prop:unitLabel "W/m²" ;
                    focal-transf-prop:variableName "SR_spring" ],
                [ focal-transf-prop:maximum 1.15e+03 ;
                    focal-transf-prop:minimum 1.75e+02 ;
                    focal-transf-prop:unitLabel "m a.s.l." ;
                    focal-transf-prop:variableName "elevation" ],
                [ focal-transf-prop:maximum 5.509e+02 ;
                    focal-transf-prop:minimum 1.374e+02 ;
                    focal-transf-prop:unitLabel "mm" ;
                    focal-transf-prop:variableName "P_summer_lag_1" ],
                [ focal-transf-prop:maximum 6.73e+02 ;
                    focal-transf-prop:minimum 1.61e+02 ;
                    focal-transf-prop:unitLabel "cg/kg" ;
                    focal-transf-prop:variableName "N_5_15" ],
                [ focal-transf-prop:maximum 1.106e+01 ;
                    focal-transf-prop:minimum 4.207e+00 ;
                    focal-transf-prop:unitLabel "°C" ;
                    focal-transf-prop:variableName "T_autumn" ],
                [ focal-transf-prop:maximum 1.814e+02 ;
                    focal-transf-prop:minimum 1.364e+02 ;
                    focal-transf-prop:unitLabel "W/m²" ;
                    focal-transf-prop:variableName "SR_veg_lag_1" ],
                [ focal-transf-prop:maximum 1.815e+02 ;
                    focal-transf-prop:minimum 1.368e+02 ;
                    focal-transf-prop:unitLabel "W/m²" ;
                    focal-transf-prop:variableName "SR_veg" ],
                [ focal-transf-prop:maximum 8.255e+02 ;
                    focal-transf-prop:minimum 1.932e+02 ;
                    focal-transf-prop:unitLabel "dg/kg" ;
                    focal-transf-prop:variableName "C" ],
                [ focal-transf-prop:maximum 3.1e+01 ;
                    focal-transf-prop:minimum 3e+00 ;
                    focal-transf-prop:unitLabel "days" ;
                    focal-transf-prop:variableName "R10mm_veg" ],
                [ focal-transf-prop:maximum 2.673e+01 ;
                    focal-transf-prop:minimum 1.588e+01 ;
                    focal-transf-prop:unitLabel "°C" ;
                    focal-transf-prop:variableName "Tmax_Aug" ],
                [ focal-transf-prop:maximum 2.9e+01 ;
                    focal-transf-prop:minimum 0e+00 ;
                    focal-transf-prop:unitLabel "days" ;
                    focal-transf-prop:variableName "FD_AprMay_lag_1" ],
                [ focal-transf-prop:maximum 4.11e+02 ;
                    focal-transf-prop:minimum 1.15e+02 ;
                    focal-transf-prop:unitLabel "cg/kg" ;
                    focal-transf-prop:variableName "N_15_30" ],
                [ focal-transf-prop:maximum 2.515e+00 ;
                    focal-transf-prop:minimum -2.009e+00 ;
                    focal-transf-prop:unitLabel "z-score" ;
                    focal-transf-prop:variableName "SPI_3_summer_lag_1" ],
                [ focal-transf-prop:maximum 3.1e+01 ;
                    focal-transf-prop:minimum 3e+00 ;
                    focal-transf-prop:unitLabel "days" ;
                    focal-transf-prop:variableName "R10mm_veg_lag_1" ],
                [ focal-transf-prop:maximum 2.8e+01 ;
                    focal-transf-prop:minimum 0e+00 ;
                    focal-transf-prop:unitLabel "days" ;
                    focal-transf-prop:variableName "FD_AprMay" ],
                [ focal-transf-prop:maximum 9e+01 ;
                    focal-transf-prop:minimum 4.5e+01 ;
                    focal-transf-prop:unitLabel "days" ;
                    focal-transf-prop:variableName "FD_winter_std" ],
                [ focal-transf-prop:maximum 1.096e+03 ;
                    focal-transf-prop:minimum 5.18e+02 ;
                    focal-transf-prop:unitLabel "cg/kg" ;
                    focal-transf-prop:variableName "N_0_5" ],
                [ focal-transf-prop:maximum 4.12e+02 ;
                    focal-transf-prop:minimum 9.756e+01 ;
                    focal-transf-prop:unitLabel "mm" ;
                    focal-transf-prop:variableName "P_prev_late" ],
                [ focal-transf-prop:maximum 3.392e+02 ;
                    focal-transf-prop:minimum 1.425e+02 ;
                    focal-transf-prop:unitLabel "g/kg" ;
                    focal-transf-prop:variableName "clay" ],
                [ focal-transf-prop:maximum 1.663e+02 ;
                    focal-transf-prop:minimum 1.12e+02 ;
                    focal-transf-prop:unitLabel "W/m²" ;
                    focal-transf-prop:variableName "SR_spring_lag_1" ],
                [ focal-transf-prop:maximum 1.44e+02 ;
                    focal-transf-prop:minimum 2.4e+01 ;
                    focal-transf-prop:unitLabel "years" ;
                    focal-transf-prop:variableName "age" ],
                [ focal-transf-prop:maximum 2.659e+01 ;
                    focal-transf-prop:minimum 1.588e+01 ;
                    focal-transf-prop:unitLabel "°C" ;
                    focal-transf-prop:variableName "Tmax_Aug_lag_1" ],
                [ focal-transf-prop:maximum 1.298e+00 ;
                    focal-transf-prop:minimum -1.054e+01 ;
                    focal-transf-prop:unitLabel "°C" ;
                    focal-transf-prop:variableName "T_min_month" ],
                [ focal-transf-prop:maximum 1.2e+01 ;
                    focal-transf-prop:minimum 0e+00 ;
                    focal-transf-prop:unitLabel "days" ;
                    focal-transf-prop:variableName "HD30_veg" ],
                [ focal-transf-prop:maximum 3.767e+01 ;
                    focal-transf-prop:minimum 9.99e+00 ;
                    focal-transf-prop:unitLabel "m" ;
                    focal-transf-prop:variableName "avg_h_lag" ],
                [ focal-transf-prop:maximum 2.67e+01 ;
                    focal-transf-prop:minimum 1.565e+01 ;
                    focal-transf-prop:unitLabel "°C" ;
                    focal-transf-prop:variableName "Tmax_Jul" ],
                [ focal-transf-prop:maximum 2.791e+01 ;
                    focal-transf-prop:minimum 1.626e+01 ;
                    focal-transf-prop:unitLabel "°C" ;
                    focal-transf-prop:variableName "T_amplitude" ],
                [ focal-transf-prop:maximum 2.667e+01 ;
                    focal-transf-prop:minimum 1.563e+01 ;
                    focal-transf-prop:unitLabel "°C" ;
                    focal-transf-prop:variableName "Tmax_Jul_lag_1" ],
                [ focal-transf-prop:maximum 1.249e+00 ;
                    focal-transf-prop:minimum -1.054e+01 ;
                    focal-transf-prop:unitLabel "°C" ;
                    focal-transf-prop:variableName "T_min_month_lag_1" ],
                [ focal-transf-prop:maximum 1.092e+01 ;
                    focal-transf-prop:minimum 4.183e+00 ;
                    focal-transf-prop:unitLabel "°C" ;
                    focal-transf-prop:variableName "T_autumn_lag_1" ],
                [ focal-transf-prop:maximum 6.5e+01 ;
                    focal-transf-prop:minimum 4.775e+01 ;
                    focal-transf-prop:unitLabel "pH × 10" ;
                    focal-transf-prop:variableName "pH" ],
                [ focal-transf-prop:maximum 2.483e+00 ;
                    focal-transf-prop:minimum -2.008e+00 ;
                    focal-transf-prop:unitLabel "z-score" ;
                    focal-transf-prop:variableName "SPI_3_summer" ],
                [ focal-transf-prop:maximum 9e+01 ;
                    focal-transf-prop:minimum 4.4e+01 ;
                    focal-transf-prop:unitLabel "days" ;
                    focal-transf-prop:variableName "FD_winter_std_lag_1" ] ] .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/growth-model> dcterms:title "LightGBM pipeline (central model + bootstrap ensemble), 45 inputs (training_feature_set_d.txt)" ;
    rdfs:comment "A replacement model takes 45 inputs in fixed order (training_feature_set_d.txt): age, elevation, aspect, slope, avg_h_lag, N_0_5, N_5_15, N_15_30, N_30_60, C, pH, clay, T_year, T_autumn, T_min_month, T_amplitude, T_veg_lag_1, T_autumn_lag_1, T_min_month_lag_1, T_amplitude_lag_1, SR_veg, SR_spring, SR_veg_lag_1, SR_spring_lag_1, P_spring, P_summer, P_prev_late, P_spring_lag_1, P_summer_lag_1, P_prev_late_lag_1, SPI_3_summer, SPI_3_summer_lag_1, Tmax_Jul, Tmax_Jul_lag_1, Tmax_Aug, Tmax_Aug_lag_1, HD30_veg, HD30_veg_lag_1, FD_AprMay, FD_AprMay_lag_1, FD_winter_std, FD_winter_std_lag_1, R10mm_veg, R10mm_veg_lag_1, species. Software: scikit-learn 1.9.1, LightGBM 4.7.0. Used by (delivered step names): growth-simulation, stress-index." ;
    focal-transf-prop:artifactRef "/inputs/growth_model" ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/workflow-input> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/czech-nfi-plots> rdfs:comment "Bounding box of the 1,756 Czech NFI (UHUL) monitoring stands used for training (1964-2025). Validation: spatial hold-out of 160 Czech stands, 2015-2025." ;
    focal-transf-prop:dimension <https://w3id.org/ogc/hosted/focal/transferability/dimensions/spatial> ;
    focal-transf-prop:inputRef "/inputs/latitude",
        "/inputs/longitude" ;
    focal-transf-prop:role <https://w3id.org/ogc/hosted/focal/transferability/roles/trained-on> ;
    focal-transf-prop:value [ geo:asWKT "POLYGON((12.2444 48.6232, 18.815 48.6232, 18.815 51.0198, 12.2444 51.0198, 12.2444 48.6232))"^^geo:wktLiteral ] .


```


### FP-WF2 — Climate stress indicators (an add-on bounded more tightly than the core)
A deterministic workflow whose general indicators move anywhere the data does, with a species add-on bounded by trait coverage and a national forest-type map. Rules that stop only some outputs name them in `affects`. Converted from the owners' record of 2026-11-18; input declarations are pending the owners' confirmation.

#### json
```json
{
  "class": "Workflow",
  "cwlVersion": "v1.2",
  "id": "",
  "label": "FWF2 - Climate stress indicators: heat, drought, SPEI (FOCAL Forest Pilot)",
  "doc": [
    "Computes heat, drought and combined climate-stress indicators, including SPEI, from daily temperature and precipitation for a point or an area, over any period and sub-period. An optional add-on links them to tree species through species heat and drought tolerance.",
    "Transferability record of workflow FP-WF2 (FWF2), record date 2026-11-18. Record basis: FWF2 code package (API, indicator engine, forest point summary, map layers, trends, species modules and tables, Rasdaman registry, source catalogue). Converted from the delivered record on 2026-11-25. Descriptive CWL profile: no steps are declared and the input and output identifiers are not yet those of an executable Application Package."
  ],
  "$namespaces": {
    "s": "https://schema.org/"
  },
  "s:identifier": "FP-WF2",
  "s:alternateName": "FWF2",
  "s:dateCreated": "2026-11-18",
  "requirements": {
    "SoftwareRequirement": {
      "packages": [
        {
          "package": "python"
        },
        {
          "package": "numpy"
        },
        {
          "package": "scipy"
        },
        {
          "package": "flask"
        },
        {
          "package": "gunicorn"
        }
      ]
    },
    "NetworkAccess": {
      "networkAccess": true
    }
  },
  "inputs": {
    "latitude": {
      "type": "double?",
      "label": "Latitude of the point",
      "doc": "Latitude in decimal degrees (WGS 84). Give latitude and longitude for a point, or bbox for an area."
    },
    "longitude": {
      "type": "double?",
      "label": "Longitude of the point",
      "doc": "Longitude in decimal degrees (WGS 84). Give together with latitude."
    },
    "bbox": {
      "type": "double[]?",
      "label": "Area of interest (bounding box)",
      "doc": "Area as [minimum longitude, minimum latitude, maximum longitude, maximum latitude] in decimal degrees (WGS 84). Alternative to latitude and longitude."
    },
    "start_date": {
      "type": "string",
      "label": "Start of the period",
      "doc": "First day of the period to evaluate (ISO 8601 date)."
    },
    "end_date": {
      "type": "string",
      "label": "End of the period",
      "doc": "Last day of the period to evaluate (ISO 8601 date)."
    },
    "sub_period": {
      "type": [
        "null",
        {
          "type": "enum",
          "symbols": [
            "whole_period",
            "month",
            "iso_week",
            "seven_day_window",
            "calendar_year",
            "user_year"
          ]
        }
      ],
      "label": "Sub-period",
      "doc": "How results are broken down within the period; averages over these units are also available."
    },
    "spei_scale": {
      "type": [
        "null",
        {
          "type": "enum",
          "symbols": [
            "monthly",
            "yearly"
          ]
        }
      ],
      "label": "SPEI time step",
      "doc": "Whether SPEI is computed monthly or yearly."
    },
    "heat_threshold": {
      "type": "float",
      "label": "Heat stress day threshold (degC)",
      "doc": "A day counts as a heat stress day when daily maximum temperature is at or above this value; heat stress units are degree-days above it. The default suits Central Europe; set it for the region.",
      "default": 30
    },
    "dry_day_threshold": {
      "type": "float",
      "label": "Dry day threshold (mm)",
      "doc": "A day with precipitation below this value counts as dry. The default suits Central Europe; set it for the region.",
      "default": 1
    },
    "dry_spell_min_days": {
      "type": "int",
      "label": "Minimum length of a drought period (days)",
      "doc": "Consecutive dry days needed for a drought period. The default suits Central Europe; set it for the region.",
      "default": 10
    },
    "heatwave_min_days": {
      "type": "int",
      "label": "Minimum length of a heatwave (days)",
      "doc": "Consecutive days needed for a heatwave in the forestry exposure summary. The default suits Central Europe; set it for the region.",
      "default": 6
    },
    "growing_season_start_month": {
      "type": "int",
      "label": "First month of the growing season",
      "doc": "Month number, 1 to 12. The default suits Central Europe; set it for the region.",
      "default": 4
    },
    "growing_season_end_month": {
      "type": "int",
      "label": "Last month of the growing season",
      "doc": "Month number, 1 to 12. The default suits Central Europe; set it for the region.",
      "default": 9
    },
    "species": {
      "type": "string[]?",
      "label": "Tree species",
      "doc": "Species to relate to heat and drought tolerance (optional species add-on), identified as in the species catalogue (species_codes.json, which carries Latin names). Outside Czechia, where the species-at-location lookup is not available, select them here."
    },
    "rasdaman_connection": {
      "type": "string",
      "label": "Data cube connection",
      "doc": "How to reach the Rasdaman instance that holds the climate data (queried with rasql over SSH). The connection variables are not named in the delivered material, so one string stands for them; we assume credentials are supplied by the execution environment."
    },
    "rasdaman_registry": {
      "type": "File",
      "label": "Data cube registry",
      "doc": "rasdaman_registry.json for that instance. The FOCAL registry is not transferable as is."
    },
    "climate_source_catalogue": {
      "type": "File",
      "label": "Climate source catalogue",
      "doc": "climate_source_catalog.json listing the sources and areas offered."
    },
    "readiness_collection": {
      "type": "string?",
      "label": "Readiness check collection",
      "doc": "Value for READINESS_COLLECTION, which defaults to a Czech ERA5-Land collection."
    },
    "t5_values": {
      "type": "File",
      "label": "Leaf heat tolerance (T5) table",
      "doc": "Leaf heat tolerance T5 per species with measurements and sources. Used by the species add-on. Ships with the workflow.",
      "default": {
        "class": "File",
        "location": "t5_values.json"
      }
    },
    "species_tolerances": {
      "type": "File",
      "label": "Drought and waterlogging tolerance table",
      "doc": "Tolerance scores 0-5 per species. Used by the species add-on. Ships with the workflow.",
      "default": {
        "class": "File",
        "location": "species_tolerances.json"
      }
    },
    "species_codes": {
      "type": "File",
      "label": "Species codes table",
      "doc": "Czech forestry species codes with Czech, English and Latin names. Used by the species add-on. Ships with the workflow.",
      "default": {
        "class": "File",
        "location": "species_codes.json"
      }
    },
    "slt_species": {
      "type": "File",
      "label": "Forest type species composition table",
      "doc": "Natural and target species composition of the Czech forest-type groups. Used by the species add-on. Ships with the workflow.",
      "default": {
        "class": "File",
        "location": "slt_species.json"
      }
    }
  },
  "outputs": {
    "heat_stress_days": {
      "type": "File",
      "label": "Heat stress days",
      "doc": "Days with daily maximum temperature at or above the threshold."
    },
    "heat_stress_units": {
      "type": "File",
      "label": "Heat stress units",
      "doc": "Degree-days above the heat threshold."
    },
    "drought_periods": {
      "type": "File",
      "label": "Drought periods",
      "doc": "Runs of consecutive dry days."
    },
    "heat_drought_periods": {
      "type": "File",
      "label": "Combined heat and drought periods",
      "doc": "Periods of combined heat and drought."
    },
    "spei": {
      "type": "File",
      "label": "SPEI",
      "doc": "Standardised Precipitation-Evapotranspiration Index, monthly or yearly."
    },
    "forest_climate_summary": {
      "type": "File",
      "label": "Forestry exposure summary",
      "doc": "SPEI-3 metrics, longest dry spell, hot days, TX90p days, longest heatwave and hot days during dry spells, with relative classes."
    },
    "trends": {
      "type": "File",
      "label": "Trends",
      "doc": "Sen's slope and Mann-Kendall trends."
    },
    "map_layers": {
      "type": "File",
      "label": "Map layers",
      "doc": "12 map layers."
    },
    "species_catalogue": {
      "type": "File?",
      "label": "Species catalogue",
      "doc": "Species with their codes and names (species add-on)."
    },
    "species_heat_threshold": {
      "type": "File?",
      "label": "Species heat thresholds",
      "doc": "T5-based heat threshold of the selected species (species add-on)."
    },
    "species_tolerance": {
      "type": "File?",
      "label": "Species tolerances",
      "doc": "Drought and waterlogging tolerance of the selected species (species add-on)."
    },
    "species_at_location": {
      "type": "File?",
      "label": "Species at the location",
      "doc": "Czech forest type and natural and target species composition at a point (species add-on)."
    },
    "forest_type_tolerance_ranking": {
      "type": "File?",
      "label": "Forest type tolerance ranking",
      "doc": "Tolerance ranking for the species of the forest type (species add-on)."
    }
  },
  "steps": {},
  "transferability": {
    "trainingRequired": false,
    "transferabilityNotes": "Envelope entries and rules that only described which data FOCAL currently holds, or its platform, are not part of this statement; what they said is kept in the notes of the artifacts concerned. An area or period for which no data is at hand is a matter of providing data (as delivered, in the data cube) that meets the artifact's criteria. The delivered record also notes: temporal extent is the year range of each collection, read from Rasdaman at runtime. The general climate-stress part is bounded only by data, the latitude limit of PET and SPEI and the need for 30 years of reference history; the species add-on adds species coverage and the Czech forest-type lookup.",
    "envelope": [
      {
        "id": "pet-latitude-limit",
        "role": "valid-for",
        "dimension": "spatial",
        "value": {
          "asWKT": "POLYGON((-180 -66.56, 180 -66.56, 180 66.56, -180 66.56, -180 -66.56))"
        },
        "inputRef": [
          "/inputs/latitude",
          "/inputs/longitude",
          "/inputs/bbox"
        ],
        "transferabilityNotes": "Latitude band |latitude| <= 66.56 degrees. FAO-56 extraterrestrial radiation in the Hargreaves PET is undefined during polar day/night; PET and SPEI return no value poleward of the Arctic/Antarctic circle. Other general indicators are unaffected."
      },
      {
        "id": "t5-species-coverage",
        "role": "valid-for",
        "dimension": "ecological",
        "value": {
          "scheme": "gbif-backbone",
          "classes": [
            "Picea abies",
            "Abies alba",
            "Pinus sylvestris",
            "Fagus sylvatica",
            "Quercus robur",
            "Carpinus betulus",
            "Acer platanoides",
            "Acer pseudoplatanus",
            "Alnus glutinosa",
            "Salix alba",
            "Salix fragilis"
          ]
        },
        "inputRef": "/inputs/species",
        "transferabilityNotes": "Species add-on only. Values are species traits from literature, independent of location; valid wherever these species grow. Species with a numeric T5. The delivered entry 'Salix alba / Salix fragilis' is listed as two taxa."
      },
      {
        "id": "tolerance-species-coverage",
        "role": "valid-for",
        "dimension": "ecological",
        "value": {
          "scheme": "gbif-backbone",
          "classes": [
            "Picea abies",
            "Abies alba",
            "Pinus sylvestris",
            "Fagus sylvatica",
            "Quercus robur",
            "Carpinus betulus",
            "Acer platanoides",
            "Acer pseudoplatanus",
            "Alnus glutinosa",
            "Larix decidua",
            "Betula pendula",
            "Sorbus aucuparia",
            "Pinus mugo",
            "Tilia cordata",
            "Populus tremula"
          ]
        },
        "inputRef": "/inputs/species",
        "transferabilityNotes": "Species add-on only. Values are species traits from literature, independent of location; valid wherever these species grow. Species with drought and waterlogging tolerance scores."
      },
      {
        "id": "czech-forest-type-map",
        "role": "can-run-on",
        "dimension": "spatial",
        "value": {
          "asWKT": "POLYGON((12.07 48.48, 18.97 48.48, 18.97 51.08, 12.07 51.08, 12.07 48.48))"
        },
        "inputRef": [
          "/inputs/latitude",
          "/inputs/longitude",
          "/inputs/bbox"
        ],
        "transferabilityNotes": "Species-at-location lookup (NLI WMS Lesni_typ + Czech forest typology). Czechia's forest land only; the box is the FOCAL Czechia bounding box standing in for the national border."
      }
    ],
    "artifacts": [
      {
        "id": "daily-climate",
        "artifact": "Daily temperature (minimum, average, maximum) and precipitation covering the requested period",
        "artifactRole": "workflow-input",
        "acceptanceCriteria": {
          "variables": [
            {
              "name": "tasmin",
              "units": [
                "DEG_C"
              ],
              "standardName": "air_temperature"
            },
            {
              "name": "tas",
              "units": [
                "DEG_C"
              ],
              "standardName": "air_temperature"
            },
            {
              "name": "tasmax",
              "units": [
                "DEG_C"
              ],
              "standardName": "air_temperature"
            },
            {
              "name": "pr",
              "units": [
                "MilliM-PER-DAY"
              ]
            }
          ],
          "temporal": {
            "resolution": "P1D",
            "calendar": [
              "standard",
              "proleptic_gregorian",
              "noleap"
            ]
          },
          "axes": [
            "time"
          ],
          "gridTypes": [
            "regular-latlon",
            "rotated-pole"
          ],
          "transferabilityNotes": "Structure: 3D [day, y, x]; temperature as a struct cell (min/avg/max) or as separate variables; 2D latitude/longitude of cell centres; no-data is NaN. 360_day calendars need conversion before ingest."
        },
        "transferabilityNotes": "As delivered, the workflow does not take these data as a file: it reads them from the Rasdaman data cube (artifact rasdaman), for the requested area and the years it needs. The delivered material gives no specification of the layout the code expects. Delivered as two datasets with the same requirements. (1) Projections: CMIP6-CORDEX EUR-11 GERICS-REMO2020 (MPI-ESM1-2-HR, EC-Earth3-Veg, MIROC6), SSP3-7.0, r1i1p1f1: daily temperature (tas_min/tas_avg/tas_max) and precipitation; SSP3-7.0 only, no historical experiment. Within FOCAL: daily data of these three simulations are held for the whole EUR-11 rotated grid and read directly, with no precompute (lon/lat bounding box 44.5939 W - 64.9644 E, 21.9878 - 72.585 N; the box overstates the rotated domain at its corners). Not usable outside that domain with these simulations: use another CORDEX domain or daily dataset meeting the criteria; other GCM-RCM pairs or scenarios can be obtained from ESGF. (2) Historical: ERA5-Land daily temperature (t2m_min/t2m_avg/t2m_max from hourly t2m) and daily precipitation sum (from hourly tp). Within FOCAL: held for Czechia, Spain and Finland; other areas by a routine precompute run. Outside FOCAL: ERA5-Land (Copernicus Climate Data Store), E-OBS or national grids. Native resolution of those sources: ERA5-Land 0.1 degrees (about 10 km), EUR-11 0.11 degrees (about 12.5 km). Used by (delivered step names): heat-stress-days, heat-stress-units, drought-periods, heat-drought-periods, spei, forest-climate-summary, trends, map-layers, spei-reference-history. SPEI, TX90p and the relative classes need 30 complete years before the evaluated period (or a fixed 30-year baseline), either in these data or in the reference history data."
      },
      {
        "id": "reference-history",
        "artifact": "Historical daily climate used as the reference history (ERA5-Land in the delivered setup)",
        "artifactRole": "workflow-input",
        "acceptanceCriteria": {
          "variables": [
            {
              "name": "tasmin",
              "units": [
                "DEG_C"
              ],
              "standardName": "air_temperature"
            },
            {
              "name": "tas",
              "units": [
                "DEG_C"
              ],
              "standardName": "air_temperature"
            },
            {
              "name": "tasmax",
              "units": [
                "DEG_C"
              ],
              "standardName": "air_temperature"
            },
            {
              "name": "pr",
              "units": [
                "MilliM-PER-DAY"
              ]
            }
          ],
          "temporal": {
            "resolution": "P1D",
            "calendar": [
              "standard",
              "proleptic_gregorian",
              "noleap"
            ],
            "minimumPrecedingYears": 30,
            "complete": true
          },
          "axes": [
            "time"
          ],
          "gridTypes": [
            "regular-latlon",
            "rotated-pole"
          ],
          "transferabilityNotes": "Structure: 3D [day, y, x]; temperature as a struct cell (min/avg/max) or as separate variables; 2D latitude/longitude of cell centres; no-data is NaN. 360_day calendars need conversion before ingest."
        },
        "transferabilityNotes": "As delivered, the workflow does not take these data as a file: it reads them from the Rasdaman data cube (artifact rasdaman), for the requested area and the years it needs. The delivered material gives no specification of the layout the code expects. Used only when the main data lack the history. SPEI, TX90p and relative classes need 30 complete years before the evaluated period (or a fixed 30-year baseline). Missing history is taken from a historical source quantile-mapped per calendar month to the primary source over their overlap, with at least 30 samples per month. Also needed when projections are evaluated. Within FOCAL: ERA5-Land is held for Czechia, Spain and Finland; other areas by a routine precompute run. Outside FOCAL: ERA5-Land (CDS), E-OBS or national grids. Used by (delivered step names): spei-reference-history, spei."
      },
      {
        "id": "t5-values",
        "artifact": "t5_values.json: leaf heat tolerance T5 (temperature at 5 % decline of Fv/Fm) per species, with measurements and sources (Kunert et al. 2022 and others)",
        "artifactRole": "workflow-input",
        "artifactRef": "/inputs/t5_values",
        "acceptanceCriteria": {
          "variables": [
            {
              "name": "code"
            },
            {
              "name": "lat"
            },
            {
              "name": "t5",
              "units": [
                "DEG_C"
              ]
            },
            {
              "name": "measurements"
            }
          ],
          "transferabilityNotes": "Endpoint T5: temperature at 5 % decline of Fv/Fm. Measurements carry their source. The key \"lat\" is the Latin species name, not a latitude."
        },
        "transferabilityNotes": "Species traits from literature, independent of location. Species add-on only. Used by (delivered step names): species-heat-threshold."
      },
      {
        "id": "species-tolerances",
        "artifact": "species_tolerances.json: drought and waterlogging tolerance 0-5 (Niinemets & Valladares 2006)",
        "artifactRole": "workflow-input",
        "artifactRef": "/inputs/species_tolerances",
        "transferabilityNotes": "A replacement gives drought and waterlogging tolerance on an ordinal 0-5 scale, from the same synthesis or an equivalent ordinal scale. The source synthesis covers temperate Northern Hemisphere trees and shrubs. Species add-on only. Used by (delivered step names): species-tolerance, forest-type-tolerance-ranking.",
        "acceptanceCriteria": {
          "variables": [
            {
              "name": "drought"
            },
            {
              "name": "waterlogging"
            }
          ]
        }
      },
      {
        "id": "species-codes",
        "artifact": "species_codes.json: Czech forestry species codes with Czech, English and Latin names",
        "artifactRole": "workflow-input",
        "artifactRef": "/inputs/species_codes",
        "transferabilityNotes": "The Latin names make it language independent. For further species, add codes. Used by (delivered step names): species-catalogue."
      },
      {
        "id": "nli-forest-type-service",
        "artifact": "NLI WMS (gp1/gp2.nli.gov.cz/wms_oprl), layer Lesni_typ, GetFeatureInfo; Czech regional forest development plans",
        "artifactRole": "external-resource",
        "transferabilityNotes": "Public service covering the forest land of Czechia only. A replacement is a point query returning a forest type or species code for the location, with coordinates in EPSG:4326 or transformable, plus an adapter. Used by (delivered step names): species-at-location."
      },
      {
        "id": "slt-species",
        "artifact": "slt_species.json: Czech forest-type groups (SLT, 105) with natural and target species composition (%)",
        "artifactRole": "workflow-input",
        "artifactRef": "/inputs/slt_species",
        "transferabilityNotes": "Defined for the Czech forest typology. Structure: {type-code: {name, natural: {species-code: %}, target: {species-code: %}}}, with the same species code list as species-codes. Used by (delivered step names): species-at-location, forest-type-tolerance-ranking."
      },
      {
        "id": "heat-threshold",
        "artifact": "Heat stress day threshold (Tmax >= 30 degC)",
        "artifactRole": "workflow-input",
        "artifactRef": "/inputs/heat_threshold",
        "transferabilityNotes": "30 degC is rarely reached in boreal climates and often in Mediterranean ones; set it per region or use TX90p."
      },
      {
        "id": "dry-day-threshold",
        "artifact": "Dry day threshold (< 1 mm)",
        "artifactRole": "workflow-input",
        "artifactRef": "/inputs/dry_day_threshold",
        "transferabilityNotes": "A request parameter."
      },
      {
        "id": "dry-spell-length",
        "artifact": "Drought period length (>= 10 days)",
        "artifactRole": "workflow-input",
        "artifactRef": "/inputs/dry_spell_min_days",
        "transferabilityNotes": "A 10-day dry spell is routine in a Mediterranean summer."
      },
      {
        "id": "heatwave-length",
        "artifact": "Heatwave length (>= 6 days)",
        "artifactRole": "workflow-input",
        "artifactRef": "/inputs/heatwave_min_days",
        "transferabilityNotes": "A request parameter."
      },
      {
        "id": "growing-season-start",
        "artifact": "Growing season start (April)",
        "artifactRole": "workflow-input",
        "artifactRef": "/inputs/growing_season_start_month",
        "transferabilityNotes": "Northern Hemisphere temperate default (April-September); e.g. shorter in boreal forests; in Mediterranean forests the summer drought falls inside it."
      },
      {
        "id": "growing-season-end",
        "artifact": "Growing season end (September)",
        "artifactRole": "workflow-input",
        "artifactRef": "/inputs/growing_season_end_month",
        "transferabilityNotes": "Northern Hemisphere temperate default (April-September); see growing-season-start."
      },
      {
        "id": "rasdaman",
        "artifact": "FOCAL Rasdaman data cube (rasql over SSH), source catalogue and registry (climate_source_catalog.json, rasdaman_registry.json)",
        "artifactRole": "infrastructure",
        "artifactRef": [
          "/inputs/rasdaman_connection",
          "/inputs/rasdaman_registry",
          "/inputs/climate_source_catalogue",
          "/inputs/readiness_collection"
        ],
        "transferabilityNotes": "The delivered workflow reads data from a Rasdaman instance queried with rasql over SSH. Another platform needs Rasdaman with the same registry layout (set READINESS_COLLECTION, which defaults to a Czech ERA5-Land collection) and its own registry, or file-based data access instead; the computation uses NumPy and SciPy. Within FOCAL: add catalogue and registry entries for a new area (user interface listing, new ERA5-Land collections). The FOCAL registry is not transferable as is. Used by (delivered step names): data-access."
      }
    ],
    "rules": [
      {
        "appliesTo": [
          "daily-climate",
          "reference-history"
        ],
        "when": [
          {
            "constraint": "pet-latitude-limit",
            "test": "outside"
          }
        ],
        "affects": [
          "/outputs/spei",
          "/outputs/forest_climate_summary"
        ],
        "actions": [
          "component-not-executable"
        ],
        "mandatory": true,
        "transferabilityNotes": "PET/SPEI undefined poleward of 66.56 deg; other indicators still run. Fix needs a code change (clipping of the sunset-angle term)."
      },
      {
        "appliesTo": [
          "t5-values"
        ],
        "when": [
          {
            "constraint": "t5-species-coverage",
            "test": "different-class-from"
          }
        ],
        "actions": [
          "replace-with-local-equivalent"
        ],
        "mandatory": false,
        "transferabilityNotes": "Add literature values for the species in question; general part unaffected. Without them there is no T5-based heat result for the species. Literature T5 values must use the same endpoint."
      },
      {
        "appliesTo": [
          "species-tolerances"
        ],
        "when": [
          {
            "constraint": "tolerance-species-coverage",
            "test": "different-class-from"
          }
        ],
        "actions": [
          "replace-with-local-equivalent"
        ],
        "mandatory": false,
        "transferabilityNotes": "Add literature values for the species in question; general part unaffected. Without them there is no tolerance result for the species. Use values from the same synthesis."
      },
      {
        "appliesTo": [
          "nli-forest-type-service",
          "slt-species"
        ],
        "when": [
          {
            "constraint": "czech-forest-type-map",
            "test": "outside"
          }
        ],
        "affects": [
          "/outputs/species_at_location",
          "/outputs/forest_type_tolerance_ranking"
        ],
        "actions": [
          "replace-with-local-equivalent",
          "component-not-executable"
        ],
        "mandatory": true,
        "transferabilityNotes": "Either connect a national forest typology/species map with a point query and a composition table, or the lookup is unavailable and users select species manually. General part unaffected."
      },
      {
        "appliesTo": [
          "heat-threshold",
          "dry-day-threshold",
          "dry-spell-length",
          "heatwave-length",
          "growing-season-start",
          "growing-season-end"
        ],
        "triggeredBy": "different-climate-regime",
        "actions": [
          "replace-with-local-equivalent"
        ],
        "mandatory": false,
        "transferabilityNotes": "The default thresholds and growing season suit Central Europe; they are request parameters and should be set per region. If kept, counts and classes based on them are less meaningful for the region."
      },
      {
        "appliesTo": [
          "rasdaman"
        ],
        "triggeredBy": "service-unavailable",
        "actions": [
          "replace-with-local-equivalent"
        ],
        "mandatory": true,
        "transferabilityNotes": "Applies where no Rasdaman instance is available to the workflow: set one up with the same layout and its own registry, or change the code that reads the data (see the rasdaman artifact). On the FOCAL instance, a missing area is instead added as new collections and entries."
      }
    ]
  },
  "computationType": "deterministic-rule-based",
  "maturityStatus": "operational",
  "qualityAnnotation": [
    {
      "dimension": "method-limitation",
      "note": "Default thresholds (Tmax >= 30 degC, dry day < 1 mm, dry spell >= 10 days, heatwave >= 6 days, growing season Apr-Sep) suit Central Europe; they are request parameters and should be set per region."
    },
    {
      "dimension": "method-limitation",
      "note": "Hargreaves PET is temperature-based; SPEI standardisation reduces but does not remove its bias."
    },
    {
      "dimension": "method-limitation",
      "note": "Historical years taken from another source are quantile-mapped per calendar month; this aligns distributions, it is not a full bias adjustment."
    },
    {
      "dimension": "proxy-variable",
      "note": "T5 is a leaf-tissue threshold from short laboratory exposures, compared with daily maximum air temperature; species heat counts are indicative."
    },
    {
      "dimension": "intended-use-limit",
      "note": "Drought and waterlogging tolerance scores are ordinal rankings, not mortality or SPEI thresholds."
    },
    {
      "dimension": "proxy-variable",
      "note": "Czech forest-type lookup returns potential natural and target composition, not the actual stand."
    },
    {
      "dimension": "method-limitation",
      "note": "10 km (ERA5-Land) and 12.5 km (EUR-11); IDW adds no detail."
    },
    {
      "dimension": "method-limitation",
      "note": "One RCM, three GCMs, one scenario (SSP3-7.0)."
    }
  ]
}

```

#### jsonld
```jsonld
{
  "@context": "https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/workflow/context.jsonld",
  "class": "Workflow",
  "cwlVersion": "v1.2",
  "id": "",
  "label": "FWF2 - Climate stress indicators: heat, drought, SPEI (FOCAL Forest Pilot)",
  "doc": [
    "Computes heat, drought and combined climate-stress indicators, including SPEI, from daily temperature and precipitation for a point or an area, over any period and sub-period. An optional add-on links them to tree species through species heat and drought tolerance.",
    "Transferability record of workflow FP-WF2 (FWF2), record date 2026-11-18. Record basis: FWF2 code package (API, indicator engine, forest point summary, map layers, trends, species modules and tables, Rasdaman registry, source catalogue). Converted from the delivered record on 2026-11-25. Descriptive CWL profile: no steps are declared and the input and output identifiers are not yet those of an executable Application Package."
  ],
  "$namespaces": {
    "s": "https://schema.org/"
  },
  "s:identifier": "FP-WF2",
  "s:alternateName": "FWF2",
  "s:dateCreated": "2026-11-18",
  "requirements": {
    "SoftwareRequirement": {
      "packages": [
        {
          "package": "python"
        },
        {
          "package": "numpy"
        },
        {
          "package": "scipy"
        },
        {
          "package": "flask"
        },
        {
          "package": "gunicorn"
        }
      ]
    },
    "NetworkAccess": {
      "networkAccess": true
    }
  },
  "inputs": {
    "latitude": {
      "type": "double?",
      "label": "Latitude of the point",
      "doc": "Latitude in decimal degrees (WGS 84). Give latitude and longitude for a point, or bbox for an area."
    },
    "longitude": {
      "type": "double?",
      "label": "Longitude of the point",
      "doc": "Longitude in decimal degrees (WGS 84). Give together with latitude."
    },
    "bbox": {
      "type": "double[]?",
      "label": "Area of interest (bounding box)",
      "doc": "Area as [minimum longitude, minimum latitude, maximum longitude, maximum latitude] in decimal degrees (WGS 84). Alternative to latitude and longitude."
    },
    "start_date": {
      "type": "string",
      "label": "Start of the period",
      "doc": "First day of the period to evaluate (ISO 8601 date)."
    },
    "end_date": {
      "type": "string",
      "label": "End of the period",
      "doc": "Last day of the period to evaluate (ISO 8601 date)."
    },
    "sub_period": {
      "type": [
        "null",
        {
          "type": "enum",
          "symbols": [
            "whole_period",
            "month",
            "iso_week",
            "seven_day_window",
            "calendar_year",
            "user_year"
          ]
        }
      ],
      "label": "Sub-period",
      "doc": "How results are broken down within the period; averages over these units are also available."
    },
    "spei_scale": {
      "type": [
        "null",
        {
          "type": "enum",
          "symbols": [
            "monthly",
            "yearly"
          ]
        }
      ],
      "label": "SPEI time step",
      "doc": "Whether SPEI is computed monthly or yearly."
    },
    "heat_threshold": {
      "type": "float",
      "label": "Heat stress day threshold (degC)",
      "doc": "A day counts as a heat stress day when daily maximum temperature is at or above this value; heat stress units are degree-days above it. The default suits Central Europe; set it for the region.",
      "default": 30
    },
    "dry_day_threshold": {
      "type": "float",
      "label": "Dry day threshold (mm)",
      "doc": "A day with precipitation below this value counts as dry. The default suits Central Europe; set it for the region.",
      "default": 1
    },
    "dry_spell_min_days": {
      "type": "int",
      "label": "Minimum length of a drought period (days)",
      "doc": "Consecutive dry days needed for a drought period. The default suits Central Europe; set it for the region.",
      "default": 10
    },
    "heatwave_min_days": {
      "type": "int",
      "label": "Minimum length of a heatwave (days)",
      "doc": "Consecutive days needed for a heatwave in the forestry exposure summary. The default suits Central Europe; set it for the region.",
      "default": 6
    },
    "growing_season_start_month": {
      "type": "int",
      "label": "First month of the growing season",
      "doc": "Month number, 1 to 12. The default suits Central Europe; set it for the region.",
      "default": 4
    },
    "growing_season_end_month": {
      "type": "int",
      "label": "Last month of the growing season",
      "doc": "Month number, 1 to 12. The default suits Central Europe; set it for the region.",
      "default": 9
    },
    "species": {
      "type": "string[]?",
      "label": "Tree species",
      "doc": "Species to relate to heat and drought tolerance (optional species add-on), identified as in the species catalogue (species_codes.json, which carries Latin names). Outside Czechia, where the species-at-location lookup is not available, select them here."
    },
    "rasdaman_connection": {
      "type": "string",
      "label": "Data cube connection",
      "doc": "How to reach the Rasdaman instance that holds the climate data (queried with rasql over SSH). The connection variables are not named in the delivered material, so one string stands for them; we assume credentials are supplied by the execution environment."
    },
    "rasdaman_registry": {
      "type": "File",
      "label": "Data cube registry",
      "doc": "rasdaman_registry.json for that instance. The FOCAL registry is not transferable as is."
    },
    "climate_source_catalogue": {
      "type": "File",
      "label": "Climate source catalogue",
      "doc": "climate_source_catalog.json listing the sources and areas offered."
    },
    "readiness_collection": {
      "type": "string?",
      "label": "Readiness check collection",
      "doc": "Value for READINESS_COLLECTION, which defaults to a Czech ERA5-Land collection."
    },
    "t5_values": {
      "type": "File",
      "label": "Leaf heat tolerance (T5) table",
      "doc": "Leaf heat tolerance T5 per species with measurements and sources. Used by the species add-on. Ships with the workflow.",
      "default": {
        "class": "File",
        "location": "t5_values.json"
      }
    },
    "species_tolerances": {
      "type": "File",
      "label": "Drought and waterlogging tolerance table",
      "doc": "Tolerance scores 0-5 per species. Used by the species add-on. Ships with the workflow.",
      "default": {
        "class": "File",
        "location": "species_tolerances.json"
      }
    },
    "species_codes": {
      "type": "File",
      "label": "Species codes table",
      "doc": "Czech forestry species codes with Czech, English and Latin names. Used by the species add-on. Ships with the workflow.",
      "default": {
        "class": "File",
        "location": "species_codes.json"
      }
    },
    "slt_species": {
      "type": "File",
      "label": "Forest type species composition table",
      "doc": "Natural and target species composition of the Czech forest-type groups. Used by the species add-on. Ships with the workflow.",
      "default": {
        "class": "File",
        "location": "slt_species.json"
      }
    }
  },
  "outputs": {
    "heat_stress_days": {
      "type": "File",
      "label": "Heat stress days",
      "doc": "Days with daily maximum temperature at or above the threshold."
    },
    "heat_stress_units": {
      "type": "File",
      "label": "Heat stress units",
      "doc": "Degree-days above the heat threshold."
    },
    "drought_periods": {
      "type": "File",
      "label": "Drought periods",
      "doc": "Runs of consecutive dry days."
    },
    "heat_drought_periods": {
      "type": "File",
      "label": "Combined heat and drought periods",
      "doc": "Periods of combined heat and drought."
    },
    "spei": {
      "type": "File",
      "label": "SPEI",
      "doc": "Standardised Precipitation-Evapotranspiration Index, monthly or yearly."
    },
    "forest_climate_summary": {
      "type": "File",
      "label": "Forestry exposure summary",
      "doc": "SPEI-3 metrics, longest dry spell, hot days, TX90p days, longest heatwave and hot days during dry spells, with relative classes."
    },
    "trends": {
      "type": "File",
      "label": "Trends",
      "doc": "Sen's slope and Mann-Kendall trends."
    },
    "map_layers": {
      "type": "File",
      "label": "Map layers",
      "doc": "12 map layers."
    },
    "species_catalogue": {
      "type": "File?",
      "label": "Species catalogue",
      "doc": "Species with their codes and names (species add-on)."
    },
    "species_heat_threshold": {
      "type": "File?",
      "label": "Species heat thresholds",
      "doc": "T5-based heat threshold of the selected species (species add-on)."
    },
    "species_tolerance": {
      "type": "File?",
      "label": "Species tolerances",
      "doc": "Drought and waterlogging tolerance of the selected species (species add-on)."
    },
    "species_at_location": {
      "type": "File?",
      "label": "Species at the location",
      "doc": "Czech forest type and natural and target species composition at a point (species add-on)."
    },
    "forest_type_tolerance_ranking": {
      "type": "File?",
      "label": "Forest type tolerance ranking",
      "doc": "Tolerance ranking for the species of the forest type (species add-on)."
    }
  },
  "steps": {},
  "transferability": {
    "trainingRequired": false,
    "transferabilityNotes": "Envelope entries and rules that only described which data FOCAL currently holds, or its platform, are not part of this statement; what they said is kept in the notes of the artifacts concerned. An area or period for which no data is at hand is a matter of providing data (as delivered, in the data cube) that meets the artifact's criteria. The delivered record also notes: temporal extent is the year range of each collection, read from Rasdaman at runtime. The general climate-stress part is bounded only by data, the latitude limit of PET and SPEI and the need for 30 years of reference history; the species add-on adds species coverage and the Czech forest-type lookup.",
    "envelope": [
      {
        "id": "pet-latitude-limit",
        "role": "valid-for",
        "dimension": "spatial",
        "value": {
          "asWKT": "POLYGON((-180 -66.56, 180 -66.56, 180 66.56, -180 66.56, -180 -66.56))"
        },
        "inputRef": [
          "/inputs/latitude",
          "/inputs/longitude",
          "/inputs/bbox"
        ],
        "transferabilityNotes": "Latitude band |latitude| <= 66.56 degrees. FAO-56 extraterrestrial radiation in the Hargreaves PET is undefined during polar day/night; PET and SPEI return no value poleward of the Arctic/Antarctic circle. Other general indicators are unaffected."
      },
      {
        "id": "t5-species-coverage",
        "role": "valid-for",
        "dimension": "ecological",
        "value": {
          "scheme": "gbif-backbone",
          "classes": [
            "Picea abies",
            "Abies alba",
            "Pinus sylvestris",
            "Fagus sylvatica",
            "Quercus robur",
            "Carpinus betulus",
            "Acer platanoides",
            "Acer pseudoplatanus",
            "Alnus glutinosa",
            "Salix alba",
            "Salix fragilis"
          ]
        },
        "inputRef": "/inputs/species",
        "transferabilityNotes": "Species add-on only. Values are species traits from literature, independent of location; valid wherever these species grow. Species with a numeric T5. The delivered entry 'Salix alba / Salix fragilis' is listed as two taxa."
      },
      {
        "id": "tolerance-species-coverage",
        "role": "valid-for",
        "dimension": "ecological",
        "value": {
          "scheme": "gbif-backbone",
          "classes": [
            "Picea abies",
            "Abies alba",
            "Pinus sylvestris",
            "Fagus sylvatica",
            "Quercus robur",
            "Carpinus betulus",
            "Acer platanoides",
            "Acer pseudoplatanus",
            "Alnus glutinosa",
            "Larix decidua",
            "Betula pendula",
            "Sorbus aucuparia",
            "Pinus mugo",
            "Tilia cordata",
            "Populus tremula"
          ]
        },
        "inputRef": "/inputs/species",
        "transferabilityNotes": "Species add-on only. Values are species traits from literature, independent of location; valid wherever these species grow. Species with drought and waterlogging tolerance scores."
      },
      {
        "id": "czech-forest-type-map",
        "role": "can-run-on",
        "dimension": "spatial",
        "value": {
          "asWKT": "POLYGON((12.07 48.48, 18.97 48.48, 18.97 51.08, 12.07 51.08, 12.07 48.48))"
        },
        "inputRef": [
          "/inputs/latitude",
          "/inputs/longitude",
          "/inputs/bbox"
        ],
        "transferabilityNotes": "Species-at-location lookup (NLI WMS Lesni_typ + Czech forest typology). Czechia's forest land only; the box is the FOCAL Czechia bounding box standing in for the national border."
      }
    ],
    "artifacts": [
      {
        "id": "daily-climate",
        "artifact": "Daily temperature (minimum, average, maximum) and precipitation covering the requested period",
        "artifactRole": "workflow-input",
        "acceptanceCriteria": {
          "variables": [
            {
              "name": "tasmin",
              "units": [
                "DEG_C"
              ],
              "standardName": "air_temperature"
            },
            {
              "name": "tas",
              "units": [
                "DEG_C"
              ],
              "standardName": "air_temperature"
            },
            {
              "name": "tasmax",
              "units": [
                "DEG_C"
              ],
              "standardName": "air_temperature"
            },
            {
              "name": "pr",
              "units": [
                "MilliM-PER-DAY"
              ]
            }
          ],
          "temporal": {
            "resolution": "P1D",
            "calendar": [
              "standard",
              "proleptic_gregorian",
              "noleap"
            ]
          },
          "axes": [
            "time"
          ],
          "gridTypes": [
            "regular-latlon",
            "rotated-pole"
          ],
          "transferabilityNotes": "Structure: 3D [day, y, x]; temperature as a struct cell (min/avg/max) or as separate variables; 2D latitude/longitude of cell centres; no-data is NaN. 360_day calendars need conversion before ingest."
        },
        "transferabilityNotes": "As delivered, the workflow does not take these data as a file: it reads them from the Rasdaman data cube (artifact rasdaman), for the requested area and the years it needs. The delivered material gives no specification of the layout the code expects. Delivered as two datasets with the same requirements. (1) Projections: CMIP6-CORDEX EUR-11 GERICS-REMO2020 (MPI-ESM1-2-HR, EC-Earth3-Veg, MIROC6), SSP3-7.0, r1i1p1f1: daily temperature (tas_min/tas_avg/tas_max) and precipitation; SSP3-7.0 only, no historical experiment. Within FOCAL: daily data of these three simulations are held for the whole EUR-11 rotated grid and read directly, with no precompute (lon/lat bounding box 44.5939 W - 64.9644 E, 21.9878 - 72.585 N; the box overstates the rotated domain at its corners). Not usable outside that domain with these simulations: use another CORDEX domain or daily dataset meeting the criteria; other GCM-RCM pairs or scenarios can be obtained from ESGF. (2) Historical: ERA5-Land daily temperature (t2m_min/t2m_avg/t2m_max from hourly t2m) and daily precipitation sum (from hourly tp). Within FOCAL: held for Czechia, Spain and Finland; other areas by a routine precompute run. Outside FOCAL: ERA5-Land (Copernicus Climate Data Store), E-OBS or national grids. Native resolution of those sources: ERA5-Land 0.1 degrees (about 10 km), EUR-11 0.11 degrees (about 12.5 km). Used by (delivered step names): heat-stress-days, heat-stress-units, drought-periods, heat-drought-periods, spei, forest-climate-summary, trends, map-layers, spei-reference-history. SPEI, TX90p and the relative classes need 30 complete years before the evaluated period (or a fixed 30-year baseline), either in these data or in the reference history data."
      },
      {
        "id": "reference-history",
        "artifact": "Historical daily climate used as the reference history (ERA5-Land in the delivered setup)",
        "artifactRole": "workflow-input",
        "acceptanceCriteria": {
          "variables": [
            {
              "name": "tasmin",
              "units": [
                "DEG_C"
              ],
              "standardName": "air_temperature"
            },
            {
              "name": "tas",
              "units": [
                "DEG_C"
              ],
              "standardName": "air_temperature"
            },
            {
              "name": "tasmax",
              "units": [
                "DEG_C"
              ],
              "standardName": "air_temperature"
            },
            {
              "name": "pr",
              "units": [
                "MilliM-PER-DAY"
              ]
            }
          ],
          "temporal": {
            "resolution": "P1D",
            "calendar": [
              "standard",
              "proleptic_gregorian",
              "noleap"
            ],
            "minimumPrecedingYears": 30,
            "complete": true
          },
          "axes": [
            "time"
          ],
          "gridTypes": [
            "regular-latlon",
            "rotated-pole"
          ],
          "transferabilityNotes": "Structure: 3D [day, y, x]; temperature as a struct cell (min/avg/max) or as separate variables; 2D latitude/longitude of cell centres; no-data is NaN. 360_day calendars need conversion before ingest."
        },
        "transferabilityNotes": "As delivered, the workflow does not take these data as a file: it reads them from the Rasdaman data cube (artifact rasdaman), for the requested area and the years it needs. The delivered material gives no specification of the layout the code expects. Used only when the main data lack the history. SPEI, TX90p and relative classes need 30 complete years before the evaluated period (or a fixed 30-year baseline). Missing history is taken from a historical source quantile-mapped per calendar month to the primary source over their overlap, with at least 30 samples per month. Also needed when projections are evaluated. Within FOCAL: ERA5-Land is held for Czechia, Spain and Finland; other areas by a routine precompute run. Outside FOCAL: ERA5-Land (CDS), E-OBS or national grids. Used by (delivered step names): spei-reference-history, spei."
      },
      {
        "id": "t5-values",
        "artifact": "t5_values.json: leaf heat tolerance T5 (temperature at 5 % decline of Fv/Fm) per species, with measurements and sources (Kunert et al. 2022 and others)",
        "artifactRole": "workflow-input",
        "artifactRef": "/inputs/t5_values",
        "acceptanceCriteria": {
          "variables": [
            {
              "name": "code"
            },
            {
              "name": "lat"
            },
            {
              "name": "t5",
              "units": [
                "DEG_C"
              ]
            },
            {
              "name": "measurements"
            }
          ],
          "transferabilityNotes": "Endpoint T5: temperature at 5 % decline of Fv/Fm. Measurements carry their source. The key \"lat\" is the Latin species name, not a latitude."
        },
        "transferabilityNotes": "Species traits from literature, independent of location. Species add-on only. Used by (delivered step names): species-heat-threshold."
      },
      {
        "id": "species-tolerances",
        "artifact": "species_tolerances.json: drought and waterlogging tolerance 0-5 (Niinemets & Valladares 2006)",
        "artifactRole": "workflow-input",
        "artifactRef": "/inputs/species_tolerances",
        "transferabilityNotes": "A replacement gives drought and waterlogging tolerance on an ordinal 0-5 scale, from the same synthesis or an equivalent ordinal scale. The source synthesis covers temperate Northern Hemisphere trees and shrubs. Species add-on only. Used by (delivered step names): species-tolerance, forest-type-tolerance-ranking.",
        "acceptanceCriteria": {
          "variables": [
            {
              "name": "drought"
            },
            {
              "name": "waterlogging"
            }
          ]
        }
      },
      {
        "id": "species-codes",
        "artifact": "species_codes.json: Czech forestry species codes with Czech, English and Latin names",
        "artifactRole": "workflow-input",
        "artifactRef": "/inputs/species_codes",
        "transferabilityNotes": "The Latin names make it language independent. For further species, add codes. Used by (delivered step names): species-catalogue."
      },
      {
        "id": "nli-forest-type-service",
        "artifact": "NLI WMS (gp1/gp2.nli.gov.cz/wms_oprl), layer Lesni_typ, GetFeatureInfo; Czech regional forest development plans",
        "artifactRole": "external-resource",
        "transferabilityNotes": "Public service covering the forest land of Czechia only. A replacement is a point query returning a forest type or species code for the location, with coordinates in EPSG:4326 or transformable, plus an adapter. Used by (delivered step names): species-at-location."
      },
      {
        "id": "slt-species",
        "artifact": "slt_species.json: Czech forest-type groups (SLT, 105) with natural and target species composition (%)",
        "artifactRole": "workflow-input",
        "artifactRef": "/inputs/slt_species",
        "transferabilityNotes": "Defined for the Czech forest typology. Structure: {type-code: {name, natural: {species-code: %}, target: {species-code: %}}}, with the same species code list as species-codes. Used by (delivered step names): species-at-location, forest-type-tolerance-ranking."
      },
      {
        "id": "heat-threshold",
        "artifact": "Heat stress day threshold (Tmax >= 30 degC)",
        "artifactRole": "workflow-input",
        "artifactRef": "/inputs/heat_threshold",
        "transferabilityNotes": "30 degC is rarely reached in boreal climates and often in Mediterranean ones; set it per region or use TX90p."
      },
      {
        "id": "dry-day-threshold",
        "artifact": "Dry day threshold (< 1 mm)",
        "artifactRole": "workflow-input",
        "artifactRef": "/inputs/dry_day_threshold",
        "transferabilityNotes": "A request parameter."
      },
      {
        "id": "dry-spell-length",
        "artifact": "Drought period length (>= 10 days)",
        "artifactRole": "workflow-input",
        "artifactRef": "/inputs/dry_spell_min_days",
        "transferabilityNotes": "A 10-day dry spell is routine in a Mediterranean summer."
      },
      {
        "id": "heatwave-length",
        "artifact": "Heatwave length (>= 6 days)",
        "artifactRole": "workflow-input",
        "artifactRef": "/inputs/heatwave_min_days",
        "transferabilityNotes": "A request parameter."
      },
      {
        "id": "growing-season-start",
        "artifact": "Growing season start (April)",
        "artifactRole": "workflow-input",
        "artifactRef": "/inputs/growing_season_start_month",
        "transferabilityNotes": "Northern Hemisphere temperate default (April-September); e.g. shorter in boreal forests; in Mediterranean forests the summer drought falls inside it."
      },
      {
        "id": "growing-season-end",
        "artifact": "Growing season end (September)",
        "artifactRole": "workflow-input",
        "artifactRef": "/inputs/growing_season_end_month",
        "transferabilityNotes": "Northern Hemisphere temperate default (April-September); see growing-season-start."
      },
      {
        "id": "rasdaman",
        "artifact": "FOCAL Rasdaman data cube (rasql over SSH), source catalogue and registry (climate_source_catalog.json, rasdaman_registry.json)",
        "artifactRole": "infrastructure",
        "artifactRef": [
          "/inputs/rasdaman_connection",
          "/inputs/rasdaman_registry",
          "/inputs/climate_source_catalogue",
          "/inputs/readiness_collection"
        ],
        "transferabilityNotes": "The delivered workflow reads data from a Rasdaman instance queried with rasql over SSH. Another platform needs Rasdaman with the same registry layout (set READINESS_COLLECTION, which defaults to a Czech ERA5-Land collection) and its own registry, or file-based data access instead; the computation uses NumPy and SciPy. Within FOCAL: add catalogue and registry entries for a new area (user interface listing, new ERA5-Land collections). The FOCAL registry is not transferable as is. Used by (delivered step names): data-access."
      }
    ],
    "rules": [
      {
        "appliesTo": [
          "daily-climate",
          "reference-history"
        ],
        "when": [
          {
            "constraint": "pet-latitude-limit",
            "test": "outside"
          }
        ],
        "affects": [
          "/outputs/spei",
          "/outputs/forest_climate_summary"
        ],
        "actions": [
          "component-not-executable"
        ],
        "mandatory": true,
        "transferabilityNotes": "PET/SPEI undefined poleward of 66.56 deg; other indicators still run. Fix needs a code change (clipping of the sunset-angle term)."
      },
      {
        "appliesTo": [
          "t5-values"
        ],
        "when": [
          {
            "constraint": "t5-species-coverage",
            "test": "different-class-from"
          }
        ],
        "actions": [
          "replace-with-local-equivalent"
        ],
        "mandatory": false,
        "transferabilityNotes": "Add literature values for the species in question; general part unaffected. Without them there is no T5-based heat result for the species. Literature T5 values must use the same endpoint."
      },
      {
        "appliesTo": [
          "species-tolerances"
        ],
        "when": [
          {
            "constraint": "tolerance-species-coverage",
            "test": "different-class-from"
          }
        ],
        "actions": [
          "replace-with-local-equivalent"
        ],
        "mandatory": false,
        "transferabilityNotes": "Add literature values for the species in question; general part unaffected. Without them there is no tolerance result for the species. Use values from the same synthesis."
      },
      {
        "appliesTo": [
          "nli-forest-type-service",
          "slt-species"
        ],
        "when": [
          {
            "constraint": "czech-forest-type-map",
            "test": "outside"
          }
        ],
        "affects": [
          "/outputs/species_at_location",
          "/outputs/forest_type_tolerance_ranking"
        ],
        "actions": [
          "replace-with-local-equivalent",
          "component-not-executable"
        ],
        "mandatory": true,
        "transferabilityNotes": "Either connect a national forest typology/species map with a point query and a composition table, or the lookup is unavailable and users select species manually. General part unaffected."
      },
      {
        "appliesTo": [
          "heat-threshold",
          "dry-day-threshold",
          "dry-spell-length",
          "heatwave-length",
          "growing-season-start",
          "growing-season-end"
        ],
        "triggeredBy": "different-climate-regime",
        "actions": [
          "replace-with-local-equivalent"
        ],
        "mandatory": false,
        "transferabilityNotes": "The default thresholds and growing season suit Central Europe; they are request parameters and should be set per region. If kept, counts and classes based on them are less meaningful for the region."
      },
      {
        "appliesTo": [
          "rasdaman"
        ],
        "triggeredBy": "service-unavailable",
        "actions": [
          "replace-with-local-equivalent"
        ],
        "mandatory": true,
        "transferabilityNotes": "Applies where no Rasdaman instance is available to the workflow: set one up with the same layout and its own registry, or change the code that reads the data (see the rasdaman artifact). On the FOCAL instance, a missing area is instead added as new collections and entries."
      }
    ]
  },
  "computationType": "deterministic-rule-based",
  "maturityStatus": "operational",
  "qualityAnnotation": [
    {
      "dimension": "method-limitation",
      "note": "Default thresholds (Tmax >= 30 degC, dry day < 1 mm, dry spell >= 10 days, heatwave >= 6 days, growing season Apr-Sep) suit Central Europe; they are request parameters and should be set per region."
    },
    {
      "dimension": "method-limitation",
      "note": "Hargreaves PET is temperature-based; SPEI standardisation reduces but does not remove its bias."
    },
    {
      "dimension": "method-limitation",
      "note": "Historical years taken from another source are quantile-mapped per calendar month; this aligns distributions, it is not a full bias adjustment."
    },
    {
      "dimension": "proxy-variable",
      "note": "T5 is a leaf-tissue threshold from short laboratory exposures, compared with daily maximum air temperature; species heat counts are indicative."
    },
    {
      "dimension": "intended-use-limit",
      "note": "Drought and waterlogging tolerance scores are ordinal rankings, not mortality or SPEI thresholds."
    },
    {
      "dimension": "proxy-variable",
      "note": "Czech forest-type lookup returns potential natural and target composition, not the actual stand."
    },
    {
      "dimension": "method-limitation",
      "note": "10 km (ERA5-Land) and 12.5 km (EUR-11); IDW adds no detail."
    },
    {
      "dimension": "method-limitation",
      "note": "One RCM, three GCMs, one scenario (SSP3-7.0)."
    }
  ]
}
```

#### ttl
```ttl
@prefix cwl: <https://w3id.org/cwl/cwl#> .
@prefix dcat: <http://www.w3.org/ns/dcat#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix dqv: <http://www.w3.org/ns/dqv#> .
@prefix focal-transf-prop: <https://w3id.org/ogc/hosted/focal/transferability/properties/> .
@prefix geo: <http://www.opengis.net/ont/geosparql#> .
@prefix ns1: <https://w3id.org/cwl/cwl#SoftwareRequirement/> .
@prefix ns2: <https://w3id.org/cwl/cwl#SoftwarePackage/> .
@prefix ns3: <https://w3id.org/cwl/cwl#NetworkAccess/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix schema: <https://schema.org/> .
@prefix sld: <https://w3id.org/cwl/salad#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/> a cwl:Workflow ;
    rdfs:label "FWF2 - Climate stress indicators: heat, drought, SPEI (FOCAL Forest Pilot)" ;
    rdfs:comment "Computes heat, drought and combined climate-stress indicators, including SPEI, from daily temperature and precipitation for a point or an area, over any period and sub-period. An optional add-on links them to tree species through species heat and drought tolerance.",
        "Transferability record of workflow FP-WF2 (FWF2), record date 2026-11-18. Record basis: FWF2 code package (API, indicator engine, forest point summary, map layers, trends, species modules and tables, Rasdaman registry, source catalogue). Converted from the delivered record on 2026-11-25. Descriptive CWL profile: no steps are declared and the input and output identifiers are not yet those of an executable Application Package." ;
    schema:alternateName "FWF2" ;
    schema:dateCreated "2026-11-18" ;
    schema:identifier "FP-WF2" ;
    cwl:inputs <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/bbox>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/climate_source_catalogue>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/dry_day_threshold>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/dry_spell_min_days>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/end_date>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/growing_season_end_month>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/growing_season_start_month>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/heat_threshold>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/heatwave_min_days>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/latitude>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/longitude>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/rasdaman_connection>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/rasdaman_registry>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/readiness_collection>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/slt_species>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/species>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/species_codes>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/species_tolerances>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/spei_scale>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/start_date>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/sub_period>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/t5_values> ;
    cwl:outputs <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/drought_periods>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/forest_climate_summary>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/forest_type_tolerance_ranking>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/heat_drought_periods>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/heat_stress_days>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/heat_stress_units>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/map_layers>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/species_at_location>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/species_catalogue>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/species_heat_threshold>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/species_tolerance>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/spei>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/trends> ;
    cwl:requirements [ a cwl:SoftwareRequirement ;
            ns1:packages [ ns2:package "numpy" ],
                [ ns2:package "flask" ],
                [ ns2:package "gunicorn" ],
                [ ns2:package "python" ],
                [ ns2:package "scipy" ] ],
        [ a cwl:NetworkAccess ;
            ns3:networkAccess true ] ;
    focal-transf-prop:computationType <https://w3id.org/ogc/hosted/focal/transferability/computation-types/deterministic-rule-based> ;
    focal-transf-prop:maturityStatus <https://w3id.org/ogc/hosted/focal/transferability/maturity-statuses/operational> ;
    focal-transf-prop:qualityAnnotation [ dqv:inDimension <https://w3id.org/ogc/hosted/focal/transferability/quality-dimensions/method-limitation> ;
            focal-transf-prop:note "One RCM, three GCMs, one scenario (SSP3-7.0)." ],
        [ dqv:inDimension <https://w3id.org/ogc/hosted/focal/transferability/quality-dimensions/intended-use-limit> ;
            focal-transf-prop:note "Drought and waterlogging tolerance scores are ordinal rankings, not mortality or SPEI thresholds." ],
        [ dqv:inDimension <https://w3id.org/ogc/hosted/focal/transferability/quality-dimensions/method-limitation> ;
            focal-transf-prop:note "Default thresholds (Tmax >= 30 degC, dry day < 1 mm, dry spell >= 10 days, heatwave >= 6 days, growing season Apr-Sep) suit Central Europe; they are request parameters and should be set per region." ],
        [ dqv:inDimension <https://w3id.org/ogc/hosted/focal/transferability/quality-dimensions/method-limitation> ;
            focal-transf-prop:note "10 km (ERA5-Land) and 12.5 km (EUR-11); IDW adds no detail." ],
        [ dqv:inDimension <https://w3id.org/ogc/hosted/focal/transferability/quality-dimensions/method-limitation> ;
            focal-transf-prop:note "Historical years taken from another source are quantile-mapped per calendar month; this aligns distributions, it is not a full bias adjustment." ],
        [ dqv:inDimension <https://w3id.org/ogc/hosted/focal/transferability/quality-dimensions/proxy-variable> ;
            focal-transf-prop:note "Czech forest-type lookup returns potential natural and target composition, not the actual stand." ],
        [ dqv:inDimension <https://w3id.org/ogc/hosted/focal/transferability/quality-dimensions/method-limitation> ;
            focal-transf-prop:note "Hargreaves PET is temperature-based; SPEI standardisation reduces but does not remove its bias." ],
        [ dqv:inDimension <https://w3id.org/ogc/hosted/focal/transferability/quality-dimensions/proxy-variable> ;
            focal-transf-prop:note "T5 is a leaf-tissue threshold from short laboratory exposures, compared with daily maximum air temperature; species heat counts are indicative." ] ;
    focal-transf-prop:transferability [ rdfs:comment "Envelope entries and rules that only described which data FOCAL currently holds, or its platform, are not part of this statement; what they said is kept in the notes of the artifacts concerned. An area or period for which no data is at hand is a matter of providing data (as delivered, in the data cube) that meets the artifact's criteria. The delivered record also notes: temporal extent is the year range of each collection, read from Rasdaman at runtime. The general climate-stress part is bounded only by data, the latitude limit of PET and SPEI and the need for 30 years of reference history; the species add-on adds species coverage and the Czech forest-type lookup." ;
            focal-transf-prop:artifacts <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/daily-climate>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/dry-day-threshold>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/dry-spell-length>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/growing-season-end>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/growing-season-start>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/heat-threshold>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/heatwave-length>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/nli-forest-type-service>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/rasdaman>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/reference-history>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/slt-species>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/species-codes>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/species-tolerances>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/t5-values> ;
            focal-transf-prop:envelope <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/czech-forest-type-map>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/pet-latitude-limit>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/t5-species-coverage>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/tolerance-species-coverage> ;
            focal-transf-prop:rules [ rdfs:comment "PET/SPEI undefined poleward of 66.56 deg; other indicators still run. Fix needs a code change (clipping of the sunset-angle term)." ;
                    focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/component-not-executable> ;
                    focal-transf-prop:affects "/outputs/forest_climate_summary",
                        "/outputs/spei" ;
                    focal-transf-prop:appliesTo <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/daily-climate>,
                        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/reference-history> ;
                    focal-transf-prop:mandatory true ;
                    focal-transf-prop:when [ focal-transf-prop:constraint <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/pet-latitude-limit> ;
                            focal-transf-prop:test <https://w3id.org/ogc/hosted/focal/transferability/tests/outside> ] ],
                [ rdfs:comment "Either connect a national forest typology/species map with a point query and a composition table, or the lookup is unavailable and users select species manually. General part unaffected." ;
                    focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/component-not-executable>,
                        <https://w3id.org/ogc/hosted/focal/transferability/actions/replace-with-local-equivalent> ;
                    focal-transf-prop:affects "/outputs/forest_type_tolerance_ranking",
                        "/outputs/species_at_location" ;
                    focal-transf-prop:appliesTo <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/nli-forest-type-service>,
                        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/slt-species> ;
                    focal-transf-prop:mandatory true ;
                    focal-transf-prop:when [ focal-transf-prop:constraint <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/czech-forest-type-map> ;
                            focal-transf-prop:test <https://w3id.org/ogc/hosted/focal/transferability/tests/outside> ] ],
                [ rdfs:comment "Add literature values for the species in question; general part unaffected. Without them there is no T5-based heat result for the species. Literature T5 values must use the same endpoint." ;
                    focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/replace-with-local-equivalent> ;
                    focal-transf-prop:appliesTo <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/t5-values> ;
                    focal-transf-prop:mandatory false ;
                    focal-transf-prop:when [ focal-transf-prop:constraint <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/t5-species-coverage> ;
                            focal-transf-prop:test <https://w3id.org/ogc/hosted/focal/transferability/tests/different-class-from> ] ],
                [ rdfs:comment "Applies where no Rasdaman instance is available to the workflow: set one up with the same layout and its own registry, or change the code that reads the data (see the rasdaman artifact). On the FOCAL instance, a missing area is instead added as new collections and entries." ;
                    focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/replace-with-local-equivalent> ;
                    focal-transf-prop:appliesTo <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/rasdaman> ;
                    focal-transf-prop:mandatory true ;
                    focal-transf-prop:triggeredBy <https://w3id.org/ogc/hosted/focal/transferability/triggers/service-unavailable> ],
                [ rdfs:comment "The default thresholds and growing season suit Central Europe; they are request parameters and should be set per region. If kept, counts and classes based on them are less meaningful for the region." ;
                    focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/replace-with-local-equivalent> ;
                    focal-transf-prop:appliesTo <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/dry-day-threshold>,
                        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/dry-spell-length>,
                        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/growing-season-end>,
                        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/growing-season-start>,
                        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/heat-threshold>,
                        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/heatwave-length> ;
                    focal-transf-prop:mandatory false ;
                    focal-transf-prop:triggeredBy <https://w3id.org/ogc/hosted/focal/transferability/triggers/different-climate-regime> ],
                [ rdfs:comment "Add literature values for the species in question; general part unaffected. Without them there is no tolerance result for the species. Use values from the same synthesis." ;
                    focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/replace-with-local-equivalent> ;
                    focal-transf-prop:appliesTo <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/species-tolerances> ;
                    focal-transf-prop:mandatory false ;
                    focal-transf-prop:when [ focal-transf-prop:constraint <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/tolerance-species-coverage> ;
                            focal-transf-prop:test <https://w3id.org/ogc/hosted/focal/transferability/tests/different-class-from> ] ] ;
            focal-transf-prop:trainingRequired false ] .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/bbox> rdfs:label "Area of interest (bounding box)" ;
    rdfs:comment "Area as [minimum longitude, minimum latitude, maximum longitude, maximum latitude] in decimal degrees (WGS 84). Alternative to latitude and longitude." ;
    sld:type <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/double[]> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/climate_source_catalogue> rdfs:label "Climate source catalogue" ;
    rdfs:comment "climate_source_catalog.json listing the sources and areas offered." ;
    sld:type cwl:File .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/drought_periods> rdfs:label "Drought periods" ;
    rdfs:comment "Runs of consecutive dry days." ;
    sld:type cwl:File .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/dry_day_threshold> rdfs:label "Dry day threshold (mm)" ;
    rdfs:comment "A day with precipitation below this value counts as dry. The default suits Central Europe; set it for the region." ;
    sld:default 1 ;
    sld:type xsd:float .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/dry_spell_min_days> rdfs:label "Minimum length of a drought period (days)" ;
    rdfs:comment "Consecutive dry days needed for a drought period. The default suits Central Europe; set it for the region." ;
    sld:default 10 ;
    sld:type xsd:int .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/end_date> rdfs:label "End of the period" ;
    rdfs:comment "Last day of the period to evaluate (ISO 8601 date)." ;
    sld:type xsd:string .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/forest_climate_summary> rdfs:label "Forestry exposure summary" ;
    rdfs:comment "SPEI-3 metrics, longest dry spell, hot days, TX90p days, longest heatwave and hot days during dry spells, with relative classes." ;
    sld:type cwl:File .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/forest_type_tolerance_ranking> rdfs:label "Forest type tolerance ranking" ;
    rdfs:comment "Tolerance ranking for the species of the forest type (species add-on)." ;
    sld:type <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/File> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/growing_season_end_month> rdfs:label "Last month of the growing season" ;
    rdfs:comment "Month number, 1 to 12. The default suits Central Europe; set it for the region." ;
    sld:default 9 ;
    sld:type xsd:int .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/growing_season_start_month> rdfs:label "First month of the growing season" ;
    rdfs:comment "Month number, 1 to 12. The default suits Central Europe; set it for the region." ;
    sld:default 4 ;
    sld:type xsd:int .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/heat_drought_periods> rdfs:label "Combined heat and drought periods" ;
    rdfs:comment "Periods of combined heat and drought." ;
    sld:type cwl:File .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/heat_stress_days> rdfs:label "Heat stress days" ;
    rdfs:comment "Days with daily maximum temperature at or above the threshold." ;
    sld:type cwl:File .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/heat_stress_units> rdfs:label "Heat stress units" ;
    rdfs:comment "Degree-days above the heat threshold." ;
    sld:type cwl:File .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/heat_threshold> rdfs:label "Heat stress day threshold (degC)" ;
    rdfs:comment "A day counts as a heat stress day when daily maximum temperature is at or above this value; heat stress units are degree-days above it. The default suits Central Europe; set it for the region." ;
    sld:default 30 ;
    sld:type xsd:float .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/heatwave_min_days> rdfs:label "Minimum length of a heatwave (days)" ;
    rdfs:comment "Consecutive days needed for a heatwave in the forestry exposure summary. The default suits Central Europe; set it for the region." ;
    sld:default 6 ;
    sld:type xsd:int .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/latitude> rdfs:label "Latitude of the point" ;
    rdfs:comment "Latitude in decimal degrees (WGS 84). Give latitude and longitude for a point, or bbox for an area." ;
    sld:type <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/double> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/longitude> rdfs:label "Longitude of the point" ;
    rdfs:comment "Longitude in decimal degrees (WGS 84). Give together with latitude." ;
    sld:type <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/double> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/map_layers> rdfs:label "Map layers" ;
    rdfs:comment "12 map layers." ;
    sld:type cwl:File .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/rasdaman_connection> rdfs:label "Data cube connection" ;
    rdfs:comment "How to reach the Rasdaman instance that holds the climate data (queried with rasql over SSH). The connection variables are not named in the delivered material, so one string stands for them; we assume credentials are supplied by the execution environment." ;
    sld:type xsd:string .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/rasdaman_registry> rdfs:label "Data cube registry" ;
    rdfs:comment "rasdaman_registry.json for that instance. The FOCAL registry is not transferable as is." ;
    sld:type cwl:File .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/readiness_collection> rdfs:label "Readiness check collection" ;
    rdfs:comment "Value for READINESS_COLLECTION, which defaults to a Czech ERA5-Land collection." ;
    sld:type <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/string> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/slt_species> rdfs:label "Forest type species composition table" ;
    rdfs:comment "Natural and target species composition of the Czech forest-type groups. Used by the species add-on. Ships with the workflow." ;
    sld:default <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/slt_species.json> ;
    sld:type cwl:File .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/slt_species.json> a cwl:File .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/species> rdfs:label "Tree species" ;
    rdfs:comment "Species to relate to heat and drought tolerance (optional species add-on), identified as in the species catalogue (species_codes.json, which carries Latin names). Outside Czechia, where the species-at-location lookup is not available, select them here." ;
    sld:type <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/string[]> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/species-codes> dcterms:title "species_codes.json: Czech forestry species codes with Czech, English and Latin names" ;
    rdfs:comment "The Latin names make it language independent. For further species, add codes. Used by (delivered step names): species-catalogue." ;
    focal-transf-prop:artifactRef "/inputs/species_codes" ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/workflow-input> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/species_at_location> rdfs:label "Species at the location" ;
    rdfs:comment "Czech forest type and natural and target species composition at a point (species add-on)." ;
    sld:type <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/File> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/species_catalogue> rdfs:label "Species catalogue" ;
    rdfs:comment "Species with their codes and names (species add-on)." ;
    sld:type <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/File> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/species_codes> rdfs:label "Species codes table" ;
    rdfs:comment "Czech forestry species codes with Czech, English and Latin names. Used by the species add-on. Ships with the workflow." ;
    sld:default <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/species_codes.json> ;
    sld:type cwl:File .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/species_codes.json> a cwl:File .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/species_heat_threshold> rdfs:label "Species heat thresholds" ;
    rdfs:comment "T5-based heat threshold of the selected species (species add-on)." ;
    sld:type <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/File> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/species_tolerance> rdfs:label "Species tolerances" ;
    rdfs:comment "Drought and waterlogging tolerance of the selected species (species add-on)." ;
    sld:type <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/File> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/species_tolerances> rdfs:label "Drought and waterlogging tolerance table" ;
    rdfs:comment "Tolerance scores 0-5 per species. Used by the species add-on. Ships with the workflow." ;
    sld:default <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/species_tolerances.json> ;
    sld:type cwl:File .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/species_tolerances.json> a cwl:File .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/spei> rdfs:label "SPEI" ;
    rdfs:comment "Standardised Precipitation-Evapotranspiration Index, monthly or yearly." ;
    sld:type cwl:File .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/spei_scale> rdfs:label "SPEI time step" ;
    rdfs:comment "Whether SPEI is computed monthly or yearly." ;
    sld:type [ sld:type <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/enum> ],
        sld:null .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/start_date> rdfs:label "Start of the period" ;
    rdfs:comment "First day of the period to evaluate (ISO 8601 date)." ;
    sld:type xsd:string .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/sub_period> rdfs:label "Sub-period" ;
    rdfs:comment "How results are broken down within the period; averages over these units are also available." ;
    sld:type [ sld:type <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/enum> ],
        sld:null .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/t5_values> rdfs:label "Leaf heat tolerance (T5) table" ;
    rdfs:comment "Leaf heat tolerance T5 per species with measurements and sources. Used by the species add-on. Ships with the workflow." ;
    sld:default <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/t5_values.json> ;
    sld:type cwl:File .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/t5_values.json> a cwl:File .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/trends> rdfs:label "Trends" ;
    rdfs:comment "Sen's slope and Mann-Kendall trends." ;
    sld:type cwl:File .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/czech-forest-type-map> rdfs:comment "Species-at-location lookup (NLI WMS Lesni_typ + Czech forest typology). Czechia's forest land only; the box is the FOCAL Czechia bounding box standing in for the national border." ;
    focal-transf-prop:dimension <https://w3id.org/ogc/hosted/focal/transferability/dimensions/spatial> ;
    focal-transf-prop:inputRef "/inputs/bbox",
        "/inputs/latitude",
        "/inputs/longitude" ;
    focal-transf-prop:role <https://w3id.org/ogc/hosted/focal/transferability/roles/can-run-on> ;
    focal-transf-prop:value [ geo:asWKT "POLYGON((12.07 48.48, 18.97 48.48, 18.97 51.08, 12.07 51.08, 12.07 48.48))"^^geo:wktLiteral ] .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/daily-climate> dcterms:title "Daily temperature (minimum, average, maximum) and precipitation covering the requested period" ;
    rdfs:comment "As delivered, the workflow does not take these data as a file: it reads them from the Rasdaman data cube (artifact rasdaman), for the requested area and the years it needs. The delivered material gives no specification of the layout the code expects. Delivered as two datasets with the same requirements. (1) Projections: CMIP6-CORDEX EUR-11 GERICS-REMO2020 (MPI-ESM1-2-HR, EC-Earth3-Veg, MIROC6), SSP3-7.0, r1i1p1f1: daily temperature (tas_min/tas_avg/tas_max) and precipitation; SSP3-7.0 only, no historical experiment. Within FOCAL: daily data of these three simulations are held for the whole EUR-11 rotated grid and read directly, with no precompute (lon/lat bounding box 44.5939 W - 64.9644 E, 21.9878 - 72.585 N; the box overstates the rotated domain at its corners). Not usable outside that domain with these simulations: use another CORDEX domain or daily dataset meeting the criteria; other GCM-RCM pairs or scenarios can be obtained from ESGF. (2) Historical: ERA5-Land daily temperature (t2m_min/t2m_avg/t2m_max from hourly t2m) and daily precipitation sum (from hourly tp). Within FOCAL: held for Czechia, Spain and Finland; other areas by a routine precompute run. Outside FOCAL: ERA5-Land (Copernicus Climate Data Store), E-OBS or national grids. Native resolution of those sources: ERA5-Land 0.1 degrees (about 10 km), EUR-11 0.11 degrees (about 12.5 km). Used by (delivered step names): heat-stress-days, heat-stress-units, drought-periods, heat-drought-periods, spei, forest-climate-summary, trends, map-layers, spei-reference-history. SPEI, TX90p and the relative classes need 30 complete years before the evaluated period (or a fixed 30-year baseline), either in these data or in the reference history data." ;
    focal-transf-prop:acceptanceCriteria [ rdfs:comment "Structure: 3D [day, y, x]; temperature as a struct cell (min/avg/max) or as separate variables; 2D latitude/longitude of cell centres; no-data is NaN. 360_day calendars need conversion before ingest." ;
            focal-transf-prop:axis <https://w3id.org/ogc/hosted/focal/transferability/axes/time> ;
            focal-transf-prop:gridType <https://w3id.org/ogc/hosted/focal/transferability/grid-types/regular-latlon>,
                <https://w3id.org/ogc/hosted/focal/transferability/grid-types/rotated-pole> ;
            focal-transf-prop:temporalRequirement [ dcat:temporalResolution "P1D"^^xsd:duration ;
                    focal-transf-prop:calendar "noleap",
                        "proleptic_gregorian",
                        "standard" ] ;
            focal-transf-prop:variable [ focal-transf-prop:standardName "air_temperature" ;
                    focal-transf-prop:unit <http://qudt.org/vocab/unit/DEG_C> ;
                    focal-transf-prop:variableName "tasmin" ],
                [ focal-transf-prop:unit <http://qudt.org/vocab/unit/MilliM-PER-DAY> ;
                    focal-transf-prop:variableName "pr" ],
                [ focal-transf-prop:standardName "air_temperature" ;
                    focal-transf-prop:unit <http://qudt.org/vocab/unit/DEG_C> ;
                    focal-transf-prop:variableName "tasmax" ],
                [ focal-transf-prop:standardName "air_temperature" ;
                    focal-transf-prop:unit <http://qudt.org/vocab/unit/DEG_C> ;
                    focal-transf-prop:variableName "tas" ] ] ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/workflow-input> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/dry-day-threshold> dcterms:title "Dry day threshold (< 1 mm)" ;
    rdfs:comment "A request parameter." ;
    focal-transf-prop:artifactRef "/inputs/dry_day_threshold" ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/workflow-input> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/dry-spell-length> dcterms:title "Drought period length (>= 10 days)" ;
    rdfs:comment "A 10-day dry spell is routine in a Mediterranean summer." ;
    focal-transf-prop:artifactRef "/inputs/dry_spell_min_days" ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/workflow-input> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/growing-season-end> dcterms:title "Growing season end (September)" ;
    rdfs:comment "Northern Hemisphere temperate default (April-September); see growing-season-start." ;
    focal-transf-prop:artifactRef "/inputs/growing_season_end_month" ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/workflow-input> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/growing-season-start> dcterms:title "Growing season start (April)" ;
    rdfs:comment "Northern Hemisphere temperate default (April-September); e.g. shorter in boreal forests; in Mediterranean forests the summer drought falls inside it." ;
    focal-transf-prop:artifactRef "/inputs/growing_season_start_month" ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/workflow-input> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/heat-threshold> dcterms:title "Heat stress day threshold (Tmax >= 30 degC)" ;
    rdfs:comment "30 degC is rarely reached in boreal climates and often in Mediterranean ones; set it per region or use TX90p." ;
    focal-transf-prop:artifactRef "/inputs/heat_threshold" ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/workflow-input> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/heatwave-length> dcterms:title "Heatwave length (>= 6 days)" ;
    rdfs:comment "A request parameter." ;
    focal-transf-prop:artifactRef "/inputs/heatwave_min_days" ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/workflow-input> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/nli-forest-type-service> dcterms:title "NLI WMS (gp1/gp2.nli.gov.cz/wms_oprl), layer Lesni_typ, GetFeatureInfo; Czech regional forest development plans" ;
    rdfs:comment "Public service covering the forest land of Czechia only. A replacement is a point query returning a forest type or species code for the location, with coordinates in EPSG:4326 or transformable, plus an adapter. Used by (delivered step names): species-at-location." ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/external-resource> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/pet-latitude-limit> rdfs:comment "Latitude band |latitude| <= 66.56 degrees. FAO-56 extraterrestrial radiation in the Hargreaves PET is undefined during polar day/night; PET and SPEI return no value poleward of the Arctic/Antarctic circle. Other general indicators are unaffected." ;
    focal-transf-prop:dimension <https://w3id.org/ogc/hosted/focal/transferability/dimensions/spatial> ;
    focal-transf-prop:inputRef "/inputs/bbox",
        "/inputs/latitude",
        "/inputs/longitude" ;
    focal-transf-prop:role <https://w3id.org/ogc/hosted/focal/transferability/roles/valid-for> ;
    focal-transf-prop:value [ geo:asWKT "POLYGON((-180 -66.56, 180 -66.56, 180 66.56, -180 66.56, -180 -66.56))"^^geo:wktLiteral ] .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/rasdaman> dcterms:title "FOCAL Rasdaman data cube (rasql over SSH), source catalogue and registry (climate_source_catalog.json, rasdaman_registry.json)" ;
    rdfs:comment "The delivered workflow reads data from a Rasdaman instance queried with rasql over SSH. Another platform needs Rasdaman with the same registry layout (set READINESS_COLLECTION, which defaults to a Czech ERA5-Land collection) and its own registry, or file-based data access instead; the computation uses NumPy and SciPy. Within FOCAL: add catalogue and registry entries for a new area (user interface listing, new ERA5-Land collections). The FOCAL registry is not transferable as is. Used by (delivered step names): data-access." ;
    focal-transf-prop:artifactRef "/inputs/climate_source_catalogue",
        "/inputs/rasdaman_connection",
        "/inputs/rasdaman_registry",
        "/inputs/readiness_collection" ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/infrastructure> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/reference-history> dcterms:title "Historical daily climate used as the reference history (ERA5-Land in the delivered setup)" ;
    rdfs:comment "As delivered, the workflow does not take these data as a file: it reads them from the Rasdaman data cube (artifact rasdaman), for the requested area and the years it needs. The delivered material gives no specification of the layout the code expects. Used only when the main data lack the history. SPEI, TX90p and relative classes need 30 complete years before the evaluated period (or a fixed 30-year baseline). Missing history is taken from a historical source quantile-mapped per calendar month to the primary source over their overlap, with at least 30 samples per month. Also needed when projections are evaluated. Within FOCAL: ERA5-Land is held for Czechia, Spain and Finland; other areas by a routine precompute run. Outside FOCAL: ERA5-Land (CDS), E-OBS or national grids. Used by (delivered step names): spei-reference-history, spei." ;
    focal-transf-prop:acceptanceCriteria [ rdfs:comment "Structure: 3D [day, y, x]; temperature as a struct cell (min/avg/max) or as separate variables; 2D latitude/longitude of cell centres; no-data is NaN. 360_day calendars need conversion before ingest." ;
            focal-transf-prop:axis <https://w3id.org/ogc/hosted/focal/transferability/axes/time> ;
            focal-transf-prop:gridType <https://w3id.org/ogc/hosted/focal/transferability/grid-types/regular-latlon>,
                <https://w3id.org/ogc/hosted/focal/transferability/grid-types/rotated-pole> ;
            focal-transf-prop:temporalRequirement [ dcat:temporalResolution "P1D"^^xsd:duration ;
                    focal-transf-prop:calendar "noleap",
                        "proleptic_gregorian",
                        "standard" ;
                    focal-transf-prop:minimumPrecedingYears 30 ;
                    focal-transf-prop:temporalComplete true ] ;
            focal-transf-prop:variable [ focal-transf-prop:standardName "air_temperature" ;
                    focal-transf-prop:unit <http://qudt.org/vocab/unit/DEG_C> ;
                    focal-transf-prop:variableName "tasmax" ],
                [ focal-transf-prop:standardName "air_temperature" ;
                    focal-transf-prop:unit <http://qudt.org/vocab/unit/DEG_C> ;
                    focal-transf-prop:variableName "tasmin" ],
                [ focal-transf-prop:unit <http://qudt.org/vocab/unit/MilliM-PER-DAY> ;
                    focal-transf-prop:variableName "pr" ],
                [ focal-transf-prop:standardName "air_temperature" ;
                    focal-transf-prop:unit <http://qudt.org/vocab/unit/DEG_C> ;
                    focal-transf-prop:variableName "tas" ] ] ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/workflow-input> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/slt-species> dcterms:title "slt_species.json: Czech forest-type groups (SLT, 105) with natural and target species composition (%)" ;
    rdfs:comment "Defined for the Czech forest typology. Structure: {type-code: {name, natural: {species-code: %}, target: {species-code: %}}}, with the same species code list as species-codes. Used by (delivered step names): species-at-location, forest-type-tolerance-ranking." ;
    focal-transf-prop:artifactRef "/inputs/slt_species" ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/workflow-input> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/species-tolerances> dcterms:title "species_tolerances.json: drought and waterlogging tolerance 0-5 (Niinemets & Valladares 2006)" ;
    rdfs:comment "A replacement gives drought and waterlogging tolerance on an ordinal 0-5 scale, from the same synthesis or an equivalent ordinal scale. The source synthesis covers temperate Northern Hemisphere trees and shrubs. Species add-on only. Used by (delivered step names): species-tolerance, forest-type-tolerance-ranking." ;
    focal-transf-prop:acceptanceCriteria [ focal-transf-prop:variable [ focal-transf-prop:variableName "waterlogging" ],
                [ focal-transf-prop:variableName "drought" ] ] ;
    focal-transf-prop:artifactRef "/inputs/species_tolerances" ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/workflow-input> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/t5-species-coverage> rdfs:comment "Species add-on only. Values are species traits from literature, independent of location; valid wherever these species grow. Species with a numeric T5. The delivered entry 'Salix alba / Salix fragilis' is listed as two taxa." ;
    focal-transf-prop:dimension <https://w3id.org/ogc/hosted/focal/transferability/dimensions/ecological> ;
    focal-transf-prop:inputRef "/inputs/species" ;
    focal-transf-prop:role <https://w3id.org/ogc/hosted/focal/transferability/roles/valid-for> ;
    focal-transf-prop:value [ focal-transf-prop:class "Abies alba",
                "Acer platanoides",
                "Acer pseudoplatanus",
                "Alnus glutinosa",
                "Carpinus betulus",
                "Fagus sylvatica",
                "Picea abies",
                "Pinus sylvestris",
                "Quercus robur",
                "Salix alba",
                "Salix fragilis" ;
            focal-transf-prop:classificationScheme <https://w3id.org/ogc/hosted/focal/transferability/classification-schemes/gbif-backbone> ] .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/t5-values> dcterms:title "t5_values.json: leaf heat tolerance T5 (temperature at 5 % decline of Fv/Fm) per species, with measurements and sources (Kunert et al. 2022 and others)" ;
    rdfs:comment "Species traits from literature, independent of location. Species add-on only. Used by (delivered step names): species-heat-threshold." ;
    focal-transf-prop:acceptanceCriteria [ rdfs:comment "Endpoint T5: temperature at 5 % decline of Fv/Fm. Measurements carry their source. The key \"lat\" is the Latin species name, not a latitude." ;
            focal-transf-prop:variable [ focal-transf-prop:unit <http://qudt.org/vocab/unit/DEG_C> ;
                    focal-transf-prop:variableName "t5" ],
                [ focal-transf-prop:variableName "lat" ],
                [ focal-transf-prop:variableName "code" ],
                [ focal-transf-prop:variableName "measurements" ] ] ;
    focal-transf-prop:artifactRef "/inputs/t5_values" ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/workflow-input> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/tolerance-species-coverage> rdfs:comment "Species add-on only. Values are species traits from literature, independent of location; valid wherever these species grow. Species with drought and waterlogging tolerance scores." ;
    focal-transf-prop:dimension <https://w3id.org/ogc/hosted/focal/transferability/dimensions/ecological> ;
    focal-transf-prop:inputRef "/inputs/species" ;
    focal-transf-prop:role <https://w3id.org/ogc/hosted/focal/transferability/roles/valid-for> ;
    focal-transf-prop:value [ focal-transf-prop:class "Abies alba",
                "Acer platanoides",
                "Acer pseudoplatanus",
                "Alnus glutinosa",
                "Betula pendula",
                "Carpinus betulus",
                "Fagus sylvatica",
                "Larix decidua",
                "Picea abies",
                "Pinus mugo",
                "Pinus sylvestris",
                "Populus tremula",
                "Quercus robur",
                "Sorbus aucuparia",
                "Tilia cordata" ;
            focal-transf-prop:classificationScheme <https://w3id.org/ogc/hosted/focal/transferability/classification-schemes/gbif-backbone> ] .


```


### FP-WF3 — Prediction of threatened stands (optional rule, degraded mode)
The sharpest evidenced example of a non-operational workflow (`maturityStatus: prototype`),
and the clearest optional-but-degrading rule: without local training labels, results are
still produced, just "treated as exploratory" (Question 7). Question 9 lists the labels
among the things that "would need to be replaced", so the optional flag on the labels combines
the two answers rather than being stated in one sentence. The EO strategy is optional
because Question 9 says it "may also need adjustment", and Question 3 says the Python
requirement is only "expected", so it is provisional. That is
`mandatory: false` with the consequence spelled out — a skippable rule with no stated
consequence tells a consumer nothing they can act on, so `shapes.shacl` rejects that pairing.

The spatial constraint is **more speculative than FP-WF1's or FP-WF2's**: no sentence in this
questionnaire names a location at all. Czechia is a proxy because this is a Forest Pilot
workflow. The owners are asked to confirm it.

Question 9 lists four things to replace for the target region: "Historical disturbance labels,
forest masks, phenological normalisation and model training data". Labels, phenology and the
EO strategy are artifacts here, and forest masks now are too. "Model training data" is read as
the labels themselves (Question 4 describes the labels as the polygons "for training or
validation"). The owners are asked to confirm that reading.

Question 5 also says "structured regression testing and full scientific validation are not yet
complete", which is what `validation-incomplete` exists for, so it is carried as a
`qualityAnnotation`, separate from `maturityStatus: prototype`.

**"Disturbance type" is a named dependency with no artifact or constraint.** Question 7 lists
four things the approach depends on: "the quality of historical damage labels, cloud-free time
series, regional phenology and disturbance type." Three are modeled (`labels`, `eo-strategy`,
`phenological-regime`); disturbance type has neither an artifact nor a rule, and unlike
phenology it is not even carried as an unresolved constraint, because nothing in the
questionnaire further specifies what "comparable disturbance type" would mean — no scheme, no
definition, no named categories to test a target against. Inventing a classification here would
be guessing at a scheme the owner never gave, the same mistake the EEA-biogeographical-regions
and Köppen-Geiger readings made elsewhere and that the 2026-09-29 reviews rejected. Flagged as
an open, unmodeled gap on the statement itself rather than built as a constraint or silently
dropped.

No temporal constraint. `steps` omitted — this workflow's own questionnaire says its
container, API and regression-test packaging are still to be completed, so there is less of
an Application Package here than anywhere else. `inputs` ids are placeholders.

#### json
```json
{
  "class": "Workflow",
  "id": "",
  "cwlVersion": "v1.2",
  "label": "FP-WF3 — Prediction of threatened stands",
  "requirements": {
    "SoftwareRequirement": { "packages": [{ "package": "python" }] }
  },
  "inputs": {
    "disturbance_labels": { "type": "File" },
    "forest_masks": { "type": "File" },
    "eo_compositing_strategy": { "type": "string" },
    "phenology_normalization_assumptions": { "type": "string" }
  },
  "transferability": {
    "trainingRequired": true,
    "envelope": [
      {
        "id": "label-extent",
        "role": "trained-on",
        "dimension": "spatial",
        "value": { "asWKT": "POLYGON ((18.16 49.26, 17.76 48.89, 17.14 48.84, 16.95 48.6, 16.54 48.8, 16.06 48.75, 14.99 49, 14.69 48.6, 14.19 48.58, 12.68 49.41, 12.39 49.74, 12.51 49.9, 12.09 50.3, 12.28 50.18, 12.55 50.39, 14.37 50.9, 14.28 51.03, 14.72 50.81, 14.99 51.01, 16.01 50.61, 16.36 50.62, 16.21 50.42, 16.64 50.1, 16.99 50.24, 16.88 50.43, 17.7 50.31, 17.63 50.12, 18.56 49.88, 18.83 49.51, 18.16 49.26))" }
      },
      {
        "id": "phenological-regime",
        "role": "valid-for",
        "dimension": "ecological",
        "value": "a comparable phenological regime"
      }
    ],
    "artifacts": [
      { "id": "labels", "artifact": "historical forest disturbance/damage labels (ground truth training data)", "artifactRole": "workflow-input", "artifactRef": "/inputs/disturbance_labels" },
      { "id": "forest-masks", "artifact": "forest masks or stand boundaries", "artifactRole": "workflow-input", "artifactRef": "/inputs/forest_masks" },
      { "id": "eo-strategy", "artifact": "EO sensor selection, cloud masking, temporal compositing strategy", "artifactRole": "workflow-input", "artifactRef": "/inputs/eo_compositing_strategy" },
      { "id": "phenology", "artifact": "regional phenology normalisation assumptions", "artifactRole": "workflow-input", "artifactRef": "/inputs/phenology_normalization_assumptions" }
    ],
    "rules": [
      {
        "appliesTo": ["labels"],
        "when": [{ "constraint": "label-extent", "test": "outside" }],
        "actions": ["retrain"],
        "mandatory": false,
        "transferabilityNotes": "Without local training labels the results are produced but should be treated as exploratory."
      },
      {
        "appliesTo": ["forest-masks"],
        "when": [{ "constraint": "label-extent", "test": "outside" }],
        "actions": ["replace-with-local-equivalent"],
        "mandatory": true
      },
      {
        "appliesTo": ["eo-strategy"],
        "when": [{ "constraint": "label-extent", "test": "outside" }],
        "actions": ["replace-with-local-equivalent"],
        "mandatory": false,
        "transferabilityNotes": "The EO sensors, cloud masking and compositing strategy may need adjusting to local conditions; the consequence of leaving it unadjusted is not stated."
      },
      {
        "appliesTo": ["phenology"],
        "when": [{ "constraint": "phenological-regime", "test": "outside" }],
        "actions": ["replace-with-local-equivalent"],
        "mandatory": true
      }
    ]
  },
  "computationType": "statistical-ml",
  "maturityStatus": "prototype",
  "qualityAnnotation": [
    {
      "dimension": "validation-incomplete",
      "note": "Question 5: 'structured regression testing and full scientific validation are not yet complete'. A separate axis from maturityStatus: it says how far the results can be trusted, not how far along the software is."
    }
  ]
}

```

#### jsonld
```jsonld
{
  "@context": "https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/workflow/context.jsonld",
  "class": "Workflow",
  "id": "",
  "cwlVersion": "v1.2",
  "label": "FP-WF3 \u2014 Prediction of threatened stands",
  "requirements": {
    "SoftwareRequirement": {
      "packages": [
        {
          "package": "python"
        }
      ]
    }
  },
  "inputs": {
    "disturbance_labels": {
      "type": "File"
    },
    "forest_masks": {
      "type": "File"
    },
    "eo_compositing_strategy": {
      "type": "string"
    },
    "phenology_normalization_assumptions": {
      "type": "string"
    }
  },
  "transferability": {
    "trainingRequired": true,
    "envelope": [
      {
        "id": "label-extent",
        "role": "trained-on",
        "dimension": "spatial",
        "value": {
          "asWKT": "POLYGON ((18.16 49.26, 17.76 48.89, 17.14 48.84, 16.95 48.6, 16.54 48.8, 16.06 48.75, 14.99 49, 14.69 48.6, 14.19 48.58, 12.68 49.41, 12.39 49.74, 12.51 49.9, 12.09 50.3, 12.28 50.18, 12.55 50.39, 14.37 50.9, 14.28 51.03, 14.72 50.81, 14.99 51.01, 16.01 50.61, 16.36 50.62, 16.21 50.42, 16.64 50.1, 16.99 50.24, 16.88 50.43, 17.7 50.31, 17.63 50.12, 18.56 49.88, 18.83 49.51, 18.16 49.26))"
        }
      },
      {
        "id": "phenological-regime",
        "role": "valid-for",
        "dimension": "ecological",
        "value": "a comparable phenological regime"
      }
    ],
    "artifacts": [
      {
        "id": "labels",
        "artifact": "historical forest disturbance/damage labels (ground truth training data)",
        "artifactRole": "workflow-input",
        "artifactRef": "/inputs/disturbance_labels"
      },
      {
        "id": "forest-masks",
        "artifact": "forest masks or stand boundaries",
        "artifactRole": "workflow-input",
        "artifactRef": "/inputs/forest_masks"
      },
      {
        "id": "eo-strategy",
        "artifact": "EO sensor selection, cloud masking, temporal compositing strategy",
        "artifactRole": "workflow-input",
        "artifactRef": "/inputs/eo_compositing_strategy"
      },
      {
        "id": "phenology",
        "artifact": "regional phenology normalisation assumptions",
        "artifactRole": "workflow-input",
        "artifactRef": "/inputs/phenology_normalization_assumptions"
      }
    ],
    "rules": [
      {
        "appliesTo": [
          "labels"
        ],
        "when": [
          {
            "constraint": "label-extent",
            "test": "outside"
          }
        ],
        "actions": [
          "retrain"
        ],
        "mandatory": false,
        "transferabilityNotes": "Without local training labels the results are produced but should be treated as exploratory."
      },
      {
        "appliesTo": [
          "forest-masks"
        ],
        "when": [
          {
            "constraint": "label-extent",
            "test": "outside"
          }
        ],
        "actions": [
          "replace-with-local-equivalent"
        ],
        "mandatory": true
      },
      {
        "appliesTo": [
          "eo-strategy"
        ],
        "when": [
          {
            "constraint": "label-extent",
            "test": "outside"
          }
        ],
        "actions": [
          "replace-with-local-equivalent"
        ],
        "mandatory": false,
        "transferabilityNotes": "The EO sensors, cloud masking and compositing strategy may need adjusting to local conditions; the consequence of leaving it unadjusted is not stated."
      },
      {
        "appliesTo": [
          "phenology"
        ],
        "when": [
          {
            "constraint": "phenological-regime",
            "test": "outside"
          }
        ],
        "actions": [
          "replace-with-local-equivalent"
        ],
        "mandatory": true
      }
    ]
  },
  "computationType": "statistical-ml",
  "maturityStatus": "prototype",
  "qualityAnnotation": [
    {
      "dimension": "validation-incomplete",
      "note": "Question 5: 'structured regression testing and full scientific validation are not yet complete'. A separate axis from maturityStatus: it says how far the results can be trusted, not how far along the software is."
    }
  ]
}
```

#### ttl
```ttl
@prefix cwl: <https://w3id.org/cwl/cwl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix dqv: <http://www.w3.org/ns/dqv#> .
@prefix focal-transf-prop: <https://w3id.org/ogc/hosted/focal/transferability/properties/> .
@prefix geo: <http://www.opengis.net/ont/geosparql#> .
@prefix ns1: <https://w3id.org/cwl/cwl#SoftwareRequirement/> .
@prefix ns2: <https://w3id.org/cwl/cwl#SoftwarePackage/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix sld: <https://w3id.org/cwl/salad#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf3/> a cwl:Workflow ;
    rdfs:label "FP-WF3 — Prediction of threatened stands" ;
    cwl:inputs <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf3/disturbance_labels>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf3/eo_compositing_strategy>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf3/forest_masks>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf3/phenology_normalization_assumptions> ;
    cwl:requirements [ a cwl:SoftwareRequirement ;
            ns1:packages [ ns2:package "python" ] ] ;
    focal-transf-prop:computationType <https://w3id.org/ogc/hosted/focal/transferability/computation-types/statistical-ml> ;
    focal-transf-prop:maturityStatus <https://w3id.org/ogc/hosted/focal/transferability/maturity-statuses/prototype> ;
    focal-transf-prop:qualityAnnotation [ dqv:inDimension <https://w3id.org/ogc/hosted/focal/transferability/quality-dimensions/validation-incomplete> ;
            focal-transf-prop:note "Question 5: 'structured regression testing and full scientific validation are not yet complete'. A separate axis from maturityStatus: it says how far the results can be trusted, not how far along the software is." ] ;
    focal-transf-prop:transferability [ focal-transf-prop:artifacts <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf3/eo-strategy>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf3/forest-masks>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf3/labels>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf3/phenology> ;
            focal-transf-prop:envelope <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf3/label-extent>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf3/phenological-regime> ;
            focal-transf-prop:rules [ focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/replace-with-local-equivalent> ;
                    focal-transf-prop:appliesTo <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf3/phenology> ;
                    focal-transf-prop:mandatory true ;
                    focal-transf-prop:when [ focal-transf-prop:constraint <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf3/phenological-regime> ;
                            focal-transf-prop:test <https://w3id.org/ogc/hosted/focal/transferability/tests/outside> ] ],
                [ rdfs:comment "The EO sensors, cloud masking and compositing strategy may need adjusting to local conditions; the consequence of leaving it unadjusted is not stated." ;
                    focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/replace-with-local-equivalent> ;
                    focal-transf-prop:appliesTo <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf3/eo-strategy> ;
                    focal-transf-prop:mandatory false ;
                    focal-transf-prop:when [ focal-transf-prop:constraint <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf3/label-extent> ;
                            focal-transf-prop:test <https://w3id.org/ogc/hosted/focal/transferability/tests/outside> ] ],
                [ rdfs:comment "Without local training labels the results are produced but should be treated as exploratory." ;
                    focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/retrain> ;
                    focal-transf-prop:appliesTo <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf3/labels> ;
                    focal-transf-prop:mandatory false ;
                    focal-transf-prop:when [ focal-transf-prop:constraint <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf3/label-extent> ;
                            focal-transf-prop:test <https://w3id.org/ogc/hosted/focal/transferability/tests/outside> ] ],
                [ focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/replace-with-local-equivalent> ;
                    focal-transf-prop:appliesTo <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf3/forest-masks> ;
                    focal-transf-prop:mandatory true ;
                    focal-transf-prop:when [ focal-transf-prop:constraint <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf3/label-extent> ;
                            focal-transf-prop:test <https://w3id.org/ogc/hosted/focal/transferability/tests/outside> ] ] ;
            focal-transf-prop:trainingRequired true ] .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf3/disturbance_labels> sld:type cwl:File .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf3/eo_compositing_strategy> sld:type xsd:string .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf3/forest_masks> sld:type cwl:File .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf3/phenology_normalization_assumptions> sld:type xsd:string .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf3/eo-strategy> dcterms:title "EO sensor selection, cloud masking, temporal compositing strategy" ;
    focal-transf-prop:artifactRef "/inputs/eo_compositing_strategy" ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/workflow-input> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf3/forest-masks> dcterms:title "forest masks or stand boundaries" ;
    focal-transf-prop:artifactRef "/inputs/forest_masks" ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/workflow-input> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf3/labels> dcterms:title "historical forest disturbance/damage labels (ground truth training data)" ;
    focal-transf-prop:artifactRef "/inputs/disturbance_labels" ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/workflow-input> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf3/phenological-regime> focal-transf-prop:dimension <https://w3id.org/ogc/hosted/focal/transferability/dimensions/ecological> ;
    focal-transf-prop:role <https://w3id.org/ogc/hosted/focal/transferability/roles/valid-for> ;
    focal-transf-prop:value "a comparable phenological regime" .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf3/phenology> dcterms:title "regional phenology normalisation assumptions" ;
    focal-transf-prop:artifactRef "/inputs/phenology_normalization_assumptions" ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/workflow-input> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf3/label-extent> focal-transf-prop:dimension <https://w3id.org/ogc/hosted/focal/transferability/dimensions/spatial> ;
    focal-transf-prop:role <https://w3id.org/ogc/hosted/focal/transferability/roles/trained-on> ;
    focal-transf-prop:value [ geo:asWKT "POLYGON ((18.16 49.26, 17.76 48.89, 17.14 48.84, 16.95 48.6, 16.54 48.8, 16.06 48.75, 14.99 49, 14.69 48.6, 14.19 48.58, 12.68 49.41, 12.39 49.74, 12.51 49.9, 12.09 50.3, 12.28 50.18, 12.55 50.39, 14.37 50.9, 14.28 51.03, 14.72 50.81, 14.99 51.01, 16.01 50.61, 16.36 50.62, 16.21 50.42, 16.64 50.1, 16.99 50.24, 16.88 50.43, 17.7 50.31, 17.63 50.12, 18.56 49.88, 18.83 49.51, 18.16 49.26))"^^geo:wktLiteral ] .


```


### UP-WF2 — Urban hot/cool spot (two footprints, a cascade, a terminal outcome)
The workflow this restructure was designed against, and the one the previous model could not
state correctly.

**Two distinct coverage footprints.** The LST datasets are bounded by the EURO-CORDEX EUR-11
domain; the CLMS layers by that product's own coverage. Previously both were workflow-level
envelope entries told apart only by putting one under `jurisdictional` — a dimension defined
as an administrative or licensing boundary, which a dataset footprint is not. Now both are
`spatial`, each has an `id`, and each rule cites the one that actually governs it.

**CLMS's exclusion of Ukraine is its own constraint, not a hole in a geometry.** The previous
model carried a computed Europe-minus-Ukraine MultiPolygon at full border resolution, with the
exclusion invisible to anyone reading it and quietly lost the moment the geometry was
simplified. Here it is a named constraint cited by a rule with `test: inside`, so falling
within the excluded area is what makes the component unexecutable. It is legible, it is
separately correctable when the authoritative CLMS geometry arrives, and it survives
simplification of the surrounding extent.

Asked "can I run this in Kyiv?", a consumer now gets a per-artifact answer: the LST datasets
are inside EURO-CORDEX and reusable, and the CLMS layers are unavailable, so hot-spot
characterization cannot run.

**`affects` is what makes that last clause a fact rather than a remark.** The rules naming
`component-not-executable` point at the step it costs, so the per-artifact answers roll up
into a per-workflow verdict: Today the run interrupts at that step, after hot and cool spot detection has finished; the owners plan to skip the step instead. Without it the model would
say "a component cannot be executed" and leave a consumer no way to find out which, which is
the difference between a partial result and no result.

**Rules are exceptions.** The CLMS layers have no rule for the case where the target is
inside coverage and outside the excluded area, because none is needed: an artifact no rule
fires for is reused unchanged. Only the LST datasets carry an explicit `reuse-as-is`, and
only because pairing it with the `outside` rule is what makes that cascade readable.

**The cascade keeps its connecting condition.** The source describes reuse inside the domain,
substitution if a compatible dataset can be produced outside it, and failure if none can.
That is two rules over the same constraint — `inside` then `outside` — rather than the
previous two flat rules that dropped the "only if a substitute exists" link. The residual
uncertainty stays where the source leaves it: an OR-set of two actions.

The **temporal constraints are directly evidenced**, unlike the omitted periods elsewhere:
three precalculated epochs (2001-2005, 2011-2015, 2022-2025), none of them a validity limit.

Geometries are coarse extents, not cadastral boundaries: `eur11-domain` is the domain's
published approximate rectangle, not its exact rotated-pole footprint, and `clms-extent` follows the owner's statement that the CLMS products cover "Europe,
except for Ukraine": a coarse union of European countries clipped to a European window, so
places outside Europe (the Maghreb coast, for one) are outside it. It does not settle whether
CLMS covers Russia, Belarus or Moldova, which the owners were asked. The Ukraine exclusion
stays a separate constraint because it was stated; any others are not known, which is what
question 3 to the workflow owners is for.

**Which inputs are required is CWL's to say, not the rules'.** The LST datasets and the CLMS
layers are plain `File` inputs, because today the workflow fails without CLMS (UP-WF2.5); only
the local climate zone input is `File?`. The owners call CLMS "recommended" and plan to skip
the step when it is missing, at which point its input becomes `File?`. The rules above say something different:
what must happen to an artifact once the target is outside its coverage.

**The data loader is an `infrastructure` artifact** with the same `different-dataset` rule
UP-WF3 uses: it expects FOCAL STAC file names, so a dataset delivered any other way needs the
loader or the file names adapted.

`outputs` omitted. `inputs` and `steps` ids are **placeholders** invented so `artifactRef`
and `affects` have something to point at; they are not UP-WF2's real interface, and the step
bodies are stubs. Hot spot detection is the root step: characterization consumes its output,
so a failure there stops everything after it, which the wiring already says. The planned
Heat Risk Indicator is not part of the workflow today and is not modeled as a step.

The questionnaire gives the Python requirement as "3.10+"; CWL's version list cannot say "and
later", so only the lower bound is recorded.

#### json
```json
{
  "class": "Workflow",
  "id": "",
  "cwlVersion": "v1.2",
  "label": "UP-WF2 — Urban hot/cool spot",
  "requirements": {
    "SoftwareRequirement": {
      "packages": [
        { "package": "python", "version": ["3.10"] },
        { "package": "rioxarray" },
        { "package": "xarray" },
        { "package": "rasterio" },
        { "package": "geopandas" },
        { "package": "shapely" },
        { "package": "numpy" },
        { "package": "pandas" },
        { "package": "matplotlib" },
        { "package": "joblib" }
      ]
    },
    "NetworkAccess": { "networkAccess": true }
  },
  "inputs": {
    "lst_datasets": { "type": "File" },
    "clms_tcd_imd": { "type": "File" },
    "lcz_data": { "type": "File?" }
  },
  "steps": {
    "hotspot_detection": {
      "run": "#hotspot_detection.cwl",
      "in": { "lst": "lst_datasets" },
      "out": ["hotspot_map"]
    },
    "hotspot_characterization": {
      "run": "#hotspot_characterization.cwl",
      "in": { "hotspots": "hotspot_detection/hotspot_map", "clms": "clms_tcd_imd", "lcz": "lcz_data" },
      "out": ["characterized_map"]
    }
  },
  "transferability": {
    "trainingRequired": false,
    "envelope": [
      {
        "id": "eur11-domain",
        "role": "valid-for",
        "dimension": "spatial",
        "value": { "asWKT": "POLYGON((-22 27,45 27,45 72,-22 72,-22 27))" }
      },
      {
        "id": "clms-extent",
        "role": "valid-for",
        "dimension": "spatial",
        "value": { "asWKT": "MULTIPOLYGON (((-9.18 43.17, -7.7 43.76, -1.99 43.35, -1.08 45.53, -0.83 45.38, -0.69 45.09, -0.55 45, -1.74 47.22, -4.72 48.54, -1.38 48.65, -1.86 49.68, 0.42 49.45, 1.77 50.94, 4.23 51.39, 3.45 51.54, 4.27 51.47, 5.53 53.27, 9.78 53.55, 8.13 55.6, 8.16 56.61, 9.2 56.7, 8.27 56.75, 8.62 57.11, 10.61 57.74, 10.28 56.62, 10.93 56.44, 9.59 55.49, 9.87 54.47, 14.58 53.64, 13.83 54.13, 18.09 54.84, 19.41 54.39, 21.11 55.62, 20.59 54.98, 21.19 54.94, 21.73 57.57, 24.38 57.25, 24.53 58.35, 23.49 59.2, 30.16 59.9, 28.51 60.68, 23.02 59.82, 21.44 60.6, 21.55 63.2, 25.37 65.01, 24.63 65.86, 22.4 65.86, 20.76 63.87, 17.41 62.51, 17.25 60.7, 18.97 59.76, 16.21 58.64, 16.92 58.49, 16.35 56.71, 14.17 55.4, 12.89 55.41, 12.88 56.62, 10.6 59.76, 8.17 58.15, 5.59 58.62, 6.42 59.55, 5.24 59.56, 7 60.51, 5.15 59.64, 5.65 60.69, 5.01 61.04, 7.04 60.95, 7.6 61.21, 5.11 61.19, 4.93 61.88, 6.02 61.79, 6.73 61.87, 5.14 62.16, 8.62 62.85, 8.58 63.6, 10.02 63.39, 11.37 63.8, 9.57 63.71, 12.92 65.34, 12.12 65.36, 14.03 66.3, 13.12 66.23, 13.65 66.91, 15.42 67.2, 14.44 67.27, 15.59 67.35, 15.05 67.96, 16.31 67.88, 19.2 69.75, 23.35 69.98, 24.66 71, 25.77 70.85, 25.04 70.11, 27.6 71.09, 28.39 70.98, 28.19 70.25, 30.07 70.7, 30.94 70.27, 28.8 70.09, 40.97 67.71, 41.19 66.83, 38.65 66.07, 34.48 66.55, 32.93 67.09, 31.9 67.16, 34.69 65.95, 35.04 64.44, 37.44 63.81, 38.06 64.09, 36.88 65.17, 39.76 64.58, 40.44 64.78, 39.82 65.6, 42.21 66.52, 44.1 66.01, 44.2 68.25, 43.33 68.67, 45 68.58, 45 42.71, 39.98 43.42, 36.63 45.15, 39.2 47.27, 35.23 46.44, 35.02 45.7, 36.39 45.07, 33.91 44.39, 32.51 45.4, 33.59 46.1, 31.83 46.28, 32.58 46.62, 31.76 47.21, 31.87 46.65, 28.89 44.92, 27.48 42.47, 28.01 41.97, 26.58 41.95, 26.04 40.73, 23.76 40.75, 23.95 39.97, 22.63 40.5, 23.33 39.17, 22.57 38.87, 24.06 37.77, 23.05 37.9, 23.16 36.45, 22.49 36.45, 21.12 37.89, 23.18 38.13, 21.11 38.38, 19.32 40.41, 19.58 41.79, 13.21 45.77, 12.27 45.45, 12.4 44.22, 18.46 40.22, 16.93 40.46, 16.52 39.75, 17.17 39, 16.06 37.94, 15.69 39.99, 8.77 44.42, 6.12 43.07, 3.26 43.19, 3.25 41.94, 0.71 40.82, -0.33 39.52, 0.2 38.76, -2.11 36.78, -5.63 36.03, -6.86 37.28, -8.94 37.02, -9.18 43.17)), ((-6.32 52.25, -10.38 51.87, -8.78 52.68, -9.92 52.57, -8.93 53.21, -10.09 53.41, -10.06 54.26, -8.55 54.24, -7.31 55.37, -5.53 54.62, -6.35 53.94, -6.32 52.25)), ((-5.26 51.88, -4.15 52.33, -4.27 53.14, -2.75 53.31, -3.59 54.56, -3.04 54.95, -4.91 54.69, -4.58 55.94, -5.73 55.33, -5.19 56.76, -6.13 56.72, -5.02 58.57, -3.05 58.63, -4.13 57.58, -1.78 57.47, -3.31 56.36, -2.67 56.25, -3.79 56.1, -2.15 55.9, -0.08 54.12, 0.12 53.61, -0.27 53.74, -0.66 53.72, 0.05 52.91, 1.75 52.47, 0.42 51.47, 1.41 51.36, 0.96 50.93, -5.66 50.08, -4.19 51.19, -3.14 51.21, -2.43 51.74, -5.26 51.88)), ((-13.6 65.04, -18.65 63.41, -22.65 63.83, -21.59 64.63, -24.03 64.86, -21.84 65.45, -24.48 65.53, -22.44 65.91, -22.89 66.44, -21.13 65.27, -20.21 66.1, -14.7 66.34, -13.6 65.04)))" }
      },
      {
        "id": "clms-excluded-ukraine",
        "role": "valid-for",
        "dimension": "spatial",
        "value": { "asWKT": "MULTIPOLYGON (((37.54 47.07, 36.79 46.71, 35.83 46.62, 35.2 46.17, 35.01 46.11, 35.28 46.28, 35.23 46.44, 34.85 46.19, 34.95 45.73, 34.69 45.98, 33.81 46.21, 33.43 46.06, 33.2 46.18, 32.48 46.08, 31.83 46.28, 32.01 46.43, 31.55 46.55, 32.36 46.47, 32.58 46.62, 32.04 46.64, 31.94 46.98, 31.76 47.21, 31.87 46.65, 31.53 46.66, 31.56 46.78, 30.8 46.55, 30.22 45.87, 29.63 45.72, 29.71 45.26, 29.4 45.42, 28.76 45.23, 28.21 45.45, 28.5 45.52, 28.49 45.67, 28.95 46.05, 28.96 46.46, 30.13 46.42, 29.92 46.54, 29.88 46.83, 29.57 46.96, 29.54 47.27, 29.13 47.49, 29.13 47.96, 27.55 48.48, 26.85 48.39, 26.31 48.2, 26.16 47.99, 24.89 47.72, 24.48 47.95, 23.14 48.09, 22.88 47.95, 22.13 48.41, 22.14 48.57, 22.54 49.07, 22.84 49.04, 22.71 49.17, 22.71 49.61, 24.09 50.53, 23.98 50.79, 24.1 50.87, 23.66 51.31, 23.61 51.61, 23.98 51.59, 24.36 51.87, 25.93 51.91, 27.14 51.75, 27.7 51.48, 28.18 51.61, 28.73 51.43, 29.1 51.63, 29.35 51.38, 30.16 51.48, 30.54 51.27, 30.58 51.69, 30.98 52.05, 32.12 52.05, 32.44 52.31, 33.74 52.34, 34.4 51.78, 34.12 51.68, 34.21 51.26, 35.06 51.2, 35.31 51.04, 35.41 50.54, 35.59 50.37, 36.12 50.41, 36.62 50.21, 37.42 50.41, 38.05 49.92, 38.26 50.05, 40.08 49.58, 40.11 49.25, 39.69 49.01, 40 48.82, 39.79 48.81, 39.64 48.59, 39.84 48.54, 39.96 48.27, 39.78 47.89, 38.9 47.86, 38.37 47.61, 38.21 47.09, 37.54 47.07)), ((32.15 46.15, 31.56 46.26, 31.51 46.37, 32.15 46.15)))" }
      },
      {
        "id": "epoch-2022-2025",
        "role": "can-run-on",
        "dimension": "temporal",
        "value": { "startDate": "2022", "endDate": "2025" },
        "transferabilityNotes": "Precalculated epochs of median summer LST, not a time series. A single LST dataset can also be run."
      },
      { "id": "epoch-2011-2015", "role": "can-run-on", "dimension": "temporal", "value": { "startDate": "2011", "endDate": "2015" } },
      { "id": "epoch-2001-2005", "role": "can-run-on", "dimension": "temporal", "value": { "startDate": "2001", "endDate": "2005" } }
    ],
    "artifacts": [
      {
        "id": "lst",
        "artifact": "median summer LST datasets (FOCAL STAC, Landsat 5/7/8/9-derived)",
        "artifactRole": "workflow-input",
        "artifactRef": "/inputs/lst_datasets",
        "acceptanceCriteria": {
          "variables": [{ "name": "band_data" }],
          "transferabilityNotes": "A georeferenced raster that xarray or rasterio can open, with one value per grid cell, read from index 0 of a `band` dimension. Packed values are unpacked with the `scale_factor` and `add_offset` attributes when present; no-data is NaN unless `rio.nodata` says otherwise. The unit does not matter to the classification. Any CRS: inputs are reprojected to EPSG:3857 on import."
        }
      },
      {
        "id": "clms",
        "artifact": "CLMS Tree Cover Density 2018 / Imperviousness Density 2024",
        "artifactRole": "workflow-input",
        "artifactRef": "/inputs/clms_tcd_imd",
        "acceptanceCriteria": {
          "variables": [{ "name": "band_data" }],
          "transferabilityNotes": "Replaceable by a newer version or another raster, since only zonal statistics are computed; other climates may call for other layers. The same raster conventions as the LST datasets; the unit does not matter. Recommended, but today the workflow fails at the zonal statistics step without it; skipping the step is planned."
        }
      },
      {
        "id": "lcz",
        "artifact": "local climate zone data",
        "artifactRole": "workflow-input",
        "artifactRef": "/inputs/lcz_data",
        "transferabilityNotes": "Recommended, not required: without it hot spot characterization lacks local climate zone statistics."
      },
      {
        "id": "focal-stac-loader",
        "artifact": "FOCAL STAC data loader, built into the workflow",
        "artifactRole": "infrastructure",
        "transferabilityNotes": "The loader expects file paths whose names follow the FOCAL STAC convention and uses them to check that the tiles are complete and connected. The check could be weakened, at the cost of strict validation."
      }
    ],
    "rules": [
      {
        "appliesTo": ["lst"],
        "when": [{ "constraint": "eur11-domain", "test": "inside" }],
        "actions": ["reuse-as-is"]
      },
      {
        "appliesTo": ["lst"],
        "when": [{ "constraint": "eur11-domain", "test": "outside" }],
        "actions": ["replace-with-local-equivalent", "component-not-executable"],
        "affects": ["/steps/hotspot_detection"],
        "mandatory": true,
        "transferabilityNotes": "Outside it, compatible LST datasets must be generated or preprocessed if possible; if none can be produced, this component cannot be executed for the target."
      },
      {
        "appliesTo": ["clms"],
        "when": [{ "constraint": "clms-extent", "test": "outside" }],
        "actions": ["replace-with-local-equivalent", "component-not-executable"],
        "affects": ["/steps/hotspot_characterization"],
        "mandatory": true,
        "transferabilityNotes": "Today the workflow interrupts at the zonal-statistics step without CLMS data; hot and cool spot detection runs before it. Skipping the step is planned."
      },
      {
        "appliesTo": ["clms"],
        "when": [{ "constraint": "clms-excluded-ukraine", "test": "inside" }],
        "actions": ["replace-with-local-equivalent", "component-not-executable"],
        "affects": ["/steps/hotspot_characterization"],
        "mandatory": true
      },
      {
        "appliesTo": ["focal-stac-loader"],
        "triggeredBy": "different-dataset",
        "actions": ["replace-with-local-equivalent"],
        "mandatory": true
      }
    ],
    "transferabilityNotes": "The hot and cool spot classification is data-agnostic: any georeferenced raster with one value per grid cell can be classified, so the algorithm is more portable than the LST input. The spots then describe high and low values of whatever quantity is supplied. A Heat Risk Indicator step and its census data are planned but not part of the workflow today; the census data becomes required when it is implemented."
  },
  "computationType": "deterministic-rule-based",
  "maturityStatus": "pre-operational",
  "qualityAnnotation": [
    {
      "dimension": "proxy-variable",
      "note": "Question 7: 'Hot spot detection is based on median summer Land Surface Temperature, which represents surface temperatures rather than near-surface air temperatures.' What the workflow computes is a stand-in for the air temperature a reader might assume, in the source region as much as in any target."
    },
    {
      "dimension": "intended-use-limit",
      "note": "Question 7: 'Results represent long-term thermal patterns for the selected epoch and are not intended for real-time heat monitoring.'"
    }
  ]
}

```

#### jsonld
```jsonld
{
  "@context": "https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/workflow/context.jsonld",
  "class": "Workflow",
  "id": "",
  "cwlVersion": "v1.2",
  "label": "UP-WF2 \u2014 Urban hot/cool spot",
  "requirements": {
    "SoftwareRequirement": {
      "packages": [
        {
          "package": "python",
          "version": [
            "3.10"
          ]
        },
        {
          "package": "rioxarray"
        },
        {
          "package": "xarray"
        },
        {
          "package": "rasterio"
        },
        {
          "package": "geopandas"
        },
        {
          "package": "shapely"
        },
        {
          "package": "numpy"
        },
        {
          "package": "pandas"
        },
        {
          "package": "matplotlib"
        },
        {
          "package": "joblib"
        }
      ]
    },
    "NetworkAccess": {
      "networkAccess": true
    }
  },
  "inputs": {
    "lst_datasets": {
      "type": "File"
    },
    "clms_tcd_imd": {
      "type": "File"
    },
    "lcz_data": {
      "type": "File?"
    }
  },
  "steps": {
    "hotspot_detection": {
      "run": "#hotspot_detection.cwl",
      "in": {
        "lst": "lst_datasets"
      },
      "out": [
        "hotspot_map"
      ]
    },
    "hotspot_characterization": {
      "run": "#hotspot_characterization.cwl",
      "in": {
        "hotspots": "hotspot_detection/hotspot_map",
        "clms": "clms_tcd_imd",
        "lcz": "lcz_data"
      },
      "out": [
        "characterized_map"
      ]
    }
  },
  "transferability": {
    "trainingRequired": false,
    "envelope": [
      {
        "id": "eur11-domain",
        "role": "valid-for",
        "dimension": "spatial",
        "value": {
          "asWKT": "POLYGON((-22 27,45 27,45 72,-22 72,-22 27))"
        }
      },
      {
        "id": "clms-extent",
        "role": "valid-for",
        "dimension": "spatial",
        "value": {
          "asWKT": "MULTIPOLYGON (((-9.18 43.17, -7.7 43.76, -1.99 43.35, -1.08 45.53, -0.83 45.38, -0.69 45.09, -0.55 45, -1.74 47.22, -4.72 48.54, -1.38 48.65, -1.86 49.68, 0.42 49.45, 1.77 50.94, 4.23 51.39, 3.45 51.54, 4.27 51.47, 5.53 53.27, 9.78 53.55, 8.13 55.6, 8.16 56.61, 9.2 56.7, 8.27 56.75, 8.62 57.11, 10.61 57.74, 10.28 56.62, 10.93 56.44, 9.59 55.49, 9.87 54.47, 14.58 53.64, 13.83 54.13, 18.09 54.84, 19.41 54.39, 21.11 55.62, 20.59 54.98, 21.19 54.94, 21.73 57.57, 24.38 57.25, 24.53 58.35, 23.49 59.2, 30.16 59.9, 28.51 60.68, 23.02 59.82, 21.44 60.6, 21.55 63.2, 25.37 65.01, 24.63 65.86, 22.4 65.86, 20.76 63.87, 17.41 62.51, 17.25 60.7, 18.97 59.76, 16.21 58.64, 16.92 58.49, 16.35 56.71, 14.17 55.4, 12.89 55.41, 12.88 56.62, 10.6 59.76, 8.17 58.15, 5.59 58.62, 6.42 59.55, 5.24 59.56, 7 60.51, 5.15 59.64, 5.65 60.69, 5.01 61.04, 7.04 60.95, 7.6 61.21, 5.11 61.19, 4.93 61.88, 6.02 61.79, 6.73 61.87, 5.14 62.16, 8.62 62.85, 8.58 63.6, 10.02 63.39, 11.37 63.8, 9.57 63.71, 12.92 65.34, 12.12 65.36, 14.03 66.3, 13.12 66.23, 13.65 66.91, 15.42 67.2, 14.44 67.27, 15.59 67.35, 15.05 67.96, 16.31 67.88, 19.2 69.75, 23.35 69.98, 24.66 71, 25.77 70.85, 25.04 70.11, 27.6 71.09, 28.39 70.98, 28.19 70.25, 30.07 70.7, 30.94 70.27, 28.8 70.09, 40.97 67.71, 41.19 66.83, 38.65 66.07, 34.48 66.55, 32.93 67.09, 31.9 67.16, 34.69 65.95, 35.04 64.44, 37.44 63.81, 38.06 64.09, 36.88 65.17, 39.76 64.58, 40.44 64.78, 39.82 65.6, 42.21 66.52, 44.1 66.01, 44.2 68.25, 43.33 68.67, 45 68.58, 45 42.71, 39.98 43.42, 36.63 45.15, 39.2 47.27, 35.23 46.44, 35.02 45.7, 36.39 45.07, 33.91 44.39, 32.51 45.4, 33.59 46.1, 31.83 46.28, 32.58 46.62, 31.76 47.21, 31.87 46.65, 28.89 44.92, 27.48 42.47, 28.01 41.97, 26.58 41.95, 26.04 40.73, 23.76 40.75, 23.95 39.97, 22.63 40.5, 23.33 39.17, 22.57 38.87, 24.06 37.77, 23.05 37.9, 23.16 36.45, 22.49 36.45, 21.12 37.89, 23.18 38.13, 21.11 38.38, 19.32 40.41, 19.58 41.79, 13.21 45.77, 12.27 45.45, 12.4 44.22, 18.46 40.22, 16.93 40.46, 16.52 39.75, 17.17 39, 16.06 37.94, 15.69 39.99, 8.77 44.42, 6.12 43.07, 3.26 43.19, 3.25 41.94, 0.71 40.82, -0.33 39.52, 0.2 38.76, -2.11 36.78, -5.63 36.03, -6.86 37.28, -8.94 37.02, -9.18 43.17)), ((-6.32 52.25, -10.38 51.87, -8.78 52.68, -9.92 52.57, -8.93 53.21, -10.09 53.41, -10.06 54.26, -8.55 54.24, -7.31 55.37, -5.53 54.62, -6.35 53.94, -6.32 52.25)), ((-5.26 51.88, -4.15 52.33, -4.27 53.14, -2.75 53.31, -3.59 54.56, -3.04 54.95, -4.91 54.69, -4.58 55.94, -5.73 55.33, -5.19 56.76, -6.13 56.72, -5.02 58.57, -3.05 58.63, -4.13 57.58, -1.78 57.47, -3.31 56.36, -2.67 56.25, -3.79 56.1, -2.15 55.9, -0.08 54.12, 0.12 53.61, -0.27 53.74, -0.66 53.72, 0.05 52.91, 1.75 52.47, 0.42 51.47, 1.41 51.36, 0.96 50.93, -5.66 50.08, -4.19 51.19, -3.14 51.21, -2.43 51.74, -5.26 51.88)), ((-13.6 65.04, -18.65 63.41, -22.65 63.83, -21.59 64.63, -24.03 64.86, -21.84 65.45, -24.48 65.53, -22.44 65.91, -22.89 66.44, -21.13 65.27, -20.21 66.1, -14.7 66.34, -13.6 65.04)))"
        }
      },
      {
        "id": "clms-excluded-ukraine",
        "role": "valid-for",
        "dimension": "spatial",
        "value": {
          "asWKT": "MULTIPOLYGON (((37.54 47.07, 36.79 46.71, 35.83 46.62, 35.2 46.17, 35.01 46.11, 35.28 46.28, 35.23 46.44, 34.85 46.19, 34.95 45.73, 34.69 45.98, 33.81 46.21, 33.43 46.06, 33.2 46.18, 32.48 46.08, 31.83 46.28, 32.01 46.43, 31.55 46.55, 32.36 46.47, 32.58 46.62, 32.04 46.64, 31.94 46.98, 31.76 47.21, 31.87 46.65, 31.53 46.66, 31.56 46.78, 30.8 46.55, 30.22 45.87, 29.63 45.72, 29.71 45.26, 29.4 45.42, 28.76 45.23, 28.21 45.45, 28.5 45.52, 28.49 45.67, 28.95 46.05, 28.96 46.46, 30.13 46.42, 29.92 46.54, 29.88 46.83, 29.57 46.96, 29.54 47.27, 29.13 47.49, 29.13 47.96, 27.55 48.48, 26.85 48.39, 26.31 48.2, 26.16 47.99, 24.89 47.72, 24.48 47.95, 23.14 48.09, 22.88 47.95, 22.13 48.41, 22.14 48.57, 22.54 49.07, 22.84 49.04, 22.71 49.17, 22.71 49.61, 24.09 50.53, 23.98 50.79, 24.1 50.87, 23.66 51.31, 23.61 51.61, 23.98 51.59, 24.36 51.87, 25.93 51.91, 27.14 51.75, 27.7 51.48, 28.18 51.61, 28.73 51.43, 29.1 51.63, 29.35 51.38, 30.16 51.48, 30.54 51.27, 30.58 51.69, 30.98 52.05, 32.12 52.05, 32.44 52.31, 33.74 52.34, 34.4 51.78, 34.12 51.68, 34.21 51.26, 35.06 51.2, 35.31 51.04, 35.41 50.54, 35.59 50.37, 36.12 50.41, 36.62 50.21, 37.42 50.41, 38.05 49.92, 38.26 50.05, 40.08 49.58, 40.11 49.25, 39.69 49.01, 40 48.82, 39.79 48.81, 39.64 48.59, 39.84 48.54, 39.96 48.27, 39.78 47.89, 38.9 47.86, 38.37 47.61, 38.21 47.09, 37.54 47.07)), ((32.15 46.15, 31.56 46.26, 31.51 46.37, 32.15 46.15)))"
        }
      },
      {
        "id": "epoch-2022-2025",
        "role": "can-run-on",
        "dimension": "temporal",
        "value": {
          "startDate": "2022",
          "endDate": "2025"
        },
        "transferabilityNotes": "Precalculated epochs of median summer LST, not a time series. A single LST dataset can also be run."
      },
      {
        "id": "epoch-2011-2015",
        "role": "can-run-on",
        "dimension": "temporal",
        "value": {
          "startDate": "2011",
          "endDate": "2015"
        }
      },
      {
        "id": "epoch-2001-2005",
        "role": "can-run-on",
        "dimension": "temporal",
        "value": {
          "startDate": "2001",
          "endDate": "2005"
        }
      }
    ],
    "artifacts": [
      {
        "id": "lst",
        "artifact": "median summer LST datasets (FOCAL STAC, Landsat 5/7/8/9-derived)",
        "artifactRole": "workflow-input",
        "artifactRef": "/inputs/lst_datasets",
        "acceptanceCriteria": {
          "variables": [
            {
              "name": "band_data"
            }
          ],
          "transferabilityNotes": "A georeferenced raster that xarray or rasterio can open, with one value per grid cell, read from index 0 of a `band` dimension. Packed values are unpacked with the `scale_factor` and `add_offset` attributes when present; no-data is NaN unless `rio.nodata` says otherwise. The unit does not matter to the classification. Any CRS: inputs are reprojected to EPSG:3857 on import."
        }
      },
      {
        "id": "clms",
        "artifact": "CLMS Tree Cover Density 2018 / Imperviousness Density 2024",
        "artifactRole": "workflow-input",
        "artifactRef": "/inputs/clms_tcd_imd",
        "acceptanceCriteria": {
          "variables": [
            {
              "name": "band_data"
            }
          ],
          "transferabilityNotes": "Replaceable by a newer version or another raster, since only zonal statistics are computed; other climates may call for other layers. The same raster conventions as the LST datasets; the unit does not matter. Recommended, but today the workflow fails at the zonal statistics step without it; skipping the step is planned."
        }
      },
      {
        "id": "lcz",
        "artifact": "local climate zone data",
        "artifactRole": "workflow-input",
        "artifactRef": "/inputs/lcz_data",
        "transferabilityNotes": "Recommended, not required: without it hot spot characterization lacks local climate zone statistics."
      },
      {
        "id": "focal-stac-loader",
        "artifact": "FOCAL STAC data loader, built into the workflow",
        "artifactRole": "infrastructure",
        "transferabilityNotes": "The loader expects file paths whose names follow the FOCAL STAC convention and uses them to check that the tiles are complete and connected. The check could be weakened, at the cost of strict validation."
      }
    ],
    "rules": [
      {
        "appliesTo": [
          "lst"
        ],
        "when": [
          {
            "constraint": "eur11-domain",
            "test": "inside"
          }
        ],
        "actions": [
          "reuse-as-is"
        ]
      },
      {
        "appliesTo": [
          "lst"
        ],
        "when": [
          {
            "constraint": "eur11-domain",
            "test": "outside"
          }
        ],
        "actions": [
          "replace-with-local-equivalent",
          "component-not-executable"
        ],
        "affects": [
          "/steps/hotspot_detection"
        ],
        "mandatory": true,
        "transferabilityNotes": "Outside it, compatible LST datasets must be generated or preprocessed if possible; if none can be produced, this component cannot be executed for the target."
      },
      {
        "appliesTo": [
          "clms"
        ],
        "when": [
          {
            "constraint": "clms-extent",
            "test": "outside"
          }
        ],
        "actions": [
          "replace-with-local-equivalent",
          "component-not-executable"
        ],
        "affects": [
          "/steps/hotspot_characterization"
        ],
        "mandatory": true,
        "transferabilityNotes": "Today the workflow interrupts at the zonal-statistics step without CLMS data; hot and cool spot detection runs before it. Skipping the step is planned."
      },
      {
        "appliesTo": [
          "clms"
        ],
        "when": [
          {
            "constraint": "clms-excluded-ukraine",
            "test": "inside"
          }
        ],
        "actions": [
          "replace-with-local-equivalent",
          "component-not-executable"
        ],
        "affects": [
          "/steps/hotspot_characterization"
        ],
        "mandatory": true
      },
      {
        "appliesTo": [
          "focal-stac-loader"
        ],
        "triggeredBy": "different-dataset",
        "actions": [
          "replace-with-local-equivalent"
        ],
        "mandatory": true
      }
    ],
    "transferabilityNotes": "The hot and cool spot classification is data-agnostic: any georeferenced raster with one value per grid cell can be classified, so the algorithm is more portable than the LST input. The spots then describe high and low values of whatever quantity is supplied. A Heat Risk Indicator step and its census data are planned but not part of the workflow today; the census data becomes required when it is implemented."
  },
  "computationType": "deterministic-rule-based",
  "maturityStatus": "pre-operational",
  "qualityAnnotation": [
    {
      "dimension": "proxy-variable",
      "note": "Question 7: 'Hot spot detection is based on median summer Land Surface Temperature, which represents surface temperatures rather than near-surface air temperatures.' What the workflow computes is a stand-in for the air temperature a reader might assume, in the source region as much as in any target."
    },
    {
      "dimension": "intended-use-limit",
      "note": "Question 7: 'Results represent long-term thermal patterns for the selected epoch and are not intended for real-time heat monitoring.'"
    }
  ]
}
```

#### ttl
```ttl
@prefix cwl: <https://w3id.org/cwl/cwl#> .
@prefix dcat: <http://www.w3.org/ns/dcat#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix dqv: <http://www.w3.org/ns/dqv#> .
@prefix focal-transf-prop: <https://w3id.org/ogc/hosted/focal/transferability/properties/> .
@prefix geo: <http://www.opengis.net/ont/geosparql#> .
@prefix ns1: <https://w3id.org/cwl/cwl#SoftwarePackage/> .
@prefix ns2: <https://w3id.org/cwl/cwl#SoftwareRequirement/> .
@prefix ns3: <https://w3id.org/cwl/cwl#NetworkAccess/> .
@prefix ns4: <https://w3id.org/cwl/cwl#Workflow/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix sld: <https://w3id.org/cwl/salad#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/> a cwl:Workflow ;
    rdfs:label "UP-WF2 — Urban hot/cool spot" ;
    ns4:steps <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/hotspot_characterization>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/hotspot_detection> ;
    cwl:inputs <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/clms_tcd_imd>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/lcz_data>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/lst_datasets> ;
    cwl:requirements [ a cwl:SoftwareRequirement ;
            ns2:packages [ ns1:package "shapely" ],
                [ ns1:package "geopandas" ],
                [ ns1:package "python" ;
                    ns1:version "3.10" ],
                [ ns1:package "rasterio" ],
                [ ns1:package "matplotlib" ],
                [ ns1:package "numpy" ],
                [ ns1:package "pandas" ],
                [ ns1:package "joblib" ],
                [ ns1:package "xarray" ],
                [ ns1:package "rioxarray" ] ],
        [ a cwl:NetworkAccess ;
            ns3:networkAccess true ] ;
    focal-transf-prop:computationType <https://w3id.org/ogc/hosted/focal/transferability/computation-types/deterministic-rule-based> ;
    focal-transf-prop:maturityStatus <https://w3id.org/ogc/hosted/focal/transferability/maturity-statuses/pre-operational> ;
    focal-transf-prop:qualityAnnotation [ dqv:inDimension <https://w3id.org/ogc/hosted/focal/transferability/quality-dimensions/intended-use-limit> ;
            focal-transf-prop:note "Question 7: 'Results represent long-term thermal patterns for the selected epoch and are not intended for real-time heat monitoring.'" ],
        [ dqv:inDimension <https://w3id.org/ogc/hosted/focal/transferability/quality-dimensions/proxy-variable> ;
            focal-transf-prop:note "Question 7: 'Hot spot detection is based on median summer Land Surface Temperature, which represents surface temperatures rather than near-surface air temperatures.' What the workflow computes is a stand-in for the air temperature a reader might assume, in the source region as much as in any target." ] ;
    focal-transf-prop:transferability [ rdfs:comment "The hot and cool spot classification is data-agnostic: any georeferenced raster with one value per grid cell can be classified, so the algorithm is more portable than the LST input. The spots then describe high and low values of whatever quantity is supplied. A Heat Risk Indicator step and its census data are planned but not part of the workflow today; the census data becomes required when it is implemented." ;
            focal-transf-prop:artifacts <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/clms>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/focal-stac-loader>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/lcz>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/lst> ;
            focal-transf-prop:envelope <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/clms-excluded-ukraine>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/clms-extent>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/epoch-2001-2005>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/epoch-2011-2015>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/epoch-2022-2025>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/eur11-domain> ;
            focal-transf-prop:rules [ focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/component-not-executable>,
                        <https://w3id.org/ogc/hosted/focal/transferability/actions/replace-with-local-equivalent> ;
                    focal-transf-prop:affects "/steps/hotspot_characterization" ;
                    focal-transf-prop:appliesTo <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/clms> ;
                    focal-transf-prop:mandatory true ;
                    focal-transf-prop:when [ focal-transf-prop:constraint <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/clms-excluded-ukraine> ;
                            focal-transf-prop:test <https://w3id.org/ogc/hosted/focal/transferability/tests/inside> ] ],
                [ rdfs:comment "Outside it, compatible LST datasets must be generated or preprocessed if possible; if none can be produced, this component cannot be executed for the target." ;
                    focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/component-not-executable>,
                        <https://w3id.org/ogc/hosted/focal/transferability/actions/replace-with-local-equivalent> ;
                    focal-transf-prop:affects "/steps/hotspot_detection" ;
                    focal-transf-prop:appliesTo <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/lst> ;
                    focal-transf-prop:mandatory true ;
                    focal-transf-prop:when [ focal-transf-prop:constraint <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/eur11-domain> ;
                            focal-transf-prop:test <https://w3id.org/ogc/hosted/focal/transferability/tests/outside> ] ],
                [ rdfs:comment "Today the workflow interrupts at the zonal-statistics step without CLMS data; hot and cool spot detection runs before it. Skipping the step is planned." ;
                    focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/component-not-executable>,
                        <https://w3id.org/ogc/hosted/focal/transferability/actions/replace-with-local-equivalent> ;
                    focal-transf-prop:affects "/steps/hotspot_characterization" ;
                    focal-transf-prop:appliesTo <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/clms> ;
                    focal-transf-prop:mandatory true ;
                    focal-transf-prop:when [ focal-transf-prop:constraint <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/clms-extent> ;
                            focal-transf-prop:test <https://w3id.org/ogc/hosted/focal/transferability/tests/outside> ] ],
                [ focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/replace-with-local-equivalent> ;
                    focal-transf-prop:appliesTo <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/focal-stac-loader> ;
                    focal-transf-prop:mandatory true ;
                    focal-transf-prop:triggeredBy <https://w3id.org/ogc/hosted/focal/transferability/triggers/different-dataset> ],
                [ focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/reuse-as-is> ;
                    focal-transf-prop:appliesTo <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/lst> ;
                    focal-transf-prop:when [ focal-transf-prop:constraint <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/eur11-domain> ;
                            focal-transf-prop:test <https://w3id.org/ogc/hosted/focal/transferability/tests/inside> ] ] ;
            focal-transf-prop:trainingRequired false ] .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/clms_tcd_imd> sld:type cwl:File .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/epoch-2001-2005> focal-transf-prop:dimension <https://w3id.org/ogc/hosted/focal/transferability/dimensions/temporal> ;
    focal-transf-prop:role <https://w3id.org/ogc/hosted/focal/transferability/roles/can-run-on> ;
    focal-transf-prop:value [ dcat:endDate "2005" ;
            dcat:startDate "2001" ] .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/epoch-2011-2015> focal-transf-prop:dimension <https://w3id.org/ogc/hosted/focal/transferability/dimensions/temporal> ;
    focal-transf-prop:role <https://w3id.org/ogc/hosted/focal/transferability/roles/can-run-on> ;
    focal-transf-prop:value [ dcat:endDate "2015" ;
            dcat:startDate "2011" ] .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/epoch-2022-2025> rdfs:comment "Precalculated epochs of median summer LST, not a time series. A single LST dataset can also be run." ;
    focal-transf-prop:dimension <https://w3id.org/ogc/hosted/focal/transferability/dimensions/temporal> ;
    focal-transf-prop:role <https://w3id.org/ogc/hosted/focal/transferability/roles/can-run-on> ;
    focal-transf-prop:value [ dcat:endDate "2025" ;
            dcat:startDate "2022" ] .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/hotspot_characterization> cwl:in "clms_tcd_imd",
        "hotspot_detection/hotspot_map",
        "lcz_data" ;
    cwl:out <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/characterized_map> ;
    cwl:run <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/#hotspot_characterization.cwl> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/hotspot_detection> cwl:in "lst_datasets" ;
    cwl:out <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/hotspot_map> ;
    cwl:run <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/#hotspot_detection.cwl> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/lcz> dcterms:title "local climate zone data" ;
    rdfs:comment "Recommended, not required: without it hot spot characterization lacks local climate zone statistics." ;
    focal-transf-prop:artifactRef "/inputs/lcz_data" ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/workflow-input> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/lcz_data> sld:type <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/File> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/lst_datasets> sld:type cwl:File .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/clms-excluded-ukraine> focal-transf-prop:dimension <https://w3id.org/ogc/hosted/focal/transferability/dimensions/spatial> ;
    focal-transf-prop:role <https://w3id.org/ogc/hosted/focal/transferability/roles/valid-for> ;
    focal-transf-prop:value [ geo:asWKT "MULTIPOLYGON (((37.54 47.07, 36.79 46.71, 35.83 46.62, 35.2 46.17, 35.01 46.11, 35.28 46.28, 35.23 46.44, 34.85 46.19, 34.95 45.73, 34.69 45.98, 33.81 46.21, 33.43 46.06, 33.2 46.18, 32.48 46.08, 31.83 46.28, 32.01 46.43, 31.55 46.55, 32.36 46.47, 32.58 46.62, 32.04 46.64, 31.94 46.98, 31.76 47.21, 31.87 46.65, 31.53 46.66, 31.56 46.78, 30.8 46.55, 30.22 45.87, 29.63 45.72, 29.71 45.26, 29.4 45.42, 28.76 45.23, 28.21 45.45, 28.5 45.52, 28.49 45.67, 28.95 46.05, 28.96 46.46, 30.13 46.42, 29.92 46.54, 29.88 46.83, 29.57 46.96, 29.54 47.27, 29.13 47.49, 29.13 47.96, 27.55 48.48, 26.85 48.39, 26.31 48.2, 26.16 47.99, 24.89 47.72, 24.48 47.95, 23.14 48.09, 22.88 47.95, 22.13 48.41, 22.14 48.57, 22.54 49.07, 22.84 49.04, 22.71 49.17, 22.71 49.61, 24.09 50.53, 23.98 50.79, 24.1 50.87, 23.66 51.31, 23.61 51.61, 23.98 51.59, 24.36 51.87, 25.93 51.91, 27.14 51.75, 27.7 51.48, 28.18 51.61, 28.73 51.43, 29.1 51.63, 29.35 51.38, 30.16 51.48, 30.54 51.27, 30.58 51.69, 30.98 52.05, 32.12 52.05, 32.44 52.31, 33.74 52.34, 34.4 51.78, 34.12 51.68, 34.21 51.26, 35.06 51.2, 35.31 51.04, 35.41 50.54, 35.59 50.37, 36.12 50.41, 36.62 50.21, 37.42 50.41, 38.05 49.92, 38.26 50.05, 40.08 49.58, 40.11 49.25, 39.69 49.01, 40 48.82, 39.79 48.81, 39.64 48.59, 39.84 48.54, 39.96 48.27, 39.78 47.89, 38.9 47.86, 38.37 47.61, 38.21 47.09, 37.54 47.07)), ((32.15 46.15, 31.56 46.26, 31.51 46.37, 32.15 46.15)))"^^geo:wktLiteral ] .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/clms-extent> focal-transf-prop:dimension <https://w3id.org/ogc/hosted/focal/transferability/dimensions/spatial> ;
    focal-transf-prop:role <https://w3id.org/ogc/hosted/focal/transferability/roles/valid-for> ;
    focal-transf-prop:value [ geo:asWKT "MULTIPOLYGON (((-9.18 43.17, -7.7 43.76, -1.99 43.35, -1.08 45.53, -0.83 45.38, -0.69 45.09, -0.55 45, -1.74 47.22, -4.72 48.54, -1.38 48.65, -1.86 49.68, 0.42 49.45, 1.77 50.94, 4.23 51.39, 3.45 51.54, 4.27 51.47, 5.53 53.27, 9.78 53.55, 8.13 55.6, 8.16 56.61, 9.2 56.7, 8.27 56.75, 8.62 57.11, 10.61 57.74, 10.28 56.62, 10.93 56.44, 9.59 55.49, 9.87 54.47, 14.58 53.64, 13.83 54.13, 18.09 54.84, 19.41 54.39, 21.11 55.62, 20.59 54.98, 21.19 54.94, 21.73 57.57, 24.38 57.25, 24.53 58.35, 23.49 59.2, 30.16 59.9, 28.51 60.68, 23.02 59.82, 21.44 60.6, 21.55 63.2, 25.37 65.01, 24.63 65.86, 22.4 65.86, 20.76 63.87, 17.41 62.51, 17.25 60.7, 18.97 59.76, 16.21 58.64, 16.92 58.49, 16.35 56.71, 14.17 55.4, 12.89 55.41, 12.88 56.62, 10.6 59.76, 8.17 58.15, 5.59 58.62, 6.42 59.55, 5.24 59.56, 7 60.51, 5.15 59.64, 5.65 60.69, 5.01 61.04, 7.04 60.95, 7.6 61.21, 5.11 61.19, 4.93 61.88, 6.02 61.79, 6.73 61.87, 5.14 62.16, 8.62 62.85, 8.58 63.6, 10.02 63.39, 11.37 63.8, 9.57 63.71, 12.92 65.34, 12.12 65.36, 14.03 66.3, 13.12 66.23, 13.65 66.91, 15.42 67.2, 14.44 67.27, 15.59 67.35, 15.05 67.96, 16.31 67.88, 19.2 69.75, 23.35 69.98, 24.66 71, 25.77 70.85, 25.04 70.11, 27.6 71.09, 28.39 70.98, 28.19 70.25, 30.07 70.7, 30.94 70.27, 28.8 70.09, 40.97 67.71, 41.19 66.83, 38.65 66.07, 34.48 66.55, 32.93 67.09, 31.9 67.16, 34.69 65.95, 35.04 64.44, 37.44 63.81, 38.06 64.09, 36.88 65.17, 39.76 64.58, 40.44 64.78, 39.82 65.6, 42.21 66.52, 44.1 66.01, 44.2 68.25, 43.33 68.67, 45 68.58, 45 42.71, 39.98 43.42, 36.63 45.15, 39.2 47.27, 35.23 46.44, 35.02 45.7, 36.39 45.07, 33.91 44.39, 32.51 45.4, 33.59 46.1, 31.83 46.28, 32.58 46.62, 31.76 47.21, 31.87 46.65, 28.89 44.92, 27.48 42.47, 28.01 41.97, 26.58 41.95, 26.04 40.73, 23.76 40.75, 23.95 39.97, 22.63 40.5, 23.33 39.17, 22.57 38.87, 24.06 37.77, 23.05 37.9, 23.16 36.45, 22.49 36.45, 21.12 37.89, 23.18 38.13, 21.11 38.38, 19.32 40.41, 19.58 41.79, 13.21 45.77, 12.27 45.45, 12.4 44.22, 18.46 40.22, 16.93 40.46, 16.52 39.75, 17.17 39, 16.06 37.94, 15.69 39.99, 8.77 44.42, 6.12 43.07, 3.26 43.19, 3.25 41.94, 0.71 40.82, -0.33 39.52, 0.2 38.76, -2.11 36.78, -5.63 36.03, -6.86 37.28, -8.94 37.02, -9.18 43.17)), ((-6.32 52.25, -10.38 51.87, -8.78 52.68, -9.92 52.57, -8.93 53.21, -10.09 53.41, -10.06 54.26, -8.55 54.24, -7.31 55.37, -5.53 54.62, -6.35 53.94, -6.32 52.25)), ((-5.26 51.88, -4.15 52.33, -4.27 53.14, -2.75 53.31, -3.59 54.56, -3.04 54.95, -4.91 54.69, -4.58 55.94, -5.73 55.33, -5.19 56.76, -6.13 56.72, -5.02 58.57, -3.05 58.63, -4.13 57.58, -1.78 57.47, -3.31 56.36, -2.67 56.25, -3.79 56.1, -2.15 55.9, -0.08 54.12, 0.12 53.61, -0.27 53.74, -0.66 53.72, 0.05 52.91, 1.75 52.47, 0.42 51.47, 1.41 51.36, 0.96 50.93, -5.66 50.08, -4.19 51.19, -3.14 51.21, -2.43 51.74, -5.26 51.88)), ((-13.6 65.04, -18.65 63.41, -22.65 63.83, -21.59 64.63, -24.03 64.86, -21.84 65.45, -24.48 65.53, -22.44 65.91, -22.89 66.44, -21.13 65.27, -20.21 66.1, -14.7 66.34, -13.6 65.04)))"^^geo:wktLiteral ] .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/focal-stac-loader> dcterms:title "FOCAL STAC data loader, built into the workflow" ;
    rdfs:comment "The loader expects file paths whose names follow the FOCAL STAC convention and uses them to check that the tiles are complete and connected. The check could be weakened, at the cost of strict validation." ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/infrastructure> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/clms> dcterms:title "CLMS Tree Cover Density 2018 / Imperviousness Density 2024" ;
    focal-transf-prop:acceptanceCriteria [ rdfs:comment "Replaceable by a newer version or another raster, since only zonal statistics are computed; other climates may call for other layers. The same raster conventions as the LST datasets; the unit does not matter. Recommended, but today the workflow fails at the zonal statistics step without it; skipping the step is planned." ;
            focal-transf-prop:variable [ focal-transf-prop:variableName "band_data" ] ] ;
    focal-transf-prop:artifactRef "/inputs/clms_tcd_imd" ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/workflow-input> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/eur11-domain> focal-transf-prop:dimension <https://w3id.org/ogc/hosted/focal/transferability/dimensions/spatial> ;
    focal-transf-prop:role <https://w3id.org/ogc/hosted/focal/transferability/roles/valid-for> ;
    focal-transf-prop:value [ geo:asWKT "POLYGON((-22 27,45 27,45 72,-22 72,-22 27))"^^geo:wktLiteral ] .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/lst> dcterms:title "median summer LST datasets (FOCAL STAC, Landsat 5/7/8/9-derived)" ;
    focal-transf-prop:acceptanceCriteria [ rdfs:comment "A georeferenced raster that xarray or rasterio can open, with one value per grid cell, read from index 0 of a `band` dimension. Packed values are unpacked with the `scale_factor` and `add_offset` attributes when present; no-data is NaN unless `rio.nodata` says otherwise. The unit does not matter to the classification. Any CRS: inputs are reprojected to EPSG:3857 on import." ;
            focal-transf-prop:variable [ focal-transf-prop:variableName "band_data" ] ] ;
    focal-transf-prop:artifactRef "/inputs/lst_datasets" ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/workflow-input> .


```


### UP-WF1 — Regional climate change (a precomputed delivery, bounded by its domain)
A precomputed delivery: the transferable unit is the climate indices derived from the NUKLEUS
ensemble, not a re-executable package, so what bounds it is the domain and the timeslices that
were delivered.

**"Nothing" did not mean "valid anywhere".** The questionnaire answered the adaptation
question with "Nothing", which first read as no boundary and no rule. The owners' review
says otherwise: the results hold only for the delivered NUKLEUS/CEU-3 domain, and another area
needs new regional climate-model input and a recalculation of the indices. The record now
says that, as a `spatial` constraint and a rule over the ensemble artifact. Inside the domain
nothing needs rerunning for a user who only wants the delivered indices, which is the
closed-world default: no rule fires, so the artifact is reused.

**The domain is a rectangle because the grid is one.** CEU-3 is a regular rectangular grid;
the box is the one the project's STAC metadata gives, so it is approximate.

**The Global Warming Levels are named.** GWL2 and GWL3 are the delivered timeslices, so there
are two `scenarioMarker` constraints, `valid-for`, rather than calendar periods.

**Maturity is pre-operational**, not operational as first read from where the workflow runs:
validation and preparation of the products and metadata are still under way.

**Redistribution permission** is a separate matter (publication of the NUKLEUS dataset is
pending), kept in the statement's `transferabilityNotes` because no shape holds licensing
status. `inputs`/`outputs` ids are placeholders; `steps` is omitted: the transferable unit is the
delivered indices, and recreating them would need the climate-model inputs and the Python index
calculation, which no Application Package describes.

**A delivery, but not only a delivery.** The owners' 2 Nov answers describe seven Python
scripts in two stages (index production, then change signals, ensemble statistics and
robustness) that could be re-run on the same inputs. The owners confirmed (UP-WF1.1) that
`precomputed-delivery` is the right `computationType` for what is transferred today.
`SoftwareRequirement` lists the
dependencies they named; `steps` stays omitted because the scripts are not yet expressed as
CWL steps.

#### json
```json
{
  "class": "Workflow",
  "id": "",
  "cwlVersion": "v1.2",
  "label": "UP-WF1 — Regional climate change",
  "requirements": {
    "SoftwareRequirement": {
      "packages": [
        { "package": "python" }, { "package": "numpy" }, { "package": "pandas" },
        { "package": "xarray" }, { "package": "xclim" }, { "package": "dask" },
        { "package": "s3fs" }, { "package": "xESMF" }, { "package": "h5netcdf" }
      ]
    }
  },
  "inputs": { "nukleus_ensemble": { "type": "File" } },
  "outputs": { "climate_indices": { "type": "File" } },
  "transferability": {
    "trainingRequired": false,
    "envelope": [
      {
        "id": "ceu3-domain",
        "role": "valid-for",
        "dimension": "spatial",
        "value": { "asWKT": "POLYGON((1.6198 44.8502,18.2799 44.8502,18.2799 56.2362,1.6198 56.2362,1.6198 44.8502))" }
      },
      { "id": "gwl-2", "role": "valid-for", "dimension": "temporal", "value": { "scenarioMarker": "gwl-2.0" } },
      { "id": "gwl-3", "role": "valid-for", "dimension": "temporal", "value": { "scenarioMarker": "gwl-3.0" } }
    ],
    "artifacts": [
      {
        "id": "nukleus-ensemble",
        "artifact": "9-member NUKLEUS regional climate ensemble",
        "artifactRole": "workflow-input",
        "artifactRef": "/inputs/nukleus_ensemble"
      }
    ],
    "rules": [
      {
        "appliesTo": ["nukleus-ensemble"],
        "when": [{ "constraint": "ceu3-domain", "test": "outside" }],
        "actions": ["replace-with-local-equivalent"],
        "mandatory": true
      }
    ],
    "transferabilityNotes": "Redistribution is a separate permission issue: the NUKLEUS publication is pending. The localized climate data is part of the ensemble processing, not a separate input. Serving the delivered indices needs no rerun inside the domain; recreating them needs the climate-model inputs and the Python index calculation."
  },
  "computationType": "precomputed-delivery",
  "maturityStatus": "pre-operational",
  "qualityAnnotation": [
    {
      "dimension": "intended-use-limit",
      "note": "Results are derived from the nine-member NUKLEUS ensemble and apply only within the delivered spatial domain and the available historical and GWL timeslices; they depend on the climate-model inputs and the ensemble representation."
    }
  ]
}

```

#### jsonld
```jsonld
{
  "@context": "https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/workflow/context.jsonld",
  "class": "Workflow",
  "id": "",
  "cwlVersion": "v1.2",
  "label": "UP-WF1 \u2014 Regional climate change",
  "requirements": {
    "SoftwareRequirement": {
      "packages": [
        {
          "package": "python"
        },
        {
          "package": "numpy"
        },
        {
          "package": "pandas"
        },
        {
          "package": "xarray"
        },
        {
          "package": "xclim"
        },
        {
          "package": "dask"
        },
        {
          "package": "s3fs"
        },
        {
          "package": "xESMF"
        },
        {
          "package": "h5netcdf"
        }
      ]
    }
  },
  "inputs": {
    "nukleus_ensemble": {
      "type": "File"
    }
  },
  "outputs": {
    "climate_indices": {
      "type": "File"
    }
  },
  "transferability": {
    "trainingRequired": false,
    "envelope": [
      {
        "id": "ceu3-domain",
        "role": "valid-for",
        "dimension": "spatial",
        "value": {
          "asWKT": "POLYGON((1.6198 44.8502,18.2799 44.8502,18.2799 56.2362,1.6198 56.2362,1.6198 44.8502))"
        }
      },
      {
        "id": "gwl-2",
        "role": "valid-for",
        "dimension": "temporal",
        "value": {
          "scenarioMarker": "gwl-2.0"
        }
      },
      {
        "id": "gwl-3",
        "role": "valid-for",
        "dimension": "temporal",
        "value": {
          "scenarioMarker": "gwl-3.0"
        }
      }
    ],
    "artifacts": [
      {
        "id": "nukleus-ensemble",
        "artifact": "9-member NUKLEUS regional climate ensemble",
        "artifactRole": "workflow-input",
        "artifactRef": "/inputs/nukleus_ensemble"
      }
    ],
    "rules": [
      {
        "appliesTo": [
          "nukleus-ensemble"
        ],
        "when": [
          {
            "constraint": "ceu3-domain",
            "test": "outside"
          }
        ],
        "actions": [
          "replace-with-local-equivalent"
        ],
        "mandatory": true
      }
    ],
    "transferabilityNotes": "Redistribution is a separate permission issue: the NUKLEUS publication is pending. The localized climate data is part of the ensemble processing, not a separate input. Serving the delivered indices needs no rerun inside the domain; recreating them needs the climate-model inputs and the Python index calculation."
  },
  "computationType": "precomputed-delivery",
  "maturityStatus": "pre-operational",
  "qualityAnnotation": [
    {
      "dimension": "intended-use-limit",
      "note": "Results are derived from the nine-member NUKLEUS ensemble and apply only within the delivered spatial domain and the available historical and GWL timeslices; they depend on the climate-model inputs and the ensemble representation."
    }
  ]
}
```

#### ttl
```ttl
@prefix cwl: <https://w3id.org/cwl/cwl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix dqv: <http://www.w3.org/ns/dqv#> .
@prefix focal-transf-prop: <https://w3id.org/ogc/hosted/focal/transferability/properties/> .
@prefix geo: <http://www.opengis.net/ont/geosparql#> .
@prefix ns1: <https://w3id.org/cwl/cwl#SoftwarePackage/> .
@prefix ns2: <https://w3id.org/cwl/cwl#SoftwareRequirement/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix sld: <https://w3id.org/cwl/salad#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf1/> a cwl:Workflow ;
    rdfs:label "UP-WF1 — Regional climate change" ;
    cwl:inputs <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf1/nukleus_ensemble> ;
    cwl:outputs <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf1/climate_indices> ;
    cwl:requirements [ a cwl:SoftwareRequirement ;
            ns2:packages [ ns1:package "s3fs" ],
                [ ns1:package "dask" ],
                [ ns1:package "xarray" ],
                [ ns1:package "pandas" ],
                [ ns1:package "h5netcdf" ],
                [ ns1:package "xclim" ],
                [ ns1:package "python" ],
                [ ns1:package "xESMF" ],
                [ ns1:package "numpy" ] ] ;
    focal-transf-prop:computationType <https://w3id.org/ogc/hosted/focal/transferability/computation-types/precomputed-delivery> ;
    focal-transf-prop:maturityStatus <https://w3id.org/ogc/hosted/focal/transferability/maturity-statuses/pre-operational> ;
    focal-transf-prop:qualityAnnotation [ dqv:inDimension <https://w3id.org/ogc/hosted/focal/transferability/quality-dimensions/intended-use-limit> ;
            focal-transf-prop:note "Results are derived from the nine-member NUKLEUS ensemble and apply only within the delivered spatial domain and the available historical and GWL timeslices; they depend on the climate-model inputs and the ensemble representation." ] ;
    focal-transf-prop:transferability [ rdfs:comment "Redistribution is a separate permission issue: the NUKLEUS publication is pending. The localized climate data is part of the ensemble processing, not a separate input. Serving the delivered indices needs no rerun inside the domain; recreating them needs the climate-model inputs and the Python index calculation." ;
            focal-transf-prop:artifacts <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf1/nukleus-ensemble> ;
            focal-transf-prop:envelope <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf1/ceu3-domain>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf1/gwl-2>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf1/gwl-3> ;
            focal-transf-prop:rules [ focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/replace-with-local-equivalent> ;
                    focal-transf-prop:appliesTo <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf1/nukleus-ensemble> ;
                    focal-transf-prop:mandatory true ;
                    focal-transf-prop:when [ focal-transf-prop:constraint <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf1/ceu3-domain> ;
                            focal-transf-prop:test <https://w3id.org/ogc/hosted/focal/transferability/tests/outside> ] ] ;
            focal-transf-prop:trainingRequired false ] .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf1/climate_indices> sld:type cwl:File .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf1/gwl-2> focal-transf-prop:dimension <https://w3id.org/ogc/hosted/focal/transferability/dimensions/temporal> ;
    focal-transf-prop:role <https://w3id.org/ogc/hosted/focal/transferability/roles/valid-for> ;
    focal-transf-prop:value [ focal-transf-prop:scenarioMarker <https://w3id.org/ogc/hosted/focal/transferability/scenario-markers/gwl-2.0> ] .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf1/gwl-3> focal-transf-prop:dimension <https://w3id.org/ogc/hosted/focal/transferability/dimensions/temporal> ;
    focal-transf-prop:role <https://w3id.org/ogc/hosted/focal/transferability/roles/valid-for> ;
    focal-transf-prop:value [ focal-transf-prop:scenarioMarker <https://w3id.org/ogc/hosted/focal/transferability/scenario-markers/gwl-3.0> ] .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf1/nukleus_ensemble> sld:type cwl:File .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf1/ceu3-domain> focal-transf-prop:dimension <https://w3id.org/ogc/hosted/focal/transferability/dimensions/spatial> ;
    focal-transf-prop:role <https://w3id.org/ogc/hosted/focal/transferability/roles/valid-for> ;
    focal-transf-prop:value [ geo:asWKT "POLYGON((1.6198 44.8502,18.2799 44.8502,18.2799 56.2362,1.6198 56.2362,1.6198 44.8502))"^^geo:wktLiteral ] .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf1/nukleus-ensemble> dcterms:title "9-member NUKLEUS regional climate ensemble" ;
    focal-transf-prop:artifactRef "/inputs/nukleus_ensemble" ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/workflow-input> .


```


### FP-WF5 — Climate zones inspired by Quitt (value ranges with a degraded zone)
The limit of this classification is climatic, not geographic: two `climatic` value-range constraints separate a good fit from a degraded one and from outside, each with its own rule. Converted from the owners' record of 2026-11-18; the rule on the degraded zone and the input declarations are pending the owners' confirmation.

#### json
```json
{
  "class": "Workflow",
  "cwlVersion": "v1.2",
  "id": "",
  "label": "FWF5 - Climate zones inspired by Quitt's classification (FOCAL Forest Pilot)",
  "doc": [
    "Assigns each location one of 23 climate units (coldest CH1 to warmest T5): the unit whose Quitt limits best match 11 multi-year mean climate characteristics. Reports trends of the characteristics and of the unit.",
    "Transferability record of workflow FP-WF5 (FWF5), record date 2026-11-18. Record basis: FWF5 code package (API, scoring, trends, Rasdaman registry, source catalogue, Quitt limit table) and the published methodology; not the round-1 questionnaire. Methodology: https://github.com/JiriVales/info4forest-backend/blob/main/methodology_climate_zones_quitt_en_updated.md Converted from the delivered record on 2026-11-25. Descriptive CWL profile: no steps are declared and the input and output identifiers are not yet those of an executable Application Package."
  ],
  "$namespaces": {
    "s": "https://schema.org/"
  },
  "s:identifier": "FP-WF5",
  "s:alternateName": "FWF5",
  "s:dateCreated": "2026-11-18",
  "s:citation": "https://github.com/JiriVales/info4forest-backend/blob/main/methodology_climate_zones_quitt_en_updated.md",
  "requirements": {
    "SoftwareRequirement": {
      "packages": [
        {
          "package": "python"
        },
        {
          "package": "numpy"
        },
        {
          "package": "flask"
        },
        {
          "package": "gunicorn"
        }
      ]
    },
    "NetworkAccess": {
      "networkAccess": true
    }
  },
  "inputs": {
    "latitude": {
      "type": "double?",
      "label": "Latitude of the point",
      "doc": "Latitude in decimal degrees (WGS 84). Give latitude and longitude for a point, or bbox for an area."
    },
    "longitude": {
      "type": "double?",
      "label": "Longitude of the point",
      "doc": "Longitude in decimal degrees (WGS 84). Give together with latitude."
    },
    "bbox": {
      "type": "double[]?",
      "label": "Area of interest (bounding box)",
      "doc": "Area as [minimum longitude, minimum latitude, maximum longitude, maximum latitude] in decimal degrees (WGS 84). Alternative to latitude and longitude."
    },
    "start_year": {
      "type": "int",
      "label": "First year of the period",
      "doc": "First year of the period over which the indicators are averaged; it must be within the years of the data."
    },
    "end_year": {
      "type": "int",
      "label": "Last year of the period",
      "doc": "Last year of the period; it must be within the years of the data. Trends need at least 2 years."
    },
    "rasdaman_connection": {
      "type": "string",
      "label": "Data cube connection",
      "doc": "How to reach the Rasdaman instance that holds the climate data (queried with rasql over SSH). The connection variables are not named in the delivered material, so one string stands for them; we assume credentials are supplied by the execution environment."
    },
    "rasdaman_registry": {
      "type": "File",
      "label": "Data cube registry",
      "doc": "rasdaman_registry.json for that instance. The FOCAL registry is not transferable as is."
    },
    "climate_source_catalogue": {
      "type": "File",
      "label": "Climate source catalogue",
      "doc": "climate_source_catalog.json listing the sources and areas offered."
    },
    "readiness_collection": {
      "type": "string?",
      "label": "Readiness check collection",
      "doc": "Value for READINESS_COLLECTION, which defaults to a Czech ERA5-Land collection. Outside that default it must be set, otherwise the readiness check fails."
    },
    "quitt_limit_table": {
      "type": "File",
      "label": "Climate unit limit table",
      "doc": "Intervals of the 11 indicators for 23 climate units (Quitt 1971, Table 2). Ships with the workflow; replace it with a regional table for climates unlike Central Europe.",
      "default": {
        "class": "File",
        "location": "FWF5_quitt_limits_11_rasdaman_index.json"
      }
    },
    "unit_descriptions": {
      "type": "File",
      "label": "Climate unit descriptions",
      "doc": "Names and descriptions of the units (Czech and English). Ships with the workflow.",
      "default": {
        "class": "File",
        "location": "FWF5_climate_metadata.json"
      }
    }
  },
  "outputs": {
    "climate_unit": {
      "type": "File",
      "label": "Climate unit",
      "doc": "Unit map and point detail: unit, fit score best_score and indicator means."
    },
    "climate_unit_trend": {
      "type": "File",
      "label": "Climate unit trend",
      "doc": "Trend of the climate unit (yearly expected fuzzy rank)."
    },
    "indicator_maps": {
      "type": "File",
      "label": "Climate characteristic maps",
      "doc": "Maps of the 11 climate characteristics."
    },
    "indicator_trends": {
      "type": "File",
      "label": "Climate characteristic trends",
      "doc": "Sen's slope and Mann-Kendall test (alpha = 0.05) per indicator."
    },
    "adverse_episode": {
      "type": "File",
      "label": "Adverse episode",
      "doc": "Adverse episode derived from the trends."
    }
  },
  "steps": {},
  "transferability": {
    "trainingRequired": false,
    "transferabilityNotes": "Envelope entries and rules that only described which data FOCAL currently holds, or its platform, are not part of this statement; what they said is kept in the notes of the artifacts concerned. An area or period for which no data is at hand is a matter of providing data (as delivered, in the data cube) that meets the artifact's criteria. The delivered record also notes: temporal extent is the year range of each collection, read from Rasdaman at runtime. The 11 climate characteristics and their trends are valid everywhere; only the climate-unit outputs are bounded, by climate rather than geography.",
    "envelope": [
      {
        "id": "quitt-limits-origin",
        "role": "derived-from",
        "dimension": "spatial",
        "value": {
          "asWKT": "POLYGON((12.07 47.63, 22.76 47.63, 22.76 51.08, 12.07 51.08, 12.07 47.63))"
        },
        "transferabilityNotes": "Bounding box of the FOCAL Czechia and Slovakia areas, standing in for former Czechoslovakia, for which Quitt (1971) derived the limit table. The limits were taken over, not fitted by FOCAL."
      },
      {
        "id": "quitt-climate-covered",
        "role": "valid-for",
        "dimension": "climatic",
        "value": {
          "variables": [
            {
              "name": "SUM25",
              "unit": "days",
              "min": 0,
              "max": 70
            },
            {
              "name": "VEG10",
              "unit": "days",
              "min": 0
            },
            {
              "name": "FROST0",
              "unit": "days",
              "min": 90,
              "max": 180
            },
            {
              "name": "ICE0",
              "unit": "days",
              "min": 0,
              "max": 80
            },
            {
              "name": "T_JAN",
              "unit": "degC",
              "min": -8,
              "max": -1
            },
            {
              "name": "T_APR",
              "unit": "degC",
              "min": 0,
              "max": 10
            },
            {
              "name": "T_JUL",
              "unit": "degC",
              "min": 10,
              "max": 20
            },
            {
              "name": "T_OCT",
              "unit": "degC",
              "min": 2,
              "max": 10
            },
            {
              "name": "RAIN1",
              "unit": "days",
              "min": 80,
              "max": 160
            },
            {
              "name": "P_APR_SEP",
              "unit": "mm",
              "min": 300,
              "max": 1000
            },
            {
              "name": "P_OCT_MAR",
              "unit": "mm",
              "min": 200,
              "max": 700
            }
          ],
          "statistic": "multi-year mean"
        },
        "inputRef": [
          "/inputs/latitude",
          "/inputs/longitude",
          "/inputs/bbox",
          "/inputs/start_year",
          "/inputs/end_year"
        ],
        "transferabilityNotes": "'covered' ranges: every multi-year indicator mean inside them. Union of the 23 unit intervals in FWF5_quitt_limits_11_rasdaman_index.json; 'outer' adds the fuzzy tolerances used in the code (10 days, 1 degC, 50 mm). Applies to the climate-unit outputs only; the 11 characteristics and their trends are valid everywhere. Applies in time as well as space: future SSP3-7.0 values in Czech lowlands are expected to approach or exceed the warm edge. Delivered reading: every multi-year indicator mean lies inside 'covered'; between 'covered' and 'outer' = degraded fit; beyond 'outer' = outside."
      },
      {
        "id": "quitt-climate-outer",
        "role": "valid-for",
        "dimension": "climatic",
        "value": {
          "variables": [
            {
              "name": "SUM25",
              "unit": "days",
              "max": 80
            },
            {
              "name": "FROST0",
              "unit": "days",
              "min": 80,
              "max": 190
            },
            {
              "name": "ICE0",
              "unit": "days",
              "max": 90
            },
            {
              "name": "T_JAN",
              "unit": "degC",
              "min": -9,
              "max": 0
            },
            {
              "name": "T_APR",
              "unit": "degC",
              "min": -1,
              "max": 11
            },
            {
              "name": "T_JUL",
              "unit": "degC",
              "min": 9,
              "max": 21
            },
            {
              "name": "T_OCT",
              "unit": "degC",
              "min": 1,
              "max": 11
            },
            {
              "name": "RAIN1",
              "unit": "days",
              "min": 70,
              "max": 170
            },
            {
              "name": "P_APR_SEP",
              "unit": "mm",
              "min": 250,
              "max": 1050
            },
            {
              "name": "P_OCT_MAR",
              "unit": "mm",
              "min": 150,
              "max": 750
            }
          ],
          "statistic": "multi-year mean"
        },
        "inputRef": [
          "/inputs/latitude",
          "/inputs/longitude",
          "/inputs/bbox",
          "/inputs/start_year",
          "/inputs/end_year"
        ],
        "transferabilityNotes": "'outer' ranges: covered ranges plus the fuzzy tolerances; a mean beyond them gets zero membership for that indicator in every unit. VEG10 has no outer limit and is not listed. Union of the 23 unit intervals in FWF5_quitt_limits_11_rasdaman_index.json; 'outer' adds the fuzzy tolerances used in the code (10 days, 1 degC, 50 mm). Applies to the climate-unit outputs only; the 11 characteristics and their trends are valid everywhere. Applies in time as well as space: future SSP3-7.0 values in Czech lowlands are expected to approach or exceed the warm edge. Delivered reading: every multi-year indicator mean lies inside 'covered'; between 'covered' and 'outer' = degraded fit; beyond 'outer' = outside."
      }
    ],
    "artifacts": [
      {
        "id": "yearly-indicators",
        "artifact": "Yearly climate indicators (11 characteristics) covering the requested period",
        "artifactRole": "workflow-input",
        "acceptanceCriteria": {
          "variables": [
            {
              "name": "SUM25",
              "units": [
                "DAY"
              ]
            },
            {
              "name": "VEG10",
              "units": [
                "DAY"
              ]
            },
            {
              "name": "FROST0",
              "units": [
                "DAY"
              ]
            },
            {
              "name": "ICE0",
              "units": [
                "DAY"
              ]
            },
            {
              "name": "T_JAN",
              "units": [
                "DEG_C"
              ]
            },
            {
              "name": "T_APR",
              "units": [
                "DEG_C"
              ]
            },
            {
              "name": "T_JUL",
              "units": [
                "DEG_C"
              ]
            },
            {
              "name": "T_OCT",
              "units": [
                "DEG_C"
              ]
            },
            {
              "name": "RAIN1",
              "units": [
                "DAY"
              ]
            },
            {
              "name": "P_APR_SEP",
              "units": [
                "MilliM"
              ]
            },
            {
              "name": "P_OCT_MAR",
              "units": [
                "MilliM"
              ]
            }
          ],
          "temporal": {
            "resolution": "P1Y",
            "complete": true
          },
          "axes": [
            "time"
          ],
          "gridTypes": [
            "regular-latlon",
            "rotated-pole"
          ],
          "transferabilityNotes": "Structure: 4D array [year, ind, y, x], float32, NaN as no-data, indicators in the fixed order SUM25, VEG10, FROST0, ICE0, T_JAN, T_APR, T_JUL, T_OCT, RAIN1, P_APR_SEP, P_OCT_MAR. Time axis: calendar year (integer); every year of a requested period present. 2D latitude/longitude of cell centres (lookup collections or separable 1D axes); EPSG:4326 for lookups. Definitions: SUM25 = count(Tmax >= 25 degC); VEG10 = count(Tavg >= 10 degC); FROST0 = count(Tmin < 0 degC); ICE0 = count(Tmax < 0 degC); T_JAN = mean(Tavg, Jan); T_APR = mean(Tavg, Apr); T_JUL = mean(Tavg, Jul); T_OCT = mean(Tavg, Oct); RAIN1 = count(P >= 1 mm); P_APR_SEP = sum(P, Apr-Sep); P_OCT_MAR = sum(P, Oct-Mar)."
        },
        "transferabilityNotes": "As delivered, the workflow does not take these data as a file: it reads them from the Rasdaman data cube (artifact rasdaman), for the requested area and the years it needs. The delivered material gives no specification of the layout the code expects. Delivered as two datasets with the same requirements. (1) Historical: ERA5-Land yearly climate indicators (Rasdaman collection era5l_cz_yindicators). Needed only for historical periods. Within FOCAL: ERA5-Land is held for Czechia, Spain and Finland (exact extents per collection); any other area is computed in a routine precompute run. Outside FOCAL: ERA5-Land from the Copernicus Climate Data Store, E-OBS, or national gridded observations. (2) Projections: CMIP6-CORDEX EUR-11 GERICS-REMO2020 (MPI-ESM1-2-HR, EC-Earth3-Veg, MIROC6), SSP3-7.0, r1i1p1f1 yearly climate indicators (Rasdaman collections *_eur11_yindicators_<area>); SSP3-7.0 only, no historical experiment. Within FOCAL: precomputed for these bounding boxes (data coverage, not administrative boundaries): Czechia 12.07-18.97 E, 48.48-51.08 N; Slovakia 16.8174-22.7629 E, 47.6296-49.705 N; Spain (Maestrazgo Mountains) -1.09395-0.297912 E, 39.8289-40.8966 N; Southern Finland 20.3719-32.7637 E, 58.9769-63.1035 N. Elsewhere in the EUR-11 domain, a routine precompute run from the daily EUR-11 collections already held (started manually, no code change), then add the new collections and area entries. If no indicators exist, derive them from daily minimum, average and maximum temperature and precipitation (see artifact daily-climate) with the definitions above; that step runs in FOCAL ingest tooling and is not part of the FWF5 package. Seasonal windows assume the Northern Hemisphere. Used by (delivered step names): indicator-means, idw, climate-unit-classification, characteristic-trends, climate-unit-trend."
      },
      {
        "id": "daily-climate",
        "artifact": "Daily Tmin, Tavg, Tmax and precipitation from which the yearly indicators are derived (ERA5-Land hourly t2m/tp aggregated to daily; CORDEX daily tasmin/tas/tasmax/pr)",
        "artifactRole": "external-resource",
        "acceptanceCriteria": {
          "variables": [
            {
              "name": "tasmin",
              "units": [
                "DEG_C"
              ],
              "standardName": "air_temperature"
            },
            {
              "name": "tas",
              "units": [
                "DEG_C"
              ],
              "standardName": "air_temperature"
            },
            {
              "name": "tasmax",
              "units": [
                "DEG_C"
              ],
              "standardName": "air_temperature"
            },
            {
              "name": "pr",
              "units": [
                "MilliM-PER-DAY"
              ]
            }
          ],
          "temporal": {
            "resolution": "P1D",
            "calendar": [
              "standard",
              "proleptic_gregorian",
              "noleap"
            ]
          },
          "axes": [
            "time"
          ],
          "gridTypes": [
            "regular-latlon",
            "rotated-pole"
          ],
          "transferabilityNotes": "360_day calendars bias the day-count indicators and need adjustment."
        },
        "transferabilityNotes": "Not read by the workflow: upstream source of the yearly indicators. The precompute step runs in FOCAL ingest tooling and is not part of the FWF5 package. Within FOCAL: daily tas, tasmin, tasmax and pr of the three REMO2020 simulations are held for the whole EUR-11 rotated grid, 412 x 424 cells (lon/lat bounding box 44.5939 W - 64.9644 E, 21.9878 - 72.585 N; the box overstates the rotated domain at its corners); FWF5 runs anywhere inside it after the yearly indicators are precomputed for the area. Outside that domain: another CORDEX domain or another daily climate dataset meeting these criteria. Used by (delivered step names): yearly-indicator-precompute."
      },
      {
        "id": "quitt-limit-table",
        "artifact": "FWF5_quitt_limits_11_rasdaman_index.json: intervals of 11 indicators for 23 units (Quitt 1971, Table 2)",
        "artifactRole": "workflow-input",
        "artifactRef": "/inputs/quitt_limit_table",
        "transferabilityNotes": "A regional table needs: the same 11 indicator codes, units and axis mapping; [min, max] per unit and indicator, null allowed for an open end; and a full cold-to-warm ordering of units (used for tie-breaking and the unit trend). The limits were derived for former Czechoslovakia. Used by (delivered step names): climate-unit-classification, climate-unit-trend.",
        "acceptanceCriteria": {
          "variables": [
            {
              "name": "SUM25",
              "units": [
                "DAY"
              ]
            },
            {
              "name": "VEG10",
              "units": [
                "DAY"
              ]
            },
            {
              "name": "FROST0",
              "units": [
                "DAY"
              ]
            },
            {
              "name": "ICE0",
              "units": [
                "DAY"
              ]
            },
            {
              "name": "T_JAN",
              "units": [
                "DEG_C"
              ]
            },
            {
              "name": "T_APR",
              "units": [
                "DEG_C"
              ]
            },
            {
              "name": "T_JUL",
              "units": [
                "DEG_C"
              ]
            },
            {
              "name": "T_OCT",
              "units": [
                "DEG_C"
              ]
            },
            {
              "name": "RAIN1",
              "units": [
                "DAY"
              ]
            },
            {
              "name": "P_APR_SEP",
              "units": [
                "MilliM"
              ]
            },
            {
              "name": "P_OCT_MAR",
              "units": [
                "MilliM"
              ]
            }
          ]
        }
      },
      {
        "id": "unit-descriptions",
        "artifact": "FWF5_climate_metadata.json: unit names and descriptions (CZ/EN)",
        "artifactRole": "workflow-input",
        "artifactRef": "/inputs/unit_descriptions",
        "transferabilityNotes": "Names and descriptions for every unit of the limit table in use. The wording reflects Central European seasons and mentions snow cover and cloudiness, which are not computed. Used by (delivered step names): output-labelling."
      },
      {
        "id": "rasdaman",
        "artifact": "FOCAL Rasdaman data cube (rasql over SSH), source catalogue and registry (climate_source_catalog.json, rasdaman_registry.json)",
        "artifactRole": "infrastructure",
        "artifactRef": [
          "/inputs/rasdaman_connection",
          "/inputs/rasdaman_registry",
          "/inputs/climate_source_catalogue",
          "/inputs/readiness_collection"
        ],
        "transferabilityNotes": "The delivered workflow reads precomputed indicator collections from a Rasdaman instance queried with rasql over SSH. Another platform needs a Rasdaman instance with the same collection layout (set the connection variables and READINESS_COLLECTION) and its own registry, or replacement of the rasql data access by file-based reading; the scoring, IDW and trend modules use NumPy only. Within FOCAL: add the new collections and area entries. Outside FOCAL: the operator's own registry. Used by (delivered step names): data-access."
      }
    ],
    "rules": [
      {
        "appliesTo": [
          "quitt-limit-table"
        ],
        "when": [
          {
            "constraint": "quitt-climate-outer",
            "test": "outside"
          }
        ],
        "affects": [
          "/outputs/climate_unit",
          "/outputs/climate_unit_trend"
        ],
        "actions": [
          "replace-with-local-equivalent"
        ],
        "mandatory": true,
        "transferabilityNotes": "Without a regional table the steps still execute but return only the nearest Central European analogue with a low best_score. Characteristic outputs and trends are unaffected."
      },
      {
        "appliesTo": [
          "unit-descriptions"
        ],
        "when": [
          {
            "constraint": "quitt-climate-outer",
            "test": "outside"
          }
        ],
        "actions": [
          "replace-with-local-equivalent"
        ],
        "mandatory": false,
        "transferabilityNotes": "Follows a replaced limit table. If not replaced, unit names and descriptions do not describe the climate of the target."
      },
      {
        "appliesTo": [
          "quitt-limit-table"
        ],
        "when": [
          {
            "constraint": "quitt-climate-covered",
            "test": "outside"
          }
        ],
        "affects": [
          "/outputs/climate_unit",
          "/outputs/climate_unit_trend"
        ],
        "actions": [
          "replace-with-local-equivalent"
        ],
        "mandatory": false,
        "transferabilityNotes": "Degraded fit: an indicator mean outside 'covered' but within 'outer' still counts towards a unit with reduced membership, so the assigned unit can be trusted less. Characteristic outputs and trends are unaffected."
      },
      {
        "appliesTo": [
          "rasdaman"
        ],
        "triggeredBy": "service-unavailable",
        "actions": [
          "replace-with-local-equivalent"
        ],
        "mandatory": true,
        "transferabilityNotes": "Applies where no Rasdaman instance is available to the workflow: set one up with the same layout and its own registry, or change the code that reads the data (see the rasdaman artifact). On the FOCAL instance, a missing area is instead added as new collections and entries."
      }
    ]
  },
  "computationType": "deterministic-rule-based",
  "maturityStatus": "operational",
  "qualityAnnotation": [
    {
      "dimension": "method-limitation",
      "note": "best_score (0-1) is a similarity to interval limits, not a probability."
    },
    {
      "dimension": "method-limitation",
      "note": "The classification always returns a unit, even outside the climate envelope; a low best_score is the only signal."
    },
    {
      "dimension": "method-limitation",
      "note": "11 of Quitt's 14 characteristics are used; snow cover, cloudiness and clear/overcast days are omitted."
    },
    {
      "dimension": "method-limitation",
      "note": "10 km (ERA5-Land) and 12.5 km (EUR-11) cells; IDW smooths but adds no detail or elevation information."
    },
    {
      "dimension": "method-limitation",
      "note": "Projections: one RCM (REMO2020) driven by three GCMs under one scenario (SSP3-7.0); not year-specific forecasts."
    },
    {
      "dimension": "method-limitation",
      "note": "Default adverse directions reflect a warming/drying stress view; overridable per request."
    },
    {
      "dimension": "decision-support-only",
      "note": "Not a substitute for local measurement, site assessment or operational forecasting."
    }
  ]
}

```

#### jsonld
```jsonld
{
  "@context": "https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/workflow/context.jsonld",
  "class": "Workflow",
  "cwlVersion": "v1.2",
  "id": "",
  "label": "FWF5 - Climate zones inspired by Quitt's classification (FOCAL Forest Pilot)",
  "doc": [
    "Assigns each location one of 23 climate units (coldest CH1 to warmest T5): the unit whose Quitt limits best match 11 multi-year mean climate characteristics. Reports trends of the characteristics and of the unit.",
    "Transferability record of workflow FP-WF5 (FWF5), record date 2026-11-18. Record basis: FWF5 code package (API, scoring, trends, Rasdaman registry, source catalogue, Quitt limit table) and the published methodology; not the round-1 questionnaire. Methodology: https://github.com/JiriVales/info4forest-backend/blob/main/methodology_climate_zones_quitt_en_updated.md Converted from the delivered record on 2026-11-25. Descriptive CWL profile: no steps are declared and the input and output identifiers are not yet those of an executable Application Package."
  ],
  "$namespaces": {
    "s": "https://schema.org/"
  },
  "s:identifier": "FP-WF5",
  "s:alternateName": "FWF5",
  "s:dateCreated": "2026-11-18",
  "s:citation": "https://github.com/JiriVales/info4forest-backend/blob/main/methodology_climate_zones_quitt_en_updated.md",
  "requirements": {
    "SoftwareRequirement": {
      "packages": [
        {
          "package": "python"
        },
        {
          "package": "numpy"
        },
        {
          "package": "flask"
        },
        {
          "package": "gunicorn"
        }
      ]
    },
    "NetworkAccess": {
      "networkAccess": true
    }
  },
  "inputs": {
    "latitude": {
      "type": "double?",
      "label": "Latitude of the point",
      "doc": "Latitude in decimal degrees (WGS 84). Give latitude and longitude for a point, or bbox for an area."
    },
    "longitude": {
      "type": "double?",
      "label": "Longitude of the point",
      "doc": "Longitude in decimal degrees (WGS 84). Give together with latitude."
    },
    "bbox": {
      "type": "double[]?",
      "label": "Area of interest (bounding box)",
      "doc": "Area as [minimum longitude, minimum latitude, maximum longitude, maximum latitude] in decimal degrees (WGS 84). Alternative to latitude and longitude."
    },
    "start_year": {
      "type": "int",
      "label": "First year of the period",
      "doc": "First year of the period over which the indicators are averaged; it must be within the years of the data."
    },
    "end_year": {
      "type": "int",
      "label": "Last year of the period",
      "doc": "Last year of the period; it must be within the years of the data. Trends need at least 2 years."
    },
    "rasdaman_connection": {
      "type": "string",
      "label": "Data cube connection",
      "doc": "How to reach the Rasdaman instance that holds the climate data (queried with rasql over SSH). The connection variables are not named in the delivered material, so one string stands for them; we assume credentials are supplied by the execution environment."
    },
    "rasdaman_registry": {
      "type": "File",
      "label": "Data cube registry",
      "doc": "rasdaman_registry.json for that instance. The FOCAL registry is not transferable as is."
    },
    "climate_source_catalogue": {
      "type": "File",
      "label": "Climate source catalogue",
      "doc": "climate_source_catalog.json listing the sources and areas offered."
    },
    "readiness_collection": {
      "type": "string?",
      "label": "Readiness check collection",
      "doc": "Value for READINESS_COLLECTION, which defaults to a Czech ERA5-Land collection. Outside that default it must be set, otherwise the readiness check fails."
    },
    "quitt_limit_table": {
      "type": "File",
      "label": "Climate unit limit table",
      "doc": "Intervals of the 11 indicators for 23 climate units (Quitt 1971, Table 2). Ships with the workflow; replace it with a regional table for climates unlike Central Europe.",
      "default": {
        "class": "File",
        "location": "FWF5_quitt_limits_11_rasdaman_index.json"
      }
    },
    "unit_descriptions": {
      "type": "File",
      "label": "Climate unit descriptions",
      "doc": "Names and descriptions of the units (Czech and English). Ships with the workflow.",
      "default": {
        "class": "File",
        "location": "FWF5_climate_metadata.json"
      }
    }
  },
  "outputs": {
    "climate_unit": {
      "type": "File",
      "label": "Climate unit",
      "doc": "Unit map and point detail: unit, fit score best_score and indicator means."
    },
    "climate_unit_trend": {
      "type": "File",
      "label": "Climate unit trend",
      "doc": "Trend of the climate unit (yearly expected fuzzy rank)."
    },
    "indicator_maps": {
      "type": "File",
      "label": "Climate characteristic maps",
      "doc": "Maps of the 11 climate characteristics."
    },
    "indicator_trends": {
      "type": "File",
      "label": "Climate characteristic trends",
      "doc": "Sen's slope and Mann-Kendall test (alpha = 0.05) per indicator."
    },
    "adverse_episode": {
      "type": "File",
      "label": "Adverse episode",
      "doc": "Adverse episode derived from the trends."
    }
  },
  "steps": {},
  "transferability": {
    "trainingRequired": false,
    "transferabilityNotes": "Envelope entries and rules that only described which data FOCAL currently holds, or its platform, are not part of this statement; what they said is kept in the notes of the artifacts concerned. An area or period for which no data is at hand is a matter of providing data (as delivered, in the data cube) that meets the artifact's criteria. The delivered record also notes: temporal extent is the year range of each collection, read from Rasdaman at runtime. The 11 climate characteristics and their trends are valid everywhere; only the climate-unit outputs are bounded, by climate rather than geography.",
    "envelope": [
      {
        "id": "quitt-limits-origin",
        "role": "derived-from",
        "dimension": "spatial",
        "value": {
          "asWKT": "POLYGON((12.07 47.63, 22.76 47.63, 22.76 51.08, 12.07 51.08, 12.07 47.63))"
        },
        "transferabilityNotes": "Bounding box of the FOCAL Czechia and Slovakia areas, standing in for former Czechoslovakia, for which Quitt (1971) derived the limit table. The limits were taken over, not fitted by FOCAL."
      },
      {
        "id": "quitt-climate-covered",
        "role": "valid-for",
        "dimension": "climatic",
        "value": {
          "variables": [
            {
              "name": "SUM25",
              "unit": "days",
              "min": 0,
              "max": 70
            },
            {
              "name": "VEG10",
              "unit": "days",
              "min": 0
            },
            {
              "name": "FROST0",
              "unit": "days",
              "min": 90,
              "max": 180
            },
            {
              "name": "ICE0",
              "unit": "days",
              "min": 0,
              "max": 80
            },
            {
              "name": "T_JAN",
              "unit": "degC",
              "min": -8,
              "max": -1
            },
            {
              "name": "T_APR",
              "unit": "degC",
              "min": 0,
              "max": 10
            },
            {
              "name": "T_JUL",
              "unit": "degC",
              "min": 10,
              "max": 20
            },
            {
              "name": "T_OCT",
              "unit": "degC",
              "min": 2,
              "max": 10
            },
            {
              "name": "RAIN1",
              "unit": "days",
              "min": 80,
              "max": 160
            },
            {
              "name": "P_APR_SEP",
              "unit": "mm",
              "min": 300,
              "max": 1000
            },
            {
              "name": "P_OCT_MAR",
              "unit": "mm",
              "min": 200,
              "max": 700
            }
          ],
          "statistic": "multi-year mean"
        },
        "inputRef": [
          "/inputs/latitude",
          "/inputs/longitude",
          "/inputs/bbox",
          "/inputs/start_year",
          "/inputs/end_year"
        ],
        "transferabilityNotes": "'covered' ranges: every multi-year indicator mean inside them. Union of the 23 unit intervals in FWF5_quitt_limits_11_rasdaman_index.json; 'outer' adds the fuzzy tolerances used in the code (10 days, 1 degC, 50 mm). Applies to the climate-unit outputs only; the 11 characteristics and their trends are valid everywhere. Applies in time as well as space: future SSP3-7.0 values in Czech lowlands are expected to approach or exceed the warm edge. Delivered reading: every multi-year indicator mean lies inside 'covered'; between 'covered' and 'outer' = degraded fit; beyond 'outer' = outside."
      },
      {
        "id": "quitt-climate-outer",
        "role": "valid-for",
        "dimension": "climatic",
        "value": {
          "variables": [
            {
              "name": "SUM25",
              "unit": "days",
              "max": 80
            },
            {
              "name": "FROST0",
              "unit": "days",
              "min": 80,
              "max": 190
            },
            {
              "name": "ICE0",
              "unit": "days",
              "max": 90
            },
            {
              "name": "T_JAN",
              "unit": "degC",
              "min": -9,
              "max": 0
            },
            {
              "name": "T_APR",
              "unit": "degC",
              "min": -1,
              "max": 11
            },
            {
              "name": "T_JUL",
              "unit": "degC",
              "min": 9,
              "max": 21
            },
            {
              "name": "T_OCT",
              "unit": "degC",
              "min": 1,
              "max": 11
            },
            {
              "name": "RAIN1",
              "unit": "days",
              "min": 70,
              "max": 170
            },
            {
              "name": "P_APR_SEP",
              "unit": "mm",
              "min": 250,
              "max": 1050
            },
            {
              "name": "P_OCT_MAR",
              "unit": "mm",
              "min": 150,
              "max": 750
            }
          ],
          "statistic": "multi-year mean"
        },
        "inputRef": [
          "/inputs/latitude",
          "/inputs/longitude",
          "/inputs/bbox",
          "/inputs/start_year",
          "/inputs/end_year"
        ],
        "transferabilityNotes": "'outer' ranges: covered ranges plus the fuzzy tolerances; a mean beyond them gets zero membership for that indicator in every unit. VEG10 has no outer limit and is not listed. Union of the 23 unit intervals in FWF5_quitt_limits_11_rasdaman_index.json; 'outer' adds the fuzzy tolerances used in the code (10 days, 1 degC, 50 mm). Applies to the climate-unit outputs only; the 11 characteristics and their trends are valid everywhere. Applies in time as well as space: future SSP3-7.0 values in Czech lowlands are expected to approach or exceed the warm edge. Delivered reading: every multi-year indicator mean lies inside 'covered'; between 'covered' and 'outer' = degraded fit; beyond 'outer' = outside."
      }
    ],
    "artifacts": [
      {
        "id": "yearly-indicators",
        "artifact": "Yearly climate indicators (11 characteristics) covering the requested period",
        "artifactRole": "workflow-input",
        "acceptanceCriteria": {
          "variables": [
            {
              "name": "SUM25",
              "units": [
                "DAY"
              ]
            },
            {
              "name": "VEG10",
              "units": [
                "DAY"
              ]
            },
            {
              "name": "FROST0",
              "units": [
                "DAY"
              ]
            },
            {
              "name": "ICE0",
              "units": [
                "DAY"
              ]
            },
            {
              "name": "T_JAN",
              "units": [
                "DEG_C"
              ]
            },
            {
              "name": "T_APR",
              "units": [
                "DEG_C"
              ]
            },
            {
              "name": "T_JUL",
              "units": [
                "DEG_C"
              ]
            },
            {
              "name": "T_OCT",
              "units": [
                "DEG_C"
              ]
            },
            {
              "name": "RAIN1",
              "units": [
                "DAY"
              ]
            },
            {
              "name": "P_APR_SEP",
              "units": [
                "MilliM"
              ]
            },
            {
              "name": "P_OCT_MAR",
              "units": [
                "MilliM"
              ]
            }
          ],
          "temporal": {
            "resolution": "P1Y",
            "complete": true
          },
          "axes": [
            "time"
          ],
          "gridTypes": [
            "regular-latlon",
            "rotated-pole"
          ],
          "transferabilityNotes": "Structure: 4D array [year, ind, y, x], float32, NaN as no-data, indicators in the fixed order SUM25, VEG10, FROST0, ICE0, T_JAN, T_APR, T_JUL, T_OCT, RAIN1, P_APR_SEP, P_OCT_MAR. Time axis: calendar year (integer); every year of a requested period present. 2D latitude/longitude of cell centres (lookup collections or separable 1D axes); EPSG:4326 for lookups. Definitions: SUM25 = count(Tmax >= 25 degC); VEG10 = count(Tavg >= 10 degC); FROST0 = count(Tmin < 0 degC); ICE0 = count(Tmax < 0 degC); T_JAN = mean(Tavg, Jan); T_APR = mean(Tavg, Apr); T_JUL = mean(Tavg, Jul); T_OCT = mean(Tavg, Oct); RAIN1 = count(P >= 1 mm); P_APR_SEP = sum(P, Apr-Sep); P_OCT_MAR = sum(P, Oct-Mar)."
        },
        "transferabilityNotes": "As delivered, the workflow does not take these data as a file: it reads them from the Rasdaman data cube (artifact rasdaman), for the requested area and the years it needs. The delivered material gives no specification of the layout the code expects. Delivered as two datasets with the same requirements. (1) Historical: ERA5-Land yearly climate indicators (Rasdaman collection era5l_cz_yindicators). Needed only for historical periods. Within FOCAL: ERA5-Land is held for Czechia, Spain and Finland (exact extents per collection); any other area is computed in a routine precompute run. Outside FOCAL: ERA5-Land from the Copernicus Climate Data Store, E-OBS, or national gridded observations. (2) Projections: CMIP6-CORDEX EUR-11 GERICS-REMO2020 (MPI-ESM1-2-HR, EC-Earth3-Veg, MIROC6), SSP3-7.0, r1i1p1f1 yearly climate indicators (Rasdaman collections *_eur11_yindicators_<area>); SSP3-7.0 only, no historical experiment. Within FOCAL: precomputed for these bounding boxes (data coverage, not administrative boundaries): Czechia 12.07-18.97 E, 48.48-51.08 N; Slovakia 16.8174-22.7629 E, 47.6296-49.705 N; Spain (Maestrazgo Mountains) -1.09395-0.297912 E, 39.8289-40.8966 N; Southern Finland 20.3719-32.7637 E, 58.9769-63.1035 N. Elsewhere in the EUR-11 domain, a routine precompute run from the daily EUR-11 collections already held (started manually, no code change), then add the new collections and area entries. If no indicators exist, derive them from daily minimum, average and maximum temperature and precipitation (see artifact daily-climate) with the definitions above; that step runs in FOCAL ingest tooling and is not part of the FWF5 package. Seasonal windows assume the Northern Hemisphere. Used by (delivered step names): indicator-means, idw, climate-unit-classification, characteristic-trends, climate-unit-trend."
      },
      {
        "id": "daily-climate",
        "artifact": "Daily Tmin, Tavg, Tmax and precipitation from which the yearly indicators are derived (ERA5-Land hourly t2m/tp aggregated to daily; CORDEX daily tasmin/tas/tasmax/pr)",
        "artifactRole": "external-resource",
        "acceptanceCriteria": {
          "variables": [
            {
              "name": "tasmin",
              "units": [
                "DEG_C"
              ],
              "standardName": "air_temperature"
            },
            {
              "name": "tas",
              "units": [
                "DEG_C"
              ],
              "standardName": "air_temperature"
            },
            {
              "name": "tasmax",
              "units": [
                "DEG_C"
              ],
              "standardName": "air_temperature"
            },
            {
              "name": "pr",
              "units": [
                "MilliM-PER-DAY"
              ]
            }
          ],
          "temporal": {
            "resolution": "P1D",
            "calendar": [
              "standard",
              "proleptic_gregorian",
              "noleap"
            ]
          },
          "axes": [
            "time"
          ],
          "gridTypes": [
            "regular-latlon",
            "rotated-pole"
          ],
          "transferabilityNotes": "360_day calendars bias the day-count indicators and need adjustment."
        },
        "transferabilityNotes": "Not read by the workflow: upstream source of the yearly indicators. The precompute step runs in FOCAL ingest tooling and is not part of the FWF5 package. Within FOCAL: daily tas, tasmin, tasmax and pr of the three REMO2020 simulations are held for the whole EUR-11 rotated grid, 412 x 424 cells (lon/lat bounding box 44.5939 W - 64.9644 E, 21.9878 - 72.585 N; the box overstates the rotated domain at its corners); FWF5 runs anywhere inside it after the yearly indicators are precomputed for the area. Outside that domain: another CORDEX domain or another daily climate dataset meeting these criteria. Used by (delivered step names): yearly-indicator-precompute."
      },
      {
        "id": "quitt-limit-table",
        "artifact": "FWF5_quitt_limits_11_rasdaman_index.json: intervals of 11 indicators for 23 units (Quitt 1971, Table 2)",
        "artifactRole": "workflow-input",
        "artifactRef": "/inputs/quitt_limit_table",
        "transferabilityNotes": "A regional table needs: the same 11 indicator codes, units and axis mapping; [min, max] per unit and indicator, null allowed for an open end; and a full cold-to-warm ordering of units (used for tie-breaking and the unit trend). The limits were derived for former Czechoslovakia. Used by (delivered step names): climate-unit-classification, climate-unit-trend.",
        "acceptanceCriteria": {
          "variables": [
            {
              "name": "SUM25",
              "units": [
                "DAY"
              ]
            },
            {
              "name": "VEG10",
              "units": [
                "DAY"
              ]
            },
            {
              "name": "FROST0",
              "units": [
                "DAY"
              ]
            },
            {
              "name": "ICE0",
              "units": [
                "DAY"
              ]
            },
            {
              "name": "T_JAN",
              "units": [
                "DEG_C"
              ]
            },
            {
              "name": "T_APR",
              "units": [
                "DEG_C"
              ]
            },
            {
              "name": "T_JUL",
              "units": [
                "DEG_C"
              ]
            },
            {
              "name": "T_OCT",
              "units": [
                "DEG_C"
              ]
            },
            {
              "name": "RAIN1",
              "units": [
                "DAY"
              ]
            },
            {
              "name": "P_APR_SEP",
              "units": [
                "MilliM"
              ]
            },
            {
              "name": "P_OCT_MAR",
              "units": [
                "MilliM"
              ]
            }
          ]
        }
      },
      {
        "id": "unit-descriptions",
        "artifact": "FWF5_climate_metadata.json: unit names and descriptions (CZ/EN)",
        "artifactRole": "workflow-input",
        "artifactRef": "/inputs/unit_descriptions",
        "transferabilityNotes": "Names and descriptions for every unit of the limit table in use. The wording reflects Central European seasons and mentions snow cover and cloudiness, which are not computed. Used by (delivered step names): output-labelling."
      },
      {
        "id": "rasdaman",
        "artifact": "FOCAL Rasdaman data cube (rasql over SSH), source catalogue and registry (climate_source_catalog.json, rasdaman_registry.json)",
        "artifactRole": "infrastructure",
        "artifactRef": [
          "/inputs/rasdaman_connection",
          "/inputs/rasdaman_registry",
          "/inputs/climate_source_catalogue",
          "/inputs/readiness_collection"
        ],
        "transferabilityNotes": "The delivered workflow reads precomputed indicator collections from a Rasdaman instance queried with rasql over SSH. Another platform needs a Rasdaman instance with the same collection layout (set the connection variables and READINESS_COLLECTION) and its own registry, or replacement of the rasql data access by file-based reading; the scoring, IDW and trend modules use NumPy only. Within FOCAL: add the new collections and area entries. Outside FOCAL: the operator's own registry. Used by (delivered step names): data-access."
      }
    ],
    "rules": [
      {
        "appliesTo": [
          "quitt-limit-table"
        ],
        "when": [
          {
            "constraint": "quitt-climate-outer",
            "test": "outside"
          }
        ],
        "affects": [
          "/outputs/climate_unit",
          "/outputs/climate_unit_trend"
        ],
        "actions": [
          "replace-with-local-equivalent"
        ],
        "mandatory": true,
        "transferabilityNotes": "Without a regional table the steps still execute but return only the nearest Central European analogue with a low best_score. Characteristic outputs and trends are unaffected."
      },
      {
        "appliesTo": [
          "unit-descriptions"
        ],
        "when": [
          {
            "constraint": "quitt-climate-outer",
            "test": "outside"
          }
        ],
        "actions": [
          "replace-with-local-equivalent"
        ],
        "mandatory": false,
        "transferabilityNotes": "Follows a replaced limit table. If not replaced, unit names and descriptions do not describe the climate of the target."
      },
      {
        "appliesTo": [
          "quitt-limit-table"
        ],
        "when": [
          {
            "constraint": "quitt-climate-covered",
            "test": "outside"
          }
        ],
        "affects": [
          "/outputs/climate_unit",
          "/outputs/climate_unit_trend"
        ],
        "actions": [
          "replace-with-local-equivalent"
        ],
        "mandatory": false,
        "transferabilityNotes": "Degraded fit: an indicator mean outside 'covered' but within 'outer' still counts towards a unit with reduced membership, so the assigned unit can be trusted less. Characteristic outputs and trends are unaffected."
      },
      {
        "appliesTo": [
          "rasdaman"
        ],
        "triggeredBy": "service-unavailable",
        "actions": [
          "replace-with-local-equivalent"
        ],
        "mandatory": true,
        "transferabilityNotes": "Applies where no Rasdaman instance is available to the workflow: set one up with the same layout and its own registry, or change the code that reads the data (see the rasdaman artifact). On the FOCAL instance, a missing area is instead added as new collections and entries."
      }
    ]
  },
  "computationType": "deterministic-rule-based",
  "maturityStatus": "operational",
  "qualityAnnotation": [
    {
      "dimension": "method-limitation",
      "note": "best_score (0-1) is a similarity to interval limits, not a probability."
    },
    {
      "dimension": "method-limitation",
      "note": "The classification always returns a unit, even outside the climate envelope; a low best_score is the only signal."
    },
    {
      "dimension": "method-limitation",
      "note": "11 of Quitt's 14 characteristics are used; snow cover, cloudiness and clear/overcast days are omitted."
    },
    {
      "dimension": "method-limitation",
      "note": "10 km (ERA5-Land) and 12.5 km (EUR-11) cells; IDW smooths but adds no detail or elevation information."
    },
    {
      "dimension": "method-limitation",
      "note": "Projections: one RCM (REMO2020) driven by three GCMs under one scenario (SSP3-7.0); not year-specific forecasts."
    },
    {
      "dimension": "method-limitation",
      "note": "Default adverse directions reflect a warming/drying stress view; overridable per request."
    },
    {
      "dimension": "decision-support-only",
      "note": "Not a substitute for local measurement, site assessment or operational forecasting."
    }
  ]
}
```

#### ttl
```ttl
@prefix cwl: <https://w3id.org/cwl/cwl#> .
@prefix dcat: <http://www.w3.org/ns/dcat#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix dqv: <http://www.w3.org/ns/dqv#> .
@prefix focal-transf-prop: <https://w3id.org/ogc/hosted/focal/transferability/properties/> .
@prefix geo: <http://www.opengis.net/ont/geosparql#> .
@prefix ns1: <https://w3id.org/cwl/cwl#SoftwarePackage/> .
@prefix ns2: <https://w3id.org/cwl/cwl#SoftwareRequirement/> .
@prefix ns3: <https://w3id.org/cwl/cwl#NetworkAccess/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix schema: <https://schema.org/> .
@prefix sld: <https://w3id.org/cwl/salad#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/> a cwl:Workflow ;
    rdfs:label "FWF5 - Climate zones inspired by Quitt's classification (FOCAL Forest Pilot)" ;
    rdfs:comment "Assigns each location one of 23 climate units (coldest CH1 to warmest T5): the unit whose Quitt limits best match 11 multi-year mean climate characteristics. Reports trends of the characteristics and of the unit.",
        "Transferability record of workflow FP-WF5 (FWF5), record date 2026-11-18. Record basis: FWF5 code package (API, scoring, trends, Rasdaman registry, source catalogue, Quitt limit table) and the published methodology; not the round-1 questionnaire. Methodology: https://github.com/JiriVales/info4forest-backend/blob/main/methodology_climate_zones_quitt_en_updated.md Converted from the delivered record on 2026-11-25. Descriptive CWL profile: no steps are declared and the input and output identifiers are not yet those of an executable Application Package." ;
    schema:alternateName "FWF5" ;
    schema:citation "https://github.com/JiriVales/info4forest-backend/blob/main/methodology_climate_zones_quitt_en_updated.md" ;
    schema:dateCreated "2026-11-18" ;
    schema:identifier "FP-WF5" ;
    cwl:inputs <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/bbox>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/climate_source_catalogue>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/end_year>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/latitude>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/longitude>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/quitt_limit_table>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/rasdaman_connection>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/rasdaman_registry>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/readiness_collection>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/start_year>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/unit_descriptions> ;
    cwl:outputs <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/adverse_episode>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/climate_unit>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/climate_unit_trend>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/indicator_maps>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/indicator_trends> ;
    cwl:requirements [ a cwl:SoftwareRequirement ;
            ns2:packages [ ns1:package "python" ],
                [ ns1:package "gunicorn" ],
                [ ns1:package "numpy" ],
                [ ns1:package "flask" ] ],
        [ a cwl:NetworkAccess ;
            ns3:networkAccess true ] ;
    focal-transf-prop:computationType <https://w3id.org/ogc/hosted/focal/transferability/computation-types/deterministic-rule-based> ;
    focal-transf-prop:maturityStatus <https://w3id.org/ogc/hosted/focal/transferability/maturity-statuses/operational> ;
    focal-transf-prop:qualityAnnotation [ dqv:inDimension <https://w3id.org/ogc/hosted/focal/transferability/quality-dimensions/method-limitation> ;
            focal-transf-prop:note "The classification always returns a unit, even outside the climate envelope; a low best_score is the only signal." ],
        [ dqv:inDimension <https://w3id.org/ogc/hosted/focal/transferability/quality-dimensions/decision-support-only> ;
            focal-transf-prop:note "Not a substitute for local measurement, site assessment or operational forecasting." ],
        [ dqv:inDimension <https://w3id.org/ogc/hosted/focal/transferability/quality-dimensions/method-limitation> ;
            focal-transf-prop:note "11 of Quitt's 14 characteristics are used; snow cover, cloudiness and clear/overcast days are omitted." ],
        [ dqv:inDimension <https://w3id.org/ogc/hosted/focal/transferability/quality-dimensions/method-limitation> ;
            focal-transf-prop:note "Default adverse directions reflect a warming/drying stress view; overridable per request." ],
        [ dqv:inDimension <https://w3id.org/ogc/hosted/focal/transferability/quality-dimensions/method-limitation> ;
            focal-transf-prop:note "best_score (0-1) is a similarity to interval limits, not a probability." ],
        [ dqv:inDimension <https://w3id.org/ogc/hosted/focal/transferability/quality-dimensions/method-limitation> ;
            focal-transf-prop:note "Projections: one RCM (REMO2020) driven by three GCMs under one scenario (SSP3-7.0); not year-specific forecasts." ],
        [ dqv:inDimension <https://w3id.org/ogc/hosted/focal/transferability/quality-dimensions/method-limitation> ;
            focal-transf-prop:note "10 km (ERA5-Land) and 12.5 km (EUR-11) cells; IDW smooths but adds no detail or elevation information." ] ;
    focal-transf-prop:transferability [ rdfs:comment "Envelope entries and rules that only described which data FOCAL currently holds, or its platform, are not part of this statement; what they said is kept in the notes of the artifacts concerned. An area or period for which no data is at hand is a matter of providing data (as delivered, in the data cube) that meets the artifact's criteria. The delivered record also notes: temporal extent is the year range of each collection, read from Rasdaman at runtime. The 11 climate characteristics and their trends are valid everywhere; only the climate-unit outputs are bounded, by climate rather than geography." ;
            focal-transf-prop:artifacts <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/daily-climate>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/quitt-limit-table>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/rasdaman>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/unit-descriptions>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/yearly-indicators> ;
            focal-transf-prop:envelope <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/quitt-climate-covered>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/quitt-climate-outer>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/quitt-limits-origin> ;
            focal-transf-prop:rules [ rdfs:comment "Applies where no Rasdaman instance is available to the workflow: set one up with the same layout and its own registry, or change the code that reads the data (see the rasdaman artifact). On the FOCAL instance, a missing area is instead added as new collections and entries." ;
                    focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/replace-with-local-equivalent> ;
                    focal-transf-prop:appliesTo <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/rasdaman> ;
                    focal-transf-prop:mandatory true ;
                    focal-transf-prop:triggeredBy <https://w3id.org/ogc/hosted/focal/transferability/triggers/service-unavailable> ],
                [ rdfs:comment "Without a regional table the steps still execute but return only the nearest Central European analogue with a low best_score. Characteristic outputs and trends are unaffected." ;
                    focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/replace-with-local-equivalent> ;
                    focal-transf-prop:affects "/outputs/climate_unit",
                        "/outputs/climate_unit_trend" ;
                    focal-transf-prop:appliesTo <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/quitt-limit-table> ;
                    focal-transf-prop:mandatory true ;
                    focal-transf-prop:when [ focal-transf-prop:constraint <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/quitt-climate-outer> ;
                            focal-transf-prop:test <https://w3id.org/ogc/hosted/focal/transferability/tests/outside> ] ],
                [ rdfs:comment "Follows a replaced limit table. If not replaced, unit names and descriptions do not describe the climate of the target." ;
                    focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/replace-with-local-equivalent> ;
                    focal-transf-prop:appliesTo <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/unit-descriptions> ;
                    focal-transf-prop:mandatory false ;
                    focal-transf-prop:when [ focal-transf-prop:constraint <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/quitt-climate-outer> ;
                            focal-transf-prop:test <https://w3id.org/ogc/hosted/focal/transferability/tests/outside> ] ],
                [ rdfs:comment "Degraded fit: an indicator mean outside 'covered' but within 'outer' still counts towards a unit with reduced membership, so the assigned unit can be trusted less. Characteristic outputs and trends are unaffected." ;
                    focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/replace-with-local-equivalent> ;
                    focal-transf-prop:affects "/outputs/climate_unit",
                        "/outputs/climate_unit_trend" ;
                    focal-transf-prop:appliesTo <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/quitt-limit-table> ;
                    focal-transf-prop:mandatory false ;
                    focal-transf-prop:when [ focal-transf-prop:constraint <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/quitt-climate-covered> ;
                            focal-transf-prop:test <https://w3id.org/ogc/hosted/focal/transferability/tests/outside> ] ] ;
            focal-transf-prop:trainingRequired false ] .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/FWF5_climate_metadata.json> a cwl:File .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/FWF5_quitt_limits_11_rasdaman_index.json> a cwl:File .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/adverse_episode> rdfs:label "Adverse episode" ;
    rdfs:comment "Adverse episode derived from the trends." ;
    sld:type cwl:File .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/bbox> rdfs:label "Area of interest (bounding box)" ;
    rdfs:comment "Area as [minimum longitude, minimum latitude, maximum longitude, maximum latitude] in decimal degrees (WGS 84). Alternative to latitude and longitude." ;
    sld:type <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/double[]> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/climate_source_catalogue> rdfs:label "Climate source catalogue" ;
    rdfs:comment "climate_source_catalog.json listing the sources and areas offered." ;
    sld:type cwl:File .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/climate_unit> rdfs:label "Climate unit" ;
    rdfs:comment "Unit map and point detail: unit, fit score best_score and indicator means." ;
    sld:type cwl:File .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/climate_unit_trend> rdfs:label "Climate unit trend" ;
    rdfs:comment "Trend of the climate unit (yearly expected fuzzy rank)." ;
    sld:type cwl:File .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/daily-climate> dcterms:title "Daily Tmin, Tavg, Tmax and precipitation from which the yearly indicators are derived (ERA5-Land hourly t2m/tp aggregated to daily; CORDEX daily tasmin/tas/tasmax/pr)" ;
    rdfs:comment "Not read by the workflow: upstream source of the yearly indicators. The precompute step runs in FOCAL ingest tooling and is not part of the FWF5 package. Within FOCAL: daily tas, tasmin, tasmax and pr of the three REMO2020 simulations are held for the whole EUR-11 rotated grid, 412 x 424 cells (lon/lat bounding box 44.5939 W - 64.9644 E, 21.9878 - 72.585 N; the box overstates the rotated domain at its corners); FWF5 runs anywhere inside it after the yearly indicators are precomputed for the area. Outside that domain: another CORDEX domain or another daily climate dataset meeting these criteria. Used by (delivered step names): yearly-indicator-precompute." ;
    focal-transf-prop:acceptanceCriteria [ rdfs:comment "360_day calendars bias the day-count indicators and need adjustment." ;
            focal-transf-prop:axis <https://w3id.org/ogc/hosted/focal/transferability/axes/time> ;
            focal-transf-prop:gridType <https://w3id.org/ogc/hosted/focal/transferability/grid-types/regular-latlon>,
                <https://w3id.org/ogc/hosted/focal/transferability/grid-types/rotated-pole> ;
            focal-transf-prop:temporalRequirement [ dcat:temporalResolution "P1D"^^xsd:duration ;
                    focal-transf-prop:calendar "noleap",
                        "proleptic_gregorian",
                        "standard" ] ;
            focal-transf-prop:variable [ focal-transf-prop:standardName "air_temperature" ;
                    focal-transf-prop:unit <http://qudt.org/vocab/unit/DEG_C> ;
                    focal-transf-prop:variableName "tasmin" ],
                [ focal-transf-prop:standardName "air_temperature" ;
                    focal-transf-prop:unit <http://qudt.org/vocab/unit/DEG_C> ;
                    focal-transf-prop:variableName "tasmax" ],
                [ focal-transf-prop:standardName "air_temperature" ;
                    focal-transf-prop:unit <http://qudt.org/vocab/unit/DEG_C> ;
                    focal-transf-prop:variableName "tas" ],
                [ focal-transf-prop:unit <http://qudt.org/vocab/unit/MilliM-PER-DAY> ;
                    focal-transf-prop:variableName "pr" ] ] ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/external-resource> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/end_year> rdfs:label "Last year of the period" ;
    rdfs:comment "Last year of the period; it must be within the years of the data. Trends need at least 2 years." ;
    sld:type xsd:int .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/indicator_maps> rdfs:label "Climate characteristic maps" ;
    rdfs:comment "Maps of the 11 climate characteristics." ;
    sld:type cwl:File .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/indicator_trends> rdfs:label "Climate characteristic trends" ;
    rdfs:comment "Sen's slope and Mann-Kendall test (alpha = 0.05) per indicator." ;
    sld:type cwl:File .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/latitude> rdfs:label "Latitude of the point" ;
    rdfs:comment "Latitude in decimal degrees (WGS 84). Give latitude and longitude for a point, or bbox for an area." ;
    sld:type <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/double> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/longitude> rdfs:label "Longitude of the point" ;
    rdfs:comment "Longitude in decimal degrees (WGS 84). Give together with latitude." ;
    sld:type <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/double> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/quitt-limits-origin> rdfs:comment "Bounding box of the FOCAL Czechia and Slovakia areas, standing in for former Czechoslovakia, for which Quitt (1971) derived the limit table. The limits were taken over, not fitted by FOCAL." ;
    focal-transf-prop:dimension <https://w3id.org/ogc/hosted/focal/transferability/dimensions/spatial> ;
    focal-transf-prop:role <https://w3id.org/ogc/hosted/focal/transferability/roles/derived-from> ;
    focal-transf-prop:value [ geo:asWKT "POLYGON((12.07 47.63, 22.76 47.63, 22.76 51.08, 12.07 51.08, 12.07 47.63))"^^geo:wktLiteral ] .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/quitt_limit_table> rdfs:label "Climate unit limit table" ;
    rdfs:comment "Intervals of the 11 indicators for 23 climate units (Quitt 1971, Table 2). Ships with the workflow; replace it with a regional table for climates unlike Central Europe." ;
    sld:default <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/FWF5_quitt_limits_11_rasdaman_index.json> ;
    sld:type cwl:File .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/rasdaman_connection> rdfs:label "Data cube connection" ;
    rdfs:comment "How to reach the Rasdaman instance that holds the climate data (queried with rasql over SSH). The connection variables are not named in the delivered material, so one string stands for them; we assume credentials are supplied by the execution environment." ;
    sld:type xsd:string .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/rasdaman_registry> rdfs:label "Data cube registry" ;
    rdfs:comment "rasdaman_registry.json for that instance. The FOCAL registry is not transferable as is." ;
    sld:type cwl:File .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/readiness_collection> rdfs:label "Readiness check collection" ;
    rdfs:comment "Value for READINESS_COLLECTION, which defaults to a Czech ERA5-Land collection. Outside that default it must be set, otherwise the readiness check fails." ;
    sld:type <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/string> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/start_year> rdfs:label "First year of the period" ;
    rdfs:comment "First year of the period over which the indicators are averaged; it must be within the years of the data." ;
    sld:type xsd:int .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/unit_descriptions> rdfs:label "Climate unit descriptions" ;
    rdfs:comment "Names and descriptions of the units (Czech and English). Ships with the workflow." ;
    sld:default <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/FWF5_climate_metadata.json> ;
    sld:type cwl:File .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/yearly-indicators> dcterms:title "Yearly climate indicators (11 characteristics) covering the requested period" ;
    rdfs:comment "As delivered, the workflow does not take these data as a file: it reads them from the Rasdaman data cube (artifact rasdaman), for the requested area and the years it needs. The delivered material gives no specification of the layout the code expects. Delivered as two datasets with the same requirements. (1) Historical: ERA5-Land yearly climate indicators (Rasdaman collection era5l_cz_yindicators). Needed only for historical periods. Within FOCAL: ERA5-Land is held for Czechia, Spain and Finland (exact extents per collection); any other area is computed in a routine precompute run. Outside FOCAL: ERA5-Land from the Copernicus Climate Data Store, E-OBS, or national gridded observations. (2) Projections: CMIP6-CORDEX EUR-11 GERICS-REMO2020 (MPI-ESM1-2-HR, EC-Earth3-Veg, MIROC6), SSP3-7.0, r1i1p1f1 yearly climate indicators (Rasdaman collections *_eur11_yindicators_<area>); SSP3-7.0 only, no historical experiment. Within FOCAL: precomputed for these bounding boxes (data coverage, not administrative boundaries): Czechia 12.07-18.97 E, 48.48-51.08 N; Slovakia 16.8174-22.7629 E, 47.6296-49.705 N; Spain (Maestrazgo Mountains) -1.09395-0.297912 E, 39.8289-40.8966 N; Southern Finland 20.3719-32.7637 E, 58.9769-63.1035 N. Elsewhere in the EUR-11 domain, a routine precompute run from the daily EUR-11 collections already held (started manually, no code change), then add the new collections and area entries. If no indicators exist, derive them from daily minimum, average and maximum temperature and precipitation (see artifact daily-climate) with the definitions above; that step runs in FOCAL ingest tooling and is not part of the FWF5 package. Seasonal windows assume the Northern Hemisphere. Used by (delivered step names): indicator-means, idw, climate-unit-classification, characteristic-trends, climate-unit-trend." ;
    focal-transf-prop:acceptanceCriteria [ rdfs:comment "Structure: 4D array [year, ind, y, x], float32, NaN as no-data, indicators in the fixed order SUM25, VEG10, FROST0, ICE0, T_JAN, T_APR, T_JUL, T_OCT, RAIN1, P_APR_SEP, P_OCT_MAR. Time axis: calendar year (integer); every year of a requested period present. 2D latitude/longitude of cell centres (lookup collections or separable 1D axes); EPSG:4326 for lookups. Definitions: SUM25 = count(Tmax >= 25 degC); VEG10 = count(Tavg >= 10 degC); FROST0 = count(Tmin < 0 degC); ICE0 = count(Tmax < 0 degC); T_JAN = mean(Tavg, Jan); T_APR = mean(Tavg, Apr); T_JUL = mean(Tavg, Jul); T_OCT = mean(Tavg, Oct); RAIN1 = count(P >= 1 mm); P_APR_SEP = sum(P, Apr-Sep); P_OCT_MAR = sum(P, Oct-Mar)." ;
            focal-transf-prop:axis <https://w3id.org/ogc/hosted/focal/transferability/axes/time> ;
            focal-transf-prop:gridType <https://w3id.org/ogc/hosted/focal/transferability/grid-types/regular-latlon>,
                <https://w3id.org/ogc/hosted/focal/transferability/grid-types/rotated-pole> ;
            focal-transf-prop:temporalRequirement [ dcat:temporalResolution "P1Y"^^xsd:duration ;
                    focal-transf-prop:temporalComplete true ] ;
            focal-transf-prop:variable [ focal-transf-prop:unit <http://qudt.org/vocab/unit/MilliM> ;
                    focal-transf-prop:variableName "P_OCT_MAR" ],
                [ focal-transf-prop:unit <http://qudt.org/vocab/unit/DEG_C> ;
                    focal-transf-prop:variableName "T_JUL" ],
                [ focal-transf-prop:unit <http://qudt.org/vocab/unit/DAY> ;
                    focal-transf-prop:variableName "VEG10" ],
                [ focal-transf-prop:unit <http://qudt.org/vocab/unit/DAY> ;
                    focal-transf-prop:variableName "FROST0" ],
                [ focal-transf-prop:unit <http://qudt.org/vocab/unit/DAY> ;
                    focal-transf-prop:variableName "ICE0" ],
                [ focal-transf-prop:unit <http://qudt.org/vocab/unit/DAY> ;
                    focal-transf-prop:variableName "RAIN1" ],
                [ focal-transf-prop:unit <http://qudt.org/vocab/unit/DAY> ;
                    focal-transf-prop:variableName "SUM25" ],
                [ focal-transf-prop:unit <http://qudt.org/vocab/unit/DEG_C> ;
                    focal-transf-prop:variableName "T_OCT" ],
                [ focal-transf-prop:unit <http://qudt.org/vocab/unit/DEG_C> ;
                    focal-transf-prop:variableName "T_APR" ],
                [ focal-transf-prop:unit <http://qudt.org/vocab/unit/MilliM> ;
                    focal-transf-prop:variableName "P_APR_SEP" ],
                [ focal-transf-prop:unit <http://qudt.org/vocab/unit/DEG_C> ;
                    focal-transf-prop:variableName "T_JAN" ] ] ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/workflow-input> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/quitt-climate-covered> rdfs:comment "'covered' ranges: every multi-year indicator mean inside them. Union of the 23 unit intervals in FWF5_quitt_limits_11_rasdaman_index.json; 'outer' adds the fuzzy tolerances used in the code (10 days, 1 degC, 50 mm). Applies to the climate-unit outputs only; the 11 characteristics and their trends are valid everywhere. Applies in time as well as space: future SSP3-7.0 values in Czech lowlands are expected to approach or exceed the warm edge. Delivered reading: every multi-year indicator mean lies inside 'covered'; between 'covered' and 'outer' = degraded fit; beyond 'outer' = outside." ;
    focal-transf-prop:dimension <https://w3id.org/ogc/hosted/focal/transferability/dimensions/climatic> ;
    focal-transf-prop:inputRef "/inputs/bbox",
        "/inputs/end_year",
        "/inputs/latitude",
        "/inputs/longitude",
        "/inputs/start_year" ;
    focal-transf-prop:role <https://w3id.org/ogc/hosted/focal/transferability/roles/valid-for> ;
    focal-transf-prop:value [ focal-transf-prop:statistic "multi-year mean" ;
            focal-transf-prop:variableRange [ focal-transf-prop:maximum 7e+01 ;
                    focal-transf-prop:minimum 0e+00 ;
                    focal-transf-prop:unitLabel "days" ;
                    focal-transf-prop:variableName "SUM25" ],
                [ focal-transf-prop:maximum 1e+01 ;
                    focal-transf-prop:minimum 0e+00 ;
                    focal-transf-prop:unitLabel "degC" ;
                    focal-transf-prop:variableName "T_APR" ],
                [ focal-transf-prop:maximum -1e+00 ;
                    focal-transf-prop:minimum -8e+00 ;
                    focal-transf-prop:unitLabel "degC" ;
                    focal-transf-prop:variableName "T_JAN" ],
                [ focal-transf-prop:maximum 1e+01 ;
                    focal-transf-prop:minimum 2e+00 ;
                    focal-transf-prop:unitLabel "degC" ;
                    focal-transf-prop:variableName "T_OCT" ],
                [ focal-transf-prop:maximum 1e+03 ;
                    focal-transf-prop:minimum 3e+02 ;
                    focal-transf-prop:unitLabel "mm" ;
                    focal-transf-prop:variableName "P_APR_SEP" ],
                [ focal-transf-prop:maximum 1.8e+02 ;
                    focal-transf-prop:minimum 9e+01 ;
                    focal-transf-prop:unitLabel "days" ;
                    focal-transf-prop:variableName "FROST0" ],
                [ focal-transf-prop:maximum 1.6e+02 ;
                    focal-transf-prop:minimum 8e+01 ;
                    focal-transf-prop:unitLabel "days" ;
                    focal-transf-prop:variableName "RAIN1" ],
                [ focal-transf-prop:maximum 2e+01 ;
                    focal-transf-prop:minimum 1e+01 ;
                    focal-transf-prop:unitLabel "degC" ;
                    focal-transf-prop:variableName "T_JUL" ],
                [ focal-transf-prop:maximum 8e+01 ;
                    focal-transf-prop:minimum 0e+00 ;
                    focal-transf-prop:unitLabel "days" ;
                    focal-transf-prop:variableName "ICE0" ],
                [ focal-transf-prop:maximum 7e+02 ;
                    focal-transf-prop:minimum 2e+02 ;
                    focal-transf-prop:unitLabel "mm" ;
                    focal-transf-prop:variableName "P_OCT_MAR" ],
                [ focal-transf-prop:minimum 0e+00 ;
                    focal-transf-prop:unitLabel "days" ;
                    focal-transf-prop:variableName "VEG10" ] ] .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/rasdaman> dcterms:title "FOCAL Rasdaman data cube (rasql over SSH), source catalogue and registry (climate_source_catalog.json, rasdaman_registry.json)" ;
    rdfs:comment "The delivered workflow reads precomputed indicator collections from a Rasdaman instance queried with rasql over SSH. Another platform needs a Rasdaman instance with the same collection layout (set the connection variables and READINESS_COLLECTION) and its own registry, or replacement of the rasql data access by file-based reading; the scoring, IDW and trend modules use NumPy only. Within FOCAL: add the new collections and area entries. Outside FOCAL: the operator's own registry. Used by (delivered step names): data-access." ;
    focal-transf-prop:artifactRef "/inputs/climate_source_catalogue",
        "/inputs/rasdaman_connection",
        "/inputs/rasdaman_registry",
        "/inputs/readiness_collection" ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/infrastructure> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/unit-descriptions> dcterms:title "FWF5_climate_metadata.json: unit names and descriptions (CZ/EN)" ;
    rdfs:comment "Names and descriptions for every unit of the limit table in use. The wording reflects Central European seasons and mentions snow cover and cloudiness, which are not computed. Used by (delivered step names): output-labelling." ;
    focal-transf-prop:artifactRef "/inputs/unit_descriptions" ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/workflow-input> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/quitt-climate-outer> rdfs:comment "'outer' ranges: covered ranges plus the fuzzy tolerances; a mean beyond them gets zero membership for that indicator in every unit. VEG10 has no outer limit and is not listed. Union of the 23 unit intervals in FWF5_quitt_limits_11_rasdaman_index.json; 'outer' adds the fuzzy tolerances used in the code (10 days, 1 degC, 50 mm). Applies to the climate-unit outputs only; the 11 characteristics and their trends are valid everywhere. Applies in time as well as space: future SSP3-7.0 values in Czech lowlands are expected to approach or exceed the warm edge. Delivered reading: every multi-year indicator mean lies inside 'covered'; between 'covered' and 'outer' = degraded fit; beyond 'outer' = outside." ;
    focal-transf-prop:dimension <https://w3id.org/ogc/hosted/focal/transferability/dimensions/climatic> ;
    focal-transf-prop:inputRef "/inputs/bbox",
        "/inputs/end_year",
        "/inputs/latitude",
        "/inputs/longitude",
        "/inputs/start_year" ;
    focal-transf-prop:role <https://w3id.org/ogc/hosted/focal/transferability/roles/valid-for> ;
    focal-transf-prop:value [ focal-transf-prop:statistic "multi-year mean" ;
            focal-transf-prop:variableRange [ focal-transf-prop:maximum 8e+01 ;
                    focal-transf-prop:unitLabel "days" ;
                    focal-transf-prop:variableName "SUM25" ],
                [ focal-transf-prop:maximum 0e+00 ;
                    focal-transf-prop:minimum -9e+00 ;
                    focal-transf-prop:unitLabel "degC" ;
                    focal-transf-prop:variableName "T_JAN" ],
                [ focal-transf-prop:maximum 1.1e+01 ;
                    focal-transf-prop:minimum 1e+00 ;
                    focal-transf-prop:unitLabel "degC" ;
                    focal-transf-prop:variableName "T_OCT" ],
                [ focal-transf-prop:maximum 2.1e+01 ;
                    focal-transf-prop:minimum 9e+00 ;
                    focal-transf-prop:unitLabel "degC" ;
                    focal-transf-prop:variableName "T_JUL" ],
                [ focal-transf-prop:maximum 1.7e+02 ;
                    focal-transf-prop:minimum 7e+01 ;
                    focal-transf-prop:unitLabel "days" ;
                    focal-transf-prop:variableName "RAIN1" ],
                [ focal-transf-prop:maximum 9e+01 ;
                    focal-transf-prop:unitLabel "days" ;
                    focal-transf-prop:variableName "ICE0" ],
                [ focal-transf-prop:maximum 7.5e+02 ;
                    focal-transf-prop:minimum 1.5e+02 ;
                    focal-transf-prop:unitLabel "mm" ;
                    focal-transf-prop:variableName "P_OCT_MAR" ],
                [ focal-transf-prop:maximum 1.1e+01 ;
                    focal-transf-prop:minimum -1e+00 ;
                    focal-transf-prop:unitLabel "degC" ;
                    focal-transf-prop:variableName "T_APR" ],
                [ focal-transf-prop:maximum 1.05e+03 ;
                    focal-transf-prop:minimum 2.5e+02 ;
                    focal-transf-prop:unitLabel "mm" ;
                    focal-transf-prop:variableName "P_APR_SEP" ],
                [ focal-transf-prop:maximum 1.9e+02 ;
                    focal-transf-prop:minimum 8e+01 ;
                    focal-transf-prop:unitLabel "days" ;
                    focal-transf-prop:variableName "FROST0" ] ] .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/quitt-limit-table> dcterms:title "FWF5_quitt_limits_11_rasdaman_index.json: intervals of 11 indicators for 23 units (Quitt 1971, Table 2)" ;
    rdfs:comment "A regional table needs: the same 11 indicator codes, units and axis mapping; [min, max] per unit and indicator, null allowed for an open end; and a full cold-to-warm ordering of units (used for tie-breaking and the unit trend). The limits were derived for former Czechoslovakia. Used by (delivered step names): climate-unit-classification, climate-unit-trend." ;
    focal-transf-prop:acceptanceCriteria [ focal-transf-prop:variable [ focal-transf-prop:unit <http://qudt.org/vocab/unit/MilliM> ;
                    focal-transf-prop:variableName "P_OCT_MAR" ],
                [ focal-transf-prop:unit <http://qudt.org/vocab/unit/DAY> ;
                    focal-transf-prop:variableName "ICE0" ],
                [ focal-transf-prop:unit <http://qudt.org/vocab/unit/DAY> ;
                    focal-transf-prop:variableName "FROST0" ],
                [ focal-transf-prop:unit <http://qudt.org/vocab/unit/MilliM> ;
                    focal-transf-prop:variableName "P_APR_SEP" ],
                [ focal-transf-prop:unit <http://qudt.org/vocab/unit/DAY> ;
                    focal-transf-prop:variableName "RAIN1" ],
                [ focal-transf-prop:unit <http://qudt.org/vocab/unit/DEG_C> ;
                    focal-transf-prop:variableName "T_JUL" ],
                [ focal-transf-prop:unit <http://qudt.org/vocab/unit/DEG_C> ;
                    focal-transf-prop:variableName "T_OCT" ],
                [ focal-transf-prop:unit <http://qudt.org/vocab/unit/DEG_C> ;
                    focal-transf-prop:variableName "T_APR" ],
                [ focal-transf-prop:unit <http://qudt.org/vocab/unit/DEG_C> ;
                    focal-transf-prop:variableName "T_JAN" ],
                [ focal-transf-prop:unit <http://qudt.org/vocab/unit/DAY> ;
                    focal-transf-prop:variableName "SUM25" ],
                [ focal-transf-prop:unit <http://qudt.org/vocab/unit/DAY> ;
                    focal-transf-prop:variableName "VEG10" ] ] ;
    focal-transf-prop:artifactRef "/inputs/quitt_limit_table" ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/workflow-input> .


```


### UP-WF3 — Urban blue-spot flood risk (the fullest contract, and the limits of the model)
The richest questionnaire in the corpus and the one this model was most recently extended
for: `acceptanceCriteria` and the `grid-structure` dimension both exist because of it. This is
their first use in a whole workflow, and it is also where the model's current edges show.

**The precipitation contract is what `replace-with-local-equivalent` was missing.** Question 9
says a replacement must carry the same variable name, be in mm or kg m⁻²s⁻¹, have a time axis,
and be on a regular lat/lon or rotated-pole grid. All four are on the artifact, not the rule,
because they hold whether or not anyone is transferring anything — a platform can check a
candidate file against them without knowing why it was offered.

**An unsupported grid is not a substitution problem.** Question 7 is categorical: "Other
projections are not handled." So the grid constraint is cited by a rule whose action is
`component-not-executable` and whose `affects` names the accumulation and detection steps —
we read "not handled" as: it does not run (for example on a Lambert-conformal grid), which the owners have confirmed. That is the
distinction the terminal action exists to draw, and this is a cleaner instance of it than
UP-WF2's, where a substitute might yet be found.

**Two threshold sets, one climatic trigger.** The 6-hour and 12-hour percentile thresholds
come from DWD station data for Germany, the 1-day and 7-day ones from E-OBS for Europe. Both
provenances are recorded as `derived-from` constraints rather than `trained-on`, since the
thresholds were computed, not fitted: this workflow trains nothing. The rule that fires is conditioned
on the climatic constraint, because that is what question 9 actually says: "for a region with
different climate regime, user should use a custom threshold". A target inside Germany with an
unlike climate is as much of a problem as one outside it.

**A support mismatch is a quality fact, not a portability one.** Question 7 states that the
vulnerability index is at NUTS3 level, "coarser than the precipitation grid and does not
align exactly with the AOI boundary". That is a relationship between the supports of two of
the workflow's own artifacts, so no envelope dimension holds it and no rule is conditioned on
it, and it holds in the source deployment as much as in any target. It belongs on the axis
that already exists for "this is `pre-operational` and you should still be careful": it is
carried by a second `qualityAnnotation` on the new `spatial-support-mismatch` dimension.

**There is no single coverage boundary.** The owners say the precipitation sources and the
contextual layers have different footprints, so the precipitation rule fires only when the
target is outside both the E-OBS and the NUKLEUS domains (two conditions in one `when`, ANDed),
and the contextual layers keep a stand-in footprint until theirs are drawn: the EU as a coarse
union of countries, which is too narrow for the non-EU countries of the NUTS3 layer. The
other extents are approximations too: Germany's simplified border stands in for the DWD
station network, the E-OBS box is its published approximate extent, and the NUKLEUS box is
the CEU-3 domain from the project's STAC metadata. The custom
threshold is optional (`mandatory: false`): the reference thresholds still run, with weaker
interpretation outside the regime they came from.

**What this example still cannot say, and does not pretend to.** Two evidenced facts from
this questionnaire have no home in the model as it stands, and each is recorded in
`transferabilityNotes` on the nearest thing to it rather than forced into a shape that would
misstate it:

1. *Exposure and vulnerability cannot be supplied by the user, for now.* The current interface
   offers no upload for these layers, which the owners call an implementation limitation
   rather than a permanent one, and no replacement contract is defined. That is a standing
   property of the interface, not an outcome triggered by a target, so no rule holds it; it
   is a note on each artifact.
2. *The available accumulation windows depend on which precipitation source is used.* E-OBS is
   daily, so only 1-day and 7-day windows work with it; 6-hour and 12-hour need hourly NUKLEUS
   data. A co-constraint between two inputs, which is a CWL-level fact this profile does not
   reach into: CWL types an input as a union of record schemas, which is where a choice
   between "E-OBS plus a daily window" and "NUKLEUS plus a sub-daily one" belongs.

The `qualityAnnotation` entries are directly evidenced, unlike FP-WF1's: the Blue Spot is
hazard information, not a flood-risk score; the thresholds are benchmarks, not local
calibrations; and the climate-state outputs describe states, not calendar years.

`maturityStatus: pre-operational` is the sharpest use of that middle term in the set — a
Python package on DKRZ's HPC system, "Container: none at this stage", recently shared for
integration testing. `inputs` and `steps` ids are placeholders invented so `artifactRef` and
`affects` resolve; they are not UP-WF3's real interface.

The questionnaire gives the Python requirement as "3.10+"; CWL's version list cannot say "and
later", so only the lower bound is recorded.

#### json
```json
{
  "class": "Workflow",
  "id": "",
  "cwlVersion": "v1.2",
  "label": "UP-WF3 — Urban blue-spot flood risk",
  "requirements": {
    "SoftwareRequirement": {
      "packages": [
        { "package": "python", "version": ["3.10"] },
        { "package": "xarray" },
        { "package": "numpy" },
        { "package": "pandas" },
        { "package": "rasterio" }
      ]
    },
    "NetworkAccess": { "networkAccess": true }
  },
  "inputs": {
    "precipitation": { "type": "File" },
    "aoi_bbox": { "type": "double[]", "label": "Rectangular WGS84 bounding box: west, south, east, north" },
    "threshold_subdaily": { "type": "File" },
    "threshold_daily": { "type": "File" },
    "exposure_layers": { "type": "File?" },
    "vulnerability_index": { "type": "File?" }
  },
  "steps": {
    "accumulation": {
      "run": "#accumulation.cwl",
      "in": { "precipitation": "precipitation" },
      "out": ["accumulated_precipitation"]
    },
    "blue_spot_detection": {
      "run": "#blue_spot_detection.cwl",
      "in": { "accumulated": "accumulation/accumulated_precipitation", "threshold": "threshold_daily" },
      "out": ["blue_spot_map"]
    },
    "exposure_overlay": {
      "run": "#exposure_overlay.cwl",
      "in": { "blue_spots": "blue_spot_detection/blue_spot_map", "exposure": "exposure_layers" },
      "out": ["exposure_map"]
    },
    "vulnerability_overlay": {
      "run": "#vulnerability_overlay.cwl",
      "in": { "blue_spots": "blue_spot_detection/blue_spot_map", "vulnerability": "vulnerability_index" },
      "out": ["vulnerability_map"]
    }
  },
  "transferability": {
    "trainingRequired": false,
    "envelope": [
      {
        "id": "dwd-stations",
        "role": "derived-from",
        "dimension": "spatial",
        "value": { "asWKT": "MULTIPOLYGON (((8.57 47.78, 8.43 47.59, 7.57 47.61, 7.62 48.16, 8.13 48.97, 6.74 49.16, 6.34 49.45, 6.49 49.8, 6.11 50.09, 6.34 50.45, 5.86 51.03, 6.13 51.15, 6.2 51.45, 5.95 51.8, 6.74 51.91, 6.72 52.08, 7.02 52.27, 7 52.42, 6.69 52.53, 7.01 52.63, 7.18 52.97, 7.2 53.28, 7.05 53.38, 7.21 53.65, 8.01 53.69, 8.11 53.47, 8.33 53.61, 8.5 53.39, 8.62 53.88, 9.21 53.86, 9.59 53.6, 9.78 53.55, 9.31 53.86, 8.98 53.93, 8.91 54.26, 8.64 54.29, 8.96 54.54, 8.67 54.9, 9.62 54.86, 10.02 54.67, 9.87 54.47, 11.01 54.38, 11.01 54.18, 10.81 54.08, 10.92 54, 11.4 53.94, 12.58 54.47, 13.03 54.41, 13.45 54.14, 13.72 54.15, 13.87 53.85, 14.26 53.73, 14.41 53.2, 14.13 52.88, 14.62 52.53, 14.55 52.36, 14.75 52.08, 14.6 51.83, 14.72 51.52, 14.94 51.44, 14.96 51.1, 14.77 50.82, 14.32 51.04, 14.37 50.9, 12.94 50.41, 12.55 50.39, 12.28 50.18, 12.09 50.27, 12.51 49.9, 12.39 49.74, 12.63 49.46, 13.77 48.82, 13.79 48.59, 13.49 48.58, 13.37 48.36, 12.76 48.11, 13.05 47.66, 13.01 47.48, 12.21 47.72, 11.04 47.39, 10.44 47.55, 10.18 47.28, 9.97 47.51, 8.57 47.78)), ((13.36 54.25, 13.16 54.36, 13.18 54.54, 13.42 54.7, 13.71 54.38, 13.36 54.25)), ((13.93 53.88, 13.83 54.13, 14.04 54.03, 14.21 53.95, 13.93 53.88)), ((11.13 54.42, 11.01 54.47, 11.08 54.53, 11.28 54.42, 11.13 54.42)), ((8.41 55.06, 8.38 54.9, 8.63 54.89, 8.31 54.79, 8.41 55.06)), ((8.55 54.69, 8.4 54.71, 8.51 54.76, 8.55 54.69)))" }
      },
      {
        "id": "eobs-extent",
        "role": "derived-from",
        "dimension": "spatial",
        "value": { "asWKT": "POLYGON((-25 25,45 25,45 71.5,-25 71.5,-25 25))" }
      },
      {
        "id": "threshold-climate-regime",
        "role": "valid-for",
        "dimension": "climatic",
        "value": "the German and European climate regime the pre-computed percentile thresholds were derived from"
      },
      {
        "id": "eu-input-coverage",
        "role": "can-run-on",
        "dimension": "spatial",
        "value": { "asWKT": "MULTIPOLYGON (((-8.79 39.08, -9.48 38.8, -8.66 41.03, -9.18 43.17, -7.7 43.76, -1.99 43.35, -1.08 45.53, -0.83 45.38, -0.69 45.09, -0.55 45, -1.74 47.22, -4.72 48.54, -1.38 48.65, -1.86 49.68, 0.42 49.45, 1.77 50.94, 4.23 51.39, 3.45 51.54, 4.27 51.47, 5.53 53.27, 9.78 53.55, 8.13 55.6, 8.16 56.61, 9.2 56.7, 8.27 56.75, 8.62 57.11, 10.61 57.74, 10.28 56.62, 10.89 56.36, 9.45 55.04, 10.92 54, 12.58 54.47, 13.72 54.15, 13.95 53.8, 14.58 53.64, 13.83 54.13, 18.09 54.84, 22.73 54.35, 22.57 55.06, 21.2 55.34, 21.46 57.32, 24.28 57.17, 24.53 58.35, 23.43 58.92, 24.38 59.47, 28.15 59.37, 27.35 57.53, 28.15 56.14, 26.59 55.67, 25.75 54.16, 23.48 53.94, 23.92 52.77, 23.18 52.29, 24.09 50.53, 22.13 48.41, 24.89 47.72, 26.9 48.21, 28.24 46.64, 28.21 45.45, 29.71 45.26, 27.48 42.47, 28.01 41.97, 26.58 41.95, 26.04 40.73, 23.76 40.75, 23.95 39.97, 22.63 40.5, 23.33 39.17, 22.57 38.87, 24.02 38.14, 22.73 37.54, 23.16 36.45, 21.12 37.89, 23.15 38.18, 21.18 38.35, 20 39.71, 20.96 40.85, 22.93 41.36, 22.34 42.31, 22.73 44.57, 19.61 46.17, 18.84 45.84, 19.01 44.87, 15.79 45.18, 17.59 42.94, 15.99 43.52, 14.55 45.3, 13.86 44.84, 13.63 45.77, 12.27 45.45, 12.4 44.22, 14.18 42.51, 18.46 40.22, 16.93 40.46, 16.52 39.75, 17.17 39, 16.06 37.94, 15.69 39.99, 8.77 44.42, 6.12 43.07, 3.26 43.19, 3.25 41.94, 0.71 40.82, -0.33 39.52, 0.2 38.76, -2.11 36.78, -5.63 36.03, -6.86 37.28, -8.74 37.07, -8.79 39.08)), ((-7.85 54.22, -6.18 54.05, -6.32 52.25, -10.12 51.6, -9.6 51.87, -10.36 52.21, -8.78 52.68, -9.92 52.57, -8.93 53.21, -10.09 53.41, -9.58 53.81, -10.09 54.22, -6.96 55.24, -7.85 54.22)), ((12.88 61.35, 12.16 61.72, 12.18 63.6, 14.06 64.1, 13.65 64.58, 14.54 66.13, 16.78 67.9, 21.27 69.27, 24.94 68.59, 26.53 69.92, 29.33 69.47, 28.41 68.9, 29.99 67.67, 29.07 66.89, 30.09 65.79, 29.6 64.97, 30.53 64.08, 29.99 63.74, 31.54 62.92, 29.25 61.29, 23.02 59.82, 21.44 60.6, 21.55 63.2, 25.37 65.01, 24.63 65.86, 22.4 65.86, 20.76 63.87, 17.38 62.46, 17.25 60.7, 18.99 59.83, 16.21 58.64, 16.92 58.49, 15.92 56.17, 12.89 55.41, 12.88 56.62, 11.25 58.37, 12.88 61.35)))" }
      },
      {
        "id": "eobs-coverage",
        "role": "can-run-on",
        "dimension": "spatial",
        "value": { "asWKT": "POLYGON((-25 25,45 25,45 71.5,-25 71.5,-25 25))" }
      },
      {
        "id": "nukleus-domain",
        "role": "can-run-on",
        "dimension": "spatial",
        "value": { "asWKT": "POLYGON((1.6198 44.8502,18.2799 44.8502,18.2799 56.2362,1.6198 56.2362,1.6198 44.8502))" }
      },
      {
        "id": "eobs-reference-period",
        "role": "derived-from",
        "dimension": "temporal",
        "value": { "startDate": "1991", "endDate": "2020" }
      },
      { "id": "gwl-2", "role": "can-run-on", "dimension": "temporal", "value": { "scenarioMarker": "gwl-2.0" } },
      { "id": "gwl-3", "role": "can-run-on", "dimension": "temporal", "value": { "scenarioMarker": "gwl-3.0" } },
      {
        "id": "supported-grids",
        "role": "can-run-on",
        "dimension": "grid-structure",
        "value": { "gridTypes": ["regular-latlon", "rotated-pole"] }
      }
    ],
    "artifacts": [
      {
        "id": "precipitation",
        "artifact": "precipitation input dataset (E-OBS or the NUKLEUS regional climate ensemble, read from the FOCAL STAC catalogue)",
        "artifactRole": "workflow-input",
        "artifactRef": "/inputs/precipitation",
        "acceptanceCriteria": {
          "variables": [{ "sameAsCurrent": true, "units": ["MilliM", "KiloGM-PER-M2-SEC"] }],
          "axes": ["time"],
          "gridTypes": ["regular-latlon", "rotated-pole"],
          "transferabilityNotes": "Matching the variable name is not the whole requirement: the variable must be the precipitation quantity the workflow needs, and the time axis must support the selected accumulation window. The name depends on the source (`pr` for NUKLEUS, `rr` for E-OBS). The current interface offers no user upload of precipitation; these criteria describe a compatible source if another were connected."
        }
      },
      {
        "id": "threshold-subdaily",
        "artifact": "pre-computed 95th/99th percentile thresholds for the 6-hour and 12-hour accumulation windows (DWD station data, Germany)",
        "artifactRole": "workflow-input",
        "artifactRef": "/inputs/threshold_subdaily",
        "acceptanceCriteria": {
          "variables": [{ "units": ["MilliM"] }],
          "transferabilityNotes": "A custom threshold is a positive value in mm for an accumulation window, for either threshold set. It need not follow the percentile method; P99 is the default and P95 is also available."
        }
      },
      {
        "id": "threshold-daily",
        "artifact": "pre-computed 95th/99th percentile thresholds for the 1-day and 7-day accumulation windows (E-OBS, Europe)",
        "artifactRole": "workflow-input",
        "artifactRef": "/inputs/threshold_daily",
        "acceptanceCriteria": {
          "variables": [{ "units": ["MilliM"] }]
        }
      },
      {
        "id": "focal-stac-loader",
        "artifact": "FOCAL STAC data loader, built into the workflow",
        "artifactRole": "infrastructure"
      },
      {
        "id": "exposure",
        "artifact": "exposure layers (Local Climate Zones, imperviousness, population)",
        "artifactRole": "workflow-input",
        "artifactRef": "/inputs/exposure_layers",
        "transferabilityNotes": "Contextual overlay, not part of the calculation. The current interface offers no user upload of your own data; that is a current limitation, not a permanent one, and no replacement contract is defined."
      },
      {
        "id": "vulnerability",
        "artifact": "vulnerability index at NUTS3 level (Risk Data Hub)",
        "artifactRole": "workflow-input",
        "artifactRef": "/inputs/vulnerability_index",
        "transferabilityNotes": "Contextual overlay with the same limitation. The NUTS3 resolution limits how finely the result can be read; it is not a transferability boundary. The layer is available through the FOCAL STAC; the source data is from the Risk Data Hub. A higher-resolution indicator is under development in WP7."
      }
    ],
    "rules": [
      {
        "appliesTo": ["threshold-subdaily", "threshold-daily"],
        "when": [{ "constraint": "threshold-climate-regime", "test": "outside" }],
        "actions": ["replace-with-local-equivalent"],
        "mandatory": false,
        "transferabilityNotes": "Skipping this is allowed: the supplied reference thresholds still run, but they are benchmarks from German and European observations, not locally calibrated, so interpretation outside that regime is weaker. A custom value is a workflow parameter and needs no code change."
      },
      {
        "appliesTo": ["precipitation"],
        "when": [
          { "constraint": "eobs-coverage", "test": "outside" },
          { "constraint": "nukleus-domain", "test": "outside" }
        ],
        "actions": ["replace-with-local-equivalent"],
        "mandatory": true
      },
      {
        "appliesTo": ["precipitation"],
        "when": [{ "constraint": "supported-grids", "test": "outside" }],
        "actions": ["component-not-executable"],
        "affects": ["/steps/accumulation", "/steps/blue_spot_detection", "/steps/exposure_overlay", "/steps/vulnerability_overlay"],
        "mandatory": true,
        "transferabilityNotes": "The calculation cannot proceed on an unsupported grid without regridding or support in the code."
      },
      {
        "appliesTo": ["focal-stac-loader"],
        "triggeredBy": "different-dataset",
        "actions": ["replace-with-local-equivalent"],
        "mandatory": true
      },
      {
        "appliesTo": ["exposure", "vulnerability"],
        "when": [{ "constraint": "eu-input-coverage", "test": "outside" }],
        "actions": ["component-not-executable"],
        "affects": ["/steps/exposure_overlay", "/steps/vulnerability_overlay"],
        "mandatory": false,
        "transferabilityNotes": "When a contextual layer does not cover the selected area, that overlay cannot be shown with the built-in data; the precipitation calculation still runs."
      }
    ],
    "transferabilityNotes": "Which accumulation windows a precipitation source supports (E-OBS: 1 d and 7 d; hourly NUKLEUS: also 6 h and 12 h) depends on the source. The AOI is a rectangular WGS84 bounding box; other geometries are still open. Climate-state mode (NUKLEUS ssp370-GWL2K and GWL3K experiments, nine GCM-RCM combinations of 30 model years) is bounded by predefined historical and GWL states, while calendar mode is bounded by the dataset's coverage; accumulation windows are processed independently."
  },
  "computationType": "deterministic-rule-based",
  "maturityStatus": "pre-operational",
  "qualityAnnotation": [
    {
      "dimension": "decision-support-only",
      "note": "The Blue Spot is precipitation-hazard information shown with contextual exposure and vulnerability layers. It supports flood-risk interpretation but is not hydrological flood modelling or a quantitative flood risk, and the layers are not combined into a risk score. Spatial overlap should not by itself be read as where flood risk is highest."
    },
    {
      "dimension": "intended-use-limit",
      "note": "The reference thresholds are benchmarks derived from specific observational datasets and regions (DWD stations for 6 h and 12 h, E-OBS 1991-2020 for 1 d and 7 d); they are not automatically locally calibrated thresholds for the target area."
    },
    {
      "dimension": "intended-use-limit",
      "note": "NUKLEUS climate-state results describe a climate state: model years are realizations, not forecasts for calendar years, the GWL year windows are model-specific, and the historical state is a baseline, not present-day conditions."
    },
    {
      "dimension": "intended-use-limit",
      "note": "Climate-state and uncertainty outputs depend on the number of model years and model combinations; smaller samples still run, but some statistics then have a more limited interpretation."
    },
    {
      "dimension": "spatial-support-mismatch",
      "note": "Question 7: the vulnerability index is provided at NUTS3 level, 'coarser than the precipitation grid and does not align exactly with the AOI boundary'. The overlay can therefore be read no finer than a NUTS3 region, whatever resolution the blue-spot map itself carries, and NUTS3 units straddling the AOI edge are only partly covered. This holds in the source deployment as much as in any target: it bounds how far a result can be read, not whether the workflow moves."
    }
  ]
}

```

#### jsonld
```jsonld
{
  "@context": "https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/workflow/context.jsonld",
  "class": "Workflow",
  "id": "",
  "cwlVersion": "v1.2",
  "label": "UP-WF3 \u2014 Urban blue-spot flood risk",
  "requirements": {
    "SoftwareRequirement": {
      "packages": [
        {
          "package": "python",
          "version": [
            "3.10"
          ]
        },
        {
          "package": "xarray"
        },
        {
          "package": "numpy"
        },
        {
          "package": "pandas"
        },
        {
          "package": "rasterio"
        }
      ]
    },
    "NetworkAccess": {
      "networkAccess": true
    }
  },
  "inputs": {
    "precipitation": {
      "type": "File"
    },
    "aoi_bbox": {
      "type": "double[]",
      "label": "Rectangular WGS84 bounding box: west, south, east, north"
    },
    "threshold_subdaily": {
      "type": "File"
    },
    "threshold_daily": {
      "type": "File"
    },
    "exposure_layers": {
      "type": "File?"
    },
    "vulnerability_index": {
      "type": "File?"
    }
  },
  "steps": {
    "accumulation": {
      "run": "#accumulation.cwl",
      "in": {
        "precipitation": "precipitation"
      },
      "out": [
        "accumulated_precipitation"
      ]
    },
    "blue_spot_detection": {
      "run": "#blue_spot_detection.cwl",
      "in": {
        "accumulated": "accumulation/accumulated_precipitation",
        "threshold": "threshold_daily"
      },
      "out": [
        "blue_spot_map"
      ]
    },
    "exposure_overlay": {
      "run": "#exposure_overlay.cwl",
      "in": {
        "blue_spots": "blue_spot_detection/blue_spot_map",
        "exposure": "exposure_layers"
      },
      "out": [
        "exposure_map"
      ]
    },
    "vulnerability_overlay": {
      "run": "#vulnerability_overlay.cwl",
      "in": {
        "blue_spots": "blue_spot_detection/blue_spot_map",
        "vulnerability": "vulnerability_index"
      },
      "out": [
        "vulnerability_map"
      ]
    }
  },
  "transferability": {
    "trainingRequired": false,
    "envelope": [
      {
        "id": "dwd-stations",
        "role": "derived-from",
        "dimension": "spatial",
        "value": {
          "asWKT": "MULTIPOLYGON (((8.57 47.78, 8.43 47.59, 7.57 47.61, 7.62 48.16, 8.13 48.97, 6.74 49.16, 6.34 49.45, 6.49 49.8, 6.11 50.09, 6.34 50.45, 5.86 51.03, 6.13 51.15, 6.2 51.45, 5.95 51.8, 6.74 51.91, 6.72 52.08, 7.02 52.27, 7 52.42, 6.69 52.53, 7.01 52.63, 7.18 52.97, 7.2 53.28, 7.05 53.38, 7.21 53.65, 8.01 53.69, 8.11 53.47, 8.33 53.61, 8.5 53.39, 8.62 53.88, 9.21 53.86, 9.59 53.6, 9.78 53.55, 9.31 53.86, 8.98 53.93, 8.91 54.26, 8.64 54.29, 8.96 54.54, 8.67 54.9, 9.62 54.86, 10.02 54.67, 9.87 54.47, 11.01 54.38, 11.01 54.18, 10.81 54.08, 10.92 54, 11.4 53.94, 12.58 54.47, 13.03 54.41, 13.45 54.14, 13.72 54.15, 13.87 53.85, 14.26 53.73, 14.41 53.2, 14.13 52.88, 14.62 52.53, 14.55 52.36, 14.75 52.08, 14.6 51.83, 14.72 51.52, 14.94 51.44, 14.96 51.1, 14.77 50.82, 14.32 51.04, 14.37 50.9, 12.94 50.41, 12.55 50.39, 12.28 50.18, 12.09 50.27, 12.51 49.9, 12.39 49.74, 12.63 49.46, 13.77 48.82, 13.79 48.59, 13.49 48.58, 13.37 48.36, 12.76 48.11, 13.05 47.66, 13.01 47.48, 12.21 47.72, 11.04 47.39, 10.44 47.55, 10.18 47.28, 9.97 47.51, 8.57 47.78)), ((13.36 54.25, 13.16 54.36, 13.18 54.54, 13.42 54.7, 13.71 54.38, 13.36 54.25)), ((13.93 53.88, 13.83 54.13, 14.04 54.03, 14.21 53.95, 13.93 53.88)), ((11.13 54.42, 11.01 54.47, 11.08 54.53, 11.28 54.42, 11.13 54.42)), ((8.41 55.06, 8.38 54.9, 8.63 54.89, 8.31 54.79, 8.41 55.06)), ((8.55 54.69, 8.4 54.71, 8.51 54.76, 8.55 54.69)))"
        }
      },
      {
        "id": "eobs-extent",
        "role": "derived-from",
        "dimension": "spatial",
        "value": {
          "asWKT": "POLYGON((-25 25,45 25,45 71.5,-25 71.5,-25 25))"
        }
      },
      {
        "id": "threshold-climate-regime",
        "role": "valid-for",
        "dimension": "climatic",
        "value": "the German and European climate regime the pre-computed percentile thresholds were derived from"
      },
      {
        "id": "eu-input-coverage",
        "role": "can-run-on",
        "dimension": "spatial",
        "value": {
          "asWKT": "MULTIPOLYGON (((-8.79 39.08, -9.48 38.8, -8.66 41.03, -9.18 43.17, -7.7 43.76, -1.99 43.35, -1.08 45.53, -0.83 45.38, -0.69 45.09, -0.55 45, -1.74 47.22, -4.72 48.54, -1.38 48.65, -1.86 49.68, 0.42 49.45, 1.77 50.94, 4.23 51.39, 3.45 51.54, 4.27 51.47, 5.53 53.27, 9.78 53.55, 8.13 55.6, 8.16 56.61, 9.2 56.7, 8.27 56.75, 8.62 57.11, 10.61 57.74, 10.28 56.62, 10.89 56.36, 9.45 55.04, 10.92 54, 12.58 54.47, 13.72 54.15, 13.95 53.8, 14.58 53.64, 13.83 54.13, 18.09 54.84, 22.73 54.35, 22.57 55.06, 21.2 55.34, 21.46 57.32, 24.28 57.17, 24.53 58.35, 23.43 58.92, 24.38 59.47, 28.15 59.37, 27.35 57.53, 28.15 56.14, 26.59 55.67, 25.75 54.16, 23.48 53.94, 23.92 52.77, 23.18 52.29, 24.09 50.53, 22.13 48.41, 24.89 47.72, 26.9 48.21, 28.24 46.64, 28.21 45.45, 29.71 45.26, 27.48 42.47, 28.01 41.97, 26.58 41.95, 26.04 40.73, 23.76 40.75, 23.95 39.97, 22.63 40.5, 23.33 39.17, 22.57 38.87, 24.02 38.14, 22.73 37.54, 23.16 36.45, 21.12 37.89, 23.15 38.18, 21.18 38.35, 20 39.71, 20.96 40.85, 22.93 41.36, 22.34 42.31, 22.73 44.57, 19.61 46.17, 18.84 45.84, 19.01 44.87, 15.79 45.18, 17.59 42.94, 15.99 43.52, 14.55 45.3, 13.86 44.84, 13.63 45.77, 12.27 45.45, 12.4 44.22, 14.18 42.51, 18.46 40.22, 16.93 40.46, 16.52 39.75, 17.17 39, 16.06 37.94, 15.69 39.99, 8.77 44.42, 6.12 43.07, 3.26 43.19, 3.25 41.94, 0.71 40.82, -0.33 39.52, 0.2 38.76, -2.11 36.78, -5.63 36.03, -6.86 37.28, -8.74 37.07, -8.79 39.08)), ((-7.85 54.22, -6.18 54.05, -6.32 52.25, -10.12 51.6, -9.6 51.87, -10.36 52.21, -8.78 52.68, -9.92 52.57, -8.93 53.21, -10.09 53.41, -9.58 53.81, -10.09 54.22, -6.96 55.24, -7.85 54.22)), ((12.88 61.35, 12.16 61.72, 12.18 63.6, 14.06 64.1, 13.65 64.58, 14.54 66.13, 16.78 67.9, 21.27 69.27, 24.94 68.59, 26.53 69.92, 29.33 69.47, 28.41 68.9, 29.99 67.67, 29.07 66.89, 30.09 65.79, 29.6 64.97, 30.53 64.08, 29.99 63.74, 31.54 62.92, 29.25 61.29, 23.02 59.82, 21.44 60.6, 21.55 63.2, 25.37 65.01, 24.63 65.86, 22.4 65.86, 20.76 63.87, 17.38 62.46, 17.25 60.7, 18.99 59.83, 16.21 58.64, 16.92 58.49, 15.92 56.17, 12.89 55.41, 12.88 56.62, 11.25 58.37, 12.88 61.35)))"
        }
      },
      {
        "id": "eobs-coverage",
        "role": "can-run-on",
        "dimension": "spatial",
        "value": {
          "asWKT": "POLYGON((-25 25,45 25,45 71.5,-25 71.5,-25 25))"
        }
      },
      {
        "id": "nukleus-domain",
        "role": "can-run-on",
        "dimension": "spatial",
        "value": {
          "asWKT": "POLYGON((1.6198 44.8502,18.2799 44.8502,18.2799 56.2362,1.6198 56.2362,1.6198 44.8502))"
        }
      },
      {
        "id": "eobs-reference-period",
        "role": "derived-from",
        "dimension": "temporal",
        "value": {
          "startDate": "1991",
          "endDate": "2020"
        }
      },
      {
        "id": "gwl-2",
        "role": "can-run-on",
        "dimension": "temporal",
        "value": {
          "scenarioMarker": "gwl-2.0"
        }
      },
      {
        "id": "gwl-3",
        "role": "can-run-on",
        "dimension": "temporal",
        "value": {
          "scenarioMarker": "gwl-3.0"
        }
      },
      {
        "id": "supported-grids",
        "role": "can-run-on",
        "dimension": "grid-structure",
        "value": {
          "gridTypes": [
            "regular-latlon",
            "rotated-pole"
          ]
        }
      }
    ],
    "artifacts": [
      {
        "id": "precipitation",
        "artifact": "precipitation input dataset (E-OBS or the NUKLEUS regional climate ensemble, read from the FOCAL STAC catalogue)",
        "artifactRole": "workflow-input",
        "artifactRef": "/inputs/precipitation",
        "acceptanceCriteria": {
          "variables": [
            {
              "sameAsCurrent": true,
              "units": [
                "MilliM",
                "KiloGM-PER-M2-SEC"
              ]
            }
          ],
          "axes": [
            "time"
          ],
          "gridTypes": [
            "regular-latlon",
            "rotated-pole"
          ],
          "transferabilityNotes": "Matching the variable name is not the whole requirement: the variable must be the precipitation quantity the workflow needs, and the time axis must support the selected accumulation window. The name depends on the source (`pr` for NUKLEUS, `rr` for E-OBS). The current interface offers no user upload of precipitation; these criteria describe a compatible source if another were connected."
        }
      },
      {
        "id": "threshold-subdaily",
        "artifact": "pre-computed 95th/99th percentile thresholds for the 6-hour and 12-hour accumulation windows (DWD station data, Germany)",
        "artifactRole": "workflow-input",
        "artifactRef": "/inputs/threshold_subdaily",
        "acceptanceCriteria": {
          "variables": [
            {
              "units": [
                "MilliM"
              ]
            }
          ],
          "transferabilityNotes": "A custom threshold is a positive value in mm for an accumulation window, for either threshold set. It need not follow the percentile method; P99 is the default and P95 is also available."
        }
      },
      {
        "id": "threshold-daily",
        "artifact": "pre-computed 95th/99th percentile thresholds for the 1-day and 7-day accumulation windows (E-OBS, Europe)",
        "artifactRole": "workflow-input",
        "artifactRef": "/inputs/threshold_daily",
        "acceptanceCriteria": {
          "variables": [
            {
              "units": [
                "MilliM"
              ]
            }
          ]
        }
      },
      {
        "id": "focal-stac-loader",
        "artifact": "FOCAL STAC data loader, built into the workflow",
        "artifactRole": "infrastructure"
      },
      {
        "id": "exposure",
        "artifact": "exposure layers (Local Climate Zones, imperviousness, population)",
        "artifactRole": "workflow-input",
        "artifactRef": "/inputs/exposure_layers",
        "transferabilityNotes": "Contextual overlay, not part of the calculation. The current interface offers no user upload of your own data; that is a current limitation, not a permanent one, and no replacement contract is defined."
      },
      {
        "id": "vulnerability",
        "artifact": "vulnerability index at NUTS3 level (Risk Data Hub)",
        "artifactRole": "workflow-input",
        "artifactRef": "/inputs/vulnerability_index",
        "transferabilityNotes": "Contextual overlay with the same limitation. The NUTS3 resolution limits how finely the result can be read; it is not a transferability boundary. The layer is available through the FOCAL STAC; the source data is from the Risk Data Hub. A higher-resolution indicator is under development in WP7."
      }
    ],
    "rules": [
      {
        "appliesTo": [
          "threshold-subdaily",
          "threshold-daily"
        ],
        "when": [
          {
            "constraint": "threshold-climate-regime",
            "test": "outside"
          }
        ],
        "actions": [
          "replace-with-local-equivalent"
        ],
        "mandatory": false,
        "transferabilityNotes": "Skipping this is allowed: the supplied reference thresholds still run, but they are benchmarks from German and European observations, not locally calibrated, so interpretation outside that regime is weaker. A custom value is a workflow parameter and needs no code change."
      },
      {
        "appliesTo": [
          "precipitation"
        ],
        "when": [
          {
            "constraint": "eobs-coverage",
            "test": "outside"
          },
          {
            "constraint": "nukleus-domain",
            "test": "outside"
          }
        ],
        "actions": [
          "replace-with-local-equivalent"
        ],
        "mandatory": true
      },
      {
        "appliesTo": [
          "precipitation"
        ],
        "when": [
          {
            "constraint": "supported-grids",
            "test": "outside"
          }
        ],
        "actions": [
          "component-not-executable"
        ],
        "affects": [
          "/steps/accumulation",
          "/steps/blue_spot_detection",
          "/steps/exposure_overlay",
          "/steps/vulnerability_overlay"
        ],
        "mandatory": true,
        "transferabilityNotes": "The calculation cannot proceed on an unsupported grid without regridding or support in the code."
      },
      {
        "appliesTo": [
          "focal-stac-loader"
        ],
        "triggeredBy": "different-dataset",
        "actions": [
          "replace-with-local-equivalent"
        ],
        "mandatory": true
      },
      {
        "appliesTo": [
          "exposure",
          "vulnerability"
        ],
        "when": [
          {
            "constraint": "eu-input-coverage",
            "test": "outside"
          }
        ],
        "actions": [
          "component-not-executable"
        ],
        "affects": [
          "/steps/exposure_overlay",
          "/steps/vulnerability_overlay"
        ],
        "mandatory": false,
        "transferabilityNotes": "When a contextual layer does not cover the selected area, that overlay cannot be shown with the built-in data; the precipitation calculation still runs."
      }
    ],
    "transferabilityNotes": "Which accumulation windows a precipitation source supports (E-OBS: 1 d and 7 d; hourly NUKLEUS: also 6 h and 12 h) depends on the source. The AOI is a rectangular WGS84 bounding box; other geometries are still open. Climate-state mode (NUKLEUS ssp370-GWL2K and GWL3K experiments, nine GCM-RCM combinations of 30 model years) is bounded by predefined historical and GWL states, while calendar mode is bounded by the dataset's coverage; accumulation windows are processed independently."
  },
  "computationType": "deterministic-rule-based",
  "maturityStatus": "pre-operational",
  "qualityAnnotation": [
    {
      "dimension": "decision-support-only",
      "note": "The Blue Spot is precipitation-hazard information shown with contextual exposure and vulnerability layers. It supports flood-risk interpretation but is not hydrological flood modelling or a quantitative flood risk, and the layers are not combined into a risk score. Spatial overlap should not by itself be read as where flood risk is highest."
    },
    {
      "dimension": "intended-use-limit",
      "note": "The reference thresholds are benchmarks derived from specific observational datasets and regions (DWD stations for 6 h and 12 h, E-OBS 1991-2020 for 1 d and 7 d); they are not automatically locally calibrated thresholds for the target area."
    },
    {
      "dimension": "intended-use-limit",
      "note": "NUKLEUS climate-state results describe a climate state: model years are realizations, not forecasts for calendar years, the GWL year windows are model-specific, and the historical state is a baseline, not present-day conditions."
    },
    {
      "dimension": "intended-use-limit",
      "note": "Climate-state and uncertainty outputs depend on the number of model years and model combinations; smaller samples still run, but some statistics then have a more limited interpretation."
    },
    {
      "dimension": "spatial-support-mismatch",
      "note": "Question 7: the vulnerability index is provided at NUTS3 level, 'coarser than the precipitation grid and does not align exactly with the AOI boundary'. The overlay can therefore be read no finer than a NUTS3 region, whatever resolution the blue-spot map itself carries, and NUTS3 units straddling the AOI edge are only partly covered. This holds in the source deployment as much as in any target: it bounds how far a result can be read, not whether the workflow moves."
    }
  ]
}
```

#### ttl
```ttl
@prefix cwl: <https://w3id.org/cwl/cwl#> .
@prefix dcat: <http://www.w3.org/ns/dcat#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix dqv: <http://www.w3.org/ns/dqv#> .
@prefix focal-transf-prop: <https://w3id.org/ogc/hosted/focal/transferability/properties/> .
@prefix geo: <http://www.opengis.net/ont/geosparql#> .
@prefix ns1: <https://w3id.org/cwl/cwl#Workflow/> .
@prefix ns2: <https://w3id.org/cwl/cwl#SoftwarePackage/> .
@prefix ns3: <https://w3id.org/cwl/cwl#SoftwareRequirement/> .
@prefix ns4: <https://w3id.org/cwl/cwl#NetworkAccess/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix sld: <https://w3id.org/cwl/salad#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/> a cwl:Workflow ;
    rdfs:label "UP-WF3 — Urban blue-spot flood risk" ;
    ns1:steps <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/accumulation>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/blue_spot_detection>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/exposure_overlay>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/vulnerability_overlay> ;
    cwl:inputs <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/aoi_bbox>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/exposure_layers>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/precipitation>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/threshold_daily>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/threshold_subdaily>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/vulnerability_index> ;
    cwl:requirements [ a cwl:SoftwareRequirement ;
            ns3:packages [ ns2:package "xarray" ],
                [ ns2:package "python" ;
                    ns2:version "3.10" ],
                [ ns2:package "pandas" ],
                [ ns2:package "numpy" ],
                [ ns2:package "rasterio" ] ],
        [ a cwl:NetworkAccess ;
            ns4:networkAccess true ] ;
    focal-transf-prop:computationType <https://w3id.org/ogc/hosted/focal/transferability/computation-types/deterministic-rule-based> ;
    focal-transf-prop:maturityStatus <https://w3id.org/ogc/hosted/focal/transferability/maturity-statuses/pre-operational> ;
    focal-transf-prop:qualityAnnotation [ dqv:inDimension <https://w3id.org/ogc/hosted/focal/transferability/quality-dimensions/spatial-support-mismatch> ;
            focal-transf-prop:note "Question 7: the vulnerability index is provided at NUTS3 level, 'coarser than the precipitation grid and does not align exactly with the AOI boundary'. The overlay can therefore be read no finer than a NUTS3 region, whatever resolution the blue-spot map itself carries, and NUTS3 units straddling the AOI edge are only partly covered. This holds in the source deployment as much as in any target: it bounds how far a result can be read, not whether the workflow moves." ],
        [ dqv:inDimension <https://w3id.org/ogc/hosted/focal/transferability/quality-dimensions/intended-use-limit> ;
            focal-transf-prop:note "NUKLEUS climate-state results describe a climate state: model years are realizations, not forecasts for calendar years, the GWL year windows are model-specific, and the historical state is a baseline, not present-day conditions." ],
        [ dqv:inDimension <https://w3id.org/ogc/hosted/focal/transferability/quality-dimensions/intended-use-limit> ;
            focal-transf-prop:note "Climate-state and uncertainty outputs depend on the number of model years and model combinations; smaller samples still run, but some statistics then have a more limited interpretation." ],
        [ dqv:inDimension <https://w3id.org/ogc/hosted/focal/transferability/quality-dimensions/decision-support-only> ;
            focal-transf-prop:note "The Blue Spot is precipitation-hazard information shown with contextual exposure and vulnerability layers. It supports flood-risk interpretation but is not hydrological flood modelling or a quantitative flood risk, and the layers are not combined into a risk score. Spatial overlap should not by itself be read as where flood risk is highest." ],
        [ dqv:inDimension <https://w3id.org/ogc/hosted/focal/transferability/quality-dimensions/intended-use-limit> ;
            focal-transf-prop:note "The reference thresholds are benchmarks derived from specific observational datasets and regions (DWD stations for 6 h and 12 h, E-OBS 1991-2020 for 1 d and 7 d); they are not automatically locally calibrated thresholds for the target area." ] ;
    focal-transf-prop:transferability [ rdfs:comment "Which accumulation windows a precipitation source supports (E-OBS: 1 d and 7 d; hourly NUKLEUS: also 6 h and 12 h) depends on the source. The AOI is a rectangular WGS84 bounding box; other geometries are still open. Climate-state mode (NUKLEUS ssp370-GWL2K and GWL3K experiments, nine GCM-RCM combinations of 30 model years) is bounded by predefined historical and GWL states, while calendar mode is bounded by the dataset's coverage; accumulation windows are processed independently." ;
            focal-transf-prop:artifacts <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/exposure>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/focal-stac-loader>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/precipitation>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/threshold-daily>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/threshold-subdaily>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/vulnerability> ;
            focal-transf-prop:envelope <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/dwd-stations>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/eobs-coverage>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/eobs-extent>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/eobs-reference-period>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/eu-input-coverage>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/gwl-2>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/gwl-3>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/nukleus-domain>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/supported-grids>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/threshold-climate-regime> ;
            focal-transf-prop:rules [ rdfs:comment "Skipping this is allowed: the supplied reference thresholds still run, but they are benchmarks from German and European observations, not locally calibrated, so interpretation outside that regime is weaker. A custom value is a workflow parameter and needs no code change." ;
                    focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/replace-with-local-equivalent> ;
                    focal-transf-prop:appliesTo <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/threshold-daily>,
                        <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/threshold-subdaily> ;
                    focal-transf-prop:mandatory false ;
                    focal-transf-prop:when [ focal-transf-prop:constraint <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/threshold-climate-regime> ;
                            focal-transf-prop:test <https://w3id.org/ogc/hosted/focal/transferability/tests/outside> ] ],
                [ rdfs:comment "The calculation cannot proceed on an unsupported grid without regridding or support in the code." ;
                    focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/component-not-executable> ;
                    focal-transf-prop:affects "/steps/accumulation",
                        "/steps/blue_spot_detection",
                        "/steps/exposure_overlay",
                        "/steps/vulnerability_overlay" ;
                    focal-transf-prop:appliesTo <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/precipitation> ;
                    focal-transf-prop:mandatory true ;
                    focal-transf-prop:when [ focal-transf-prop:constraint <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/supported-grids> ;
                            focal-transf-prop:test <https://w3id.org/ogc/hosted/focal/transferability/tests/outside> ] ],
                [ rdfs:comment "When a contextual layer does not cover the selected area, that overlay cannot be shown with the built-in data; the precipitation calculation still runs." ;
                    focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/component-not-executable> ;
                    focal-transf-prop:affects "/steps/exposure_overlay",
                        "/steps/vulnerability_overlay" ;
                    focal-transf-prop:appliesTo <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/exposure>,
                        <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/vulnerability> ;
                    focal-transf-prop:mandatory false ;
                    focal-transf-prop:when [ focal-transf-prop:constraint <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/eu-input-coverage> ;
                            focal-transf-prop:test <https://w3id.org/ogc/hosted/focal/transferability/tests/outside> ] ],
                [ focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/replace-with-local-equivalent> ;
                    focal-transf-prop:appliesTo <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/precipitation> ;
                    focal-transf-prop:mandatory true ;
                    focal-transf-prop:when [ focal-transf-prop:constraint <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/eobs-coverage> ;
                            focal-transf-prop:test <https://w3id.org/ogc/hosted/focal/transferability/tests/outside> ],
                        [ focal-transf-prop:constraint <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/nukleus-domain> ;
                            focal-transf-prop:test <https://w3id.org/ogc/hosted/focal/transferability/tests/outside> ] ],
                [ focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/replace-with-local-equivalent> ;
                    focal-transf-prop:appliesTo <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/focal-stac-loader> ;
                    focal-transf-prop:mandatory true ;
                    focal-transf-prop:triggeredBy <https://w3id.org/ogc/hosted/focal/transferability/triggers/different-dataset> ] ;
            focal-transf-prop:trainingRequired false ] .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/accumulation> cwl:in "precipitation" ;
    cwl:out <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/accumulated_precipitation> ;
    cwl:run <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/#accumulation.cwl> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/aoi_bbox> rdfs:label "Rectangular WGS84 bounding box: west, south, east, north" ;
    sld:type <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/double[]> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/blue_spot_detection> cwl:in "accumulation/accumulated_precipitation",
        "threshold_daily" ;
    cwl:out <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/blue_spot_map> ;
    cwl:run <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/#blue_spot_detection.cwl> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/dwd-stations> focal-transf-prop:dimension <https://w3id.org/ogc/hosted/focal/transferability/dimensions/spatial> ;
    focal-transf-prop:role <https://w3id.org/ogc/hosted/focal/transferability/roles/derived-from> ;
    focal-transf-prop:value [ geo:asWKT "MULTIPOLYGON (((8.57 47.78, 8.43 47.59, 7.57 47.61, 7.62 48.16, 8.13 48.97, 6.74 49.16, 6.34 49.45, 6.49 49.8, 6.11 50.09, 6.34 50.45, 5.86 51.03, 6.13 51.15, 6.2 51.45, 5.95 51.8, 6.74 51.91, 6.72 52.08, 7.02 52.27, 7 52.42, 6.69 52.53, 7.01 52.63, 7.18 52.97, 7.2 53.28, 7.05 53.38, 7.21 53.65, 8.01 53.69, 8.11 53.47, 8.33 53.61, 8.5 53.39, 8.62 53.88, 9.21 53.86, 9.59 53.6, 9.78 53.55, 9.31 53.86, 8.98 53.93, 8.91 54.26, 8.64 54.29, 8.96 54.54, 8.67 54.9, 9.62 54.86, 10.02 54.67, 9.87 54.47, 11.01 54.38, 11.01 54.18, 10.81 54.08, 10.92 54, 11.4 53.94, 12.58 54.47, 13.03 54.41, 13.45 54.14, 13.72 54.15, 13.87 53.85, 14.26 53.73, 14.41 53.2, 14.13 52.88, 14.62 52.53, 14.55 52.36, 14.75 52.08, 14.6 51.83, 14.72 51.52, 14.94 51.44, 14.96 51.1, 14.77 50.82, 14.32 51.04, 14.37 50.9, 12.94 50.41, 12.55 50.39, 12.28 50.18, 12.09 50.27, 12.51 49.9, 12.39 49.74, 12.63 49.46, 13.77 48.82, 13.79 48.59, 13.49 48.58, 13.37 48.36, 12.76 48.11, 13.05 47.66, 13.01 47.48, 12.21 47.72, 11.04 47.39, 10.44 47.55, 10.18 47.28, 9.97 47.51, 8.57 47.78)), ((13.36 54.25, 13.16 54.36, 13.18 54.54, 13.42 54.7, 13.71 54.38, 13.36 54.25)), ((13.93 53.88, 13.83 54.13, 14.04 54.03, 14.21 53.95, 13.93 53.88)), ((11.13 54.42, 11.01 54.47, 11.08 54.53, 11.28 54.42, 11.13 54.42)), ((8.41 55.06, 8.38 54.9, 8.63 54.89, 8.31 54.79, 8.41 55.06)), ((8.55 54.69, 8.4 54.71, 8.51 54.76, 8.55 54.69)))"^^geo:wktLiteral ] .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/eobs-extent> focal-transf-prop:dimension <https://w3id.org/ogc/hosted/focal/transferability/dimensions/spatial> ;
    focal-transf-prop:role <https://w3id.org/ogc/hosted/focal/transferability/roles/derived-from> ;
    focal-transf-prop:value [ geo:asWKT "POLYGON((-25 25,45 25,45 71.5,-25 71.5,-25 25))"^^geo:wktLiteral ] .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/eobs-reference-period> focal-transf-prop:dimension <https://w3id.org/ogc/hosted/focal/transferability/dimensions/temporal> ;
    focal-transf-prop:role <https://w3id.org/ogc/hosted/focal/transferability/roles/derived-from> ;
    focal-transf-prop:value [ dcat:endDate "2020" ;
            dcat:startDate "1991" ] .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/exposure_layers> sld:type <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/File> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/exposure_overlay> cwl:in "blue_spot_detection/blue_spot_map",
        "exposure_layers" ;
    cwl:out <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/exposure_map> ;
    cwl:run <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/#exposure_overlay.cwl> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/gwl-2> focal-transf-prop:dimension <https://w3id.org/ogc/hosted/focal/transferability/dimensions/temporal> ;
    focal-transf-prop:role <https://w3id.org/ogc/hosted/focal/transferability/roles/can-run-on> ;
    focal-transf-prop:value [ focal-transf-prop:scenarioMarker <https://w3id.org/ogc/hosted/focal/transferability/scenario-markers/gwl-2.0> ] .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/gwl-3> focal-transf-prop:dimension <https://w3id.org/ogc/hosted/focal/transferability/dimensions/temporal> ;
    focal-transf-prop:role <https://w3id.org/ogc/hosted/focal/transferability/roles/can-run-on> ;
    focal-transf-prop:value [ focal-transf-prop:scenarioMarker <https://w3id.org/ogc/hosted/focal/transferability/scenario-markers/gwl-3.0> ] .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/threshold_daily> sld:type cwl:File .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/threshold_subdaily> sld:type cwl:File .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/vulnerability_index> sld:type <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/File> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/vulnerability_overlay> cwl:in "blue_spot_detection/blue_spot_map",
        "vulnerability_index" ;
    cwl:out <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/vulnerability_map> ;
    cwl:run <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/#vulnerability_overlay.cwl> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/eobs-coverage> focal-transf-prop:dimension <https://w3id.org/ogc/hosted/focal/transferability/dimensions/spatial> ;
    focal-transf-prop:role <https://w3id.org/ogc/hosted/focal/transferability/roles/can-run-on> ;
    focal-transf-prop:value [ geo:asWKT "POLYGON((-25 25,45 25,45 71.5,-25 71.5,-25 25))"^^geo:wktLiteral ] .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/eu-input-coverage> focal-transf-prop:dimension <https://w3id.org/ogc/hosted/focal/transferability/dimensions/spatial> ;
    focal-transf-prop:role <https://w3id.org/ogc/hosted/focal/transferability/roles/can-run-on> ;
    focal-transf-prop:value [ geo:asWKT "MULTIPOLYGON (((-8.79 39.08, -9.48 38.8, -8.66 41.03, -9.18 43.17, -7.7 43.76, -1.99 43.35, -1.08 45.53, -0.83 45.38, -0.69 45.09, -0.55 45, -1.74 47.22, -4.72 48.54, -1.38 48.65, -1.86 49.68, 0.42 49.45, 1.77 50.94, 4.23 51.39, 3.45 51.54, 4.27 51.47, 5.53 53.27, 9.78 53.55, 8.13 55.6, 8.16 56.61, 9.2 56.7, 8.27 56.75, 8.62 57.11, 10.61 57.74, 10.28 56.62, 10.89 56.36, 9.45 55.04, 10.92 54, 12.58 54.47, 13.72 54.15, 13.95 53.8, 14.58 53.64, 13.83 54.13, 18.09 54.84, 22.73 54.35, 22.57 55.06, 21.2 55.34, 21.46 57.32, 24.28 57.17, 24.53 58.35, 23.43 58.92, 24.38 59.47, 28.15 59.37, 27.35 57.53, 28.15 56.14, 26.59 55.67, 25.75 54.16, 23.48 53.94, 23.92 52.77, 23.18 52.29, 24.09 50.53, 22.13 48.41, 24.89 47.72, 26.9 48.21, 28.24 46.64, 28.21 45.45, 29.71 45.26, 27.48 42.47, 28.01 41.97, 26.58 41.95, 26.04 40.73, 23.76 40.75, 23.95 39.97, 22.63 40.5, 23.33 39.17, 22.57 38.87, 24.02 38.14, 22.73 37.54, 23.16 36.45, 21.12 37.89, 23.15 38.18, 21.18 38.35, 20 39.71, 20.96 40.85, 22.93 41.36, 22.34 42.31, 22.73 44.57, 19.61 46.17, 18.84 45.84, 19.01 44.87, 15.79 45.18, 17.59 42.94, 15.99 43.52, 14.55 45.3, 13.86 44.84, 13.63 45.77, 12.27 45.45, 12.4 44.22, 14.18 42.51, 18.46 40.22, 16.93 40.46, 16.52 39.75, 17.17 39, 16.06 37.94, 15.69 39.99, 8.77 44.42, 6.12 43.07, 3.26 43.19, 3.25 41.94, 0.71 40.82, -0.33 39.52, 0.2 38.76, -2.11 36.78, -5.63 36.03, -6.86 37.28, -8.74 37.07, -8.79 39.08)), ((-7.85 54.22, -6.18 54.05, -6.32 52.25, -10.12 51.6, -9.6 51.87, -10.36 52.21, -8.78 52.68, -9.92 52.57, -8.93 53.21, -10.09 53.41, -9.58 53.81, -10.09 54.22, -6.96 55.24, -7.85 54.22)), ((12.88 61.35, 12.16 61.72, 12.18 63.6, 14.06 64.1, 13.65 64.58, 14.54 66.13, 16.78 67.9, 21.27 69.27, 24.94 68.59, 26.53 69.92, 29.33 69.47, 28.41 68.9, 29.99 67.67, 29.07 66.89, 30.09 65.79, 29.6 64.97, 30.53 64.08, 29.99 63.74, 31.54 62.92, 29.25 61.29, 23.02 59.82, 21.44 60.6, 21.55 63.2, 25.37 65.01, 24.63 65.86, 22.4 65.86, 20.76 63.87, 17.38 62.46, 17.25 60.7, 18.99 59.83, 16.21 58.64, 16.92 58.49, 15.92 56.17, 12.89 55.41, 12.88 56.62, 11.25 58.37, 12.88 61.35)))"^^geo:wktLiteral ] .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/exposure> dcterms:title "exposure layers (Local Climate Zones, imperviousness, population)" ;
    rdfs:comment "Contextual overlay, not part of the calculation. The current interface offers no user upload of your own data; that is a current limitation, not a permanent one, and no replacement contract is defined." ;
    focal-transf-prop:artifactRef "/inputs/exposure_layers" ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/workflow-input> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/focal-stac-loader> dcterms:title "FOCAL STAC data loader, built into the workflow" ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/infrastructure> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/nukleus-domain> focal-transf-prop:dimension <https://w3id.org/ogc/hosted/focal/transferability/dimensions/spatial> ;
    focal-transf-prop:role <https://w3id.org/ogc/hosted/focal/transferability/roles/can-run-on> ;
    focal-transf-prop:value [ geo:asWKT "POLYGON((1.6198 44.8502,18.2799 44.8502,18.2799 56.2362,1.6198 56.2362,1.6198 44.8502))"^^geo:wktLiteral ] .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/supported-grids> focal-transf-prop:dimension <https://w3id.org/ogc/hosted/focal/transferability/dimensions/grid-structure> ;
    focal-transf-prop:role <https://w3id.org/ogc/hosted/focal/transferability/roles/can-run-on> ;
    focal-transf-prop:value [ focal-transf-prop:gridType <https://w3id.org/ogc/hosted/focal/transferability/grid-types/regular-latlon>,
                <https://w3id.org/ogc/hosted/focal/transferability/grid-types/rotated-pole> ] .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/threshold-climate-regime> focal-transf-prop:dimension <https://w3id.org/ogc/hosted/focal/transferability/dimensions/climatic> ;
    focal-transf-prop:role <https://w3id.org/ogc/hosted/focal/transferability/roles/valid-for> ;
    focal-transf-prop:value "the German and European climate regime the pre-computed percentile thresholds were derived from" .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/threshold-daily> dcterms:title "pre-computed 95th/99th percentile thresholds for the 1-day and 7-day accumulation windows (E-OBS, Europe)" ;
    focal-transf-prop:acceptanceCriteria [ focal-transf-prop:variable [ focal-transf-prop:unit <http://qudt.org/vocab/unit/MilliM> ] ] ;
    focal-transf-prop:artifactRef "/inputs/threshold_daily" ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/workflow-input> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/threshold-subdaily> dcterms:title "pre-computed 95th/99th percentile thresholds for the 6-hour and 12-hour accumulation windows (DWD station data, Germany)" ;
    focal-transf-prop:acceptanceCriteria [ rdfs:comment "A custom threshold is a positive value in mm for an accumulation window, for either threshold set. It need not follow the percentile method; P99 is the default and P95 is also available." ;
            focal-transf-prop:variable [ focal-transf-prop:unit <http://qudt.org/vocab/unit/MilliM> ] ] ;
    focal-transf-prop:artifactRef "/inputs/threshold_subdaily" ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/workflow-input> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/vulnerability> dcterms:title "vulnerability index at NUTS3 level (Risk Data Hub)" ;
    rdfs:comment "Contextual overlay with the same limitation. The NUTS3 resolution limits how finely the result can be read; it is not a transferability boundary. The layer is available through the FOCAL STAC; the source data is from the Risk Data Hub. A higher-resolution indicator is under development in WP7." ;
    focal-transf-prop:artifactRef "/inputs/vulnerability_index" ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/workflow-input> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/precipitation> dcterms:title "precipitation input dataset (E-OBS or the NUKLEUS regional climate ensemble, read from the FOCAL STAC catalogue)" ;
    sld:type cwl:File ;
    focal-transf-prop:acceptanceCriteria [ rdfs:comment "Matching the variable name is not the whole requirement: the variable must be the precipitation quantity the workflow needs, and the time axis must support the selected accumulation window. The name depends on the source (`pr` for NUKLEUS, `rr` for E-OBS). The current interface offers no user upload of precipitation; these criteria describe a compatible source if another were connected." ;
            focal-transf-prop:axis <https://w3id.org/ogc/hosted/focal/transferability/axes/time> ;
            focal-transf-prop:gridType <https://w3id.org/ogc/hosted/focal/transferability/grid-types/regular-latlon>,
                <https://w3id.org/ogc/hosted/focal/transferability/grid-types/rotated-pole> ;
            focal-transf-prop:variable [ focal-transf-prop:sameAsCurrent true ;
                    focal-transf-prop:unit <http://qudt.org/vocab/unit/KiloGM-PER-M2-SEC>,
                        <http://qudt.org/vocab/unit/MilliM> ] ] ;
    focal-transf-prop:artifactRef "/inputs/precipitation" ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/workflow-input> .


```

## Schema

```yaml
$schema: https://json-schema.org/draft/2020-12/schema
title: Transferability Workflow
description: "A profile of a CWL Workflow (`ogc.cwl.v1_2_1.CWLWorkflow`) adding FOCAL's
  machine-readable transferability facts, extracted from FOCAL's 8 pilot-workflow
  questionnaires:\n- `transferability` \u2014 the workflow's portability boundary,
  one\n  [`transferabilityStatement`](bblocks://ogc.focal.transferability.transferabilityStatement)\n
  \ (its `envelope`, `artifacts` and `rules`). Required: every evidenced workflow
  states one.\n- `computationType`, `maturityStatus` \u2014 the two workflow-level
  classification mixins (see\n  [`computationType`](bblocks://ogc.focal.transferability.computationType)
  and\n  [`maturityStatus`](bblocks://ogc.focal.transferability.maturityStatus) for
  which is optional\n  and which is required).\n- `qualityAnnotation` \u2014 a repeatable,
  optional workflow-level fact (see its own block for\n  evidence density and omission
  rules).\n\n`computationType`/`maturityStatus`/`qualityAnnotation` stay outside `transferability`
  on purpose: they describe the workflow's implementation and result quality generally,
  not its portability boundary \u2014 see `transferabilityStatement` for the same
  distinction from its side.\n"
allOf:
- $ref: https://ogcincubator.github.io/bblocks-cwl/build/annotated/cwl/v1_2_1/CWLWorkflow/schema.yaml
- $ref: https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/computationType/schema.yaml
- $ref: https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/maturityStatus/schema.yaml
- type: object
  required:
  - transferability
  properties:
    id:
      $ref: https://opengeospatial.github.io/bblocks/annotated-schemas/ogc-utils/iri-or-curie/schema.yaml
      description: 'Identifier for the workflow, resolved against the document''s
        base URI. Optional, but worth setting: without it the workflow is an anonymous
        node in RDF, and its envelope constraints and artifacts end up as named resources
        hanging off a subject nothing can refer to. An empty string resolves to the
        base URI itself, i.e. "the workflow this document describes".

        '
      x-jsonld-id: '@id'
    transferability:
      $ref: https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/transferabilityStatement/schema.yaml
      description: 'The workflow''s portability boundary: where its results are valid
        (`envelope`) and which artifacts it depends on, and what must happen to each
        outside it. See `transferabilityStatement` for the three lists and how they
        reference each other.

        '
      x-jsonld-id: https://w3id.org/ogc/hosted/focal/transferability/properties/transferability
    qualityAnnotation:
      type: array
      items:
        $ref: https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/qualityAnnotation/schema.yaml
      description: 'Uncertainty/confidence statements about the workflow''s results,
        independent of `maturityStatus`. Optional and repeatable.

        '
      x-jsonld-id: https://w3id.org/ogc/hosted/focal/transferability/properties/qualityAnnotation
      x-jsonld-container: '@set'
x-jsonld-prefixes:
  focal-transf-prop: https://w3id.org/ogc/hosted/focal/transferability/properties/
x-bblocks-metadata:
  itemIdentifier: ogc.focal.transferability.workflow
  register: https://ogcincubator.github.io/bblocks-focal/build/register.json
  version: '0.18'
  dateOfLastChange: '2026-11-25'

```

Links to the schema:

* YAML version: [schema.yaml](https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/workflow/schema.json)
* JSON version: [schema.json](https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/workflow/schema.yaml)


# JSON-LD Context

```jsonld
{
  "@context": {
    "version": "cwl:SoftwarePackage/version",
    "doc": "rdfs:comment",
    "label": "rdfs:label",
    "Workflow": "cwl:Workflow",
    "class": "@type",
    "hints": {
      "@context": {
        "DockerRequirement": "cwl:DockerRequirement",
        "EnvVarRequirement": "cwl:EnvVarRequirement",
        "InitialWorkDirRequirement": "cwl:InitialWorkDirRequirement",
        "InlineJavascriptRequirement": "cwl:InlineJavascriptRequirement",
        "InplaceUpdateRequirement": "cwl:InplaceUpdateRequirement",
        "LoadListingRequirement": "cwl:LoadListingRequirement",
        "MultipleInputFeatureRequirement": "cwl:MultipleInputFeatureRequirement",
        "NetworkAccess": "cwl:NetworkAccess",
        "ResourceRequirement": "cwl:ResourceRequirement",
        "ScatterFeatureRequirement": "cwl:ScatterFeatureRequirement",
        "SchemaDefRequirement": "cwl:SchemaDefRequirement",
        "ShellCommandRequirement": "cwl:ShellCommandRequirement",
        "SoftwareRequirement": "cwl:SoftwareRequirement",
        "StepInputExpressionRequirement": "cwl:StepInputExpressionRequirement",
        "SubworkflowFeatureRequirement": "cwl:SubworkflowFeatureRequirement",
        "ToolTimeLimit": "cwl:ToolTimeLimit",
        "WorkReuse": "cwl:WorkReuse",
        "dockerFile": "cwl:DockerRequirement/dockerFile",
        "dockerImageId": "cwl:DockerRequirement/dockerImageId",
        "dockerImport": "cwl:DockerRequirement/dockerImport",
        "dockerLoad": "cwl:DockerRequirement/dockerLoad",
        "dockerOutputDirectory": "cwl:DockerRequirement/dockerOutputDirectory",
        "dockerPull": "cwl:DockerRequirement/dockerPull",
        "packages": {
          "@context": {
            "package": "cwl:SoftwarePackage/package",
            "specs": {
              "@id": "cwl:SoftwarePackage/specs",
              "@type": "@id"
            }
          },
          "@id": "cwl:SoftwareRequirement/packages",
          "@container": "@id"
        },
        "envDef": {
          "@context": {
            "envName": "cwl:EnvironmentDef/envName",
            "envValue": "cwl:EnvironmentDef/envValue"
          },
          "@id": "cwl:EnvVarRequirement/envDef",
          "@container": "@id"
        },
        "types": {
          "@context": {
            "type": {
              "@id": "sld:type",
              "@type": "@vocab"
            },
            "fields": {
              "@context": {
                "format": {
                  "@id": "cwl:format",
                  "@type": "@id"
                },
                "loadContents": "cwl:loadContents",
                "secondaryFiles": "cwl:secondaryFiles",
                "streamable": "cwl:FieldBase/streamable"
              },
              "@id": "sld:fields",
              "@container": "@id"
            },
            "name": "@id",
            "items": {
              "@id": "sld:items",
              "@type": "@vocab"
            }
          },
          "@id": "cwl:SchemaDefRequirement/types"
        },
        "listing": "cwl:listing",
        "expressionLib": "cwl:InlineJavascriptRequirement/expressionLib",
        "inplaceUpdate": "cwl:InplaceUpdateRequirement/inplaceUpdate",
        "loadListing": "cwl:loadListing",
        "networkAccess": "cwl:NetworkAccess/networkAccess",
        "coresMin": "cwl:ResourceRequirement/coresMin",
        "coresMax": "cwl:ResourceRequirement/coresMax",
        "ramMin": "cwl:ResourceRequirement/ramMin",
        "ramMax": "cwl:ResourceRequirement/ramMax",
        "outdirMin": "cwl:ResourceRequirement/outdirMin",
        "outdirMax": "cwl:ResourceRequirement/outdirMax",
        "tmpdirMin": "cwl:ResourceRequirement/tmpdirMin",
        "tmpdirMax": "cwl:ResourceRequirement/tmpdirMax",
        "timelimit": "cwl:ToolTimeLimit/timelimit",
        "enableReuse": "cwl:WorkReuse/enableReuse"
      },
      "@id": "cwl:hints",
      "@container": "@type"
    },
    "inputs": {
      "@context": {
        "default": {
          "@context": {
            "basename": "cwl:basename",
            "location": "@id",
            "nameroot": "cwl:File/nameroot",
            "path": {
              "@id": "cwl:path",
              "@type": "@id"
            }
          },
          "@id": "sld:default"
        },
        "type": {
          "@id": "sld:type",
          "@type": "@vocab"
        },
        "inputBinding": {
          "@context": {
            "itemSeparator": "cwl:CommandLineBinding/itemSeparator",
            "position": "cwl:CommandLineBinding/position",
            "prefix": "cwl:CommandLineBinding/prefix",
            "shellQuote": "cwl:CommandLineBinding/shellQuote",
            "valueFrom": "cwl:valueFrom"
          },
          "@id": "cwl:inputBinding"
        }
      },
      "@id": "cwl:inputs",
      "@container": "@id"
    },
    "outputs": {
      "@context": {
        "outputBinding": {
          "@context": {
            "glob": "cwl:CommandOutputBinding/glob"
          },
          "@id": "cwl:outputBinding"
        },
        "type": {
          "@id": "sld:type",
          "@type": "@vocab"
        }
      },
      "@id": "cwl:outputs",
      "@container": "@id"
    },
    "requirements": {
      "@context": {
        "DockerRequirement": "cwl:DockerRequirement",
        "EnvVarRequirement": "cwl:EnvVarRequirement",
        "InitialWorkDirRequirement": "cwl:InitialWorkDirRequirement",
        "InlineJavascriptRequirement": "cwl:InlineJavascriptRequirement",
        "InplaceUpdateRequirement": "cwl:InplaceUpdateRequirement",
        "LoadListingRequirement": "cwl:LoadListingRequirement",
        "MultipleInputFeatureRequirement": "cwl:MultipleInputFeatureRequirement",
        "NetworkAccess": "cwl:NetworkAccess",
        "ResourceRequirement": "cwl:ResourceRequirement",
        "ScatterFeatureRequirement": "cwl:ScatterFeatureRequirement",
        "SchemaDefRequirement": "cwl:SchemaDefRequirement",
        "ShellCommandRequirement": "cwl:ShellCommandRequirement",
        "SoftwareRequirement": "cwl:SoftwareRequirement",
        "StepInputExpressionRequirement": "cwl:StepInputExpressionRequirement",
        "SubworkflowFeatureRequirement": "cwl:SubworkflowFeatureRequirement",
        "ToolTimeLimit": "cwl:ToolTimeLimit",
        "WorkReuse": "cwl:WorkReuse",
        "dockerFile": "cwl:DockerRequirement/dockerFile",
        "dockerImageId": "cwl:DockerRequirement/dockerImageId",
        "dockerImport": "cwl:DockerRequirement/dockerImport",
        "dockerLoad": "cwl:DockerRequirement/dockerLoad",
        "dockerOutputDirectory": "cwl:DockerRequirement/dockerOutputDirectory",
        "dockerPull": "cwl:DockerRequirement/dockerPull",
        "packages": {
          "@context": {
            "package": "cwl:SoftwarePackage/package",
            "specs": {
              "@id": "cwl:SoftwarePackage/specs",
              "@type": "@id"
            }
          },
          "@id": "cwl:SoftwareRequirement/packages",
          "@container": "@id"
        },
        "envDef": {
          "@context": {
            "envName": "cwl:EnvironmentDef/envName",
            "envValue": "cwl:EnvironmentDef/envValue"
          },
          "@id": "cwl:EnvVarRequirement/envDef",
          "@container": "@id"
        },
        "types": {
          "@context": {
            "type": {
              "@id": "sld:type",
              "@type": "@vocab"
            },
            "fields": {
              "@context": {
                "format": {
                  "@id": "cwl:format",
                  "@type": "@id"
                },
                "loadContents": "cwl:loadContents",
                "secondaryFiles": "cwl:secondaryFiles",
                "streamable": "cwl:FieldBase/streamable"
              },
              "@id": "sld:fields",
              "@container": "@id"
            },
            "name": "@id",
            "items": {
              "@id": "sld:items",
              "@type": "@vocab"
            }
          },
          "@id": "cwl:SchemaDefRequirement/types"
        },
        "listing": "cwl:listing",
        "expressionLib": "cwl:InlineJavascriptRequirement/expressionLib",
        "inplaceUpdate": "cwl:InplaceUpdateRequirement/inplaceUpdate",
        "loadListing": "cwl:loadListing",
        "networkAccess": "cwl:NetworkAccess/networkAccess",
        "coresMin": "cwl:ResourceRequirement/coresMin",
        "coresMax": "cwl:ResourceRequirement/coresMax",
        "ramMin": "cwl:ResourceRequirement/ramMin",
        "ramMax": "cwl:ResourceRequirement/ramMax",
        "outdirMin": "cwl:ResourceRequirement/outdirMin",
        "outdirMax": "cwl:ResourceRequirement/outdirMax",
        "tmpdirMin": "cwl:ResourceRequirement/tmpdirMin",
        "tmpdirMax": "cwl:ResourceRequirement/tmpdirMax",
        "timelimit": "cwl:ToolTimeLimit/timelimit",
        "enableReuse": "cwl:WorkReuse/enableReuse"
      },
      "@id": "cwl:requirements",
      "@container": "@type"
    },
    "steps": {
      "@context": {
        "in": {
          "@context": {
            "linkMerge": "cwl:linkMerge",
            "source": {
              "@id": "cwl:source",
              "@type": "@id"
            },
            "valueFrom": "cwl:valueFrom",
            "default": {
              "@context": {
                "basename": "cwl:basename",
                "location": "@id",
                "nameroot": "cwl:File/nameroot",
                "path": {
                  "@id": "cwl:path",
                  "@type": "@id"
                }
              },
              "@id": "sld:default",
              "@container": "@list"
            }
          },
          "@id": "cwl:in",
          "@container": "@id"
        },
        "out": {
          "@id": "cwl:out",
          "@type": "@id"
        },
        "run": {
          "@context": {
            "arguments": {
              "@context": {
                "itemSeparator": "cwl:CommandLineBinding/itemSeparator",
                "position": "cwl:CommandLineBinding/position",
                "prefix": "cwl:CommandLineBinding/prefix",
                "shellQuote": "cwl:CommandLineBinding/shellQuote",
                "valueFrom": "cwl:valueFrom"
              },
              "@id": "cwl:arguments",
              "@container": "@list"
            },
            "baseCommand": {
              "@id": "cwl:baseCommand",
              "@container": "@list"
            },
            "intent": {
              "@id": "cwl:Process/intent",
              "@type": "@id"
            },
            "stderr": "cwl:stderr",
            "stdin": "cwl:stdin",
            "stdout": "cwl:stdout"
          },
          "@id": "cwl:run",
          "@type": "@id"
        },
        "when": "cwl:when",
        "scatter": {
          "@id": "cwl:scatter",
          "@type": "@id",
          "@container": "@list"
        },
        "scatterMethod": {
          "@id": "cwl:scatterMethod",
          "@type": "@vocab"
        }
      },
      "@id": "cwl:Workflow/steps",
      "@container": "@id"
    },
    "computationType": {
      "@context": {
        "@base": "https://w3id.org/ogc/hosted/focal/transferability/computation-types/"
      },
      "@id": "focal-transf-prop:computationType",
      "@type": "@id"
    },
    "maturityStatus": {
      "@context": {
        "@base": "https://w3id.org/ogc/hosted/focal/transferability/maturity-statuses/"
      },
      "@id": "focal-transf-prop:maturityStatus",
      "@type": "@id"
    },
    "id": "@id",
    "transferability": {
      "@context": {
        "transferabilityNotes": "rdfs:comment",
        "envelope": {
          "@context": {
            "role": {
              "@context": {
                "@base": "https://w3id.org/ogc/hosted/focal/transferability/roles/"
              },
              "@id": "focal-transf-prop:role",
              "@type": "@id"
            },
            "dimension": {
              "@context": {
                "@base": "https://w3id.org/ogc/hosted/focal/transferability/dimensions/"
              },
              "@id": "focal-transf-prop:dimension",
              "@type": "@id"
            },
            "inputRef": {
              "@id": "focal-transf-prop:inputRef",
              "@container": "@set"
            },
            "value": {
              "@context": {
                "asWKT": {
                  "@id": "geo:asWKT",
                  "@type": "geo:wktLiteral"
                },
                "startDate": "dcat:startDate",
                "endDate": "dcat:endDate",
                "scenarioMarker": {
                  "@context": {
                    "@base": "https://w3id.org/ogc/hosted/focal/transferability/scenario-markers/"
                  },
                  "@id": "focal-transf-prop:scenarioMarker",
                  "@type": "@id"
                },
                "gridTypes": {
                  "@context": {
                    "@base": "https://w3id.org/ogc/hosted/focal/transferability/grid-types/"
                  },
                  "@id": "focal-transf-prop:gridType",
                  "@type": "@id",
                  "@container": "@set"
                },
                "variables": {
                  "@context": {
                    "name": "focal-transf-prop:variableName",
                    "unit": "focal-transf-prop:unitLabel",
                    "min": {
                      "@id": "focal-transf-prop:minimum",
                      "@type": "xsd:double"
                    },
                    "max": {
                      "@id": "focal-transf-prop:maximum",
                      "@type": "xsd:double"
                    }
                  },
                  "@id": "focal-transf-prop:variableRange",
                  "@container": "@set"
                },
                "statistic": "focal-transf-prop:statistic",
                "scheme": {
                  "@context": {
                    "@base": "https://w3id.org/ogc/hosted/focal/transferability/classification-schemes/"
                  },
                  "@id": "focal-transf-prop:classificationScheme",
                  "@type": "@id"
                },
                "sameClassAs": {
                  "@id": "focal-transf-prop:sameClassAs",
                  "@type": "@id"
                },
                "classes": {
                  "@id": "focal-transf-prop:class",
                  "@container": "@set"
                }
              },
              "@id": "focal-transf-prop:value"
            }
          },
          "@id": "focal-transf-prop:envelope",
          "@container": "@set"
        },
        "noConstraintsStated": "focal-transf-prop:noConstraintsStated",
        "trainingRequired": "focal-transf-prop:trainingRequired",
        "artifacts": {
          "@context": {
            "artifact": "dct:title",
            "artifactRole": {
              "@context": {
                "@base": "https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/"
              },
              "@id": "focal-transf-prop:artifactRole",
              "@type": "@id"
            },
            "acceptanceCriteria": {
              "@context": {
                "variables": {
                  "@context": {
                    "name": "focal-transf-prop:variableName",
                    "sameAsCurrent": "focal-transf-prop:sameAsCurrent",
                    "standardName": {
                      "@id": "focal-transf-prop:standardName",
                      "@container": "@set"
                    },
                    "units": {
                      "@context": {
                        "@base": "http://qudt.org/vocab/unit/"
                      },
                      "@id": "focal-transf-prop:unit",
                      "@type": "@id",
                      "@container": "@set"
                    }
                  },
                  "@id": "focal-transf-prop:variable",
                  "@container": "@set"
                },
                "axes": {
                  "@context": {
                    "@base": "https://w3id.org/ogc/hosted/focal/transferability/axes/"
                  },
                  "@id": "focal-transf-prop:axis",
                  "@type": "@id",
                  "@container": "@set"
                },
                "gridTypes": {
                  "@context": {
                    "@base": "https://w3id.org/ogc/hosted/focal/transferability/grid-types/"
                  },
                  "@id": "focal-transf-prop:gridType",
                  "@type": "@id",
                  "@container": "@set"
                },
                "temporal": {
                  "@context": {
                    "resolution": {
                      "@id": "dcat:temporalResolution",
                      "@type": "xsd:duration"
                    },
                    "calendar": {
                      "@id": "focal-transf-prop:calendar",
                      "@container": "@set"
                    },
                    "minimumPrecedingYears": {
                      "@id": "focal-transf-prop:minimumPrecedingYears",
                      "@type": "xsd:integer"
                    },
                    "complete": "focal-transf-prop:temporalComplete",
                    "startDate": "dcat:startDate",
                    "endDate": "dcat:endDate"
                  },
                  "@id": "focal-transf-prop:temporalRequirement"
                },
                "conformsTo": {
                  "@id": "dct:conformsTo",
                  "@type": "@id",
                  "@container": "@set"
                }
              },
              "@id": "focal-transf-prop:acceptanceCriteria"
            },
            "artifactRef": {
              "@id": "focal-transf-prop:artifactRef",
              "@container": "@set"
            }
          },
          "@id": "focal-transf-prop:artifacts",
          "@container": "@set"
        },
        "rules": {
          "@context": {
            "appliesTo": {
              "@id": "focal-transf-prop:appliesTo",
              "@type": "@id",
              "@container": "@set"
            },
            "when": {
              "@context": {
                "constraint": {
                  "@id": "focal-transf-prop:constraint",
                  "@type": "@id"
                },
                "test": {
                  "@context": {
                    "@base": "https://w3id.org/ogc/hosted/focal/transferability/tests/"
                  },
                  "@id": "focal-transf-prop:test",
                  "@type": "@id"
                }
              },
              "@id": "focal-transf-prop:when",
              "@container": "@set"
            },
            "triggeredBy": {
              "@context": {
                "@base": "https://w3id.org/ogc/hosted/focal/transferability/triggers/"
              },
              "@id": "focal-transf-prop:triggeredBy",
              "@type": "@id"
            },
            "affects": {
              "@id": "focal-transf-prop:affects",
              "@container": "@set"
            },
            "actions": {
              "@context": {
                "@base": "https://w3id.org/ogc/hosted/focal/transferability/actions/"
              },
              "@id": "focal-transf-prop:actions",
              "@type": "@id",
              "@container": "@set"
            },
            "mandatory": "focal-transf-prop:mandatory"
          },
          "@id": "focal-transf-prop:rules",
          "@container": "@set"
        }
      },
      "@id": "focal-transf-prop:transferability"
    },
    "qualityAnnotation": {
      "@context": {
        "dimension": {
          "@context": {
            "@base": "https://w3id.org/ogc/hosted/focal/transferability/quality-dimensions/"
          },
          "@id": "dqv:inDimension",
          "@type": "@id"
        },
        "note": "focal-transf-prop:note"
      },
      "@id": "focal-transf-prop:qualityAnnotation",
      "@container": "@set"
    },
    "writable": "cwl:Dirent/writable",
    "checksum": "cwl:File/checksum",
    "size": "cwl:File/size",
    "null": "sld:null",
    "boolean": "xsd:boolean",
    "int": "xsd:int",
    "integer": "xsd:int",
    "long": "xsd:long",
    "float": "xsd:float",
    "double": "xsd:double",
    "string": "xsd:string",
    "File": "cwl:File",
    "Directory": "cwl:Directory",
    "BuiltinRequirement": "ogccwl:BuiltinRequirement",
    "OGCAPIRequirement": "ogccwl:OGCAPIRequirement",
    "WPS1Requirement": "ogccwl:WPS1Requirement",
    "CommandLineTool": "cwl:CommandLineTool",
    "ExpressionTool": "cwl:ExpressionTool",
    "s": "https://schema.org/",
    "cwl": "https://w3id.org/cwl/cwl#",
    "cwltool": "http://commonwl.org/cwltool#",
    "sld": "https://w3id.org/cwl/salad#",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
    "ogccwl": "https://w3id.org/ogc/cwl/",
    "dct": "http://purl.org/dc/terms/",
    "focal-transf-prop": "focal-transf:properties/",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "dcterms": "http://purl.org/dc/terms/",
    "focal-transf": "https://w3id.org/ogc/hosted/focal/transferability/",
    "prov": "http://www.w3.org/ns/prov#",
    "geo": "http://www.opengis.net/ont/geosparql#",
    "dcat": "http://www.w3.org/ns/dcat#",
    "dqv": "http://www.w3.org/ns/dqv#",
    "@version": 1.1
  }
}
```

You can find the full JSON-LD context here:
[context.jsonld](https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/workflow/context.jsonld)


# For developers

The source code for this Building Block can be found in the following repository:

* URL: [https://github.com/ogcincubator/bblocks-focal](https://github.com/ogcincubator/bblocks-focal)
* Path: `_sources/transferability/workflow`

