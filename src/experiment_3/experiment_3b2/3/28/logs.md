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


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
To solve the problem of fitting the best straight line \( y = bx + a \) to the given data points while minimizing the sum of absolute deviations, we need to formulate this as a linear programming problem. Let's detail the approach in the form of a linear program.

Given:
- \( y = [y_1, y_2, \ldots, y_K] \)
- \( x = [x_1, x_2, \ldots, x_K] \)

We aim to find the values of \( a \) (intercept) and \( b \) (slope) that minimize the sum of absolute deviations between the observed \( y_k \) and the predicted \( \hat{y}_k = bx_k + a \).

######### Linear Programming Formulation

Objective:
Minimize the sum of absolute deviations: 

\[ \sum_{k=1}^{K} |y_k - (bx_k + a)| \]

Introduce auxiliary variables \( z_k \) to represent the absolute deviations such that:

\[ z_k \geq y_k - (bx_k + a) \]
\[ z_k \geq - (y_k - (bx_k + a)) \]

Hence, our linear program is:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective:}

\[
\text{Minimize } \sum_{k=1}^{K} z_k
\]

\textbf{Subject to:}

\[
z_k \geq y_k - (b x_k + a), \quad k = 1, 2, \ldots, K
\]

\[
z_k \geq - (y_k - (b x_k + a)), \quad k = 1, 2, \ldots, K
\]

\[
z_k \geq 0, \quad k = 1, 2, \ldots, K
\]

\textbf{Variables:}

- \( a \) (intercept)
- \( b \) (slope)
- \( z_k \geq 0 \) for each \( k \).

\end{document}
```

In the output, the variables \( a \) and \( b \) are the intercept and slope of the fitted line, respectively.

This linear programming formulation can be solved using any linear programming solver to obtain the optimal values of \( a \) and \( b \). The given constraints ensure that the absolute deviation of each point from the fitted line is considered, satisfying the goal of minimizing the total absolute deviation.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective:}

\[
\text{Minimize } \sum_{k=1}^{K} z_k
\]

\textbf{Subject to:}

\[
z_k \geq y_k - (b x_k + a), \quad k = 1, 2, \ldots, K
\]

\[
z_k \geq - (y_k - (b x_k + a)), \quad k = 1, 2, \ldots, K
\]

\[
z_k \geq 0, \quad k = 1, 2, \ldots, K
\]

\textbf{Variables:}

- \( a \) (intercept)
- \( b \) (slope)
- \( z_k \geq 0 \) for each \( k \).

\end{document}</MATH_MODEL>
<DATA>
{'K': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from the input
data = {
    'K': 19,
    'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3],
    'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]
}

K = data['K']
Y = data['Y']
X = data['X']

#### Create a linear programming problem
problem = pulp.LpProblem("Minimize_z", pulp.LpMinimize)

#### Define variables
a = pulp.LpVariable("a", lowBound=None)  #### intercept
b = pulp.LpVariable("b", lowBound=None)  #### slope
z = [pulp.LpVariable(f"z_{k}", lowBound=0) for k in range(K)]  #### z_k variables

#### Objective function
problem += pulp.lpSum(z[k] for k in range(K)), "Objective"

#### Constraints
for k in range(K):
    problem += z[k] >= Y[k] - (b * X[k] + a), f"Constraint_1_{k}"
    problem += z[k] >= -(Y[k] - (b * X[k] + a)), f"Constraint_2_{k}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

