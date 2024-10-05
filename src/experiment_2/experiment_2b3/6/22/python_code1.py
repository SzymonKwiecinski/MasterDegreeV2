import pulp

data = {
    "requirement": [[1000, 1400, 1000], [500, 2000, 1500], [0, 2500, 2000]], 
    "strength": [2000, 1500, 1000], 
    "lessonewaste": [0.25, 0.2, 0.1], 
    "moreonewaste": [0.1, 0.05, 0.05], 
    "recruit": [500, 800, 500], 
    "costredundancy": [200, 500, 500], 
    "num_overman": 150, 
    "costoverman": [1500, 2000, 3000], 
    "costshort": [500, 400, 400],
    "num_shortwork": 50
}

requirements = data["requirement"]
strength = data["strength"]
lessonewaste = data["lessonewaste"]
moreonewaste = data["moreonewaste"]
recruit_limit = data["recruit"]
cost_redundancy = data["costredundancy"]
num_overman = data["num_overman"]
cost_overman = data["costoverman"]
num_shortwork = data["num_shortwork"]
cost_shortwork = data["costshort"]

K = len(strength)
I = len(requirements[0])

# Define the LP problem
problem = pulp.LpProblem("Minimize_Redundancy", pulp.LpMinimize)

# Decision variables
recruits = [[pulp.LpVariable(f"recruit_{k}_{i}", lowBound=0, upBound=recruit_limit[k], cat='Integer') for i in range(I)] for k in range(K)]
overmanning = [[pulp.LpVariable(f"overmanning_{k}_{i}", lowBound=0, upBound=num_overman, cat='Integer') for i in range(I)] for k in range(K)]
short = [[pulp.LpVariable(f"short_{k}_{i}", lowBound=0, upBound=num_shortwork, cat='Integer') for i in range(I)] for k in range(K)]

# Objective function: Minimize redundancy cost
redundancy_cost = pulp.lpSum(cost_redundancy[k] * recruits[k][i] for k in range(K) for i in range(I))
problem += redundancy_cost

# Constraints on manpower
for k in range(K):
    for i in range(I):
        if i == 0:
            manpower_prev = strength[k]
        else:
            manpower_prev = (
                strength[k] + pulp.lpSum(recruits[k][:i]) * (1 - moreonewaste[k]) +
                (strength[k] * (1 - moreonewaste[k]) - short[k][i-1] / 2)
            )

        manpower_current = (
            manpower_prev +
            recruits[k][i] -
            (requirements[k][i] - short[k][i]/2)
        )

        problem += manpower_current >= requirements[k][i]
        problem += manpower_current <= requirements[k][i] + num_overman

# Solve the problem
problem.solve()

# Extract results
result = {
    "recruit": [[pulp.value(recruits[k][i]) for i in range(I)] for k in range(K)],
    "overmanning": [[pulp.value(overmanning[k][i]) for i in range(I)] for k in range(K)],
    "short": [[pulp.value(short[k][i]) for i in range(I)] for k in range(K)]
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')