import pulp

# Data
data = {
    'inputone': [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]],
    'manpowerone': [0.6, 0.3, 0.2],
    'inputtwo': [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]],
    'manpowertwo': [0.4, 0.2, 0.1],
    'stock': [150, 80, 100],
    'capacity': [300, 350, 280],
    'manpower_limit': 470000000.0
}

# Constants
K = len(data['stock'])  # number of industries
T = 5  # number of years (for example)

# Define the problem
problem = pulp.LpProblem("Industry_Production", pulp.LpMaximize)

# Decision variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(1, T+1)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(1, T+1)), lowBound=0)
stock = pulp.LpVariable.dicts("stock", ((k, t) for k in range(K) for t in range(T)), lowBound=0)

# Initial conditions
for k in range(K):
    problem += stock[k, 0] == data['stock'][k]

# Objective function
problem += pulp.lpSum(produce[k, T-1] + produce[k, T] for k in range(K)), "Maximize_Total_Production_Last_Two_Years"

# Constraints
# Production constraints
for k in range(K):
    for t in range(1, T):
        problem += produce[k, t] <= stock[k, t-1] + pulp.lpSum(data['inputone'][k][j] * produce[j, t-1] for j in range(K)), f"Production_Constraint_{k}_{t}"

# Manpower constraints
for t in range(1, T+1):
    problem += pulp.lpSum(data['manpowerone'][k] * produce[k, t] for k in range(K)) + pulp.lpSum(data['manpowertwo'][k] * buildcapa[k, t] for k in range(K)) <= data['manpower_limit'], f"Manpower_Constraint_{t}"

# Capacity building constraints
# Updated to handle 't+2', ensured valid indices are used
for k in range(K):
    for t in range(T-2):  # Ensure index (t+2) never exceeds the range
        problem += data['capacity'][k] + pulp.lpSum(data['inputtwo'][k][j] * buildcapa[j, t] for j in range(K)) <= data['capacity'][k], f"Capacity_Building_Constraint_{k}_{t}"

# Stock balance constraints
# Assume initial stock is correct
for k in range(K):
    for t in range(1, T):
        problem += stock[k, t] == stock[k, t-1] + produce[k, t] - pulp.lpSum(buildcapa[j, t] * data['inputtwo'][j][k] for j in range(K)), f"Stock_Balance_Constraint_{k}_{t}"

# Solve the problem
problem.solve()

# Output
produce_output = [[pulp.value(produce[k, t]) for t in range(1, T+1)] for k in range(K)]
buildcapa_output = [[pulp.value(buildcapa[k, t]) for t in range(1, T+1)] for k in range(K)]
stockhold_output = [[pulp.value(stock[k, t]) for t in range(T)] for k in range(K)]

print(f"Produce Output: {produce_output}")
print(f"Build Capa Output: {buildcapa_output}")
print(f"Stockhold Output: {stockhold_output}")
print(f" (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")