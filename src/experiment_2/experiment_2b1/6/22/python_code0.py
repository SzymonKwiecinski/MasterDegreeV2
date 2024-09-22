import pulp
import json

# Input data
data = {
    'requirement': [[1000, 1400, 1000], [500, 2000, 1500], [0, 2500, 2000]],
    'strength': [2000, 1500, 1000],
    'lessonewaste': [0.25, 0.2, 0.1],
    'moreonewaste': [0.1, 0.05, 0.05],
    'recruit': [500, 800, 500],
    'costredundancy': [200, 500, 500],
    'num_overman': 150,
    'costoverman': [1500, 2000, 3000],
    'num_shortwork': 50,
    'costshort': [500, 400, 400]
}

# Parameters
K = len(data['requirement'])  # Number of manpower types
I = len(data['requirement'][0])  # Number of years

# Create the LP problem
problem = pulp.LpProblem("Minimize_Redundancy", pulp.LpMinimize)

# Decision variables
recruit = pulp.LpVariable.dicts("Recruit", ((k, i) for k in range(K) for i in range(I)), lowBound=0)
overmanning = pulp.LpVariable.dicts("Overmanning", ((k, i) for k in range(K) for i in range(I)), lowBound=0)
short = pulp.LpVariable.dicts("Short", ((k, i) for k in range(K) for i in range(I)), lowBound=0)

# Objective function: Minimize redundancy costs
problem += pulp.lpSum(data['costredundancy'][k] * overmanning[k, i] for k in range(K) for i in range(I))

# Constraints for each manpower type over the years
for k in range(K):
    for i in range(I):
        # The total manpower after accounting for wastage, recruitment, overmanning, and short-time working
        if i == 0:
            problem += (
                data['strength'][k] + recruit[k, i] * (1 - data['lessonewaste'][k]) +
                overmanning[k, i] - short[k, i] >= data['requirement'][k][i]
            )
        else:
            problem += (
                (data['strength'][k] * (1 - data['moreonewaste'][k]) + 
                recruit[k, i] * (1 - data['lessonewaste'][k]) +
                overmanning[k, i] - short[k, i]) >= data['requirement'][k][i]
            )
        
        # Constraints on recruitment and overmanning
        problem += (recruit[k, i] <= data['recruit'][k])
        problem += (overmanning[k, i] <= data['num_overman'])
        problem += (short[k, i] <= data['num_shortwork'])

# Solve the problem
problem.solve()

# Output results
results = {
    "recruit": [[pulp.value(recruit[k, i]) for i in range(I)] for k in range(K)],
    "overmanning": [[pulp.value(overmanning[k, i]) for i in range(I)] for k in range(K)],
    "short": [[pulp.value(short[k, i]) for i in range(I)] for k in range(K)]
}

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')