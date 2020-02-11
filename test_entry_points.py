import sys
import site
import os.path
import importlib
from pprint import pprint
from itertools import chain
from dataclasses import dataclass, asdict
from json import dumps, JSONEncoder

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

def test_entry_points(contributions_path, results_path):
  results = {}

  with open(contributions_path) as file:
    contributions = yaml.load(file)

  entry_points = chain(*(next(iter(cont.values())) for cont in contributions))

  for one_entry_point in entry_points:
    module_fqn, function_name = one_entry_point.split(':')
    module = importlib.import_module(module_fqn)
    metadata = get_metadata(module)
    try:
      function = getattr(module, function_name)
      if metadata.name not in results:
        results[metadata.name] = { **asdict(metadata), 'results': [] }

      results[metadata.name]['results'].append((one_entry_point, test(function)))
    except AttributeError:
      notify_cannot_find_entry_point(metadata.author_email, one_entry_point)

  with open(results_path, 'w+') as file:
    file.write(dumps(results, cls=ResultEncoder))

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
          description=meta['Description']
        )

@dataclass
class metadata:

  name: str

  description: str

  author: str

  author_email: str


def get_dist_files(dist):
  for path in files(dist.project_name):
    path = os.path.normpath(os.path.join(dist.location, path))
    yield path

def test(function):
  return benchmark.test(function)

def notify_cannot_find_entry_point(email, entry_point):
  print(f'send "{entry_point} not working" @ {email}')

if __name__ == '__main__':
  test_entry_points(sys.argv[1], sys.argv[2])