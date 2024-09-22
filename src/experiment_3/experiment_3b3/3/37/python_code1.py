import pulp

# Data
data = {
    'time': [
        [2, 3],  # Time required for part 1 in shop 1 and shop 2
        [1, 2],  # Time required for part 2 in shop 1 and shop 2
        [3, 2],  # Time required for part 3 in shop 1 and shop 2
        [3, 1],  # Time required for part 4 in shop 1 and shop 2
        [1, 1]   # Time required for part 5 in shop 1 and shop 2
    ],
    'profit': [30, 20, 40, 25, 10],  # Profit for each part
    'capacity': [700, 1000]  # Capacity of shop 1 and shop 2
}

num_parts = len(data['profit'])
num_shops = len(data['capacity'])

# Define the Linear Program
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
quantity = [pulp.LpVariable(f'quantity_{k}', lowBound=0, cat='Continuous') for k in range(num_parts)]

# Objective function
problem += pulp.lpSum(data['profit'][k] * quantity[k] for k in range(num_parts)), "Total_Profit"

# Constraints
for s in range(num_shops):
    problem += (
        pulp.lpSum(data['time'][k][s] * quantity[k] for k in range(num_parts)) <= data['capacity'][s],
        f"Capacity_Constraint_Shop_{s + 1}"
    )

# Solve the problem
problem.solve()

# Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')