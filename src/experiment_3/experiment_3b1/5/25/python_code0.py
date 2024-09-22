import pulp
import json

# Data from the provided JSON
data = json.loads('{"inputone": [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]], "manpowerone": [0.6, 0.3, 0.2], "inputtwo": [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]], "manpowertwo": [0.4, 0.2, 0.1], "stock": [150, 80, 100], "capacity": [300, 350, 280], "manpower_limit": 470000000.0}')

K = len(data['manpowerone'])
T = 2  # Total years of production as stated in the objective function

# Create the problem variable
problem = pulp.LpProblem("Economic_Production", pulp.LpMaximize)

# Decision Variables
produce = pulp.LpVariable.dicts("produce", (range(K), range(1, T + 1)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", (range(K), range(1, T + 1)), lowBound=0)
stockhold = pulp.LpVariable.dicts("stockhold", (range(K), range(1, T + 1)), lowBound=0)

# Objective Function
problem += pulp.lpSum(produce[k][T] + produce[k][T-1] for k in range(K))

# Constraints
# Production input constraints
for k in range(K):
    for t in range(1, T + 1):
        problem += (
            pulp.lpSum(data['inputone'][k][j] * produce[j][t - 1] for j in range(K)) + stockhold[k][t - 1] 
            >= produce[k][t], 
            f"Input_Constraint_Industry_{k}_Year_{t}"
        )

# Manpower constraints
for k in range(K):
    for t in range(1, T + 1):
        problem += (
            data['manpowerone'][k] * produce[k][t] + data['manpowertwo'][k] * buildcapa[k][t] 
            <= data['manpower_limit'], 
            f"Manpower_Constraint_Industry_{k}_Year_{t}"
        )

# Capacity constraints
for k in range(K):
    for t in range(1, T + 1):
        problem += (
            pulp.lpSum(data['inputtwo'][k][j] * buildcapa[j][t] for j in range(K)) 
            <= data['capacity'][k] + data['stock'][k] + pulp.lpSum(produce[k][t_prime] for t_prime in range(1, t - 1)), 
            f"Capacity_Constraint_Industry_{k}_Year_{t}"
        )

# Stockholding constraints
for k in range(K):
    for t in range(1, T + 1):
        problem += (
            stockhold[k][t] == data['stock'][k] + stockhold[k][t - 1] + produce[k][t - 1] - produce[k][t], 
            f"Stockholding_Constraint_Industry_{k}_Year_{t}"
        )

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')