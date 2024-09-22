import pulp
import json

# Data from JSON
data = json.loads('{"inputone": [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]], "manpowerone": [0.6, 0.3, 0.2], "inputtwo": [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]], "manpowertwo": [0.4, 0.2, 0.1], "stock": [150, 80, 100], "capacity": [300, 350, 280], "manpower_limit": 470000000.0}')

K = len(data['capacity'])
T = 2  # Considering we have T=2 years in this model (0 and 1 are the years we are interested in)

# Create the LP problem
problem = pulp.LpProblem("Industrial_Production", pulp.LpMaximize)

# Decision Variables
produce = pulp.LpVariable.dicts("produce", (range(K), range(T)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", (range(K), range(T)), lowBound=0)
stock = pulp.LpVariable.dicts("stock", (range(K), range(T + 1)), lowBound=0)

# Objective Function
problem += pulp.lpSum(produce[k][t] for k in range(K) for t in range(T)), "Total_Production"

# Constraints
for t in range(T):
    for k in range(K):
        # Production Constraints
        problem += produce[k][t] <= data['capacity'][k] + stock[k][t], f"Production_Constraint_{k}_{t}"
        
        # Input Constraints for Production
        problem += pulp.lpSum(data['inputone'][k][j] * produce[j][t-1] for j in range(K)) + stock[k][t-1] >= produce[k][t], f"Input_Production_Constraint_{k}_{t}"
        
        # Capacity Building Constraints
        problem += buildcapa[k][t] <= data['capacity'][k] + stock[k][t-1], f"Capacity_Building_Constraint_{k}_{t}"
        
        # Input Constraints for Capacity Building
        problem += pulp.lpSum(data['inputtwo'][k][j] * buildcapa[j][t-1] for j in range(K)) + stock[k][t-1] >= buildcapa[k][t], f"Input_Capacity_Constraint_{k}_{t}"

    # Manpower Constraints for Production
    problem += pulp.lpSum(data['manpowerone'][k] * produce[k][t] for k in range(K)) <= data['manpower_limit'], f"Manpower_Production_Constraint_{t}"
    
    # Manpower Constraints for Capacity Building
    problem += pulp.lpSum(data['manpowertwo'][k] * buildcapa[k][t] for k in range(K)) <= data['manpower_limit'], f"Manpower_Capacity_Constraint_{t}"

# Stock Balance Constraints
for k in range(K):
    problem += stock[k][0] == data['stock'][k], f"Initial_Stock_Constraint_{k}"
    
for t in range(1, T + 1):
    for k in range(K):
        problem += stock[k][t] == stock[k][t-1] + produce[k][t-1] - pulp.lpSum(data['inputone'][j][k] * produce[j][t-1] for j in range(K)) - buildcapa[k][t-1], f"Stock_Balance_Constraint_{k}_{t}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')