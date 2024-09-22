import pulp
import json

# Data provided in JSON format
data = json.loads('{"NumShifts": 6, "OfficersNeeded": [15, 13, 11, 11, 9, 7], "ShiftCosts": [500, 480, 450, 460, 470, 490]}')

# Problem setup
num_shifts = data['NumShifts']
officers_needed = data['OfficersNeeded']
shift_costs = data['ShiftCosts']

# Create a linear programming problem
problem = pulp.LpProblem("Police_Officer_Shift_Assignment", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(1, num_shifts + 1), cat='Binary')  # Shift start variables
officers_assigned = pulp.LpVariable.dicts("officers_assigned", range(1, num_shifts + 1), lowBound=0)

# Objective Function
problem += pulp.lpSum(shift_costs[s-1] * x[s] for s in range(1, num_shifts + 1)), "Total_Cost"

# Constraints
# Each shift must meet the required officers
for s in range(1, num_shifts + 1):
    problem += officers_assigned[s] >= officers_needed[s - 1], f"Officers_Needed_{s}"

# Officers assigned constraints
for s in range(2, num_shifts):
    problem += officers_assigned[s] == officers_assigned[s - 1] + officers_assigned[s + 1], f"Consecutive_Shifts_{s}"

# Boundary conditions
problem += officers_assigned[1] == officers_assigned[2], "First_Condition"
problem += officers_assigned[num_shifts] == officers_assigned[num_shifts - 1], "Last_Condition"

# Solve the problem
problem.solve()

# Output the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')