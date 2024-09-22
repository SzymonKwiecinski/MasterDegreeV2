import pulp
import json

# Given data
data = '''{
    "NumObs": 19,
    "Y": [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3],
    "X": [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]
}'''

data_dict = json.loads(data)
NumObs = data_dict['NumObs']
Y = data_dict['Y']
X = data_dict['X']

# Create the linear programming problem
problem = pulp.LpProblem("BestFitLine", pulp.LpMinimize)

# Decision Variables
b = pulp.LpVariable("b", lowBound=None)  # slope of the fitted line
a = pulp.LpVariable("a", lowBound=None)  # intercept of the fitted line
D = pulp.LpVariable("D", lowBound=0)     # maximum deviation

# Deviation Variables
d = [pulp.LpVariable(f"d_{k}", lowBound=0) for k in range(NumObs)]

# Objective Function: Minimize the maximum deviation
problem += D

# Constraints
for k in range(NumObs):
    problem += d[k] >= Y[k] - (b * X[k] + a)
    problem += d[k] >= -(Y[k] - (b * X[k] + a))
    problem += D >= d[k]

# Solve the problem
problem.solve()

# Output the results
intercept = a.varValue
slope = b.varValue
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print(f'Output: {{ "intercept": {intercept}, "slope": {slope} }}')