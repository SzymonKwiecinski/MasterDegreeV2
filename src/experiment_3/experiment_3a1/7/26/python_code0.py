import pulp
import json

# Data from the provided JSON
data = {
    'inputone': [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]],
    'manpowerone': [0.6, 0.3, 0.2],
    'inputtwo': [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]],
    'manpowertwo': [0.4, 0.2, 0.1],
    'stock': [150, 80, 100],
    'capacity': [300, 350, 280],
    'demand': [60000000.0, 60000000.0, 30000000.0]
}

K = len(data['manpowerone'])
T = 5  # number of years

# Create the problem variable
problem = pulp.LpProblem("Industry_Production", pulp.LpMaximize)

# Decision variables
produce = pulp.LpVariable.dicts("produce", (range(K), range(1, T + 1)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", (range(K), range(1, T + 1)), lowBound=0)
stockhold = pulp.LpVariable.dicts("stockhold", (range(K), range(T + 1)), lowBound=0)

# Objective Function
problem += pulp.lpSum(data['manpowerone'][k] * produce[k][t] for k in range(K) for t in range(1, T + 1)) + \
           pulp.lpSum(data['manpowertwo'][k] * buildcapa[k][t] for k in range(K) for t in range(1, T + 1)), "Total_Manpower"

# Production Constraints
for k in range(K):
    for t in range(1, T + 1):
        if t == 1:
            previous_stock = data['stock'][k]
        else:
            previous_stock = stockhold[k][t - 1]
        
        problem += (produce[k][t] + previous_stock == data['demand'][k] + 
                     stockhold[k][t] + 
                     pulp.lpSum(data['inputone'][k][j] * produce[j][t - 1] for j in range(K)) + 
                     pulp.lpSum(data['inputtwo'][k][j] * buildcapa[j][t - 2] for j in range(K)), 
                     f"Production_Constraint_k{str(k)}_t{str(t)}")

# Capacity Building Constraints
for k in range(K):
    for t in range(1, T + 1):
        problem += buildcapa[k][t] <= data['capacity'][k], f"Capacity_Constraint_k{str(k)}_t{str(t)}"

# Initial Stocks
for k in range(K):
    problem += stockhold[k][0] == data['stock'][k], f"Initial_Stock_k{str(k)}"

# Manpower Limits
max_manpower = 1000  # Example maximum manpower available
for k in range(K):
    for t in range(1, T + 1):
        problem += (data['manpowerone'][k] * produce[k][t] + data['manpowertwo'][k] * buildcapa[k][t] <= max_manpower, 
                     f"Manpower_Limit_k{str(k)}_t{str(t)}")

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')