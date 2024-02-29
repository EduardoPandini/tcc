from edge_sim_py import *


# Creating a Python dictionary representing a sample dataset with a couple of users
my_simplified_dataset = {
    "User": [
        {
            "attributes": {
                "id": 1,
                "coordinates": [
                    1,
                    1
                ]
            },
            "relationships": {}
        },
        {
            "attributes": {
                "id": 2,
                "coordinates": [
                    3,
                    3
                ]
            },
            "relationships": {}
        },
        {
            "attributes": {
                "id": 3,
                "coordinates": [
                    5,
                    1
                ]
            },
            "relationships": {}
        },
        {
            "attributes": {
                "id": 4,
                "coordinates": [
                    0,
                    0
                ]
            },
            "relationships": {}
        }
    ]
}

# Creating a Simulator object
simulator = Simulator()

# Loading the dataset from the dictionary "my_simplified_dataset"
simulator.initialize(input_file=my_simplified_dataset)

# Displaying the objects loaded from the dataset
for user in User.all():
    print(f"{user}. Coordinates: {user.coordinates}")