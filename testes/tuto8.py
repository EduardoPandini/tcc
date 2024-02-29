#algoritimo de migração (?)

from edge_sim_py import *

#define parametros dnv...



def my_algorithm(parameters): 
    # Let's iterate over the list of services using the 'all()' helper method
    print("\n\n")
    for service in Service.all():
        
        # We don't want to migrate services are are already being migrated
        if not service.being_provisioned:

            # We need to sort edge servers based on amount of free resources they have. To do so, we are going to use Python's
            # "sorted" method (you can learn more about "sorted()" in this link: https://docs.python.org/3/howto/sorting.html). As
            # the capacity of edge servers is modeled in three layers (CPU, memory, and disk), we calculate the geometric mean
            # between these to get the average resource utilization of edge servers. Finally, we set the sorted method "reverse"
            # attribute as "True" as we want to sort edge servers by their free resources in descending order

            #^^^^^^^^^^^^^^^^^^meudeus^^^^^^^^^parece importante

            edge_servers = sorted(
                EdgeServer.all(),
                key=lambda s: ((s.cpu - s.cpu_demand) * (s.memory - s.memory_demand) * (s.disk - s.disk_demand)) ** (1 / 3),
                
                #essa key é o calculo do paragrafo ali em cima, atentar
                
                reverse=True,
            )

            for edge_server in edge_servers:
                # Checking if the edge server has resources to host the service
                if edge_server.has_capacity_to_host(service=service):
                    # We just need to migrate the service if it's not already in the least occupied edge server
                    if service.server != edge_server:
                        print(f"[STEP {parameters['current_step']}] Migrating {service} From {service.server} to {edge_server}")
                        
                        service.provision(target_server=edge_server)

                        # After start migrating the service we can move on to the next service
                        break



def stopping_criterion(model: object):    
    # As EdgeSimPy will halt the simulation whenever this function returns True,
    # its output will be a boolean expression that checks if the current time step is 600
    return model.schedule.steps == 600

#quando executa ele caga pra duração de tick

# Creating a Simulator object
simulator = Simulator(
    tick_duration=1,
    tick_unit="seconds",
    stopping_criterion=stopping_criterion,
    resource_management_algorithm=my_algorithm,
)

# Loading a sample dataset from GitHub
simulator.initialize(input_file="https://raw.githubusercontent.com/EdgeSimPy/edgesimpy-tutorials/master/datasets/sample_dataset1.json")

# Executing the simulation
simulator.run_model()

#bom ele meio que sempre migra apesar de dar i, "só precisa migrar se..." não vi um caso onde ele não migra alghum deles
#correção, bem no começo ele não migra em alguns passos, só n vi pq o terminal tinha apagado
#ele engasga quando manda fazer muitos passos, calma com o coitado
