import random

def fitness(x):
    return x**3 - 6*x + 14

def decode(individual, x_min, x_max):
    decimal_value = int("".join(str(bit) for bit in individual), 2)
    precision = (x_max - x_min) / (2**len(individual) - 1)
    return x_min + decimal_value * precision

def create_individual(num_bits):
    return [random.randint(0, 1) for _ in range(num_bits)]

def create_population(pop_size, num_bits):
    return [create_individual(num_bits) for _ in range(pop_size)]

def crossover(parent1, parent2, num_cuts):
    if num_cuts == 1:
        cut_point = random.randint(1, len(parent1) - 1)
        return parent1[:cut_point] + parent2[cut_point:], parent2[:cut_point] + parent1[cut_point:]
    elif num_cuts == 2:
        cut_point1 = random.randint(1, len(parent1) - 2)
        cut_point2 = random.randint(cut_point1 + 1, len(parent1) - 1)
        return (parent1[:cut_point1] + parent2[cut_point1:cut_point2] + parent1[cut_point2:],
                parent2[:cut_point1] + parent1[cut_point1:cut_point2] + parent2[cut_point2:])

def mutate(individual, mutation_rate):
    return [bit if random.random() > mutation_rate else 1 - bit for bit in individual]

def tournament_selection(population, k, x_min, x_max):
    selected = random.sample(population, k)
    selected_fitness = [fitness(decode(ind, x_min, x_max)) for ind in selected]
    return selected[selected_fitness.index(min(selected_fitness))]

def genetic_algorithm(pop_size, num_bits, x_min, x_max, max_generations, mutation_rate, num_cuts):
    population = create_population(pop_size, num_bits)
    
    for generation in range(max_generations):
        new_population = []
        
        while len(new_population) < pop_size:
            parent1 = tournament_selection(population, 3, x_min, x_max)
            parent2 = tournament_selection(population, 3, x_min, x_max)
            
            offspring1, offspring2 = crossover(parent1, parent2, num_cuts)
            new_population.append(mutate(offspring1, mutation_rate))
            if len(new_population) < pop_size:
                new_population.append(mutate(offspring2, mutation_rate))
        
        population = new_population
    
    best_individual = min(population, key=lambda ind: fitness(decode(ind, x_min, x_max)))
    return decode(best_individual, x_min, x_max)

x_min, x_max = -10, 10
num_bits = 16

print("Configuração do Algoritmo Genético")
pop_size = int(input("Tamanho da população (padrão 10): ") or 10)
max_generations = int(input("Número máximo de gerações: "))
mutation_rate = float(input("Taxa de mutação (padrão 0.01): ") or 0.01)
num_cuts = int(input("Número de pontos de corte para crossover (1 ou 2): "))

best_x = genetic_algorithm(pop_size, num_bits, x_min, x_max, max_generations, mutation_rate, num_cuts)
print("\nResultados:")
print("Melhor x encontrado:", best_x)
print("Valor mínimo de f(x):", fitness(best_x))