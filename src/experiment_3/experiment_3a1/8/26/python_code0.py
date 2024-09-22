import pulp
import json

# Data from the provided JSON format
data = json.loads('{"inputone": [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]], "manpowerone": [0.6, 0.3, 0.2], "inputtwo": [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]], "manpowertwo": [0.4, 0.2, 0.1], "stock": [150, 80, 100], "capacity": [300, 350, 280], "demand": [60000000.0, 60000000.0, 30000000.0]}')

# Extracting data
inputone = data['inputone']
manpowerone = data['manpowerone']
inputtwo = data['inputtwo']
manpowertwo = data['manpowertwo']
stock = data['stock']
capacity = data['capacity']
demand = data['demand']
manpower_available = 1000000  # Example value for total manpower available

# Number of industries and years
K = len(manpowerone)
T = 5

# Create the linear programming problem
problem = pulp.LpProblem("Industry_Production_Optimization", pulp.LpMaximize)

# Decision variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(1, T + 1)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(1, T + 1)), lowBound=0)
stockhold = pulp.LpVariable.dicts("stockhold", ((k, t) for k in range(K) for t in range(0, T + 1)), lowBound=0)

# Objective function
problem += pulp.lpSum(manpowerone[k] * produce[k, t] for k in range(K) for t in range(1, T + 1)) + \
           pulp.lpSum(manpowertwo[k] * buildcapa[k, t] for k in range(K) for t in range(1, T + 1))

# Constraints
for k in range(K):
    for t in range(1, T + 1):
        problem += stockhold[k, t-1] + produce[k, t-1] + buildcapa[k, t-1] - stockhold[k, t] >= demand[k], f"Demand_Constraint_{k}_{t}"
        
    problem += stockhold[k, 0] == stock[k], f"Initial_Stock_{k}"
    
    for t in range(1, T + 1):
        problem += pulp.lpSum(inputone[k][j] * produce[j, t-1] for j in range(K)) + \
                   pulp.lpSum(inputtwo[k][j] * buildcapa[j, t-1] for j in range(K)) <= capacity[k], f"Input_Constraint_{k}_{t}"
        problem += pulp.lpSum(manpowerone[k] * produce[k, t] for k in range(K)) + \
                   manpowertwo[k] * buildcapa[k, t] <= manpower_available, f"Manpower_Constraint_{k}_{t}"
        
        # Update stock for the next year
        if t < T:
            problem += stockhold[k, t+1] == stockhold[k, t] + produce[k, t] - demand[k], f"Stock_Update_{k}_{t}"
            
# Capacity Building Constraint
for k in range(K):
    problem += capacity[k] >= pulp.lpSum(buildcapa[k, t] for t in range(1, T + 1)), f"Capacity_Building_{k}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')