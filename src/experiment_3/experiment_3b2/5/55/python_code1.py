import pulp
import json

# Data provided in JSON format
data = '''
{
    "time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    "machine_costs": [160, 10, 15],
    "availability": [200, 300, 500],
    "prices": [570, 250, 585, 430],
    "min_batches": [10, 10, 10, 10],
    "standard_cost": 20,
    "overtime_cost": 30,
    "overtime_hour": 400,
    "min_profit": 5000
}
'''

# Load data from JSON
data = json.loads(data)

# Define sets and indices
P = len(data['prices'])
M = len(data['machine_costs'])

# Create a linear programming problem
problem = pulp.LpProblem("Auto_Parts_Manufacturing", pulp.LpMaximize)

# Decision Variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Integer')
profit = pulp.LpVariable("profit")

# Objective Function
total_profit = (pulp.lpSum(data['prices'][p] * batches[p] for p in range(P)) -
                pulp.lpSum((data['machine_costs'][m] * 
                             pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)))
                            for m in range(1, M)) -
                pulp.lpSum((data['standard_cost'] * 
                             pulp.lpSum(data['time_required'][0][p] * batches[p] for p in range(P)))) +
                (pulp.lpSum(data['time_required'][0][p] * batches[p] for p in range(P)) - 
                 data['overtime_hour']) * (data['overtime_cost'] - data['standard_cost']))

problem += total_profit, "Total_Profit"

# Constraints
for m in range(1, M):
    problem += (pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) <= data['availability'][m], 
                       f"Availability_Constraint_{m}")

for p in range(P):
    problem += (batches[p] >= data['min_batches'][p], f"Min_Batches_Constraint_{p}")

problem += (profit >= data['min_profit'], "Min_Profit_Constraint")

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')