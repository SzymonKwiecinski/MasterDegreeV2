import pulp

# Data from JSON
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

# Parameters
K = len(data["strength"])
I = len(data["requirement"][0])
requirement = data["requirement"]
strength = data["strength"]
lessonewaste = data["lessonewaste"]
moreonewaste = data["moreonewaste"]
recruit_limit = data["recruit"]
redundancy_cost = data["costredundancy"]
max_overman = data["num_overman"]
overman_cost = data["costoverman"]
max_shortwork = data["num_shortwork"]
shortwork_cost = data["costshort"]

# Problem
problem = pulp.LpProblem("Minimize_Workforce_Cost", pulp.LpMinimize)

# Decision variables
recruit = [[pulp.LpVariable(f"recruit_{k}_{i}", lowBound=0, upBound=recruit_limit[k], cat='Integer') for i in range(I)] for k in range(K)]
overmanning = [[pulp.LpVariable(f"overmanning_{k}_{i}", lowBound=0, upBound=max_overman, cat='Integer') for i in range(I)] for k in range(K)]
short = [[pulp.LpVariable(f"short_{k}_{i}", lowBound=0, upBound=max_shortwork, cat='Integer') for i in range(I)] for k in range(K)]

# Objective function
total_cost = pulp.lpSum(
    redundancy_cost[k] * (strength[k] - pulp.lpSum(requirement[k][i] + overmanning[k][i] - recruit[k][i] - short[k][i] for i in range(I)))
    + overman_cost[k] * pulp.lpSum(overmanning[k][i] for i in range(I))
    + shortwork_cost[k] * pulp.lpSum(short[k][i] for i in range(I))
    for k in range(K)
)

problem += total_cost

# Constraints
for k in range(K):
    manpower = strength[k]
    for i in range(I):
        manpower = (manpower - requirement[k][i]) * (1 - moreonewaste[k]) + recruit[k][i]
        
        problem += manpower >= requirement[k][i] - 0.5 * pulp.lpSum(short[k][i] for i in range(I))
        problem += manpower <= requirement[k][i] + overmanning[k][i]

# Solve
problem.solve()

# Prepare the result
output = {
    "recruit": [[pulp.value(recruit[k][i]) for i in range(I)] for k in range(K)],
    "overmanning": [[pulp.value(overmanning[k][i]) for i in range(I)] for k in range(K)],
    "short": [[pulp.value(short[k][i]) for i in range(I)] for k in range(K)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')