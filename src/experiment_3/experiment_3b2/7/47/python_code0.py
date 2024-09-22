import pulp

# Data from JSON format
data = {
    'NumShifts': 6,
    'OfficersNeeded': [15, 13, 11, 11, 9, 7],
    'ShiftCosts': [500, 480, 450, 460, 470, 490]
}

# Extracting parameters from data
S = data['NumShifts']
officers_needed = data['OfficersNeeded']
shift_cost = data['ShiftCosts']

# Define the problem
problem = pulp.LpProblem("Officer_Assignment", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("officers_starting", range(1, S + 1), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(shift_cost[s-1] * x[s] for s in range(1, S + 1)), "Total_Cost"

# Constraints
for s in range(1, S + 1):
    problem += (x[s] + x[s - 1 if s > 1 else S] >= officers_needed[s - 1]), f"Demand_Constraint_{s}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')