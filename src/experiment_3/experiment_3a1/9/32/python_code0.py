import pulp
import json

# Data
data = '''{
    "NumProducts": 2,
    "NumMachines": 2,
    "ProduceTime": [[1, 3], [2, 1]],
    "AvailableTime": [200, 100],
    "Profit": [20, 10]
}'''

data_dict = json.loads(data)

# Parameters
K = data_dict['NumProducts']
S = data_dict['NumMachines']
produce_time = data_dict['ProduceTime']
available_time = data_dict['AvailableTime']
profit = data_dict['Profit']

# Problem Definition
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(K), lowBound=0)

# Objective Function
problem += pulp.lpSum(profit[k] * x[k] for k in range(K)), "Total_Profit"

# Constraints
for s in range(S):
    problem += pulp.lpSum(produce_time[k][s] * x[k] for k in range(K)) <= available_time[s], f"Time_Constraint_{s+1}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')