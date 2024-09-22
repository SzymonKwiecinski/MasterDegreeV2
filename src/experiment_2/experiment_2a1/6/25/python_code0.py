import pulp
import json

# Input data from JSON format
data = json.loads('{"inputone": [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]], "manpowerone": [0.6, 0.3, 0.2], "inputtwo": [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]], "manpowertwo": [0.4, 0.2, 0.1], "stock": [150, 80, 100], "capacity": [300, 350, 280], "manpower_limit": 470000000.0}')

# Extracting parameters
K = len(data['inputone'])  # Number of industries
T = 3  # Number of years (as per year 0 to year 2)

# Create a problem
problem = pulp.LpProblem("Industry_Production", pulp.LpMaximize)

# Decision variables
produce = pulp.LpVariable.dicts("produce", (range(K), range(T)), lowBound=0, cat='Continuous')
buildcapa = pulp.LpVariable.dicts("buildcapa", (range(K), range(T)), lowBound=0, cat='Continuous')
stockhold = pulp.LpVariable.dicts("stockhold", (range(K), range(T)), lowBound=0, cat='Continuous')

# Constraints

# Manpower constraints
for t in range(T):
    problem += (pulp.lpSum(data['manpowerone'][k] * produce[k][t] for k in range(K)) +
                 pulp.lpSum(data['manpowertwo'][k] * buildcapa[k][t] for k in range(K))) <= data['manpower_limit'], f"Manpower_Constraint_{t}")

# Input constraints for production at year t
for t in range(T):
    for k in range(K):
        if t > 0:  # Only consider production from the previous year
            problem += (produce[k][t] <= data['stock'][k] + stockhold[k][t-1] + 
                         pulp.lpSum(data['inputone'][k][j] * produce[j][t-1] for j in range(K)), f"Production_Constraint_{k}_{t}")

# Capacity constraints
for t in range(T):
    for k in range(K):
        problem += (produce[k][t] + stockhold[k][t] <= data['capacity'][k] + 
                     pulp.lpSum(buildcapa[k][t-1] for t in range(T)) - pulp.lpSum(data['manpowertwo'][k] * buildcapa[k][t] for k in range(K)), f"Capacity_Constraint_{k}_{t}")

# Output constraints for build capacity
for t in range(1, T):
    for k in range(K):
        problem += (buildcapa[k][t] <= data['capacity'][k], f"Build_Capacity_Constraint_{k}_{t}")

# Objective function: Maximize total production in the last two years
problem += pulp.lpSum(produce[k][t] for k in range(K) for t in range(T-2, T)), "Total_Production"

# Solve the problem
problem.solve()

# Prepare output
output = {
    "produce": [[produce[k][t].varValue for t in range(T)] for k in range(K)],
    "buildcapa": [[buildcapa[k][t].varValue for t in range(T)] for k in range(K)],
    "stockhold": [[stockhold[k][t].varValue for t in range(T)] for k in range(K)]
}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')