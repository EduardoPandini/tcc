# Importing EdgeSimPy components
from edge_sim_py.components.edge_server import EdgeServer
from edge_sim_py.components.service import Service

# Importing helper methods
from simulation.helper_methods import *


def dcf(parameters: dict = {}):
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

        
        for service in services:
            if service.server is not None:
                    servi+=1
            # if not service.being_provisioned:
            app = service.application
            user = app.users[0]
            services_per_server = {server: 0 for server in EdgeServer.all()}
            for server in services_per_server.keys():
                for srv in server.services:
                    if srv.application == app:
                        # print("é igual")
                        services_per_server[server] += 1
                        # print(services_per_server[server])
                
                # Ordenando os servidores com base no número de serviços da mesma aplicação (do menor para o maior) e caso igual, pela cpu
                edge_servers = sorted(services_per_server.keys(), key=lambda server: (
                    -services_per_server[server], -(user.providers_trust[str(server.infrastructure_provider)]), service.cpu_demand - server.cpu_demand))
                    
            
            for edge_server in edge_servers:

                #se nao tem server ainda é aqui
                if edge_server.has_capacity_to_host(service) and service.server is None:
                    provision(user=user, application=app, service=service, edge_server=edge_server)                       
                    # contar_pares_ocorrencias(user.set_communication_path(app), contador)
                    servi+=1
                    break
                    


                #se já tem
                elif service in topN_servi and edge_server.has_capacity_to_host(service) and edge_server != service.server:
                    # print("quanto tá usando",edge_server.cpu_demand)
                    # print("quanto deveria ficar",edge_server.cpu_demand+service.cpu_demand)
                    service.provision(target_server=edge_server)
                    # print("quanto ficou",edge_server.cpu_demand)
                    # contar_pares_ocorrencias(user.set_communication_path(app), contador)
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
        
        # Caminho relativo para o diretório "logs"
        logs_dir = os.path.join(os.getcwd(), 'logs/paths/dataset2')
        if not os.path.exists(logs_dir):
            os.makedirs(logs_dir)
        
        # Caminho do arquivo Excel
        excel_path = os.path.join(logs_dir, 'path_dcf.xlsx')
        
        # Atualizar o arquivo Excel com o novo DataFrame
        append_to_excel(excel_path, df)
        df = pd.DataFrame({
        'Servi': [servi],
        'Total Services': [servicosTotal],
        'Difference': [diferenca]
        })


        excel_path = os.path.join(logs_dir, 'servi_dcf.xlsx')
        # # Salve o DataFrame em um arquivo Excel
        df.to_excel(excel_path, index=False) 