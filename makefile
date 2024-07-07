# Definição das variáveis
DATASET = "datasets/dataset1.json"
ALGORITMOS = spp dcf argos faticanti2020 thea

# Regra para executar a simulação com cada algoritmo
run_simulation:
	$(foreach algoritmo,$(ALGORITMOS), \
		echo "Executando simulação com o algoritmo: $(algoritmo)"; \
		python -B -m simulation --dataset $(DATASET) --algorithm $(algoritmo);)

# Regra padrão
all: 
	run_simulation
