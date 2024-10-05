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


OBJECTIVE: Fit the ‘best’ quadratic curve y = c * x^2 + b * x + a to this set of data points. The objective is to minimize the sum of absolute deviations of each observed value of y from the value predicted by the quadratic relationship.

OUTPUT INFO:

- \var{quadratic} represents the coefficient of quadratic term
- \var{linear} represents the coefficient of linear term
- \var{constant} represents the coefficient of constant

OUTPUT FORMAT:

{
    "quadratic": quadratic,
    "linear": linear,
    "constant": constant
}
</DESCRIPTION>
<DATA>
{'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data Input
data = {'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 
        'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}

y_values = data["y"]
x_values = data["x"]
K = len(y_values)

#### Problem
problem = pulp.LpProblem("Quadratic_Fit", pulp.LpMinimize)

#### Decision Variables
c = pulp.LpVariable("quadratic_term", lowBound=None, upBound=None, cat='Continuous')
b = pulp.LpVariable("linear_term", lowBound=None, upBound=None, cat='Continuous')
a = pulp.LpVariable("constant_term", lowBound=None, upBound=None, cat='Continuous')
deviations = [pulp.LpVariable(f"deviation_{k}", lowBound=0, cat='Continuous') for k in range(K)]

#### Objective Function: Minimize the sum of absolute deviations
objective = pulp.lpSum(deviations)
problem += objective

#### Constraints: Control absolute deviation |y_k - (c * x_k^2 + b * x_k + a)|
for k, (y_k, x_k) in enumerate(zip(y_values, x_values)):
    predicted_y = c * (x_k**2) + b * x_k + a
    problem += deviations[k] >= y_k - predicted_y
    problem += deviations[k] >= predicted_y - y_k

#### Solve Problem
problem.solve()

#### Extract Solution
result = {
    "quadratic": pulp.value(c),
    "linear": pulp.value(b),
    "constant": pulp.value(a)
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

