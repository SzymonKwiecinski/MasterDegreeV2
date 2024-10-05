import pulp

# Data from JSON input
data = {
    'NumParts': 5,
    'NumMachines': 2,
    'Time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]],
    'Profit': [30, 20, 40, 25, 10],
    'Capacity': [700, 1000]
}

# Extracting data
K = data['NumParts']
S = data['NumMachines']
time = data['Time']
profit = data['Profit']
capacity = data['Capacity']

# Create a problem variable
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("Part", range(K), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(profit[k] * x[k] for k in range(K)), "Total_Profit"

# Constraints
for s in range(S):
    problem += pulp.lpSum(time[k][s] * x[k] for k in range(K)) <= capacity[s], f"Capacity_Constraint_{s}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')