import pulp

# Data from the provided JSON
data = {
    'benefit': [[10, 10], [15, 20], [10, 15], [20, 15], [5, 15]],
    'communication': [[0.0, 0.0, 1.0, 1.5, 0.0], [0.0, 0.0, 1.4, 1.2, 0.0], [1.0, 1.4, 0.0, 0.0, 2.0], [1.5, 1.2, 0.0, 2.0, 0.7], [0.0, 0.0, 2.0, 0.7, 0.0]],
    'cost': [[5, 14, 13], [15, 5, 9], [13, 9, 10]]
}

# Extracting sets sizes
K = len(data['benefit'])
L = len(data['benefit'][0])

# Define the Linear Program
problem = pulp.LpProblem("Department_Relocation", pulp.LpMinimize)

# Decision Variables
islocated = pulp.LpVariable.dicts("islocated", ((k, l) for k in range(K) for l in range(L)), 
                                  cat='Binary')

# Objective Function
benefit_term = pulp.lpSum(-data['benefit'][k][l] * islocated[k, l] for k in range(K) for l in range(L))
communication_cost_term = pulp.lpSum(
    data['communication'][k][j] * data['cost'][l][m] * islocated[k, l] * islocated[j, m] 
    for k in range(K) for j in range(K) for l in range(L) for m in range(L)
)

problem += benefit_term + communication_cost_term, "Total_Cost"

# Constraints
for k in range(K):
    problem += pulp.lpSum(islocated[k, l] for l in range(L)) == 1, f"Department_{k}_in_one_city"

for l in range(L):
    problem += pulp.lpSum(islocated[k, l] for k in range(K)) <= 3, f"Max_3_departments_in_city_{l}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')