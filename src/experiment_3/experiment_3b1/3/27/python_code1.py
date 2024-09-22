import pulp
import json

# Data in JSON format
data = {
    'benefit': [[10, 10], [15, 20], [10, 15], [20, 15], [5, 15]], 
    'communication': [[0.0, 0.0, 1.0, 1.5, 0.0], 
                     [0.0, 0.0, 1.4, 1.2, 0.0], 
                     [1.0, 1.4, 0.0, 0.0, 2.0], 
                     [1.5, 1.2, 0.0, 2.0, 0.7], 
                     [0.0, 0.0, 2.0, 0.7, 0.0]], 
    'cost': [[5, 14, 13], 
             [15, 5, 9], 
             [13, 9, 10]]
}

# Extracting parameters
benefit = data['benefit']
communication = data['communication']
cost = data['cost']

K = len(benefit)  # Total number of departments
L = len(cost[0])  # Total number of cities, corrected to use the first row of cost

# Create the problem variable
problem = pulp.LpProblem("Relocation_Problem", pulp.LpMinimize)

# Decision Variables: islocated[k][l]
islocated = pulp.LpVariable.dicts("islocated", 
                                    ((k, l) for k in range(K) for l in range(L)), 
                                    cat='Binary')

# Objective Function
problem += pulp.lpSum(benefit[k][l] * islocated[k, l] for k in range(K) for l in range(L)) \
           - pulp.lpSum(communication[k][j] * cost[l][j] * islocated[k, l] 
                        for k in range(K) for l in range(L) for j in range(len(cost[0]))), "Total_Cost"

# Constraints
# Each department can only be located in one city
for k in range(K):
    problem += pulp.lpSum(islocated[k, l] for l in range(L)) == 1, f"One_City_per_Department_{k}"

# No city can host more than three departments
for l in range(L):
    problem += pulp.lpSum(islocated[k, l] for k in range(K)) <= 3, f"Max_Departments_per_City_{l}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')