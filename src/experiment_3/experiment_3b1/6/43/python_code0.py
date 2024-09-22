import pulp

# Data from the provided JSON format
data = {
    'available': [240000, 8000, 75000],
    'requirements': [[48, 1, 10], [40, 1, 10], [0, 1, 2]],
    'prices': [40, 38, 9],
    'costs': [30, 26, 7],
    'demands': [10000, 2000, 10000]
}

# Parameters
M = len(data['prices'])  # Number of products
N = len(data['available'])  # Number of raw materials
available = data['available']
req = data['requirements']
prices = data['prices']
costs = data['costs']
demands = data['demands']

# Define the problem
problem = pulp.LpProblem("Production_Optimization", pulp.LpMaximize)

# Decision Variables
amount = pulp.LpVariable.dicts("amount", range(M), lowBound=0)

# Objective Function: Maximize total profit
problem += pulp.lpSum((prices[j] - costs[j]) * amount[j] for j in range(M)), "Total_Profit"

# Constraints for raw materials
for i in range(N):
    problem += pulp.lpSum(req[i][j] * amount[j] for j in range(M)) <= available[i], f"Raw_Material_Constraint_{i}"

# Constraints for demand
for j in range(M):
    problem += amount[j] <= demands[j], f"Demand_Constraint_{j}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')