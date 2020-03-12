import sys
import site
import os
import importlib
import json
from datetime import datetime
from pprint import pprint
from itertools import chain
from dataclasses import dataclass, asdict
from json import dumps, load, JSONEncoder
from contextlib import suppress

import yaml
import pkg_resources
import importlib_metadata
from importlib_metadata import distribution, files
from qiskit import QuantumCircuit
from qiskit.transpiler.pass_manager_config import PassManagerConfig
from qiskit.transpiler import CouplingMap

import benchmark


class ResultEncoder(JSONEncoder):
  def default(self, obj):
    if isinstance(obj, QuantumCircuit):
      return obj.name
    if isinstance(obj, PassManagerConfig):
      return obj.__dict__
    if isinstance(obj, CouplingMap):
      return obj.get_edges()
    return JSONEncoder.default(self, obj)


def test_entry_points(contributions_path, contribution_key, results_path, overwrite=False):
  contribution_results = {}

  with open(contributions_path) as file:
    contributions = yaml.load(file, Loader=yaml.SafeLoader)

  entry_points = next(filter(lambda m: contribution_key in m, contributions))[contribution_key]

  for one_entry_point in entry_points:
    module_fqn, function_name = one_entry_point.split(':')
    module = importlib.import_module(module_fqn)
    metadata = get_metadata(module)
    try:
      function = getattr(module, function_name)
      if contribution_key not in contribution_results:
        contribution_results[contribution_key] = { **asdict(metadata), 'results': [] }

      entry_point_results = test(function)
      contribution_results[contribution_key]['results'].append((one_entry_point, entry_point_results))
    except AttributeError:
      notify_cannot_find_entry_point(metadata.author_email, one_entry_point)

  results = {}
  if os.path.exists(results_path):
    with open(results_path, 'r') as file:
      with suppress(json.decoder.JSONDecodeError):
        results = load(file)

  results.update(contribution_results)

  with open(results_path, 'w') as file:
    file.write(dumps(results, cls=ResultEncoder, indent=2))

def get_metadata(module):
  module_path = module.__file__
  for dist in pkg_resources.working_set:
    for path in get_dist_files(dist):
      if module_path == path:
        meta = importlib_metadata.metadata(dist.project_name)
        return metadata(
          name=meta['Name'],
          author=meta['Author'],
          author_email=meta['Author-email'],
          description=meta['Summary'],
          timestamp=str(datetime.now()),
          version=meta['Version']
        )

@dataclass
class metadata:

  name: str

  description: str

  author: str

  author_email: str

  timestamp: str

  version: str


def get_dist_files(dist):
  for path in files(dist.project_name):
    path = os.path.normpath(os.path.join(dist.location, path))
    yield path

def test(function):
  return benchmark.test(function)

def notify_cannot_find_entry_point(email, entry_point):
  print(f'send "{entry_point} not working" @ {email}')

if __name__ == '__main__':
  contributions_path = os.path.join(os.getcwd(), sys.argv[1])
  contribution_key = sys.argv[2]
  results_path = os.path.join(os.getcwd(), sys.argv[3])
  test_entry_points(contributions_path, contribution_key, results_path)