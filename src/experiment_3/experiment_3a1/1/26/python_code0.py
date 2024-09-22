import pulp
import json

# Input data in JSON format
data = json.loads('{"inputone": [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]], "manpowerone": [0.6, 0.3, 0.2], "inputtwo": [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]], "manpowertwo": [0.4, 0.2, 0.1], "stock": [150, 80, 100], "capacity": [300, 350, 280], "demand": [60000000.0, 60000000.0, 30000000.0]}')

# Parameters
K = len(data['manpowerone'])  # Number of industries
T = 5  # Planning horizon (5 years)
inputone = data['inputone']
manpowerone = data['manpowerone']
inputtwo = data['inputtwo']
manpowertwo = data['manpowertwo']
stock = data['stock']
capacity = data['capacity']
demand = data['demand']

# Create the problem
problem = pulp.LpProblem("Industry_Production", pulp.LpMaximize)

# Decision Variables
produce = pulp.LpVariable.dicts("produce", (range(K), range(T)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", (range(K), range(T)), lowBound=0)
stockhold = pulp.LpVariable.dicts("stockhold", (range(K), range(T)), lowBound=0)

# Objective Function
problem += pulp.lpSum(manpowerone[k] * produce[k][t] + manpowertwo[k] * buildcapa[k][t] for k in range(K) for t in range(T)), "Total_Manpower"

# Constraints
# Initial stock and capacity
for k in range(K):
    problem += (stockhold[k][0] == stock[k]), f"Initial_Stock_{k}"
    problem += (stockhold[k][0] == stock[k]), f"Initial_Capacity_{k}"

# Demand Constraints
for k in range(K):
    for t in range(T):
        if t == 0:
            problem += (produce[k][t] + stockhold[k][t] - demand[k] >= 0), f"Demand_Constraint_{k}_{t}"
        else:
            problem += (produce[k][t] + stockhold[k][t-1] - stockhold[k][t] >= demand[k]), f"Demand_Constraint_{k}_{t}"

# Production capacity constraint
for k in range(K):
    for t in range(2, T):
        capacity_increase = pulp.lpSum(buildcapa[j][t-2] * inputtwo[j][k] for j in range(K))
        problem += (produce[k][t] <= capacity[k] + capacity_increase), f"Production_Capacity_{k}_{t}"

# Stock balance
for k in range(K):
    for t in range(1, T):
        problem += (stockhold[k][t] == stockhold[k][t-1] + produce[k][t] - demand[k]), f"Stock_Balance_{k}_{t}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')