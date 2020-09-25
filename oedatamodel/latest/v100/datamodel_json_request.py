
import logging
import os

import requests

OEP_URL = 'https://openenergy-platform.org'
TOKEN = os.environ['OEP_TOKEN']


def insert_test_data():
    scenario = {
        'query': {
            'scenario': 'Test Scenario',
            'region': {},
            'year': 2020,
            'source': 'scenario source',
            'comment': 'scenario comment',
        },
    }
    result = requests.put(
        OEP_URL + '/api/v0/schema/model_draft/tables/oed_scenario/rows/100',
        json=scenario,
        headers={'Authorization': 'Token %s' % TOKEN},
    )
    logging.debug(result)

    data = {
        'query': {
            'scenario_id': 100,
            'region': ['scalar region1', 'scalar region2'],
            'input_energy_vector': 'scalar input vector',
            'output_energy_vector': 'scalar output vector',
            'parameter_name': 'scalar parameter',
            'technology': 'scalar technology',
            'technology_type': 'scalar technology type',
            'type': 'scalar',
            'unit': 'scalar unit',
            'tags': {'scalar tags': 'tag1'},
            'method': {'scalar method': 'method'},
            'source': 'scalar source',
            'comment': 'scalar comment',
        },
    }
    result = requests.put(
        OEP_URL + '/api/v0/schema/model_draft/tables/oed_data/rows/200',
        json=data,
        headers={'Authorization': 'Token %s' % TOKEN},
    )
    logging.debug(result)

    data = {
        'query': {
            'scenario_id': 100,
            'region': ['timeseries region1', 'timeseries region2'],
            'input_energy_vector': 'timeseries input vector',
            'output_energy_vector': 'timeseries output vector',
            'parameter_name': 'timeseries parameter',
            'technology': 'timeseries technology',
            'technology_type': 'timeseries technology type',
            'type': 'timeseries',
            'unit': 'timeseries unit',
            'tags': {'timeseries tags': 'tag1'},
            'method': {'timeseries method': 'method'},
            'source': 'timeseries source',
            'comment': 'timeseries comment',
        },
    }
    result = requests.put(
        OEP_URL + '/api/v0/schema/model_draft/tables/oed_data/rows/201',
        json=data,
        headers={'Authorization': 'Token %s' % TOKEN},
    )
    logging.debug(result)

    data = {
        'query': {
            'value': 20,
        },
    }
    result = requests.put(
        OEP_URL + '/api/v0/schema/model_draft/tables/oed_scalar/rows/200',
        json=data,
        headers={'Authorization': 'Token %s' % TOKEN},
    )
    logging.debug(result)

    data = {
        'query': {
            'timeindex_start': '2020-09-01, 00:00:00',
            'timeindex_stop': '2020-09-01, 12:00:00',
            'timeindex_resolution': '1d',
            'series': [20, 30, 40],
        },
    }
    result = requests.put(
        OEP_URL + '/api/v0/schema/model_draft/tables/oed_timeseries/rows/201',
        json=data,
        headers={'Authorization': 'Token %s' % TOKEN},
    )
    logging.debug(result)


def select_join(scenario_id):
    join = {
        "from": {
            "type": "join",
            "left": {
                "type": "table",
                "table": "oed_scenario",
                "schema": "model_draft",
                "alias": "s",
            },
            "right": {
                "type": "join",
                "is_full": True,
                "left": {
                    "type": "join",
                    "is_full": True,
                    "left": {
                        "type": "table",
                        "table": "oed_data",
                        "schema": "model_draft",
                        "alias": "d",
                    },
                    "right": {
                        "type": "table",
                        "table": "oed_timeseries",
                        "schema": "model_draft",
                        "alias": "ts",
                    },
                    "on": {
                        "operands": [
                            {"type": "column", "column": "id", "table": "d"},
                            {"type": "column", "column": "id", "table": "ts"},
                        ],
                        "operator": "=",
                        "type": "operator",
                    },
                },
                "right": {
                    "type": "table",
                    "table": "oed_scalar",
                    "schema": "model_draft",
                    "alias": "sc",
                },
                "on": {
                    "operands": [
                        {"type": "column", "column": "id", "table": "d"},
                        {"type": "column", "column": "id", "table": "sc"},
                    ],
                    "operator": "=",
                    "type": "operator",
                },
            },
            "on": {
                "operands": [
                    {"type": "column", "column": "id", "table": "s"},
                    {"type": "column", "column": "scenario_id", "table": "d"},
                ],
                "operator": "=",
                "type": "operator",
            },
        },
        "where": {
            "operands": [
                {
                    "type": "column",
                    "table": "s",
                    "column": "id",
                },
                scenario_id,
            ],
            "operator": "=",
            "type": "operator",
        },
    }
    data = {'query': join}
    response = requests.post(
        OEP_URL + '/api/v0/advanced/search',
        json=data,
        headers={'Authorization': 'Token %s' % TOKEN},
    )
    json = response.json()
    return json['data']


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.DEBUG)
    # insert_test_data()
    scenario_data = select_join(scenario_id=100)
    for row in scenario_data:
        logging.info(row)
