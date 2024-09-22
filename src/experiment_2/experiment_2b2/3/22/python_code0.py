import pulp

# Given data
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

requirement = data["requirement"]
strength = data["strength"]
lessonewaste = data["lessonewaste"]
moreonewaste = data["moreonewaste"]
recruit_limits = data["recruit"]
costredundancy = data["costredundancy"]
num_overman = data["num_overman"]
costoverman = data["costoverman"]
num_shortwork = data["num_shortwork"]
costshort = data["costshort"]

K = len(strength)  # Number of manpower categories
I = len(requirement[0])  # Number of years

# Define the problem
problem = pulp.LpProblem("Minimize_Redundancy", pulp.LpMinimize)

# Decision variables
recruit = [[pulp.LpVariable(f'recruit_{k}_{i}', lowBound=0, upBound=recruit_limits[k], cat='Integer') for i in range(I)] for k in range(K)]
overmanning = [[pulp.LpVariable(f'overmanning_{k}_{i}', lowBound=0, upBound=num_overman, cat='Integer') for i in range(I)] for k in range(K)]
short = [[pulp.LpVariable(f'short_{k}_{i}', lowBound=0, upBound=num_shortwork, cat='Integer') for i in range(I)] for k in range(K)]

# Objective function
problem += pulp.lpSum(costredundancy[k] * (strength[k] + pulp.lpSum(recruit[k][j] for j in range(i)) -
               requirement[k][i] - overmanning[k][i] - 0.5 * short[k][i]) for k in range(K) for i in range(I))

# Constraints
for i in range(I):
    for k in range(K):
        if i == 0:
            # Initial year balance
            available = strength[k] - lessonewaste[k] * recruit[k][i]
        else:
            # Subsequent years
            available = strength[k] * (1 - moreonewaste[k]) + pulp.lpSum(recruit[k][j] * (1 - moreonewaste[k]) ** (i-j) for j in range(i))

        # Recruitment feasibility
        problem += recruit[k][i] <= recruit_limits[k]

        # Staffing requirements and overmanning
        problem += available + recruit[k][i] + overmanning[k][i] + 0.5 * short[k][i] >= requirement[k][i]

        # Redundancy costs can occur if staffing is more than needed
        problem += available + recruit[k][i] - requirement[k][i] <= overmanning[k][i]

# Solve the problem
problem.solve()

# Extracting results
result = {
    "recruit": [[pulp.value(recruit[k][i]) for i in range(I)] for k in range(K)],
    "overmanning": [[pulp.value(overmanning[k][i]) for i in range(I)] for k in range(K)],
    "short": [[pulp.value(short[k][i]) for i in range(I)] for k in range(K)],
}

# Print result
print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')