# Imports
from network.peers.tests import Params
from tools.Debug import Debug
import random
import dns.resolver


class PeerDiscovery:
    def __init__(self):
        self.seeds = Params.DNS_SEEDS
        self.resolver = dns.resolver.Resolver()
        self.resolver.timeout = 5
        self.resolver.lifetime = 5

    def resolve_seed(self, seed):
        addresses = []
        try:
            answer = self.resolver.resolve(seed, 'A')
            for record in answer:
                addresses.append((str(record), Params.DEFAULT_PORT))
        except Exception as error:
            Debug.error("Resolver seed: {0}".format(str(error)))
            pass
        return addresses

    def discover_peers(self):
        addresses = []

        for seed in self.seeds:
           seed_addresses = self.resolve_seed(seed)
           for address in seed_addresses:
               addresses.append(address)

        random.shuffle(addresses)

        return addresses[:Params.MAX_PEERS]
