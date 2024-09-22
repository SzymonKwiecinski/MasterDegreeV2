import pulp
import json

# Input data
data = {'K': 19, 
        'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 
              3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 
        'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 
              5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}

# Define the model
problem = pulp.LpProblem("Line_Fitting", pulp.LpMinimize)

# Define decision variables
b = pulp.LpVariable("b", None)
a = pulp.LpVariable("a", None)
e = pulp.LpVariable.dicts("e", range(data['K']), lowBound=0)

# Objective function: Minimize the sum of e_k
problem += pulp.lpSum(e[k] for k in range(data['K']))

# Constraints
for k in range(data['K']):
    problem += e[k] >= data['Y'][k] - (b * data['X'][k] + a)
    problem += e[k] >= -data['Y'][k] + (b * data['X'][k] + a)

# Solve the problem
problem.solve()

# Output the results
intercept = a.varValue
slope = b.varValue

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print(json.dumps({"intercept": intercept, "slope": slope}))