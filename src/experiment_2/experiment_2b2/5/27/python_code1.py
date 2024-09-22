import pulp

# Data from the problem statement
data = {'benefit': [[10, 10], [15, 20], [10, 15], [20, 15], [5, 15]], 
        'communication': [[0.0, 0.0, 1.0, 1.5, 0.0], [0.0, 0.0, 1.4, 1.2, 0.0], 
                          [1.0, 1.4, 0.0, 0.0, 2.0], [1.5, 1.2, 0.0, 2.0, 0.7], 
                          [0.0, 0.0, 2.0, 0.7, 0.0]], 
        'cost': [[5, 14, 13], [15, 5, 9], [13, 9, 10]]
       }

benefit = data["benefit"]
communication = data["communication"]
cost = data["cost"]

num_departments = len(benefit)
num_cities = len(benefit[0])

# Problem
problem = pulp.LpProblem("Department_Location_Problem", pulp.LpMinimize)

# Decision Variables
islocated = pulp.LpVariable.dicts("islocated", 
                                  ((k, l) for k in range(num_departments) for l in range(num_cities)),
                                  cat='Binary')

# Create an auxiliary variable for each pair of departments and cities
communication_cost_pairs = pulp.LpVariable.dicts("communication_cost_pairs", 
                                                 ((k, j, l, m) for k in range(num_departments) 
                                                  for j in range(num_departments)
                                                  for l in range(num_cities) 
                                                  for m in range(num_cities)), 
                                                 cat='Binary')

# Objective Function
total_benefit = sum(islocated[k, l] * benefit[k][l] for k in range(num_departments) for l in range(num_cities))
total_communication_cost = sum(communication_cost_pairs[k, j, l, m] * communication[k][j] * cost[l][m]
                               for k in range(num_departments) for j in range(num_departments)
                               for l in range(num_cities) for m in range(num_cities))

problem += -total_benefit + total_communication_cost, "Total Costs"

# Constraints
for k in range(num_departments):
    problem += sum(islocated[k, l] for l in range(num_cities)) == 1, f"Department_{k}_Location_Constraint"

for l in range(num_cities):
    problem += sum(islocated[k, l] for k in range(num_departments)) <= 3, f"City_{l}_Capacity_Constraint"

for k in range(num_departments):
    for j in range(num_departments):
        for l in range(num_cities):
            for m in range(num_cities):
                problem += communication_cost_pairs[k, j, l, m] <= islocated[k, l], f"Auxiliary_constraint1_{k}_{j}_{l}_{m}"
                problem += communication_cost_pairs[k, j, l, m] <= islocated[j, m], f"Auxiliary_constraint2_{k}_{j}_{l}_{m}"
                problem += communication_cost_pairs[k, j, l, m] >= islocated[k, l] + islocated[j, m] - 1, f"Auxiliary_constraint3_{k}_{j}_{l}_{m}"

# Solve
problem.solve()

# Output Solution
islocated_result = [[int(pulp.value(islocated[k, l])) for l in range(num_cities)] for k in range(num_departments)]

solution = {
    "islocated": islocated_result,
}

print(solution)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')