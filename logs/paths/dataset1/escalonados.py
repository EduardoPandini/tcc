import pandas as pd
import os
import matplotlib.pyplot as plt
import matplotlib

def read_excel_files_to_dict(directory_path):
    data_dict = {}
    files = [f for f in os.listdir(directory_path) if f.startswith('servi_') and f.endswith('.xlsx')]
    
    for file in files:
        file_path = os.path.join(directory_path, file)
        df = pd.read_excel(file_path)
        
        file_key = file.split('servi_')[-1].replace('.xlsx', '')  # Extrai o nome do arquivo sem 'servi_' e sem extensão
        for column in df.columns:
            key = f"{column} ({file_key})"
            if key not in data_dict:
                data_dict[key] = []
            data_dict[key].extend(df[column].tolist())
    
    return data_dict
matplotlib.rc('font', size=20)  # Tamanho geral da fonte
matplotlib.rc('axes', titlesize=20)  # Tamanho da fonte para os títulos dos eixos
matplotlib.rc('axes', labelsize=20)  # Tamanho da fonte para os rótulos dos eixos
matplotlib.rc('xtick', labelsize=20)  # Tamanho da fonte para os rótulos do eixo x
matplotlib.rc('ytick', labelsize=20)  # Tamanho da fonte para os rótulos do eixo y
matplotlib.rc('legend', fontsize=20)  # Tamanho da fonte para a legenda
matplotlib.rc('figure', titlesize=20)

# Defina o caminho do diretório onde estão seus arquivos .xlsx
directory_path = '.'  # '.' indica o diretório atual

# Chama a função e armazena o resultado no dicionário
excel_data_dict = read_excel_files_to_dict(directory_path)

# Converte o dicionário para um DataFrame para facilitar a plotagem
df_combined = pd.DataFrame.from_dict(excel_data_dict)

# Nomes personalizados para as variáveis na legenda (com primeira letra maiúscula)
legend_names = {
    'Nome_da_Coluna_1': 'Serviços Provisionados',
    'Nome_da_Coluna_2': 'Total de Serviços',
    'Nome_da_Coluna_3': 'Serviços não Provisionados'
    # Adicione mais entradas conforme necessário
}

# Plotar os dados em um gráfico de barras único
plt.figure(figsize=(10, 6))  # Ajuste do tamanho do gráfico

# Configuração das cores para cada tipo de variável
unique_columns = {col.split(' (')[0] for col in df_combined.columns}
colors = plt.cm.get_cmap('tab20', len(unique_columns))
color_map = {column: colors(i) for i, column in enumerate(unique_columns)}

# Número de colunas e grupos de colunas
num_columns = len(df_combined.columns)
num_groups = num_columns // 3

# Plotar cada grupo de colunas com o mesmo espaço entre eles
bar_width = 0.8 / num_columns
group_width = 0.8 / num_groups
indices = range(len(df_combined))

# Criar legendas personalizadas
legend_handles = []

for i, column in enumerate(df_combined.columns):
    column_name = column.split(' (')[0]
    group_index = i // 3
    group_offset = group_index * group_width
    bars = plt.bar([x + i * bar_width + group_offset for x in indices], df_combined[column], bar_width, label=legend_names.get(column_name, column_name), color=color_map[column_name])
    legend_handles.append(bars[0])  # Adiciona apenas uma barra de cada grupo na legenda
    # Adiciona o nome do arquivo abaixo de cada conjunto de 3 barras
    if i % 3 == 0:
        file_name = column.split(' (')[1].replace(')', '').capitalize()  # Capitaliza o nome do arquivo
        plt.text(i * bar_width + group_offset + 1.5 * bar_width, -2, file_name, ha='center', fontsize=5)  # Ajuste para texto na horizontal e posição mais baixa
    # Adiciona o nome do arquivo abaixo de cada conjunto de barras
    for bar, file_name in zip(bars, excel_data_dict[column]):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), str(file_name), ha='center', va='bottom', fontsize=1)

plt.xticks([])  # Remove os números do eixo x
# plt.ylabel('Serviços')
# # Ajuste da legenda para mostrar apenas uma vez cada tipo de variável
# plt.legend(legend_handles, legend_names.values(),  bbox_to_anchor=(1.05, 1), loc='upper left')
# plt.tight_layout()  # Ajusta o layout para evitar sobreposição

# Defina o caminho do diretório onde deseja salvar a imagem
save_directory = '/home/pandini/Desktop/thea/thea/imagens_dataset1'

# Certifique-se de que o diretório existe
os.makedirs(save_directory, exist_ok=True)

# Defina o caminho completo do arquivo
save_path = os.path.join(save_directory, 'grafico_servicos.png')

# Salve a figura
plt.savefig(save_path)

plt.show()
