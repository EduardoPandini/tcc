#possivelmente o mais importante aqui? é literalmente o tcc lol
#automatização de experimentos 

from edge_sim_py import *

# Python libraries
import itertools
import os
import random
import msgpack
import pandas as pd


#For conciseness, this notebook doesn't
#  focus on configuring simulations on EdgeSimPy.
#  Instead, we will use the scenario described in this notebook, https://github.com/EdgeSimPy/edgesimpy-tutorials/blob/master/notebooks/creating-placement-algorithm.ipynb
#  in which a First-Fit algorithm defines which edge servers should host services within the infrastructure.

#def do algoritimo e condição de parada




def my_algorithm(parameters):
    print(f"parameters: {parameters}")
    # We can always call the 'all()' method to get a list with all created instances of a given class
    for service in Service.all():
        # We don't want to migrate services are are already being migrated
        if service.server == None and not service.being_provisioned:

            # Let's iterate over the list of edge servers to find a suitable host for our service
            for edge_server in EdgeServer.all():

                # We must check if the edge server has enough resources to host the service
                if edge_server.has_capacity_to_host(service=service):

                    # Start provisioning the service in the edge server
                    service.provision(target_server=edge_server)

                    # After start migrating the service we can move on to the next service
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

#parametros arbitrários

parameters = {
    "a": [1, 2, 3],
    "b": [100, 200, 3],
}


#automação dos experimentos

for combination in itertools.product(*parameters.values()):
    specification = {}
    specification_name = ''
    for parameter_id, parameter_value in enumerate(combination):
        parameter_name = list(parameters.keys())[parameter_id]
        
        # Formatting the logs directory name according to the current specification's parameters
        specification_name += f";{parameter_name}={parameter_value}" if parameter_id else f"{parameter_name}={parameter_value}"

        # Building a dictionary from the current specification
        specification[parameter_name] = parameter_value
    
    # Creating a Simulator object with the current parameters specification and its logs directory
    simulator = Simulator(
        dump_interval=5,
        tick_duration=1,
        tick_unit="seconds",
        stopping_criterion=stopping_criterion,
        resource_management_algorithm=my_algorithm,
        resource_management_algorithm_parameters=specification,
        logs_directory=specification_name
    )

    # Loading a sample dataset from GitHub
    simulator.initialize(input_file="https://raw.githubusercontent.com/EdgeSimPy/edgesimpy-tutorials/master/datasets/sample_dataset2.json")

    # Executing the simulation
    print(f"==== Running Simulation with Specification: {specification} ====")
    simulator.run_model()
    
logs = pd.DataFrame(simulator.agent_metrics["NetworkSwitch"])

logs.to_excel('~/Área de Trabalho/tcc/testes/logs/xml/1.xlsx')
    #ok ele gerou todos numa boa mas TÁ EM .MSGPACK DENOVO E EU N SEI LER AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
logs = pd.DataFrame(simulator.agent_metrics["EdgeServer"])
print(logs)

