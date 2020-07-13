import sys
import time

sys.path.append("../..")
from qunetsim.backends import CQCBackend
from qunetsim.components.host import Host
from qunetsim.components.network import Network
from qunetsim.objects import Qubit


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

    q = Qubit(hosts['bob'])
    q.X()

    q_id = hosts['bob'].send_qubit(hosts['alice'].host_id, q)

    i = 0
    rec_q = hosts['alice'].get_data_qubit(hosts['bob'].host_id, q_id)
    while i < 15 and rec_q is None:
        rec_q = hosts['alice'].get_data_qubit(hosts['bob'].host_id, q_id)
        i += 1
        time.sleep(1)

    assert rec_q is not None
    assert rec_q.measure() == 1
    print("All tests succesfull!")
    network.stop(True)
    exit()


if __name__ == '__main__':
    main()
