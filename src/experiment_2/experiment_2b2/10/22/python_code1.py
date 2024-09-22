import pulp

# Data from the given JSON format
data = {
    "requirement": [[1000, 1400, 1000], [500, 2000, 1500], [0, 2500, 2000]],
    "strength": [2000, 1500, 1000],
    "lessonewaste": [0.25, 0.2, 0.1],
    "moreonewaste": [0.1, 0.05, 0.05],
    "recruit": [500, 800, 500],
    "costredundancy": [200, 500, 500],
    "num_overman": 150,
    "costoverman": [1500, 2000, 3000],
    "num_shortwork": 50,
    "costshort": [500, 400, 400]
}

# Extract variables from data
requirement = data["requirement"]
strength = data["strength"]
lessonewaste = data["lessonewaste"]
moreonewaste = data["moreonewaste"]
max_recruit = data["recruit"]
costredundancy = data["costredundancy"]
num_overman = data["num_overman"]
costoverman = data["costoverman"]
num_shortwork = data["num_shortwork"]
costshort = data["costshort"]

K = len(strength)
I = len(requirement[0])

# Create a linear programming problem
problem = pulp.LpProblem("Manpower_Optimization", pulp.LpMinimize)

# Define decision variables
recruit = [[pulp.LpVariable(f'recruit_{k}_{i}', lowBound=0, upBound=max_recruit[k], cat='Integer') for i in range(I)] for k in range(K)]
overmanning = [[pulp.LpVariable(f'overmanning_{k}_{i}', lowBound=0, upBound=num_overman if i == 0 else 0, cat='Integer') for i in range(I)] for k in range(K)]
short = [[pulp.LpVariable(f'short_{k}_{i}', lowBound=0, upBound=num_shortwork, cat='Integer') for i in range(I)] for k in range(K)]
redundancy = [[pulp.LpVariable(f'redundancy_{k}_{i}', lowBound=0, cat='Integer') for i in range(I)] for k in range(K)]

# Objective function: Minimize redundancy costs
problem += pulp.lpSum(redundancy[k][i] * costredundancy[k] for k in range(K) for i in range(I))

# Constraints
for k in range(K):
    manpower_available = strength[k]  # Initialize manpower available

    for i in range(I):
        if i > 0:
            # Manpower carried from previous year minus wastage and redundancy
            manpower_available += recruit[k][i-1] - redundancy[k][i-1]
            manpower_available *= (1 - moreonewaste[k])

        # Wastage of newly recruited workers
        effective_new_recruits = recruit[k][i] * (1 - lessonewaste[k])
        manpower_available += effective_new_recruits
        
        # Effective manpower calculation
        effective_manpower = manpower_available + overmanning[k][i] - requirement[k][i] - redundancy[k][i] + short[k][i] * 0.5
        
        # Enforce manpower availability to meet requirements
        problem += effective_manpower >= 0

# Solve the problem
problem.solve()

# Extract the results
output = {
    "recruit": [[int(recruit[k][i].varValue) for i in range(I)] for k in range(K)],
    "overmanning": [[int(overmanning[k][i].varValue) for i in range(I)] for k in range(K)],
    "short": [[int(short[k][i].varValue) for i in range(I)] for k in range(K)],
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')