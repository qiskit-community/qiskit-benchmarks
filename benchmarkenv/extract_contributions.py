import os
import sys

import yaml

def extract_contributions(contributions_path):
  with open(contributions_path) as file:
    contributions = yaml.load(file, Loader=yaml.SafeLoader)

  for contribution_data in contributions:
    yield _get_key(contribution_data)


def _get_key(map):
  return next(iter(map.keys()))

if __name__ == '__main__':
  contributions_path = os.path.join(os.getcwd(), sys.argv[1])
  for contribution in extract_contributions(contributions_path):
    print(contribution)