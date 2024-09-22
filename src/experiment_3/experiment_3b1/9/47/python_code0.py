import pulp
import json

# Load data from JSON
data = json.loads('{"NumShifts": 6, "OfficersNeeded": [15, 13, 11, 11, 9, 7], "ShiftCosts": [500, 480, 450, 460, 470, 490]}')

# Extract data
num_shifts = data['NumShifts']
officers_needed = data['OfficersNeeded']
shift_costs = data['ShiftCosts']

# Create the linear programming problem
problem = pulp.LpProblem("Minimize_Shift_Cost", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("officers_assigned", range(1, num_shifts + 1), lowBound=0, cat='Integer')

# Objective function
problem += pulp.lpSum(shift_costs[s - 1] * x[s] for s in range(1, num_shifts + 1)), "Total_Cost"

# Constraints
# Officers needed for each shift
for s in range(1, num_shifts + 1):
    problem += x[s] >= officers_needed[s - 1], f"Officers_Needed_Constraint_{s}"

# Shift continuity constraint
for s in range(2, num_shifts + 1):
    problem += x[s] == x[s - 1], f"Shift_Continuity_Constraint_{s}"

# Solve the problem
problem.solve()

# Collect results
officers_assigned = [x[s].varValue for s in range(1, num_shifts + 1)]

# Output results
total_cost = pulp.value(problem.objective)
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')