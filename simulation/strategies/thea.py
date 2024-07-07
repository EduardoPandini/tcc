# Importing EdgeSimPy components
from edge_sim_py.components.edge_server import EdgeServer
from edge_sim_py.components.application import Application
from edge_sim_py.components.service import Service
import time
# Importing helper methods
from simulation.helper_methods import *


def thea(parameters: dict = {}):
    try:
        
        #aqui a logica pra migrar conforme o mais longe
        contador = defaultdict(int)

        #eis o dict de distancia serviço -> serv
        tampath = defaultdict(int)
        servi = 0
        services = sorted(Service.all(), key=lambda service: -service.application.services.index(service))
        for service in services:
            if service.server is not None:
                app = service.application
                user = app.users[0]
                
                tam = path_string(user.set_communication_path(app))
                tampath[service] = tam
        sortpath = dict(sorted(tampath.items(), key=lambda item: item[1], reverse=True))       
        top_servi = list(sortpath.keys())[:10]  # Pega até os 5 primeiros, ou menos se não houver 5 entradas
        topN_servi = [service for service in top_servi]
        # for servim in topN_servi:
        #     print(servim, tampath[servim])
        """Heuristic algorithm that provisions composite applications on federated edge infrastructures taking into account the delay
        and privacy requirements of applications, the trust degree between application users and infrastructure providers, and the
        power consumption of edge servers.

        Args:
            parameters (dict, optional): Algorithm parameters. Defaults to {}.
        """
        # Sorting applications according to their delay and privacy scores
        apps_metadata = []
        for app in Application.all():
            app_attrs = {
                "object": app,
                "number_of_services": len(app.services),
                "delay_sla": app.users[0].delay_slas[str(app.id)],
                "delay_score": get_application_delay_score(app=app),
                "privacy_score": get_application_privacy_score(app=app),
            }
            apps_metadata.append(app_attrs)

        # Gathering the application with the highest delay and privacy score to be provisioned
        min_and_max = find_minimum_and_maximum(metadata=apps_metadata)
        apps_metadata = sorted(
            apps_metadata,
            key=lambda app: (
                get_norm(metadata=app, attr_name="delay_score", min=min_and_max["minimum"], max=min_and_max["maximum"])
                + get_norm(metadata=app, attr_name="privacy_score", min=min_and_max["minimum"], max=min_and_max["maximum"])
            ),
            reverse=True,
        )

        # Iterating over the sorted list of applications to provision their services
        for app_metadata in apps_metadata:
            app = app_metadata["object"]
            user = app.users[0]

            # Iterating over the list of services that compose the application
            for service in app.services:
                if service.server is not None:
                    servi+=1
                # Gathering the list of edge servers candidates for hosting the service
                edge_servers = get_host_candidates(user=user, service=service)

                # Finding the minimum and maximum values for the edge server attributes
                min_and_max = find_minimum_and_maximum(metadata=edge_servers)

                # Sorting edge server host candidates based on the number of SLA violations they
                # would cause to the application and their power consumption and delay costs
                edge_servers = sorted(
                    edge_servers,
                    key=lambda s: (
                        s["sla_violations"],
                        get_norm(metadata=s, attr_name="affected_services_cost", min=min_and_max["minimum"], max=min_and_max["maximum"])
                        + get_norm(metadata=s, attr_name="power_consumption", min=min_and_max["minimum"], max=min_and_max["maximum"])
                        + get_norm(metadata=s, attr_name="delay_cost", min=min_and_max["minimum"], max=min_and_max["maximum"]),
                    ),
                )

                # Greedily iterating over the list of edge servers to find a host for the service
                for edge_server_metadata in edge_servers:
                    edge_server = edge_server_metadata["object"]

                    # print(f"[STEP {parameters['current_step']}]")
                    #se nao tem server ainda é aqui
                    if edge_server.has_capacity_to_host(service) and service.server is None:
                        provision(user=user, application=app, service=service, edge_server=edge_server)                       
                        # contar_pares_ocorrencias(user.set_communication_path(app), contador)
                        servi+=1
                        break



                    #se já tem server é aqui
                    elif service in topN_servi and edge_server.has_capacity_to_host(service) and edge_server != service.server:
                        # print("quanto tá usando",edge_server.cpu_demand)
                        # print("quanto deveria ficar",edge_server.cpu_demand+service.cpu_demand)
                        service.provision(target_server=edge_server)
                        # contar_pares_ocorrencias(user.set_communication_path(app), contador)
                        # print("quanto ficou",edge_server.cpu_demand)
                        break
                contar_pares_ocorrencias(user.set_communication_path(app), contador)

            # Setting the application as provisioned once all of its services have been provisioned
            if all([service.server != None for service in app.services]):
                app.provisioned = True
            else:
            #     raise Exception(f"{app} could not be provisioned.")
                current_step = int(parameters.get('current_step', 0))

    finally:
        current_step = int(parameters.get('current_step', 0))
        print(current_step)
        servicosTotal = int(len(Service.all()))
        diferenca  = servicosTotal - servi
        print("todos os servi", servicosTotal)
        print("servi escalonado", servi)
        print("servi não escalonado", diferenca)
        # gerar_grafico_contagem(dict(sorted(contador.items(), key=lambda item: item[1], reverse=True)))
        
        # Criar DataFrame a partir do contador
        df = pd.DataFrame(list(contador.items()), columns=['Par', 'Ocorrências'])
        
        # Ordenar o DataFrame pelo número de ocorrências de forma decrescente
        df = df.sort_values(by='Ocorrências', ascending=False)
        
        # Caminho relativo para o diretório "logs"
        logs_dir = os.path.join(os.getcwd(), 'logs/paths/dataset2')
        if not os.path.exists(logs_dir):
            os.makedirs(logs_dir)
        
        # Caminho do arquivo Excel
        excel_path = os.path.join(logs_dir, 'path_thea.xlsx')
        
        # Atualizar o arquivo Excel com o novo DataFrame
        append_to_excel(excel_path, df)
        df = pd.DataFrame({
        'Servi': [servi],
        'Total Services': [servicosTotal],
        'Difference': [diferenca]
        })


        excel_path = os.path.join(logs_dir, 'servi_thea.xlsx')
        # # Salve o DataFrame em um arquivo Excel
        df.to_excel(excel_path, index=False) 
        

def get_application_delay_score(app: object) -> float:
    """Calculates the application delay score considering the number application's SLA and the number of edge servers close enough
    to the application's user that could be used to host the application's services without violating the delay SLA.

    Args:
        app (object): Application whose delay score will be calculated.

    Returns:
        app_delay_score (float): Application's delay score.
    """
    # Gathering information about the application
    delay_sla = app.users[0].delay_slas[str(app.id)]
    user_switch = app.users[0].base_station.network_switch

    # Gathering the list of hosts close enough to the user that could be used to host the services without violating the delay SLA
    edge_servers_that_dont_violate_delay_sla = 0
    for edge_server in EdgeServer.all():
        if calculate_path_delay(origin_network_switch=user_switch, target_network_switch=edge_server.network_switch) <= delay_sla:
            edge_servers_that_dont_violate_delay_sla += 1

    if edge_servers_that_dont_violate_delay_sla == 0:
        app_delay_score = 0
    else:
        app_delay_score = 1 / ((edge_servers_that_dont_violate_delay_sla * delay_sla) ** (1 / 2))

    app_delay_score = app_delay_score * len(app.services)

    return app_delay_score


def get_application_privacy_score(app: object):
    """Calculates the application privacy score considering the demand and privacy requirements of its services.

    Args:
        app (object): Application whose privacy score will be calculated.

    Returns:
        app_privacy_score (float): Application's privacy score.
    """
    app_privacy_score = 0

    for service in app.services:
        normalized_demand = normalize_cpu_and_memory(cpu=service.cpu_demand, memory=service.memory_demand)
        privacy_requirement = service.privacy_requirement
        service_privacy_score = normalized_demand * (1 + privacy_requirement)
        app_privacy_score += service_privacy_score

    return app_privacy_score


def get_host_candidates(user: object, service: object) -> list:
    """Get list of host candidates for hosting services of a given user.
    Args:
        user (object): User object.
    Returns:
        host_candidates (list): List of host candidates.
    """
    chain = list([service.application.users[0]] + service.application.services)
    prev_item = chain[chain.index(service) - 1]

    if chain.index(service) - 1 == 0:
        if prev_item.base_station is not None:
            switch_of_previous_item_in_chain = prev_item.base_station.network_switch
        else:
            switch_of_previous_item_in_chain = None  # Lida com a situação em que prev_item.base_station é None
    else:
        if prev_item.server is not None:
            switch_of_previous_item_in_chain = prev_item.server.network_switch
        else:
            switch_of_previous_item_in_chain = None  # Lida com a situação em que prev_item.server é None

    app_delay = user.delays.get(str(service.application.id), 0)

    host_candidates = []

    for edge_server in EdgeServer.all():
        additional_delay = 0
        if switch_of_previous_item_in_chain is not None and edge_server.network_switch is not None:
            additional_delay = calculate_path_delay(
                origin_network_switch=switch_of_previous_item_in_chain, target_network_switch=edge_server.network_switch
            )
        overall_delay = app_delay + additional_delay
        delay_cost = additional_delay if service == service.application.services[-1] else 0

        violates_privacy_sla = 1 if user.providers_trust.get(str(edge_server.infrastructure_provider), 0) < service.privacy_requirement else 0
        violates_delay_sla = 1 if overall_delay > user.delay_slas.get(str(service.application.id), 0) else 0
        sla_violations = violates_delay_sla + violates_privacy_sla

        static_power_consumption = edge_server.power_model_parameters.get("static_power_percentage", 0)
        consumption_per_core = edge_server.power_model_parameters.get("max_power_consumption", 0) / edge_server.cpu
        power_consumption = consumption_per_core + static_power_consumption * (1 - sign(edge_server.cpu_demand))

        affected_services = []
        if edge_server.network_switch is not None:
            for affected_service in Service.all():
                affected_user = affected_service.application.users[0]
                trust_on_the_edge_server = affected_user.providers_trust.get(str(edge_server.infrastructure_provider), 0)
                relies_on_the_edge_server = trust_on_the_edge_server >= affected_service.privacy_requirement

                if affected_service.server is None and affected_service != service and relies_on_the_edge_server:
                    distance_to_affected_user = calculate_path_delay(
                        origin_network_switch=affected_user.base_station.network_switch, target_network_switch=edge_server.network_switch
                    )
                    distance_cost = 1 / max(1, distance_to_affected_user)
                    affected_services.append(distance_cost)

        affected_services_cost = sum(affected_services) if service == service.application.services[-1] else 0

        host_candidates.append(
            {
                "object": edge_server,
                "sla_violations": sla_violations,
                "affected_services_cost": affected_services_cost,
                "power_consumption": power_consumption,
                "delay_cost": delay_cost,
            }
        )

    return host_candidates

