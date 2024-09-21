import pulp

# Data from the provided JSON
data = {
    'capacity': 10,
    'holding_cost': 2,
    'price': [1, 2, 100],
    'cost': [100, 1, 100]
}

# Initialize the Linear Program
N = len(data['price'])  # Number of periods
problem = pulp.LpProblem("Optimal_Trading_Strategy", pulp.LpMaximize)

# Decision variables for each period
B = pulp.LpVariable.dicts("Buy", range(N), lowBound=0)  # Quantity bought
S = pulp.LpVariable.dicts("Sell", range(N), lowBound=0)  # Quantity sold
I = pulp.LpVariable.dicts("Inventory", range(N), lowBound=0, upBound=data['capacity'])  # Inventory levels

# Objective function: Maximize total profit
problem += pulp.lpSum(data['price'][t] * S[t] - data['cost'][t] * B[t] - data['holding_cost'] * I[t] for t in range(N)), "Total_Profit"

# Constraints

# Inventory balance and initial condition
problem += (I[0] == 0, "Initial_Inventory")

for t in range(N):
    if t > 0:
        problem += (I[t] == I[t-1] + B[t] - S[t], f"Inventory_Balance_{t}")
    
    # Non-negative inventory, sales, and purchases
    problem += (I[t] >= 0, f"Non_Negative_Inventory_{t}")
    problem += (S[t] >= 0, f"Non_Negative_Sales_{t}")
    problem += (B[t] >= 0, f"Non_Negative_Purchases_{t}")
    
    # Storage capacity constraint
    problem += (I[t] <= data['capacity'], f"Storage_Capacity_{t}")

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')