import pulp
import json

# Data in JSON format
data = '''{
    "NumParts": 5,
    "NumMachines": 2,
    "Time": [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]],
    "Profit": [30, 20, 40, 25, 10],
    "Capacity": [700, 1000]
}'''

# Parse the data
data_dict = json.loads(data)

# Parameters
K = data_dict['NumParts']
S = data_dict['NumMachines']
time = data_dict['Time']
profit = data_dict['Profit']
capacity = data_dict['Capacity']

# Decision Variables
quantity = pulp.LpVariable.dicts("quantity", range(K), lowBound=0)

# Problem Definition
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Objective Function
problem += pulp.lpSum(profit[k] * quantity[k] for k in range(K))

# Constraints
for s in range(S):
    problem += pulp.lpSum(time[k][s] * quantity[k] for k in range(K)) <= capacity[s]

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')