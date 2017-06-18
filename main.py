from pprint import pprint
from functools import reduce, wraps
from copy import deepcopy
from collections import OrderedDict

def preserve_immutability(update):
    @wraps(update)
    def inner(*args, **kwargs):
        return update(deepcopy(args[0]), *args[1:], **kwargs)
    return inner

#@preserve_immutability
def update(data, service, count, predict=False):
    clasters = [(claster, services) for (claster, services) in data.items()]
    clasters.sort(key=lambda x: x[0])

    sums_per_claster = {claster: sum(services.values()) for (claster, services) in clasters}
    sums = sums_per_claster.values()
    diff = sum([max(sums) - s for s in sums])

    total = count + sum(sums_per_claster.values())
    avg = total // len(clasters)
    rest = total % len(clasters)
    for claster, services in clasters:
        amount_to_add = avg - sums_per_claster[claster]
        if rest:
            amount_to_add += 1
            rest -= 1
        services.update({service: amount_to_add})
    return {claster: services for (claster, services) in clasters}


def main():
    config = {
        'ginger': {},
        'cucumber': {},
    }
    update(config, 'flask', 3)
    update(config, 'django', 3)

main()
