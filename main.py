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
def update(data, service, count):
    clasters = [(claster, services) for (claster, services) in data.items()]
    clasters.sort(key=lambda x: x[0])

    sums_per_claster = {claster: sum(services.values()) for (claster, services) in clasters}
    sums = sums_per_claster.values()
    diff = sum([max(sums) - s for s in sums])

    # case1:
    #  the data could be well-configured just by adding a new service,
    if count > diff - (len(sums_per_claster) - 1):
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

    # case2:
    #  the input data should be reconfugured
    #  eg,  { 'ginger': {'flask': 5},
    #        'cucumber': {'django: 1'} } with the new service {'aiohttp': 1}
    #  couldn'b be configured without changing current configuration
    else:
        return reconfigure(data)

def reconfigure(data):
    config = {claster: dict() for claster in data}
    for service, count in order_services(data).items():
        config = update(config, service, count)
    return config

def order_services(data):
    services = dict()
    for claster in data.values():
        for (service, amount) in claster.items():
            services.update({service: services.get(service, 0) + amount})
    return services

def main():
    data = {
        'ginger': {
            'flask': 5
        },
        'cucumber' : {
            'django': 1
        }
    }

    actual = update(data, 'aiohttp', 1)
    print(actual)

if __name__ == '__main__':
    main()
