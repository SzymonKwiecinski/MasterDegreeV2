import pulp
import numpy as np

# Data from JSON
requirement = np.array([[1000, 1400, 1000], [500, 2000, 1500], [0, 2500, 2000]])
strength = np.array([2000, 1500, 1000])
lessonewaste = np.array([0.25, 0.2, 0.1])
moreonewaste = np.array([0.1, 0.05, 0.05])
recruit = np.array([500, 800, 500])
costredundancy = np.array([200, 500, 500])
num_overman = 150
num_shortwork = 50
costshort = np.array([500, 400, 400])

K = range(len(recruit))
I = range(requirement.shape[1])

# Define the problem
problem = pulp.LpProblem("Minimize_Redundancy_Costs", pulp.LpMinimize)

# Decision Variables
recruit_vars = pulp.LpVariable.dicts("recruit", [(k, i) for k in K for i in I], lowBound=0)
overmanning_vars = pulp.LpVariable.dicts("overmanning", [(k, i) for k in K for i in I], lowBound=0)
short_vars = pulp.LpVariable.dicts("short", [(k, i) for k in K for i in I], lowBound=0)
redundancy_vars = pulp.LpVariable.dicts("redundancy", [(k, i) for k in K for i in I], lowBound=0)

# Objective Function
problem += pulp.lpSum(costredundancy[k] * redundancy_vars[k, i] for k in K for i in I)

# Constraints
strength_vars = pulp.LpVariable.dicts("strength", [(k, i) for k in K for i in I], lowBound=0)

# Initial strength
for k in K:
    strength_vars[k, 0] = strength[k]

# Strength update
for k in K:
    for i in range(1, len(I)):
        problem += (strength_vars[k, i] == 
                     strength_vars[k, i-1] + 
                     recruit_vars[k, i-1] - 
                     redundancy_vars[k, i-1] - 
                     lessonewaste[k] * recruit_vars[k, i-1] - 
                     moreonewaste[k] * (strength_vars[k, i-1] - recruit_vars[k, i-1]))

# Requirement constraint
for k in K:
    for i in I:
        problem += (strength_vars[k, i] + 
                     overmanning_vars[k, i] + 
                     0.5 * short_vars[k, i] - 
                     redundancy_vars[k, i] >= 
                     requirement[k, i])

# Recruit constraints
for k in K:
    for i in I:
        problem += recruit_vars[k, i] <= recruit[k]

# Overmanning constraints
for i in I:
    problem += pulp.lpSum(overmanning_vars[k, i] for k in K) <= num_overman

for k in K:
    for i in I:
        problem += overmanning_vars[k, i] <= requirement[k, i]

# Short-time worker constraints
for k in K:
    for i in I:
        problem += short_vars[k, i] <= num_shortwork

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')