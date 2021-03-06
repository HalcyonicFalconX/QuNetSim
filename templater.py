from string import ascii_uppercase, ascii_lowercase


def gen_imports():
    imports = ""
    imports += "from qunetsim.components import Host, Network\n"
    imports += "from qunetsim.objects import Qubit, Logger\n"
    imports += "Logger.DISABLED = True\n\n\n"
    return imports


def gen_protocols():
    content = ""
    content += "def protocol_1(host, receiver):" + "\n"
    content += "    " + "# Here we write the protocol code for a host.\n"
    content += "    " + "for i in range(5):\n"
    content += "        " + "q = Qubit(host)\n"
    content += "        " + "q.H()\n"
    content += "        " + "print('Sending qubit %d.' % (i+1))\n"
    content += "        " + "host.send_qubit(receiver, q, await_ack=True)\n"
    content += "        " + "print('Qubit %d was received by %s.' % (i+1, receiver))" + "\n\n\n"

    content += "def protocol_2(host, sender):" + "\n"
    content += "    " + "# Here we write the protocol code for another host.\n"
    content += "    " + "for _ in range(5):\n"
    content += "        " + "# Wait for a qubit from Alice for 10 seconds.\n"
    content += "        " + "q = host.get_data_qubit(sender, wait=10)\n"
    content += "        " + "print('%s received a qubit in the %d state.' % (host.host_id, q.measure()))\n\n\n"
    return content


def gen_main():
    main_content = ""
    main_content += "def main():" + "\n"
    main_content += "   " + "network = Network.get_instance()" + "\n"
    num_nodes = int(input("How many nodes are in the network? "))
    nodes = []

    node_names = list(ascii_uppercase)
    node_names.extend(ascii_lowercase)

    if (num_nodes > len(node_names)):
        print('Please use less than %d nodes' % len(num_nodes))

    for i in range(num_nodes):
        nodes.append(node_names[i])
    main_content += "   " + "nodes = " + str(nodes) + "\n"
    main_content += "   " + "network.start(nodes)" + "\n"
    main_content += "\n"
    for n in nodes:
        main_content += "   " + "host_" + n + " = Host('" + n + "')" + "\n"
        for m in nodes:
            if m != n:
                main_content += "   " + "host_" + n + ".add_connection('" + m + "')" + "\n"

        main_content += "   " + "host_" + n + ".start()" + "\n"
    main_content += "\n"
    for n in nodes:
        main_content += "   network.add_host(" + "host_" + n + ") \n"

    main_content += "\n"
    main_content += "   " + "t1 = host_" + nodes[0] + ".run_protocol(protocol_1, (host_" \
                    + nodes[-1] + ".host_id,))\n"
    main_content += "   " + "t2 = host_" + nodes[-1] + ".run_protocol(protocol_2, (host_" \
                    + nodes[0] + ".host_id,))\n"
    main_content += "   " + "t1.join()\n"
    main_content += "   " + "t2.join()\n"
    main_content += "   " + "network.stop(True)\n\n"
    return main_content


if __name__ == '__main__':
    file_name = input("File name? (exclude file type (i.e. don't put .py)): ")
    if file_name == "":
        print("File name must not be empty.")
    else:
        file_content = gen_imports()
        file_content += gen_protocols()
        file_content += gen_main()
        file_content += "if __name__ == '__main__':\n"
        file_content += "   main()\n"
        f = open(file_name + '.py', 'w')
        f.write(file_content)
