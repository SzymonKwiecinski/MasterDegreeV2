import pulp

# Given data
data = {
    'NumProducts': 2,
    'NumMachines': 2,
    'ProduceTime': [[1, 3], [2, 1]],
    'AvailableTime': [200, 100],
    'Profit': [20, 10],
}

# Define sets
K = range(data['NumProducts'])  # Products
S = range(data['NumMachines'])   # Stages

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Define decision variables
quantity = pulp.LpVariable.dicts("quantity", K, lowBound=0)

# Objective function
problem += pulp.lpSum(data['Profit'][k] * quantity[k] for k in K), "Total_Profit"

# Constraints
for s in S:
    problem += (pulp.lpSum(data['ProduceTime'][k][s] * quantity[k] for k in K) <= data['AvailableTime'][s], 
                 f"Time_Constraint_Stage_{s}")

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')