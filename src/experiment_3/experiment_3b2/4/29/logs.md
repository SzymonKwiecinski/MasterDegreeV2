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
To solve this problem, we aim to fit a straight line \( y = bx + a \) to the given data such that the maximum deviation of the observed \( y \) values from the predicted \( y \) values is minimized. This is a linear programming problem known as minimizing the maximum absolute deviation.

Let's denote:
- \( K \) as the number of data points.
- \( y_k \) and \( x_k \) as the \( k \)-th values of \( y \) and \( x \) respectively.
- \( a \) as the intercept of the fitted line.
- \( b \) as the slope of the fitted line.
- \( z \) as a variable representing the maximum deviation.

The objective is to minimize \( z \), subject to the constraints that the deviation for each data point is less than or equal to \( z \). The deviation for a data point \( (x_k, y_k) \) can be given as \( |y_k - (bx_k + a)| \).

The constraints can be written as:
- \( y_k - (bx_k + a) \leq z \)
- \( (bx_k + a) - y_k \leq z \)

These can be reformulated as:
- \( bx_k + a - z \leq y_k \)
- \( y_k \leq bx_k + a + z \)

We can now formulate the linear programming model in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

Minimize:
\[
z
\]

Subject to:
\[
bx_k + a - z \leq y_k, \quad \forall k = 1, \ldots, K
\]
\[
y_k \leq bx_k + a + z, \quad \forall k = 1, \ldots, K
\]

Where:
\begin{align*}
y_k & \text{ is the } k\text{-th observed value of } y, \\
x_k & \text{ is the } k\text{-th observed value of } x, \\
a & \text{ is the intercept of the fitted line,} \\
b & \text{ is the slope of the fitted line,} \\
z & \text{ is the maximum deviation to be minimized.}
\end{align*}

The decision variables are \( a \), \( b \), and \( z \).

\end{document}
```

The output from solving this linear programming model will give you the values for the intercept and slope, which should be presented in the specified output format as:

```json
{
    "intercept": a,
    "slope": b
}
```

Where \( a \) and \( b \) are the optimal values of the intercept and slope obtained from solving the linear program.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

Minimize:
\[
z
\]

Subject to:
\[
bx_k + a - z \leq y_k, \quad \forall k = 1, \ldots, K
\]
\[
y_k \leq bx_k + a + z, \quad \forall k = 1, \ldots, K
\]

Where:
\begin{align*}
y_k & \text{ is the } k\text{-th observed value of } y, \\
x_k & \text{ is the } k\text{-th observed value of } x, \\
a & \text{ is the intercept of the fitted line,} \\
b & \text{ is the slope of the fitted line,} \\
z & \text{ is the maximum deviation to be minimized.}
\end{align*}

The decision variables are \( a \), \( b \), and \( z \).

\end{document}
{
    "intercept": a,
    "slope": b
}</MATH_MODEL>
<DATA>
{'NumObs': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Given data
data = {
    'NumObs': 19,
    'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3],
    'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]
}

#### Number of observations
K = data['NumObs']
Y = data['Y']
X = data['X']

#### Create the problem
problem = pulp.LpProblem("Minimize_Max_Deviation", pulp.LpMinimize)

#### Decision Variables
a = pulp.LpVariable("a", lowBound=None)  #### intercept
b = pulp.LpVariable("b", lowBound=None)  #### slope
z = pulp.LpVariable("z", lowBound=0)     #### maximum deviation (non-negative)

#### Objective function
problem += z, "Objective"

#### Constraints
for k in range(K):
    problem += (b * X[k] + a - z <= Y[k]), f"Constraint1_{k+1}"
    problem += (Y[k] <= b * X[k] + a + z), f"Constraint2_{k+1}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

