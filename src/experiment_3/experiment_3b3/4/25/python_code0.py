import pulp

# Data from JSON
data = {
    'inputone': [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]],
    'manpowerone': [0.6, 0.3, 0.2],
    'inputtwo': [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]],
    'manpowertwo': [0.4, 0.2, 0.1],
    'stock': [150, 80, 100],
    'capacity': [300, 350, 280],
    'manpower_limit': 470000000.0
}

K = 3  # number of industries
T = 5  # number of years

# Initialize the problem
problem = pulp.LpProblem("Maximize_Production", pulp.LpMaximize)

# Decision variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(T)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(T)), lowBound=0)
stock = pulp.LpVariable.dicts("stock", ((k, t) for k in range(K) for t in range(T)), lowBound=0)

# Objective function
problem += pulp.lpSum(produce[k, T-1] + produce[k, T-2] for k in range(K)), "Total_Production_Last_Two_Years"

# Constraints
for k in range(K):
    for t in range(T):
        if t == 0:
            prev_produce = 0
            prev_stock = data['stock'][k]
        else:
            prev_produce = produce[k, t-1]
            prev_stock = stock[k, t-1]

        # Production Constraints
        problem += produce[k, t] <= data['capacity'][k] + prev_stock, f"Production_Capacity_{k}_{t}"

        # Input Requirements
        problem += produce[k, t] <= (
            pulp.lpSum(data['inputone'][k][j] * (produce[j, t-1] if t > 0 else 0) for j in range(K)) + prev_stock
        ), f"Input_Requirements_{k}_{t}"

        # Manpower Constraints
        problem += (
            data['manpowerone'][k] * produce[k, t] + data['manpowertwo'][k] * buildcapa[k, t]
            <= data['manpower_limit']
        ), f"Manpower_{k}_{t}"

        # Building Capacity
        problem += buildcapa[k, t] <= (
            pulp.lpSum(data['inputtwo'][k][j] * (produce[j, t-1] if t > 0 else 0) for j in range(K)) + prev_stock
        ), f"Building_Capacity_{k}_{t}"

        # Stock Flow
        problem += stock[k, t] == prev_stock + produce[k, t] - buildcapa[k, t], f"Stock_Flow_{k}_{t}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')