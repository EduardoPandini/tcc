#nesse: PLACEMENT ALG
from edge_sim_py import *
from helper_methods import *
import networkx as nx

#esse vai trabalhar com first fit aparentemente
#tldr: provisiona o primeiro server que consegue hostear

#1 define o alg na função my_algorythm q recebe os parametros 

def faticanti2020(parameters: dict = {}):
    """Adapted version of [1], that focuses on finding host servers for microservice-based applications on
    Edge Computing scenarios with multiple infrastructure providers.

    [1] Faticanti, Francescomaria, et al. "Deployment of Application Microservices in Multi-Domain Federated
    Fog Environments." International Conference on Omni-layer Intelligent Systems (COINS). IEEE, 2020.

    Args:
        parameters (dict, optional): Algorithm parameters. Defaults to {}.
    """
    # Sorting services based on their positions in their application's service chain
    services = sorted(Service.all(), key=lambda service: service.application.services.index(service))

    for service in services:
        app = service.application
        user = app.users[0]

        # Sorting edge servers by: trustworthiness, distance from user (in terms of delay), and free resources
        edge_servers = sorted(
            EdgeServer.all(),
            key=lambda s: (
                -(user.providers_trust[str(s.infrastructure_provider)]),
                calculate_path_delay(origin_network_switch=user.base_station.network_switch, target_network_switch=s.network_switch),
                s.cpu - s.cpu_demand,
            ),
        )

        # Greedily iterating over the list of EdgeNode candidates to find the best node to host the service
        for edge_server in edge_servers:
            if edge_server.has_capacity_to_host(service):
                provision(user=user, application=app, service=service, edge_server=edge_server)
                break

def stopping_criterion(model: object):
    # Defining a variable that will help us to count the number of services successfully provisioned within the infrastructure
    provisioned_services = 0
    
    # Iterating over the list of services to count the number of services provisioned within the infrastructure
    for service in Service.all():

        # Initially, services are not hosted by any server (i.e., their "server" attribute is None).
        # Once that value changes, we know that it has been successfully provisioned inside an edge server.
        if service.server != None:
            provisioned_services += 1
    
    # As EdgeSimPy will halt the simulation whenever this function returns True, its output will be a boolean expression
    # that checks if the number of provisioned services equals to the number of services spawned in our simulation
    return provisioned_services == Service.count()

#definindo o algoritimo e a parada podemos simular :)


G=nx.Graph()
G.add_nodes_from([2,3])

# Creating a Simulator object
simulator = Simulator(
    tick_duration=1,
    tick_unit="seconds",
    stopping_criterion=stopping_criterion,
    resource_management_algorithm=faticanti2020
)
# Loading a sample dataset from GitHub
simulator.initialize(input_file="https://raw.githubusercontent.com/paulosevero/thea/master/datasets/dataset1.json")
simulator.topology = G

#simulator.initialize()
# Executing the simulation
simulator.run_model()

# Checking the placement output
for service in EdgeServer.all():
    print(f"{service}. Host: {EdgeServer}")

    #na saida todos foram pro server1, n sei se tá certo mas vou confiar no tutorial né 
    #se tiver certo, sugiro pro tutorial colocar serviços q o server1 n de conta
    #mas tirando isso esse foi deboa, n tive duvida

