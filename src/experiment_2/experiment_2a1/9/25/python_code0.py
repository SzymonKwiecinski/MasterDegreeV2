import pulp
import json

# Input data
data = {
    'inputone': [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]],
    'manpowerone': [0.6, 0.3, 0.2],
    'inputtwo': [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]],
    'manpowertwo': [0.4, 0.2, 0.1],
    'stock': [150, 80, 100],
    'capacity': [300, 350, 280],
    'manpower_limit': 470000000.0
}

K = len(data['inputone'])  # Number of industries
T = 2  # Number of years we are considering

# Create a LP problem
problem = pulp.LpProblem("Maximize_Production", pulp.LpMaximize)

# Decision Variables
produce = pulp.LpVariable.dicts("Produce", (range(K), range(T)), lowBound=0, cat='Continuous')
buildcapa = pulp.LpVariable.dicts("BuildCapa", (range(K), range(T)), lowBound=0, cat='Continuous')
stockhold = pulp.LpVariable.dicts("StockHold", (range(K), range(T)), lowBound=0, cat='Continuous')

# Objective Function: Maximize production in last two years
problem += pulp.lpSum(produce[k][t] for k in range(K) for t in range(T))

# Constraints
# Manpower Constraint
for t in range(T):
    problem += pulp.lpSum(data['manpowerone'][k] * produce[k][t] + data['manpowertwo'][k] * buildcapa[k][t] 
                          for k in range(K)) <= data['manpower_limit']

# Input Constraints for production
for k in range(K):
    for t in range(T):
        if t == 0:  # Year 0
            problem += produce[k][t] <= data['stock'][k] + data['capacity'][k]
        else:  # Year 1
            problem += produce[k][t] <= (data['stock'][k] + data['capacity'][k] + 
                                          pulp.lpSum(buildcapa[k_prime][t - 1] * data['inputone'][k_prime][k]
                                          for k_prime in range(K)))

# Capacity building constraints
for k in range(K):
    for t in range(T):
        problem += stockhold[k][t] == data['stock'][k] + pulp.lpSum(produce[k_prime][t_prime] 
                                                                      for k_prime in range(K) 
                                                                      for t_prime in range(t + 1)) - produce[k][t]

# Capacity increase from previous year
for k in range(K):
    for t in range(1, T):
        problem += stockhold[k][t] >= data['capacity'][k] + (pulp.lpSum(buildcapa[k_prime][t - 1] * data['inputtwo'][k_prime][k]
                                                                      for k_prime in range(K)) if t > 0 else 0)

# Solve the problem
problem.solve()

# Prepare output
output = {
    "produce": [[pulp.value(produce[k][t]) for t in range(T)] for k in range(K)],
    "buildcapa": [[pulp.value(buildcapa[k][t]) for t in range(T)] for k in range(K)],
    "stockhold": [[pulp.value(stockhold[k][t]) for t in range(T)] for k in range(K)]
}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')