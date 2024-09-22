import pulp

# Data from the JSON
data = {
    'S': 3, 
    'G': 2, 
    'N': 4, 
    'Capacity': [[15, 20], [20, 15], [5, 17]], 
    'Population': [[7, 19], [4, 12], [9, 2], [6, 8]], 
    'Distance': [[5.2, 4.0, 3.1], [3.8, 5.5, 6.1], [4.2, 3.5, 5.0], [5.0, 4.1, 3.2]]
}

# Extract data
S = list(range(data['S']))
G = list(range(data['G']))
N = list(range(data['N']))
capacity = data['Capacity']
population = data['Population']
distance = data['Distance']

# Create the LP problem
problem = pulp.LpProblem("School_Assignment", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", ((n, s, g) for n in N for s in S for g in G), 
                          lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(distance[n][s] * x[n, s, g] for n in N for s in S for g in G)

# Capacity Constraints
for s in S:
    for g in G:
        problem += (pulp.lpSum(x[n, s, g] for n in N) <= capacity[s][g], 
                    f"Capacity_Constraint_S{s}_G{g}")

# Demand Constraints
for n in N:
    for g in G:
        problem += (pulp.lpSum(x[n, s, g] for s in S) == population[n][g], 
                    f"Demand_Constraint_N{n}_G{g}")

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')