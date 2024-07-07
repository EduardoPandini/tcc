# Importing EdgeSimPy components
from edge_sim_py.components.edge_server import EdgeServer
from edge_sim_py.components.service import Service
import time

# Importing helper methods
from simulation.helper_methods import *
from __main__ import *



def faticanti2020(parameters: dict = {}):
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
        """Adapted version of [1], that focuses on finding host servers for microservice-based applications on
        Edge Computing scenarios with multiple infrastructure providers.

        [1] Faticanti, Francescomaria, et al. "Deployment of Application Microservices in Multi-Domain Federated
        Fog Environments." International Conference on Omni-layer Intelligent Systems (COINS). IEEE, 2020.

        Args:
            parameters (dict, optional): Algorithm parameters. Defaults to {}.
        """
        # Sorting services based on their positions in their application's service chain
        services = sorted(Service.all(), key=lambda service: service.application.services.index(service))

        for service in services:
            if service.server is not None:
                    servi+=1
            app = service.application
            user = app.users[0]

            # Sorting edge servers by: trustworthiness, distance from user (in terms of delay), and free resources
            edge_servers = sorted(
                EdgeServer.all(),
                key=lambda s: (
                    -(user.providers_trust[str(s.infrastructure_provider)]),
                    calculate_path_delay(origin_network_switch=user.base_station.network_switch, target_network_switch=s.network_switch),
                    s.cpu - s.cpu_demand,
                ),
            )

            # Greedily iterating over the list of EdgeNode candidates to find the best node to host the service
            for edge_server in edge_servers:

                        #se nao tem server ainda é aqui
                        if edge_server.has_capacity_to_host(service) and service.server is None:
                            provision(user=user, application=app, service=service, edge_server=edge_server)                       
                            servi+=1
                            break



                        #se já tem server é aqui
                        elif service in topN_servi and edge_server.has_capacity_to_host(service) and edge_server != service.server:
                            service.provision(target_server=edge_server)
                            print("migrei")
                            break
            contar_pares_ocorrencias(user.set_communication_path(app), contador)
    finally:
        current_step = int(parameters.get('current_step', 0))
        print(current_step)
        servicosTotal = int(len(Service.all()))
        diferenca  = servicosTotal - servi
        print("todos os servi", servicosTotal)
        print("servi escalonado", servi)
        print("servi não escalonado", diferenca)
        gerar_grafico_contagem(dict(sorted(contador.items(), key=lambda item: item[1], reverse=True)))
        
        # Criar DataFrame a partir do contador
        df = pd.DataFrame(list(contador.items()), columns=['Par', 'Ocorrências'])
        
        # Ordenar o DataFrame pelo número de ocorrências de forma decrescente
        df = df.sort_values(by='Ocorrências', ascending=False)
        
        # # Caminho relativo para o diretório "logs"
        logs_dir = os.path.join(os.getcwd(), 'logs/paths/dataset2')
        if not os.path.exists(logs_dir):
            os.makedirs(logs_dir)
        
        # Caminho do arquivo Excel
        excel_path = os.path.join(logs_dir, 'path_faticanti.xlsx')
        
        # Atualizar o arquivo Excel com o novo DataFrame
        append_to_excel(excel_path, df)
        df = pd.DataFrame({
        'Servi': [servi],
        'Total Services': [servicosTotal],
        'Difference': [diferenca]
        })
        

        excel_path = os.path.join(logs_dir, 'servi_fati.xlsx')
        # # Salve o DataFrame em um arquivo Excel
        df.to_excel(excel_path, index=False) 

