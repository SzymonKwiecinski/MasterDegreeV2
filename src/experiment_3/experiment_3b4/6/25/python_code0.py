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

# Indices
K = len(data['capacity'])  # Number of industries
T = 4  # Number of years

# Initialize the Problem
problem = pulp.LpProblem("Maximize_Production", pulp.LpMaximize)

# Decision Variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(T+1)), lowBound=0, cat='Continuous')
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(T+1)), lowBound=0, cat='Continuous')
stockhold = pulp.LpVariable.dicts("stockhold", ((k, t) for k in range(K) for t in range(T+1)), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(produce[k, t] for k in range(K) for t in range(T-1, T+1)), "Total_Production_Last_Two_Years"

# Constraints

# Production Capacity Constraint
for k in range(K):
    for t in range(1, T+1):
        if t == 1:
            problem += (
                produce[k, t] + buildcapa[k, t] <= data['capacity'][k],
                f"Production_Capacity_Constraint_Industry_{k}_Year_{t}"
            )
        else:
            problem += (
                produce[k, t] + buildcapa[k, t] <= data['capacity'][k] + pulp.lpSum(buildcapa[j, t-2] for j in range(K)),
                f"Production_Capacity_Constraint_Industry_{k}_Year_{t}"
            )

# Input Constraints
for k in range(K):
    for t in range(1, T+1):
        if t == 1:
            previous_stock = data['stock'][k]
        else:
            previous_stock = stockhold[k, t-1] + produce[k, t-1]

        problem += (
            pulp.lpSum(data['inputone'][k][j] * produce[k, t] for j in range(K)) +
            pulp.lpSum(data['inputtwo'][k][j] * buildcapa[k, t] for j in range(K)) <= previous_stock,
            f"Input_Constraints_Industry_{k}_Year_{t}"
        )

# Stock Balance Constraint
for k in range(K):
    for t in range(1, T+1):
        if t == 1:
            problem += (
                stockhold[k, t] == data['stock'][k] - produce[k, t] - buildcapa[k, t],
                f"Stock_Balance_Constraint_Industry_{k}_Year_{t}"
            )
        else:
            problem += (
                stockhold[k, t] == stockhold[k, t-1] + produce[k, t-1] - produce[k, t] - buildcapa[k, t],
                f"Stock_Balance_Constraint_Industry_{k}_Year_{t}"
            )

# Manpower Constraint
for t in range(1, T+1):
    problem += (
        pulp.lpSum(data['manpowerone'][k] * produce[k, t] + data['manpowertwo'][k] * buildcapa[k, t] for k in range(K)) <= data['manpower_limit'],
        f"Manpower_Constraint_Year_{t}"
    )

# Solve the Problem
problem.solve()

# Print the Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')