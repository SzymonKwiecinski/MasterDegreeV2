import pulp

# Problem data
data = {
    'inputone': [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]],
    'manpowerone': [0.6, 0.3, 0.2],
    'inputtwo': [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]],
    'manpowertwo': [0.4, 0.2, 0.1],
    'stock': [150, 80, 100],
    'capacity': [300, 350, 280],
    'demand': [60000000.0, 60000000.0, 30000000.0]
}

inputone = data['inputone']
manpowerone = data['manpowerone']
inputtwo = data['inputtwo']
manpowertwo = data['manpowertwo']
stock = data['stock']
capacity = data['capacity']
demand = data['demand']

K = len(demand)
T = 5  # number of years

# Create LP problem
problem = pulp.LpProblem("Maximize_Manpower", pulp.LpMaximize)

# Decision variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(T)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(T)), lowBound=0)
stockhold = pulp.LpVariable.dicts("stockhold", ((k, t) for k in range(K) for t in range(T+1)), lowBound=0)  # Extended T+1

# Objective Function: Maximize the total manpower requirement over five years
problem += pulp.lpSum([manpowerone[k] * produce[k, t] + manpowertwo[k] * buildcapa[k, t] for k in range(K) for t in range(T)])

# Constraints
for k in range(K):
    # Initial stock balance constraint
    problem += stock[k] + capacity[k] >= demand[k] + stockhold[k, 0]  
    
    for t in range(T):
        # For period t+1, check the previous stock balance with adjustments
        if t < T - 1:
            problem += stockhold[k, t] + produce[k, t] - demand[k] == stockhold[k, t + 1]
        
        # Ensure that production and stock do not exceed capacity plus stocks
        problem += produce[k, t] + stockhold[k, t] <= stock[k] + capacity[k]

        for j in range(K):
            # Input requirements
            if t >= 1:
                # Production within capacity plus any increase in capacity from two periods ago
                problem += produce[k, t] <= capacity[k] + (buildcapa[k, t-2] if t >= 2 else 0)
                # Input balance from produce
                problem += inputone[k][j] * produce[k, t] + inputtwo[k][j] * buildcapa[k, t] <= produce[j, max(t-1, 0)]

# Solve the problem
problem.solve()

# Prepare output data
output_data = {
    "produce": [[pulp.value(produce[k, t]) for t in range(T)] for k in range(K)],
    "buildcapa": [[pulp.value(buildcapa[k, t]) for t in range(T)] for k in range(K)],
    "stockhold": [[pulp.value(stockhold[k, t]) for t in range(T)] for k in range(K)]
}

print(output_data)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')