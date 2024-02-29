from edge_sim_py import *



# Creating a Simulator object
simulator = Simulator()

# Loading the dataset file from the external JSON file
simulator.initialize(input_file="https://raw.githubusercontent.com/EdgeSimPy/edgesimpy-tutorials/master/datasets/sample_dataset1.json")

# Displaying some of the objects loaded from the dataset
for user in User.all():
    print(f"{user}. Coordinates: {user.coordinates}")


    #!curl https://raw.githubusercontent.com/EdgeSimPy/edgesimpy-tutorials/master/datasets/sample_dataset1.json --output dataset.json