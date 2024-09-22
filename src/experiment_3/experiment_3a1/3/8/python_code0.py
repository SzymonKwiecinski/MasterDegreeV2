import pulp
import json

# Data provided in JSON format
data = '''{
    "NumParts": 5, 
    "NumMachines": 2, 
    "Time": [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], 
    "Profit": [30, 20, 40, 25, 10], 
    "Capacity": [700, 1000]
}'''

# Load data
data = json.loads(data)

# Indices
K = data['NumParts']
S = data['NumMachines']
time = data['Time']
profit = data['Profit']
capacity = data['Capacity']

# Create the LP problem
problem = pulp.LpProblem("Spare_Parts_Production", pulp.LpMaximize)

# Decision Variables
quantity = pulp.LpVariable.dicts("quantity", range(K), lowBound=0)

# Objective Function
problem += pulp.lpSum(profit[k] * quantity[k] for k in range(K)), "Total_Profit"

# Constraints
for s in range(S):
    problem += (pulp.lpSum(time[k][s] * quantity[k] for k in range(K)) <= capacity[s]), f"Capacity_Constraint_{s + 1}"

# Solve the problem
problem.solve()

# Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')