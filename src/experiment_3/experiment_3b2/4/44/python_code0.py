import pulp
import json

# Load data
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10]
}

# Initialize the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Define decision variables
num_parts = len(data['prices'])
x = pulp.LpVariable.dicts("x", range(num_parts), lowBound=0)  # Production quantities

# Define the objective function
profit_terms = [data['prices'][p] * x[p] - pulp.lpSum(data['time_required[m][p]'] * data['machine_costs'][m] * x[p] for m in range(len(data['machine_costs']))) for p in range(num_parts)]
problem += pulp.lpSum(profit_terms)

# Constraints for machine availability
for m in range(len(data['availability'])):
    problem += (pulp.lpSum(data['time_required'][m][p] * x[p] for p in range(num_parts)) <= data['availability'][m], f"Machine_Availability_{m}")

# Minimum production requirements for each part
for p in range(num_parts):
    problem += (x[p] >= data['min_batches'][p], f"Min_Production_{p}")

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')