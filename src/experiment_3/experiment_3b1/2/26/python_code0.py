import pulp
import json

# Data input from JSON format
data = {
    'inputone': [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]],
    'manpowerone': [0.6, 0.3, 0.2],
    'inputtwo': [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]],
    'manpowertwo': [0.4, 0.2, 0.1],
    'stock': [150, 80, 100],
    'capacity': [300, 350, 280],
    'demand': [60000000.0, 60000000.0, 30000000.0]
}

K = len(data['stock'])  # Number of industries
T = 5  # Number of years

# Create the problem
problem = pulp.LpProblem("Maximize_Manpower_Requirement", pulp.LpMaximize)

# Decision Variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(1, T + 1)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(1, T + 1)), lowBound=0)
stockhold = pulp.LpVariable.dicts("stockhold", ((k, t) for k in range(K) for t in range(1, T + 1)), lowBound=0)

# Objective Function
problem += pulp.lpSum(data['manpowerone'][k] * produce[(k, t)] + data['manpowertwo'][k] * buildcapa[(k, t)]
                      for k in range(K) for t in range(1, T + 1))

# Constraints
# Production Capacity
for k in range(K):
    for t in range(1, T + 1):
        problem += (produce[(k, t)] + (stockhold[(k, t-1)] if t > 1 else data['stock'][k]) - stockhold[(k, t)]) <= data['capacity'][k]

# Demand Satisfaction
for k in range(K):
    for t in range(1, T + 1):
        problem += (produce[(k, t)] + (stockhold[(k, t-1)] if t > 1 else data['stock'][k])) >= data['demand'][k] + stockhold[(k, t)]

# Manpower Requirement for Production
for k in range(K):
    for t in range(1, T + 1):
        problem += (data['manpowerone'][k] * produce[(k, t)]) <= 1  # Assuming 1 available manpower unit per year

# Building Capacity
for k in range(K):
    for t in range(1, T + 1):
        problem += buildcapa[(k, t)] <= stockhold[(k, t)]

# Stock Holding
for k in range(K):
    for t in range(1, T + 1):
        problem += stockhold[(k, t)] == (stockhold[(k, t-1)] if t > 1 else data['stock'][k]) + produce[(k, t)] - data['demand'][k]

# Capacity Building Delay
for k in range(K):
    problem += data['capacity'][k] + pulp.lpSum(buildcapa[(k, t)] for t in range(1, T-1)) >= data['capacity'][k] + pulp.lpSum(produce[(k, t)] for t in range(1, T + 1))

# Solve the problem
problem.solve()

# Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

for k in range(K):
    for t in range(1, T + 1):
        print(f'Produce [{k}, {t}]: {produce[(k, t)].varValue}, BuildCapa [{k}, {t}]: {buildcapa[(k, t)].varValue}, StockHold [{k}, {t}]: {stockhold[(k, t)].varValue}')