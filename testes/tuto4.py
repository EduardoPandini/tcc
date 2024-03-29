#NESSE TUTO: CONSULTAS E CRIAÇÃO DE METODOS

from edge_sim_py import *

# Creating a Simulator object
simulator = Simulator(
    tick_duration=1,
    tick_unit="seconds",
    stopping_criterion=lambda model: 1,
)

# Loading a sample dataset from GitHub
simulator.initialize(input_file="https://raw.githubusercontent.com/EdgeSimPy/edgesimpy-tutorials/master/datasets/sample_dataset2.json")


all_users = User.all()

#for user in all_users:
    #print(f"    {user}")

first_user = User.first()
last_user = User.last()

print(f"First user: {first_user}")
print(f"Last user: {last_user}")

number_of_netswitch_servers = NetworkSwitch.count()

print(f"There are {number_of_netswitch_servers} switches within the infrastructure")



network_switch = NetworkSwitch.find_by_id(1)

print(f"Network Switch with ID 1: {network_switch}")



base_station_at_2_0 = BaseStation.find_by(attribute_name="coordinates", attribute_value=[2, 0])

print(f"Base Station located in coordinates [2,0]: {base_station_at_2_0}")

def sorted_by(cls, attribute: str, order: str = "ascending") -> list:
    """Returns the list of created objects of a given class sorted by a given attribute.

    Args:
        attribute (str): Attribute that will be used to sort the class instances.
        order (str): Sorting order. Valid values are "ascending" or "descending". Defaults to "ascending".

    Returns:
        instances (list): Sorted list of objects from a given class.
    """
    #Gathering the list of class instances
    instances = cls._instances

    # Checking if all the instances have the passed attribute and if the instance attributes are comparable
    comparable_instance_pairs = 0
    for index in range(len(instances) - 1):
        # Gathering a pair of instances (i.e., "a" and "b") from the given class
        a = instances[index]
        b = instances[index + 1]

        # Checking if instances "a" and "b" have the passed attribute. If "a" or "b" don't have the passed attribute, we
        # break the outer for loop as the comparison will not work. In that case, the exception down below will be triggered
        if not hasattr(a, attribute) or not hasattr(b, attribute):
            break

        # If the break was not triggered, "a" and "b" have the passed attribute.
        # Then, we must check if the attribute values are comparable
        a_attr = getattr(a, attribute)
        b_attr = getattr(b, attribute)
        if (a_attr).__eq__(b_attr) != NotImplemented or (b_attr).__eq__(a_attr) != NotImplemented:
            comparable_instance_pairs += 1

    # If all instances have the passed attribute and the attribute values are comparable, sorts the list of class instances
    if comparable_instance_pairs == len(instances) - 1:
        instances = sorted(
            instances,
            key=lambda instance: getattr(instance, attribute),
            reverse=order == "descending",
        )
    else:
        msg = f"Error. Make sure all instances of {cls.__name__} have the {attribute} attribute with comparable values."
        raise Exception(msg)

    return instances



ComponentManager.sorted_by = classmethod(sorted_by)

# Sorting the list of edge servers with our new "sorted_by" method
edge_servers = EdgeServer.sorted_by(attribute="id", order="ascending")
for edge_server in edge_servers:
    print(f"{edge_server}")





