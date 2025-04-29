import random

class Book:
    def __init__(self):
        self.state = "Available"       # starea initiala
        self.res_cust_id = None        # ID client care a rezervat
        self.bor_cust_id = None        # ID client care a imprumutat

    # functie de reserve
    def res(self, x):
        if self.state == "Available" and x > 0:
            self.res_cust_id = x
            self.state = "Reserved"
            return True
        return False

    # functie de imprumut
    def bor(self, x):
        if self.state == "Reserved" and x == self.res_cust_id:
            self.bor_cust_id = x
            self.state = "Borrowed"
            return True
        return False


#functie fitness
def evaluate_fitness(individual):
    x1, x2 = individual
    book = Book()

    if not book.res(x1):
        return 2 + normalize(branch_distance_res(book, x1))  # penalizare mare 
    if not book.bor(x2):
        return 1 + normalize(branch_distance_bor(book, x2))  # penalizare mai mica
    return 0  # succes

# functie de distanta pentru reserve
def branch_distance_res(book, x):
    if book.state != "Available":
        return 1e6  # Penalizare mare
    return max(0, 1 - x)  # Vrem ca x > 0

# functie de distanta pentru borrow
def branch_distance_bor(book, x):
    if book.state != "Reserved":
        return 1e6  # penalizare mare
    return abs(x - book.res_cust_id)  # vrem ca x == res_cust_id

# normalizare a distantei într-un interval [0, 1)
def normalize(distance):
    return distance / (1 + distance)


#algoritm genetic
POP_SIZE = 30            # nr. indivizi pe generatie
GENERATIONS = 100        # nr. total de generatii
MUTATION_RATE = 0.3      # prob de mutație
DOMAIN = (-10, 10)       

# initializam populatie cu indiv. aleatori
population = [[random.randint(*DOMAIN), random.randint(*DOMAIN)] for _ in range(POP_SIZE)]

solution = None
for gen in range(GENERATIONS):
    # calculam fitness-ul pt fiecare individ
    fitnesses = [evaluate_fitness(ind) for ind in population]

    best_fit = min(fitnesses)
    best_index = fitnesses.index(best_fit)
    print(f"Generatia {gen}: Cel mai bun fitness = {best_fit:.4f}")
    print(f"  Cel mai bun individ: {population[best_index]}")

    # daca am gasit individ perfect, ne oprim
    if best_fit == 0:
        solution = population[best_index]
        print(f"Individ cu fitness 0 găsit în generatia {gen}: {solution}")
        break

    # luam cei mai buni indivizi
    sorted_pop = [x for _, x in sorted(zip(fitnesses, population))]
    parents = sorted_pop[:POP_SIZE // 2]

    # crossover si mutatie pentru a genera urmasi
    offspring = []
    while len(offspring) < POP_SIZE // 2:
        p1, p2 = random.sample(parents, 2)  # luam 2 parinti
        cut = random.randint(1, 1)  # poz unde se face crossover (la mijloc)
        child = p1[:cut] + p2[cut:]  # combina genele parintilor
        if random.random() < MUTATION_RATE:
            idx = random.randint(0, 1)
            child[idx] = random.randint(*DOMAIN)  # mutam aleatoriu una din gene
        offspring.append(child)

    # noua populatie = parinti + urmasi
    population = parents + offspring

# sol finala
solution = solution if solution else population[0]
fitness_value = evaluate_fitness(solution)
print(f"\nSolutie finala gasita: {solution}, Fitness: {fitness_value}")
