import pulp
import json

# Data provided in JSON format
data = json.loads('{"inputone": [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]], "manpowerone": [0.6, 0.3, 0.2], "inputtwo": [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]], "manpowertwo": [0.4, 0.2, 0.1], "stock": [150, 80, 100], "capacity": [300, 350, 280], "manpower_limit": 470000000.0}')

# Decoding the JSON data
inputone = data['inputone']
manpowerone = data['manpowerone']
inputtwo = data['inputtwo']
manpowertwo = data['manpowertwo']
stock = data['stock']
capacity = data['capacity']
manpower_limit = data['manpower_limit']

K = len(stock)  # Number of industries
T = 10  # Number of years (example value for this model)

# Create the problem variable
problem = pulp.LpProblem("Economic_Planning", pulp.LpMaximize)

# Decision Variables
produce = pulp.LpVariable.dicts("produce", (range(K), range(T)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", (range(K), range(T)), lowBound=0)
stockhold = pulp.LpVariable.dicts("stockhold", (range(K), range(T)), lowBound=0)
capacity_var = pulp.LpVariable.dicts("capacity", (range(K), range(T)), lowBound=0)

# Initial Conditions
for k in range(K):
    stockhold[k][0] = stock[k]
    capacity_var[k][0] = capacity[k]

# Objective Function
problem += pulp.lpSum(produce[k][T-1] for k in range(K)), "Total_Production_Last_Year"

# Constraints
# Production and Capacity Constraints
for t in range(T):
    for k in range(K):
        problem += (produce[k][t] + pulp.lpSum(inputone[k][j] * produce[j][t] for j in range(K)) <= capacity_var[k][t]), f"Capacity_Constraint_{k}_{t}"

# Capacity Build Constraint
for t in range(T - 2):
    for k in range(K):
        problem += (capacity_var[k][t + 2] == capacity_var[k][t + 2] + buildcapa[k][t]), f"Capacity_Build_Constraint_{k}_{t}"

# Stock Balance Constraints
for t in range(T - 1):
    for k in range(K):
        problem += (stockhold[k][t + 1] == stockhold[k][t] + produce[k][t] - pulp.lpSum(inputone[j][k] * produce[j][t] for j in range(K)) - buildcapa[k][t]), f"Stock_Balance_Constraint_{k}_{t}"

# Manpower Constraint
for t in range(1, T):
    problem += (pulp.lpSum(manpowerone[k] * produce[k][t] + manpowertwo[k] * buildcapa[k][t] for k in range(K)) <= manpower_limit), f"Manpower_Constraint_{t}"

# Non-negativity Constraints are already handled by lowBound parameter for variables.

# Solve the problem
problem.solve()

# Print the Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')