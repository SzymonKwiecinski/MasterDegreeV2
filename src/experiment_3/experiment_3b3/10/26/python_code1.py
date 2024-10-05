import pulp

# Initialize data
inputone = [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]]
manpowerone = [0.6, 0.3, 0.2]
inputtwo = [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]]
manpowertwo = [0.4, 0.2, 0.1]
initial_stock = [150, 80, 100]
capacity = [300, 350, 280]
demand = [60000000.0, 60000000.0, 30000000.0]

K = len(demand)
T = 5

# Define the problem
problem = pulp.LpProblem("EconomicProductionMaximization", pulp.LpMaximize)

# Define decision variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(1, T+1)), lowBound=0, cat='Continuous')
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(1, T+1)), lowBound=0, cat='Continuous')
stock = pulp.LpVariable.dicts("stock", ((k, t) for k in range(K) for t in range(T+1)), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(manpowerone[k] * produce[k, t] + manpowertwo[k] * buildcapa[k, t] for k in range(K) for t in range(1, T+1))

# Constraints
# Balance constraints for production and consumption
for k in range(K):
    for t in range(1, T+1):
        problem += produce[k, t] + (stock[k, t-1] if t > 1 else initial_stock[k]) == demand[k] + stock[k, t]

# Capacity constraints
for k in range(K):
    for t in range(1, T+1):
        problem += stock[k, t] <= capacity[k]

# Resource constraints for production
for k in range(K):
    for t in range(1, T+1):
        problem += pulp.lpSum(inputone[k][j] * produce[j, t] for j in range(K)) + (stock[k, t-1] if t > 1 else initial_stock[k]) >= produce[k, t]

# Resource constraints for building capacity
for k in range(K):
    for t in range(1, T+1):
        problem += pulp.lpSum(inputtwo[k][j] * buildcapa[j, t] for j in range(K)) + (stock[k, t-1] if t > 1 else initial_stock[k]) >= buildcapa[k, t]

# Initial conditions
# Stock for year 0 initialized
for k in range(K):
    stock[k, 0] = initial_stock[k]

# Solve the problem
problem.solve()

# Display results
produce_result = [[pulp.value(produce[k, t]) for t in range(1, T+1)] for k in range(K)]
buildcapa_result = [[pulp.value(buildcapa[k, t]) for t in range(1, T+1)] for k in range(K)]
stock_result = [[pulp.value(stock[k, t]) for t in range(T+1)] for k in range(K)]

print("Produce:", produce_result)
print("Build Capacity:", buildcapa_result)
print("Stock Hold:", stock_result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')