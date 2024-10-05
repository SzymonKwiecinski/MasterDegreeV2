import pulp

# Data input
data = {'inputone': [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]],
        'manpowerone': [0.6, 0.3, 0.2],
        'inputtwo': [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]],
        'manpowertwo': [0.4, 0.2, 0.1],
        'stock': [150, 80, 100],
        'capacity': [300, 350, 280],
        'manpower_limit': 470000000.0}

# Number of industries (K)
K = len(data['inputone'])

# Number of years (T), we need results for the last two years which are year 1 and 2
T = 3

# Initialize the problem
problem = pulp.LpProblem("Maximize_Production", pulp.LpMaximize)

# Variables for production, building capacity, and stock holding
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Continuous')
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Continuous')
stockhold = pulp.LpVariable.dicts("stockhold", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Continuous')

# Objective: Maximize production in the last two years
problem += pulp.lpSum(produce[(k, t)] for k in range(K) for t in range(1, T)), "Total_Production_Last_2_Years"

# Constraints
for t in range(T):
    # Capacity constraints
    for k in range(K):
        if t == 0:
            problem += produce[k, t] <= data['capacity'][k], f"Capacity_Constraint_Year0_Industry{k}"
        else:
            problem += (produce[k, t] <= data['capacity'][k] + buildcapa[(k, t - 2)] 
                        if t - 2 >= 0 else produce[k, t] <= data['capacity'][k]), f"Capacity_Constraint_Year{t}_Industry{k}"
    
    # Manpower constraints
    problem += (pulp.lpSum(data['manpowerone'][k] * produce[(k, t)] for k in range(K)) +
                pulp.lpSum(data['manpowertwo'][k] * buildcapa[(k, t)] for k in range(K))) <= data['manpower_limit'], f"Manpower_Constraint_Year{t}"

    # Stock and input constraints
    if t == 0:
        for k in range(K):
            problem += stockhold[(k, t)] == data['stock'][k] + produce[(k, t)] - pulp.lpSum(data['inputone'][k][j] * produce[(j, t)] for j in range(K)) - buildcapa[(k, t)], f"Stock_Constraint_Year0_Industry{k}"
    else:
        for k in range(K):
            problem += stockhold[(k, t)] == stockhold[(k, t - 1)] + produce[(k, t)] - pulp.lpSum(data['inputone'][k][j] * produce[(j, t)] for j in range(K)) - buildcapa[(k, t)], f"Stock_Constraint_Year{t}_Industry{k}"

# Solve the problem
problem.solve()

# Output results
output = {
    "produce": [[pulp.value(produce[(k, t)]) for t in range(T)] for k in range(K)],
    "buildcapa": [[pulp.value(buildcapa[(k, t)]) for t in range(T)] for k in range(K)],
    "stockhold": [[pulp.value(stockhold[(k, t)]) for t in range(T)] for k in range(K)]
}

print(output)

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')