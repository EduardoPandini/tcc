from edge_sim_py import *


# Creating a Simulator object
simulator = Simulator()

# Loading the dataset from the local "dataset.json" file
simulator.initialize(input_file="dataset.json")

# Displaying some of the objects loaded from the dataset
for edge_server in EdgeServer.all():
    print(f"{edge_server}. CPU Capacity: {edge_server.cpu} cores")