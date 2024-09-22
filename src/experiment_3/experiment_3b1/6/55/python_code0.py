import pulp
import json

# Load the data
data = json.loads('{"time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], "machine_costs": [160, 10, 15], "availability": [200, 300, 500], "prices": [570, 250, 585, 430], "min_batches": [10, 10, 10, 10], "standard_cost": 20, "overtime_cost": 30, "overtime_hour": 400, "min_profit": 5000}')

# Define sets
P = len(data['prices'])
M = len(data['machine_costs'])

# Create the problem
problem = pulp.LpProblem("AutoPartsMaxProfit", pulp.LpMaximize)

# Decision Variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0)

# Objective Function
total_profit = pulp.lpSum(data['prices'][p] * batches[p] for p in range(P))
total_cost = pulp.lpSum(data['machine_costs'][m] * pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) for m in range(M))

# Labor costs calculation
H = pulp.lpSum(data['time_required'][0][p] * batches[p] for p in range(P))
labor_costs = pulp.LpVariable("labor_costs")

# Handling labor cost based on hours used
problem += labor_costs >= data['standard_cost'] * H
problem += labor_costs >= data['standard_cost'] * data['overtime_hour'] + data['overtime_cost'] * (H - data['overtime_hour'])
problem += (H <= data['overtime_hour']) >> (labor_costs == data['standard_cost'] * H)
problem += (H > data['overtime_hour']) >> (labor_costs == data['standard_cost'] * data['overtime_hour'] + data['overtime_cost'] * (H - data['overtime_hour']))

# Objective to maximize
problem += total_profit - total_cost - labor_costs

# Constraints
# Machine availability constraints
for m in range(M):
    problem += pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) <= data['availability'][m]

# Minimum production requirements
for p in range(P):
    problem += batches[p] >= data['min_batches'][p]

# Profit constraint
problem += total_profit - total_cost - labor_costs >= data['min_profit']

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')