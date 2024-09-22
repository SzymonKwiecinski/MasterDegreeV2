import pulp
import json

# Data provided in JSON format
data_json = '''{
    "time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    "machine_costs": [160, 10, 15],
    "availability": [200, 300, 500],
    "prices": [570, 250, 585, 430],
    "setup_time": [12, 8, 4, 0]
}'''

# Loading data from JSON
data = json.loads(data_json)

# Defining sets
P = len(data['prices'])  # Total number of parts
M = len(data['machine_costs'])  # Total number of machines

# Defining the problem
problem = pulp.LpProblem("Auto_Parts_Manufacturing", pulp.LpMaximize)

# Decision Variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Continuous')
setup_flag = pulp.LpVariable.dicts("setup_flag", range(P), cat='Binary')

# Objective Function
profit = pulp.lpSum(data['prices'][p] * batches[p] for p in range(P)) - \
         pulp.lpSum(data['machine_costs'][m] * pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) for m in range(M))

problem += profit, "Total Profit"

# Machine Availability Constraints
for m in range(M):
    problem += pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) <= data['availability'][m], f"Availability_Constraint_Machine_{m+1}"

# Setup Time Constraint for Machine 1
for p in range(P):
    problem += setup_flag[p] * data['setup_time'][p] + pulp.lpSum(data['time_required'][0][p] * batches[p] for p in range(P)) <= data['availability'][0], f"Setup_Time_Constraint_Part_{p+1}"

# Solving the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')