# Imports
from tools.logger import Logger
from network.params import params
import random
import dns.resolver


class PeerDiscovery:

    def __init__(self):
        # Configs;
        self.seeds = params.DNS_SEEDS
        self.resolver = dns.resolver.Resolver()
        self.resolver.timeout = 5
        self.resolver.lifetime = 5

        # Objects;
        self.logger = Logger("peer_discovery", "peer_discovery.log", "debug")

    def resolve_seed(self, seed):
        # Vars;
        addresses = []

        try:
            answer = self.resolver.resolve(seed, "A")
            for record in answer:
                self.logger.print_logger("info", "Resolving new peer address: {0}:{1}.".format(str(record), str(params.DEFAULT_PORT)))
                addresses.append((str(record), params.DEFAULT_PORT))

        except Exception as error:
            self.logger.print_logger("error", "Resolver seed: {0}".format(str(error)))
            pass

        return addresses

    def discover_peers(self):
        # Vars;
        addresses = []

        # Resolver addresses;
        for seed in self.seeds:
            seed_addresses = self.resolve_seed(seed)

            # Add address resolvers in list;
            for address in seed_addresses:
                addresses.append(address)

        # Random mix addresses;
        random.shuffle(addresses)

        # Return with max peers rule;
        return addresses[:params.MAX_PEERS]
