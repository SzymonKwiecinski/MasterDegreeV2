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
K = len(data['capacity'])
T = 5  # Assuming there are 5 years, as it is not specified

# Create the problem
problem = pulp.LpProblem("Industry_Capacity_Planning", pulp.LpMaximize)

# Decision Variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(T)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(T)), lowBound=0)
stockhold = pulp.LpVariable.dicts("stockhold", ((k, t) for k in range(K) for t in range(T)), lowBound=0)

# Objective Function
problem += pulp.lpSum(produce[k, t] for k in range(K) for t in range(T-2, T)), "Total_Production_Last_Two_Years"

# Constraints
for k in range(K):
    for t in range(T):
        if t >= 2:
            problem += produce[k, t] <= data['capacity'][k] + pulp.lpSum(buildcapa[k, t-2] for j in range(K)), f"Capacity_Constraint_{k}_{t}"
        else:
            problem += produce[k, t] <= data['capacity'][k], f"Initial_Capacity_Constraint_{k}_{t}"

for k in range(K):
    problem += stockhold[k, 0] == data['stock'][k], f"Initial_Stock_{k}"

for t in range(T):
    problem += pulp.lpSum(data['manpowerone'][k] * produce[k, t] + data['manpowertwo'][k] * buildcapa[k, t] for k in range(K)) <= data['manpower_limit'], f"Manpower_Constraint_{t}"

for k in range(K):
    for t in range(T):
        problem += (pulp.lpSum(data['inputone'][k][j] * produce[j, t] for j in range(K)) + 
                    pulp.lpSum(data['inputtwo'][k][j] * buildcapa[j, t] for j in range(K))) <= stockhold[k, t] + produce[k, t], f"Stock_Use_Constraint_{k}_{t}"

for k in range(K):
    for t in range(T-1):
        problem += (stockhold[k, t+1] ==
                    stockhold[k, t] -
                    pulp.lpSum(data['inputone'][j][k] * produce[j, t] for j in range(K)) -
                    pulp.lpSum(data['inputtwo'][j][k] * buildcapa[j, t] for j in range(K)) +
                    produce[k, t]), f"Stock_Transition_{k}_{t}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')