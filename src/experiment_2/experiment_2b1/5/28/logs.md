# START: OnePrompt 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Python. Based on description you solve given problem using Pulp python library. Python code place between ```python and ```. You receive the data in json format between: <DATA></DATA>. Do not change data format! Do not use `while` loop in python code! Do not include 'pip install' in script. Assume every python package is installed Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')`  
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP
PROBLEM INFO:

- A quantity y is known to depend on another quantity x. A set of corresponding values has been collected for x and y and is presented.
- The \var{k}-th y value takes \var{y_{k}} and the \var{k}-th x value takes \var{x_{k}}.

INPUT FORMAT:

{
    "y": [y_{k} for k = 1,...,K],
    "x": [x_{k} for k = 1,...,K]
}


OBJECTIVE: Fit the ‘best’ straight line y = bx + a to this set of data points. The objective is to minimise the sum of absolute deviations of each observed value of y from the value predicted by the linear relationship.

OUTPUT INFO:

- \var{intercept} represents the intercept of the fitted line
- \var{slope} represents the slope of the fitted line

OUTPUT FORMAT:

{
    "intercept": intercept,
    "slope": slope
}
</DESCRIPTION>
<DATA>
{'K': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Given data in JSON format
data = {'K': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}

#### Extract values
K = data['K']
Y = data['Y']
X = data['X']

#### Create a linear programming problem
problem = pulp.LpProblem("FitBestLine", pulp.LpMinimize)

#### Define intercept (a) and slope (b)
intercept = pulp.LpVariable('intercept', lowBound=None)
slope = pulp.LpVariable('slope', lowBound=None)

#### Define the absolute deviations
deviations = [pulp.LpVariable(f'dev_{k}', lowBound=0) for k in range(K)]

#### Objective function: minimize the sum of absolute deviations
problem += pulp.lpSum(deviations), "Minimize_Absolute_Deviation"

#### Constraints for each data point
for k in range(K):
    problem += deviations[k] >= Y[k] - (slope * X[k] + intercept), f"Upper_Bound_{k}"
    problem += deviations[k] >= -(Y[k] - (slope * X[k] + intercept)), f"Lower_Bound_{k}"

#### Solve the problem
problem.solve()

#### Get the results
fitted_intercept = pulp.value(intercept)
fitted_slope = pulp.value(slope)

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

#### Prepare the output
output = {
    "intercept": fitted_intercept,
    "slope": fitted_slope
}

#### Print output
print(output)
```

