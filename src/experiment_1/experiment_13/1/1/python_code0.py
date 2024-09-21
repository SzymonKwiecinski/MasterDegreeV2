import pulp

# Data from the provided JSON
data = {
    'M': 4,
    'N': 5,
    'Available': [10, 20, 15, 35, 25],
    'Requirements': [
        [3, 2, 0, 0, 0],
        [0, 5, 2, 1, 0],
        [1, 0, 0, 5, 3],
        [0, 3, 1, 1, 5]
    ],
    'Prices': [7, 10, 5, 9]
}

# Number of goods and raw materials
M = data['M']
N = data['N']
Available = data['Available']
Requirements = data['Requirements']
Prices = data['Prices']

# Create a linear programming problem
problem = pulp.LpProblem("Maximize_Total_Revenue", pulp.LpMaximize)

# Decision variables for the quantity of each good produced
x = pulp.LpVariable.dicts("x", range(M), lowBound=0)  # x[i]: quantity of good i produced

# Objective function
problem += pulp.lpSum(Prices[i] * x[i] for i in range(M)), "Total_Revenue"

# Constraints for raw material availability
for j in range(N):
    problem += pulp.lpSum(Requirements[i][j] * x[i] for i in range(M)) <= Available[j], f"Raw_Material_Constraint_{j}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')