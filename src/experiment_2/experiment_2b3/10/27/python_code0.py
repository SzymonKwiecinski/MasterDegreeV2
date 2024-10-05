import pulp

# Data from the JSON
benefit_data = {'benefit': [[10, 10], [15, 20], [10, 15], [20, 15], [5, 15]], 
                'communication': [[0.0, 0.0, 1.0, 1.5, 0.0], [0.0, 0.0, 1.4, 1.2, 0.0], 
                                  [1.0, 1.4, 0.0, 0.0, 2.0], [1.5, 1.2, 0.0, 2.0, 0.7], 
                                  [0.0, 0.0, 2.0, 0.7, 0.0]], 
                'cost': [[5, 14, 13], [15, 5, 9], [13, 9, 10]]}

benefit = benefit_data['benefit']
communication = benefit_data['communication']
cost = benefit_data['cost']

K = len(communication)  # Number of departments
L = len(cost)           # Number of cities

# Create a Linear Programming problem
problem = pulp.LpProblem("Department_Relocation", pulp.LpMinimize)

# Decision variables
islocated = [[pulp.LpVariable(f"islocated_{k}_{l}", cat='Binary') for l in range(L)] for k in range(K)]

# Objective Function: Minimize cost = - benefits + communication costs
objective = pulp.lpSum([
    -benefit[k][l] * islocated[k][l] 
    for k in range(K) for l in range(L)
]) + pulp.lpSum([
    communication[k][j] * cost[l][m] * islocated[k][l] * islocated[j][m]
    for k in range(K) for j in range(K) for l in range(L) for m in range(L)
])

problem += objective

# Constraints:

# Each department must be located in exactly one city
for k in range(K):
    problem += pulp.lpSum([islocated[k][l] for l in range(L)]) == 1

# Each city can host at most 3 departments
for l in range(L):
    problem += pulp.lpSum([islocated[k][l] for k in range(K)]) <= 3

# Solve the problem
problem.solve()

# Extract results
islocated_result = [[int(islocated[k][l].varValue) for l in range(L)] for k in range(K)]

result = {
    "islocated": islocated_result,
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')