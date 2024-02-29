# Gathering the list of msgpack files in the current directory
from edge_sim_py import *
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
    stopping_criterion=lambda model: 1,
    resource_management_algorithm=my_algorithm,
)

# Loading a sample dataset from GitHub
simulator.initialize(input_file="https://raw.githubusercontent.com/EdgeSimPy/edgesimpy-tutorials/master/datasets/sample_dataset2.json")

# Executing the simulation
simulator.run_model()

# Creating a Pandas data frame with the network switch logs
logs = pd.DataFrame(simulator.agent_metrics["NetworkSwitch"])
logs
with open('/logs/EdgeServer.msgpack', 'rb') as f:
    my_deserialized_dict = msgpack.load(f)


    #eu não sei ler os .msgpack !!!!! socorro