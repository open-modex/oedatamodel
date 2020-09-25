# Oedatamodel v1.0.0 - Technical description 

The oedatamodel release version 1.0.0 contains two datamodel´s as UML-ERM and the corresponding datapackage
for each datamodel. This section describes the technical aspects for each datamodel. 

We have created two variants of the data model to achieve different results. First we needed a good solution for 
the application of the data model in a database environment. For this purpose we have created "OEDataModel-normalization".
This data model is developed as a [joint-table inheritance](https://docs.sqlalchemy.org/en/13/orm/inheritance.html#joined-table-inheritance) data model and is in a [normalized](https://en.wikipedia.org/wiki/Database_normalization#Example_of_a_step_by_step_normalization) state. By normalizing the 
data model we eliminate redundancies (within columns) and ensure that the data model meets the general requirements of
Data to be stored on a relational database system. Common table inheritance is our solution for 
the redundancy in the data tables "timeseries" and "scalar". We introduced an aggregated "data" table to 
the data model. The "data" table contains all redundant fields from the "timeseries" data and "scalar" data tables.
By introducing a shared primary key "data_id" in all data related tables and by introducing a new field in 
aggregated "data" table named "type" we can define the data type ("scalar" or "time series") for each row in the
Table. When retrieving the data, SQL allows us to connect the data tables with each other and create a readable 
joint record. 


The other result is called "OEDataModel-concrete". This format is intended to be more user-friendly when working 
with datasets, for example, using a tool like Excel. The usability aspect that we wanted to achieve with this data 
model is to allow a user to edit a dataset in a table that contains all fields. This leads to a lot of redundant 
fields. In the data related tables, but the usability is much better for this use case. Since we need to map this 
approach to the "OEDataModel-joint" data model, the development of an adapter is required. We plan the development 
of the adapter within the next iterations of the development process. 

## Requesting scenario data from oedatamodel

An example of grabbing scenario data from OEP via json request can be found in _datamodel_json_request.py_.
In order to grab scenario data from OEP for a given scenario ID or name, the following request can be used 
(i.e. with command *curl* in linux):
<pre>
curl
    -X POST
    -H 'Content-Type: application/json'
    -H 'Authorization: Token your-token'
    -d '{
            "query": {
                "from": {
                    "type": "join",
                    "left": {
                        "type": "table",
                        "table": "oed_scenario",
                        "schema": "model_draft",
                        "alias": "s"
                    },
                    "right": {
                        "type": "join",
                        "is_full": "True",
                        "left": {
                            "type": "join",
                            "is_full": "True",
                            "left": {
                                "type": "table",
                                "table": "oed_data",
                                "schema": "model_draft",
                                "alias": "d"
                            },
                            "right": {
                                "type": "table",
                                "table": "oed_timeseries",
                                "schema": "model_draft",
                                "alias": "ts"
                            },
                            "on": {
                                "operands": [
                                    {"type": "column", "column": "id", "table": "d"},
                                    {"type": "column", "column": "id", "table": "ts"}
                                ],
                                "operator": "=",
                                "type": "operator"
                            }
                        },
                        "right": {
                            "type": "table",
                            "table": "oed_scalar",
                            "schema": "model_draft",
                            "alias": "sc"
                        },
                        "on": {
                            "operands": [
                                {"type": "column", "column": "id", "table": "d"},
                                {"type": "column", "column": "id", "table": "sc"}
                            ],
                            "operator": "=",
                            "type": "operator",
                        }
                    },
                    "on": {
                        "operands": [
                            {"type": "column", "column": "id", "table": "s"},
                            {"type": "column", "column": "scenario_id", "table": "d"}
                        ],
                        "operator": "=",
                        "type": "operator"
                    }
                },
                "where": {
                    "operands": [
                        {
                            "type": "column",
                            "table": "s",
                            "column": "id"
                        },
                        100 
                    ],
                    "operator": "=",
                    "type": "operator"
                }
            }
        }'
    'https://openenergy-platform.org/api/v0/advanced/search'
</pre>

Which will return something like:
<pre>
{
    "content": {
        "description": [
            ["id", 20, null, 8, null, null, null], 
            ["scenario", 25, null, -1, null, null, null], 
            ["region", 1009, null, -1, null, null, null], 
            ["year", 23, null, 4, null, null, null], 
            ["source", 25, null, -1, null, null, null], 
            ["comment", 25, null, -1, null, null, null], 
            ["id", 20, null, 8, null, null, null], 
            ["scenario_id", 20, null, 8, null, null, null], 
            ["region", 1009, null, -1, null, null, null], 
            ["input_energy_vector", 25, null, -1, null, null, null], 
            ["output_energy_vector", 25, null, -1, null, null, null], 
            ["parameter_name", 25, null, -1, null, null, null], 
            ["technology", 25, null, -1, null, null, null], 
            ["technology_type", 25, null, -1, null, null, null], 
            ["type", 25, null, -1, null, null, null], 
            ["unit", 25, null, -1, null, null, null], 
            ["tags", 114, null, -1, null, null, null], 
            ["method", 114, null, -1, null, null, null], 
            ["source", 25, null, -1, null, null, null], 
            ["comment", 25, null, -1, null, null, null], 
            ["id", 20, null, 8, null, null, null], 
            ["timeindex_start", 1114, null, 8, null, null, null], 
            ["timeindex_stop", 1114, null, 8, null, null, null], 
            ["timeindex_resolution", 1186, null, 16, null, null, null], 
            ["series", 1022, null, -1, null, null, null], 
            ["id", 20, null, 8, null, null, null], 
            ["value", 701, null, 8, null, null, null]
        ], 
        "rowcount": 2
    }, 
    "cursor_id": 8046029639016208186, 
    "data": [
        [100, "Test Scenario", [], 2020, "scenario source", "scenario comment", 200, 100, ["scalar region1", "scalar region2"], "scalar input vector", "scalar output vector", "scalar parameter", "scalar technology", "scalar technology type", "scalar", "scalar unit", {"scalar tags": "tag1"}, {"scalar method": "method"}, "scalar source", "scalar comment", null, null, null, null, null, 200, 20.0], 
        [100, "Test Scenario", [], 2020, "scenario source", "scenario comment", 201, 100, ["timeseries region1", "timeseries region2"], "timeseries input vector", "timeseries output vector", "timeseries parameter", "timeseries technology", "timeseries technology type", "timeseries", "timeseries unit", {"timeseries tags": "tag1"}, {"timeseries method": "method"}, "timeseries source", "timeseries comment", 201, "2020-09-01T00:00:00", "2020-09-01T12:00:00", "P1DT00H00M00S", [20.0, 30.0, 40.0], null, null]
    ], 
    "description": [
        ["id", 20, null, 8, null, null, null], 
        ["scenario", 25, null, -1, null, null, null], 
        ["region", 1009, null, -1, null, null, null], 
        ["year", 23, null, 4, null, null, null], 
        ["source", 25, null, -1, null, null, null], 
        ["comment", 25, null, -1, null, null, null], 
        ["id", 20, null, 8, null, null, null], 
        ["scenario_id", 20, null, 8, null, null, null], 
        ["region", 1009, null, -1, null, null, null], 
        ["input_energy_vector", 25, null, -1, null, null, null], 
        ["output_energy_vector", 25, null, -1, null, null, null], 
        ["parameter_name", 25, null, -1, null, null, null], 
        ["technology", 25, null, -1, null, null, null], 
        ["technology_type", 25, null, -1, null, null, null], 
        ["type", 25, null, -1, null, null, null], 
        ["unit", 25, null, -1, null, null, null], 
        ["tags", 114, null, -1, null, null, null], 
        ["method", 114, null, -1, null, null, null], 
        ["source", 25, null, -1, null, null, null], 
        ["comment", 25, null, -1, null, null, null], 
        ["id", 20, null, 8, null, null, null], 
        ["timeindex_start", 1114, null, 8, null, null, null], 
        ["timeindex_stop", 1114, null, 8, null, null, null], 
        ["timeindex_resolution", 1186, null, 16, null, null, null], 
        ["series", 1022, null, -1, null, null, null], 
        ["id", 20, null, 8, null, null, null], 
        ["value", 701, null, 8, null, null, null]
    ], 
    "rowcount": 2
}
</pre>