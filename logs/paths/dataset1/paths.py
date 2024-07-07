import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rc('font', size=15)  # Tamanho geral da fonte
matplotlib.rc('axes', titlesize=15)  # Tamanho da fonte para os títulos dos eixos
matplotlib.rc('axes', labelsize=15)  # Tamanho da fonte para os rótulos dos eixos
matplotlib.rc('xtick', labelsize=15)  # Tamanho da fonte para os rótulos do eixo x
matplotlib.rc('ytick', labelsize=15)  # Tamanho da fonte para os rótulos do eixo y
matplotlib.rc('legend', fontsize=15)  # Tamanho da fonte para a legenda
matplotlib.rc('figure', titlesize=15)
# Diretório para salvar as imagens
output_dir = "/home/pandini/Desktop/thea/thea/imagens_dataset1"
# file_names = ['path_argos_1.xlsx', 'path_thea_1.xlsx', 'path_fati_1.xlsx', 'path_spp_1.xlsx', 'path_dcf_1.xlsx']
file_names = ['path_argos.xlsx', 'path_thea.xlsx', 'path_faticanti.xlsx', 'path_spp.xlsx', 'path_dcf.xlsx']
# Verificar se o diretório de saída existe, senão, criá-lo
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
# Função para carregar os dados de um arquivo Excel específico
def load_data(file):
    df = pd.read_excel(file)
    return df['Ocorrências']

# Definir cores padrão para os gráficos
colors = ['blue', 'red', 'green', 'orange', 'purple']

# Listas para armazenar os dados acumulados
all_bins_count = []
all_cdfs = []

# Iterar sobre cada arquivo Excel e acumular os dados
for file, color in zip(file_names, colors):
    data = load_data(file)

    # Calcular o histograma
    count, bins_count = np.histogram(data, bins=10, density=True)

    # Adicionar os dados ao acumulador
    all_bins_count.append(bins_count)
    all_cdfs.append(np.cumsum(count / sum(count)))

    # Plotar o CDF do arquivo atual
    plt.figure()
    plt.plot(bins_count[1:], np.cumsum(count / sum(count)), label=f'{os.path.basename(file).split("_")[1].split(".")[0].capitalize()}', color=color)
    plt.xlabel('Valores')
    plt.ylabel('Probabilidade acumulada')
    # plt.xlim(0, 25)  # Intervalo X fixado entre 0 e 25
    plt.ylim(0, 1)   # Intervalo Y fixado entre 0 e 1
    plt.legend()
    plt.grid(False)  # Remover o grid de fundo

    # Salvar o gráfico na pasta de saída com o nome adequado
    output_filename = os.path.join(output_dir, f"{os.path.basename(file).split('_')[1].split('.')[0].lower()}_cdf.png")
    plt.savefig(output_filename, dpi=120)
    
    plt.show()

# Plotar todos os CDFs juntos
plt.figure()
for bins_count, cdf, file_name, color in zip(all_bins_count, all_cdfs, file_names, colors):
    plt.plot(bins_count[1:], cdf, label=f'{os.path.basename(file_name).split("_")[1].split(".")[0].capitalize()}', color=color)

plt.xlabel('Valores')
plt.ylabel('Probabilidade acumulada')
plt.xlim(0, 25)  # Intervalo X fixado entre 0 e 25
plt.ylim(0, 1)   # Intervalo Y fixado entre 0 e 1
plt.legend()
plt.grid(False)  # Remover o grid de fundo

# Salvar o gráfico com todos os CDFs juntos na pasta de saída
# output_filename = os.path.join(output_dir, "all_cdfs_1.png")
output_filename = os.path.join(output_dir, "all_cdfs.png")
plt.savefig(output_filename, dpi=120)

plt.show()