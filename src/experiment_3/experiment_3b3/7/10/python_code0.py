import pulp

# Data from JSON format
data = {
    'S': 3,
    'G': 2,
    'N': 4,
    'Capacity': [[15, 20], [20, 15], [5, 17]],
    'Population': [[7, 19], [4, 12], [9, 2], [6, 8]],
    'Distance': [[5.2, 4.0, 3.1], [3.8, 5.5, 6.1], [4.2, 3.5, 5.0], [5.0, 4.1, 3.2]]
}

# Sets
N = range(data['N'])
S = range(data['S'])
G = range(data['G'])

# Parameters
capacity = data['Capacity']
population = data['Population']
distance = data['Distance']

# Problem
problem = pulp.LpProblem("School_Assignment_Problem", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", (N, S, G), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(distance[n][s] * x[n][s][g] for n in N for s in S for g in G)

# Constraints
# Capacity Constraints
for s in S:
    for g in G:
        problem += pulp.lpSum(x[n][s][g] for n in N) <= capacity[s][g], f"Capacity_Constraint_s{s}_g{g}"

# Demand Constraints
for n in N:
    for g in G:
        problem += pulp.lpSum(x[n][s][g] for s in S) == population[n][g], f"Demand_Constraint_n{n}_g{g}"

# Solving the problem
problem.solve()

# Output
assignment = [[[pulp.value(x[n][s][g]) for g in G] for s in S] for n in N]
total_distance = pulp.value(problem.objective)

print({
    "assignment": assignment,
    "total_distance": total_distance
})

print(f' (Objective Value): <OBJ>{total_distance}</OBJ>')