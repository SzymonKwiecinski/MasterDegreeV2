import pulp
import json

# Data input
data_json = '''{'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}'''
data = json.loads(data_json.replace("'", '"'))

# Define model
problem = pulp.LpProblem("Nurse_Scheduling", pulp.LpMinimize)

# Define variables
start = pulp.LpVariable.dicts("start", range(1, data['T'] + 1), lowBound=0, cat='Integer')

# Objective function
problem += pulp.lpSum(start[j] for j in range(1, data['T'] + 1)), "Total_Starts"

# Constraints
for j in range(1, data['T'] + 1):
    problem += pulp.lpSum(start[(j - k - 1) % data['T'] + 1] for k in range(data['Period'])) >= data['Demand'][j - 1], f"Demand_Constraint_{j}"

# Solve the problem
problem.solve()

# Print results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')