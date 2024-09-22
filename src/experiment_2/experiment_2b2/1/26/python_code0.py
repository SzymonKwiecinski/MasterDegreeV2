import pulp

data = {
    "inputone": [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]],
    "manpowerone": [0.6, 0.3, 0.2],
    "inputtwo": [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]],
    "manpowertwo": [0.4, 0.2, 0.1],
    "stock": [150, 80, 100],
    "capacity": [300, 350, 280],
    "demand": [60000000.0, 60000000.0, 30000000.0]
}

# Parameters
K = len(data['capacity'])
T = 5

# Indices
industries = range(K)
years = range(T)

# Create LP problem
problem = pulp.LpProblem("Maximize_Manpower", pulp.LpMaximize)

# Decision variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in industries for t in years), lowBound=0, cat='Continuous')
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in industries for t in years), lowBound=0, cat='Continuous')
stockhold = pulp.LpVariable.dicts("stockhold", ((k, t) for k in industries for t in years), lowBound=0, cat='Continuous')

# Objective function: Maximize total manpower over 5 years
problem += pulp.lpSum(data['manpowerone'][k] * produce[k, t] + data['manpowertwo'][k] * buildcapa[k, t] for k in industries for t in years)

# Constraints

# Initial stock constraints
for k in industries:
    problem += stockhold[k, 0] == data['stock'][k]

# Capacity constraints
for k in industries:
    for t in years:
        problem += produce[k, t] + buildcapa[k, t] <= data['capacity'][k]
        if t >= 2:
            problem += produce[k, t] <= data['capacity'][k] + sum(buildcapa[k, t-2] for t in range(t-2+1))

# Demand and stock flow constraints
for k in industries:
    for t in years:
        if t == 0:
            problem += stockhold[k, t] >= 0
        elif t == 1:
            problem += produce[k, t] + stockhold[k, t-1] >= data['demand'][k] + stockhold[k, t]
        else:
            problem += produce[k, t] + stockhold[k, t-1] >= data['demand'][k] + stockhold[k, t]

# Solve the problem
problem.solve()

# Prepare the output
output = {
    "produce": [[pulp.value(produce[k, t]) for t in years] for k in industries],
    "buildcapa": [[pulp.value(buildcapa[k, t]) for t in years] for k in industries],
    "stockhold": [[pulp.value(stockhold[k, t]) for t in years] for k in industries]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')