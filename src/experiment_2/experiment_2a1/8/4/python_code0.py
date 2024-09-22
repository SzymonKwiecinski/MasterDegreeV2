import pulp
import json

# Parse the input data
data = {'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}
period = data['Period']
demand = data['Demand']

# Create the linear programming problem
problem = pulp.LpProblem("Nurse_Scheduling", pulp.LpMinimize)

# Define decision variables for the number of nurses starting on each day
start = pulp.LpVariable.dicts("start", range(7), lowBound=0, cat='Integer')

# Objective function: minimize the total number of nurses
problem += pulp.lpSum(start[j] for j in range(7))

# Add constraints for the demand for each day
for j in range(7):
    problem += pulp.lpSum(start[(j - k) % 7] for k in range(period)) >= demand[j]

# Solve the problem
problem.solve()

# Extract results
result_start = [start[j].varValue for j in range(7)]
total_nurses = pulp.value(problem.objective)

# Prepare the output
output = {
    'start': result_start,
    'total': total_nurses
}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# If you want to see the output in the specified format
print(json.dumps(output))