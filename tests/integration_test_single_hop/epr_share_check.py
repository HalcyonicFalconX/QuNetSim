import sys
import time

sys.path.append("../..")
from qunetsim.backends import CQCBackend
from qunetsim.components.host import Host
from qunetsim.components.network import Network
MAX_WAIT = 10

def main():
    backend = CQCBackend()
    network = Network.get_instance()
    nodes = ["Alice", "Bob", "Eve", "Dean"]
    network.start(nodes, backend)
    network.delay = 0.7
    hosts = {'alice': Host('Alice', backend),
             'bob': Host('Bob', backend)}


    # A <-> B
    hosts['alice'].add_connection('Bob')
    hosts['bob'].add_connection('Alice')

    hosts['alice'].start()
    hosts['bob'].start()

    for h in hosts.values():
        network.add_host(h)

    q_id = hosts['alice'].send_epr(hosts['bob'].host_id)
    q1 = hosts['alice'].shares_epr(hosts['bob'].host_id)
    i = 0
    while not q1 and i < MAX_WAIT:
        q1 = hosts['alice'].shares_epr(hosts['bob'].host_id)
        i += 1
        time.sleep(1)

    i = 0
    q2 = hosts['bob'].shares_epr(hosts['alice'].host_id)
    while not q2 and i < 5:
        q2 = hosts['bob'].shares_epr(hosts['alice'].host_id)
        i += 1
        time.sleep(1)


    assert hosts['alice'].shares_epr(hosts['bob'].host_id)
    assert hosts['bob'].shares_epr(hosts['alice'].host_id)
    q_alice = hosts['alice'].get_epr(hosts['bob'].host_id, q_id)
    q_bob = hosts['bob'].get_epr(hosts['alice'].host_id, q_id)
    assert q_alice is not None
    assert q_bob is not None
    assert q_alice.measure() == q_bob.measure()
    assert not hosts['alice'].shares_epr(hosts['bob'].host_id)
    assert not hosts['bob'].shares_epr(hosts['alice'].host_id)
    print("All tests succesfull!")
    network.stop(True)
    exit()


if __name__ == '__main__':
    main()
