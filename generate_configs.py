#!/usr/bin/env python

import argparse
from dataclasses import asdict
import itertools

import yaml

from cctestbed2.configuration import ApplicationConfig, EnvVariable, NetworkConfig, Testcase


TC_SETTINGS = [
    {
        'name': 'static',
        'phases': [
            {
                'tc': True,
                'bandwidth': '5mbit',
                'latency': '50ms',
                'delay': 50000,
                'duration': 100,
            },
        ],
    },
    {
        'name': 'variable',
        'phases': [
            {
                'tc': True,
                'bandwidth': '1mbit',
                'latency': '50ms',
                'delay': 50000,
                'duration': 40,
            },
            {
                'tc': True,
                'bandwidth': '2500kbit',
                'latency': '50ms',
                'delay': 50000,
                'duration': 20,
            },
            {
                'tc': True,
                'bandwidth': '600kbit',
                'latency': '50ms',
                'delay': 50000,
                'duration': 20,
            },
            {
                'tc': True,
                'bandwidth': '1mbit',
                'latency': '50ms',
                'delay': 50000,
                'duration': 20,
            },
        ],
    },
]


APP_SETTINGS = [
    {
        'name': 'static',
        'apps': [
            {
                'name': 'receiver',
                'namespace': 'ns1',
                'start_time': 0,
                'duration': 100,
                'environment': [],
                'binary': 'pioncc/pioncc',
                'arguments': [
                    '-receiver', '10.1.0.10:8080',
                    '-sender', '10.3.0.20:8080',
                ],
            },
            {
                'name': 'sender',
                'namespace': 'ns4',
                'start_time': 0,
                'duration': 100,
                'environment': [],
                'binary': 'pioncc/pioncc',
                'arguments': [
                    '-receiver', '10.1.0.10:8080',
                    '-sender', '10.3.0.20:8080',
                    '-send',
                ],
            },
        ],
    },
    {
        'name': 'gcc',
        'apps': [
            {
                'name': 'receiver',
                'namespace': 'ns1',
                'start_time': 0,
                'duration': 100,
                'environment': [],
                'binary': 'pioncc/pioncc',
                'arguments': [
                    '-receiver', '10.1.0.10:8080',
                    '-sender', '10.3.0.20:8080',
                ],
            },
            {
                'name': 'sender',
                'namespace': 'ns4',
                'start_time': 0,
                'duration': 100,
                'environment': [],
                'binary': 'pioncc/pioncc',
                'arguments': [
                    '-receiver', '10.1.0.10:8080',
                    '-sender', '10.3.0.20:8080',
                    '-send',
                    '-gcc',
                ],
            },
        ],
    },
    {
        'name': 'generic_loss_cc',
        'apps': [
            {
                'name': 'receiver',
                'namespace': 'ns1',
                'start_time': 0,
                'duration': 100,
                'environment': [],
                'binary': 'pioncc/pioncc',
                'arguments': [
                    '-receiver', '10.1.0.10:8080',
                    '-sender', '10.3.0.20:8080',
                    '-ccfb',
                ],
            },
            {
                'name': 'sender',
                'namespace': 'ns4',
                'start_time': 0,
                'duration': 100,
                'environment': [],
                'binary': 'pioncc/pioncc',
                'arguments': [
                    '-receiver', '10.1.0.10:8080',
                    '-sender', '10.3.0.20:8080',
                    '-send',
                    '-gencc',
                ],
            },
        ],
    },
]


def generate_retralid_configs(directory):
    combinations = itertools.product(
        TC_SETTINGS,
        APP_SETTINGS,
    )
    for combination in combinations:
        tc = combination[0]
        app_settings = combination[1]
        name = f'{tc["name"]}_{app_settings["name"]}'

        apps = [ApplicationConfig(
            name=app['name'],
            namespace=app['namespace'],
            start_time=app['start_time'],
            duration=app['duration'],
            environment=app['environment'],
            binary=app['binary'],
            arguments=app['arguments'],
        ) for app in app_settings['apps']]

        nc = [NetworkConfig(
            traffic_control=p['tc'],
            duration=p['duration'],
            bandwidth=p['bandwidth'],
            latency=p['latency'],
            delay=p['delay']
        ) for p in tc['phases']]

        duration = sum([p.duration for p in nc])

        tc = Testcase(
            name=name,
            network=nc,
            applications=apps,
            duration=30,
        )
        with open(f'{directory}/{name}.yaml', 'w') as file:
            file.write(yaml.dump(asdict(tc)))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-o', '--output', help='output directory', required=True)
    args = parser.parse_args()
    generate_retralid_configs(args.output)


if __name__ == "__main__":
    main()
