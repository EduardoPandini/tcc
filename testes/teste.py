

# Importing EdgeSimPy components
from edge_sim_py import *

# Importing Python libraries
import os
import random
import msgpack
import pandas as pd



def my_algorithm(parameters):
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


# Gathering the list of msgpack files in the current directory
logs_directory = f"{os.getcwd()}/logs"
dataset_files = [file for file in os.listdir(logs_directory) if ".msgpack" in file]

# Reading msgpack files found
datasets = {}
for file in dataset_files:
    with open(f"logs/{file}", "rb") as data_file:
        datasets[file.replace(".msgpack", "")] = pd.DataFrame(msgpack.unpackb(data_file.read(), strict_map_key=False))
datasets["EdgeServer"]


# Defining the data frame columns that will be exhibited
properties = ['Coordinates', 'CPU Demand', 'RAM Demand', 'Disk Demand', 'Services']
columns = ['Time Step', 'Instance ID'] + properties

dataframe = datasets["EdgeServer"].filter(items=columns)
dataframe



def custom_collect_method(self) -> dict:
    temperature = random.randint(10, 50)  # Generating a random integer between 10 and 50 representing the switch's temperature
    metrics = {
        "Instance ID": self.id,
        "Power Consumption": self.get_power_consumption(),
        "Temperature": temperature,
    }
    return metrics

# Overriding the NetworkSwitch's collect() method
NetworkSwitch.collect = custom_collect_method

# Creating a Simulator object
simulator = Simulator(
    dump_interval=5,
    tick_duration=1,
    tick_unit="seconds",
    stopping_criterion=stopping_criterion,
    resource_management_algorithm=my_algorithm,
)

# Loading a sample dataset from GitHub
simulator.initialize(input_file="https://raw.githubusercontent.com/EdgeSimPy/edgesimpy-tutorials/master/datasets/sample_dataset2.json")

# Executing the simulation
simulator.run_model()

# # Gathering the list of msgpack files in the current directory
# logs_directory = f"{os.getcwd()}/logs"
# dataset_files = [file for file in os.listdir(logs_directory) if ".msgpack" in file]

# # Reading msgpack files found
# datasets = {}
# countF=0
# for file in dataset_files:
with open(f"/home/g06843614930/Área de Trabalho/tcc/testes/logs/NetworkFlow.msgpack", "rb"):
        #datasets[file.replace(".msgpack", "")] = pd.DataFrame(msgpack.unpackb(data_file.read(), strict_map_key=False))
        dataframe.to_excel('~/Área de Trabalho/tcc/testes/logs/xml/1.xlsx')








