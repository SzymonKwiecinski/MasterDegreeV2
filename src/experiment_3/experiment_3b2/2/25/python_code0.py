import pulp
import json

# Data in JSON format
data = json.loads('{"inputone": [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]], "manpowerone": [0.6, 0.3, 0.2], "inputtwo": [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]], "manpowertwo": [0.4, 0.2, 0.1], "stock": [150, 80, 100], "capacity": [300, 350, 280], "manpower_limit": 470000000.0}')

# Indices
K = len(data['stock'])  # Number of industries
T = 3  # Number of years (assuming 0, 1, 2)

# Create the problem
problem = pulp.LpProblem("Maximize_Production", pulp.LpMaximize)

# Decision Variables
produce = pulp.LpVariable.dicts("produce", (range(K), range(T)), lowBound=0, cat='Continuous')
buildcapa = pulp.LpVariable.dicts("buildcapa", (range(K), range(T)), lowBound=0, cat='Continuous')
stockhold = pulp.LpVariable.dicts("stockhold", (range(K), range(T)), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum([produce[k][T-1] + produce[k][T] for k in range(K)]), "Total_Production"

# Constraints
# Stock and Production Balance
for k in range(K):
    for t in range(1, T):
        problem += (stockhold[k][t-1] + pulp.lpSum(data['inputone'][k][j] * produce[j][t] for j in range(K)) + buildcapa[k][t] 
                    <= data['capacity'][k] + buildcapa[k][t-2], f"Stock_Production_Balance_{k}_{t}")

# Manpower Constraint
for t in range(T):
    problem += (pulp.lpSum(data['manpowerone'][k] * produce[k][t] + data['manpowertwo'][k] * buildcapa[k][t] for k in range(K)) 
                <= data['manpower_limit'], f"Manpower_Constraint_{t}")

# Initial Stock and Capacity
for k in range(K):
    problem += (stockhold[k][0] == data['stock'][k], f"Initial_Stock_{k}")
    problem += (buildcapa[k][0] == 0, f"Initial_Capacity_{k}")  # Assuming we don't build capacity in the first year

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')