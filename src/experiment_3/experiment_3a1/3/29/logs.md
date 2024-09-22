# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
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


OBJECTIVE: Fit the ‘best’ straight line y = bx + a where the objective is to minimize the maximum deviation of all the observed values of y from the value predicted by the linear relationship.

OUTPUT INFO:

- \var{intercept} represents the intercept of the fitted line
- \var{slope} represents the slope of the fitted line

OUTPUT FORMAT:

{
    "intercept": intercept,
    "slope": slope
}
</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model to Fit a Line}

Given a set of observations for quantities \( x \) and \( y \) where \( k = 1, \ldots, K \):

\[
y_k \text{ for } k = 1, \ldots, K
\]
\[
x_k \text{ for } k = 1, \ldots, K
\]

The objective is to fit the best straight line of the form:

\[
y = bx + a
\]

where \( b \) is the slope and \( a \) is the intercept. We want to minimize the maximum deviation of the observed \( y_k \) values from the predicted \( y \) values based on the linear model.

Define the deviations \( d_k \) for each observation, which represent the difference between the observed values and the values predicted by the model:

\[
d_k = y_k - (bx_k + a)
\]

We aim to minimize the maximum deviation:

\[
\min \, t
\]

subject to the constraints:

\[
d_k \leq t \quad \forall k
\]
\[
-d_k \leq t \quad \forall k
\]

This leads us to the following inequalities:

\[
y_k - (bx_k + a) \leq t \quad \forall k
\]
\[
-(y_k - (bx_k + a)) \leq t \quad \forall k
\]

Thus, the formulation of our linear programming problem is:

\[
\begin{align*}
\text{Minimize} & \quad t \\
\text{Subject to:} & \quad y_k - (bx_k + a) \leq t, \quad \forall k \\
& \quad -(y_k - (bx_k + a)) \leq t, \quad \forall k \\
& \quad b, a \text{ are parameters to be determined}
\end{align*}
\]

The solution to this problem will yield the values of \( a \) (intercept) and \( b \) (slope) of the best-fit line.

\end{document}
```

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model to Fit a Line}

Given a set of observations for quantities \( x \) and \( y \) where \( k = 1, \ldots, K \):

\[
y_k \text{ for } k = 1, \ldots, K
\]
\[
x_k \text{ for } k = 1, \ldots, K
\]

The objective is to fit the best straight line of the form:

\[
y = bx + a
\]

where \( b \) is the slope and \( a \) is the intercept. We want to minimize the maximum deviation of the observed \( y_k \) values from the predicted \( y \) values based on the linear model.

Define the deviations \( d_k \) for each observation, which represent the difference between the observed values and the values predicted by the model:

\[
d_k = y_k - (bx_k + a)
\]

We aim to minimize the maximum deviation:

\[
\min \, t
\]

subject to the constraints:

\[
d_k \leq t \quad \forall k
\]
\[
-d_k \leq t \quad \forall k
\]

This leads us to the following inequalities:

\[
y_k - (bx_k + a) \leq t \quad \forall k
\]
\[
-(y_k - (bx_k + a)) \leq t \quad \forall k
\]

Thus, the formulation of our linear programming problem is:

\[
\begin{align*}
\text{Minimize} & \quad t \\
\text{Subject to:} & \quad y_k - (bx_k + a) \leq t, \quad \forall k \\
& \quad -(y_k - (bx_k + a)) \leq t, \quad \forall k \\
& \quad b, a \text{ are parameters to be determined}
\end{align*}
\]

The solution to this problem will yield the values of \( a \) (intercept) and \( b \) (slope) of the best-fit line.

\end{document}</MATH_MODEL>
<DATA>
{'NumObs': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data provided in the JSON format
data_json = '{"NumObs": 19, "Y": [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], "X": [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}'
data = json.loads(data_json)

#### Extracting the number of observations, Y and X values
num_obs = data['NumObs']
Y = data['Y']
X = data['X']

#### Create the linear programming problem
problem = pulp.LpProblem("BestFitLine", pulp.LpMinimize)

#### Defining variables
b = pulp.LpVariable("b", lowBound=None)  #### slope
a = pulp.LpVariable("a", lowBound=None)  #### intercept
t = pulp.LpVariable("t", lowBound=0)     #### maximum deviation

#### Adding constraints for each observation
for k in range(num_obs):
    problem += (Y[k] - (b * X[k] + a) <= t), f"UpperBound_{k}"
    problem += (-(Y[k] - (b * X[k] + a)) <= t), f"LowerBound_{k}"

#### Objective function to minimize
problem += t, "Objective"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

