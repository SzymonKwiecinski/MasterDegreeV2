import pulp
import json

# Input data in JSON format
data_json = '{"NumShifts": 6, "OfficersNeeded": [15, 13, 11, 11, 9, 7], "ShiftCosts": [500, 480, 450, 460, 470, 490]}'
data = json.loads(data_json)

# Extracting data
num_shifts = data['NumShifts']
officers_needed = data['OfficersNeeded']
shift_costs = data['ShiftCosts']

# Create the linear programming problem
problem = pulp.LpProblem("PoliceOfficerShiftScheduling", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(num_shifts), lowBound=0, cat='Integer')

# Objective Function
problem += pulp.lpSum(shift_costs[s] * x[s] for s in range(num_shifts)), "TotalCost"

# Constraints
for s in range(num_shifts):
    problem += x[s] + x[(s - 1) % num_shifts] >= officers_needed[s], f"Constraint_{s+1}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')