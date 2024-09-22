import pulp

# Data
data = {
    'NumObs': 19, 
    'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 
    'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]
}

# Extract data
num_obs = data['NumObs']
y = data['Y']
x = data['X']

# Initialize the Linear Programming problem
problem = pulp.LpProblem("Minimize_Max_Absolute_Deviation", pulp.LpMinimize)

# Decision Variables
b = pulp.LpVariable("b", cat='Continuous')  # slope
a = pulp.LpVariable("a", cat='Continuous')  # intercept
M = pulp.LpVariable("M", lowBound=0, cat='Continuous')  # max deviation

# Define the objective function to minimize M
problem += M

# Add the constraints for each observation
for k in range(num_obs):
    d_k = y[k] - (b * x[k] + a)
    problem += d_k <= M  # y_k - (bx_k + a) <= M
    problem += -d_k <= M  # -(y_k - (bx_k + a)) <= M

# Solve the problem
problem.solve()

# Output the results
print(f'Slope (b): {pulp.value(b)}')
print(f'Intercept (a): {pulp.value(a)}')
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')