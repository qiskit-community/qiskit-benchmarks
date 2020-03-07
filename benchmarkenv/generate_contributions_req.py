import sys

import yaml


def generate_contributions_req(contributions_path, contributions_req):
    with open(contributions_path) as file:
        contributions = yaml.load(file)

    requirements = (next(iter(cont.keys())) for cont in contributions)
    with open(contributions_req, 'w+') as file:
        file.write('\n'.join(requirements))


if __name__ == '__main__':
    generate_contributions_req(sys.argv[1], sys.argv[2])
