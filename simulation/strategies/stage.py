# Importing EdgeSimPy components
from edge_sim_py.components.edge_server import EdgeServer
from edge_sim_py.components.application import Application

# Importing helper methods
from simulation.helper_methods import *



def argos(parameters: dict = {}):
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


        servi=0
        """Privacy-aware service provisioning strategy for edge computing environments proposed in [1].

        [1] Souza, P.; Crestani, Â.; Rubin, F.; Ferreto, T. and Rossi, F. (2022). Latency-aware Privacy-preserving
        Service Migration in Federated Edges. In International Conference on Cloud Computing and Services Science (CLOSER),
        pages 288-295. DOI: 10.5220/0011084500003200.

        Args:
            parameters (dict, optional): Algorithm parameters. Defaults to {}.
        """
        apps = sorted(Application.all(), key=lambda app: app.users[0].delay_slas[str(app.id)])

        for app in apps:
            user = app.users[0]
            services = sorted(app.services, key=lambda s: (-s.privacy_requirement, -s.cpu_demand))

            edge_servers = sorted(get_host_candidates(user=user), key=lambda s: (-s["trust_degree"], s["delay"]))

            for service in services:
                if service.server is not None:
                    servi+=1
                # Greedily iterating over the list of edge servers to find a host for the service
                for edge_server_metadata in edge_servers:
                    edge_server = edge_server_metadata["object"]


                    #se nao tem server ainda é aqui
                    if edge_server.has_capacity_to_host(service) and service.server is None:
                        provision(user=user, application=app, service=service, edge_server=edge_server)   
                        servi+=1                    
                        break



                    #se já tem server é aqui
                    elif service in topN_servi and edge_server.has_capacity_to_host(service) and edge_server != service.server:
                        service.provision(target_server=edge_server)
                        break
                
                contar_pares_ocorrencias(user.set_communication_path(app), contador)
    finally:
        servicosTotal = int(len(Service.all()))
        diferenca  = servicosTotal-servi
        print("todos os servi", servicosTotal)
        print("servi escalonado", servi)
        print("servi não escalonado", diferenca)
        # print(dict(sorted(contador.items(), key=lambda item: item[1], reverse=True)))
        gerar_grafico_contagem(dict(sorted(contador.items(), key=lambda item: item[1], reverse=True)))
        df = pd.DataFrame(list(contador.items()), columns=['Par', 'Ocorrências'])
    
        # Ordenar o DataFrame pelo número de ocorrências de forma decrescente
        df = df.sort_values(by='Ocorrências', ascending=False)
        
        # Caminho relativo para o diretório "logs"
        logs_dir = os.path.join(os.getcwd(), 'logs')
        
        # Salvar o DataFrame em um arquivo Excel no diretório "logs"
        current_step = int(parameters.get('current_step', 0))
        
        print(current_step)
        if current_step == 1 or current_step == 100:
            logs_dir = os.path.join(os.getcwd(), 'logs/paths/dataset2')
            excel_path = os.path.join(logs_dir, f'path_argos_{current_step}.xlsx')
            df.to_excel(excel_path, index=False)
        df = pd.DataFrame({
        'Servi': [servi],
        'Total Services': [servicosTotal],
        'Difference': [diferenca]
        })


        excel_path = os.path.join(logs_dir, 'servi_argos.xlsx')
        # # Salve o DataFrame em um arquivo Excel
        df.to_excel(excel_path, index=False) 
        


def get_host_candidates(user: object) -> list:
    """Get list of host candidates for hosting services of a given user.

    Args:
        user (object): User object.

    Returns:
        list: List of host candidates.
    """
    user_switch = user.base_station.network_switch
    host_candidates = []
    for edge_server in EdgeServer.all():
        host_candidates.append(
            {
                "object": edge_server,
                "delay": calculate_path_delay(origin_network_switch=user_switch, target_network_switch=edge_server.network_switch),
                "trust_degree": user.providers_trust[str(edge_server.infrastructure_provider)],
            }
        )

    return host_candidates

