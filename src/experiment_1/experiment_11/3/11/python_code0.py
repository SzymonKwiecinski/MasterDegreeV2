import pulp

# Data from the provided JSON format
data = {
    'capacity': 10,
    'holding_cost': 2,
    'price': [1, 2, 100],
    'cost': [100, 1, 100],
}

# Parameters
N = len(data['price'])
Capacity = data['capacity']
HoldingCost = data['holding_cost']
Price = data['price']
Cost = data['cost']

# Create a linear programming problem
problem = pulp.LpProblem("Optimal_Trading_Strategy", pulp.LpMaximize)

# Decision Variables
B = pulp.LpVariable.dicts("B", range(N), lowBound=0)  # Amount bought
S = pulp.LpVariable.dicts("S", range(N), lowBound=0)  # Amount sold
I = pulp.LpVariable.dicts("I", range(N), lowBound=0, upBound=Capacity)  # Inventory levels

# Objective Function
profit = pulp.lpSum(Price[t] * S[t] - Cost[t] * B[t] - HoldingCost * I[t] for t in range(N))
problem += profit, "Total_Profit"

# Constraints
# Inventory balance and initial inventory
problem += (I[0] == 0), "Initial_Inventory"
for t in range(1, N):
    problem += (I[t] == I[t-1] + B[t] - S[t]), f"Inventory_Balance_{t}"
    
# Non-negativity and storage capacity constraints
for t in range(N):
    problem += (I[t] >= 0), f"Non_Negative_Inventory_{t}"
    problem += (S[t] >= 0), f"Non_Negative_Sales_{t}"
    problem += (B[t] >= 0), f"Non_Negative_Purchases_{t}"
    problem += (I[t] <= Capacity), f"Storage_Capacity_{t}"

# Solve the problem
problem.solve()

# Print the optimal objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')