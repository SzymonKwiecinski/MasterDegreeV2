import pulp

# Data from JSON
data = {
    'inputone': [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]],
    'manpowerone': [0.6, 0.3, 0.2],
    'inputtwo': [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]],
    'manpowertwo': [0.4, 0.2, 0.1],
    'stock': [150, 80, 100],
    'capacity': [300, 350, 280],
    'manpower_limit': 470000000.0
}

# Model parameters
K = len(data['capacity'])  # Number of industries
T = 5  # Number of years (example)

# Initialize problem
problem = pulp.LpProblem("Economic_Production", pulp.LpMaximize)

# Variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Continuous')
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Continuous')
stock = pulp.LpVariable.dicts("stock", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Continuous')

# Objective
problem += pulp.lpSum(produce[k, T-2] + produce[k, T-1] for k in range(K)), "Maximize_Last_Two_Years_Production"

# Constraints
# 1. Production Constraints
for k in range(K):
    for t in range(T):
        problem += produce[k, t] <= data['capacity'][k] + (stock[k, t-1] if t > 0 else data['stock'][k]), f"Production_Constraint_{k}_{t}"

# 2. Manpower Constraints
for t in range(T):
    problem += (
        sum(data['manpowerone'][k] * produce[k, t] for k in range(K)) +
        sum(data['manpowertwo'][k] * buildcapa[k, t] for k in range(K))
        <= data['manpower_limit']
    ), f"Manpower_Constraint_{t}"

# 3. Input Constraints for Production
for k in range(K):
    for t in range(T):
        problem += (
            sum(data['inputone'][k][j] * produce[j, t-1] for j in range(K)) <= produce[k, t]
        ), f"Input_Production_Constraint_{k}_{t}"

# 4. Input Constraints for Capacity Building
for k in range(K):
    for t in range(T):
        problem += (
            sum(data['inputtwo'][k][j] * buildcapa[j, t] for j in range(K)) <= buildcapa[k, t]
        ), f"Input_Capacity_Constraint_{k}_{t}"

# 5. Stock Constraints
for k in range(K):
    for t in range(T):
        if t > 0:
            problem += (
                stock[k, t] == stock[k, t-1] + produce[k, t-1] - sum(data['inputone'][j][k] * produce[j, t-1] for j in range(K))
            ), f"Stock_Constraint_{k}_{t}"

# 6. Initial Stocks
for k in range(K):
    problem += stock[k, 0] == data['stock'][k], f"Initial_Stock_{k}"

# Solve problem
problem.solve()

# Output
print("Status:", pulp.LpStatus[problem.status])

# Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Output variables
produce_vals = {key: pulp.value(var) for key, var in produce.items()}
buildcapa_vals = {key: pulp.value(var) for key, var in buildcapa.items()}
stock_vals = {key: pulp.value(var) for key, var in stock.items()}

print("Production:", produce_vals)
print("Build Capacity:", buildcapa_vals)
print("Stock:", stock_vals)