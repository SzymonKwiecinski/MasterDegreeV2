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
To solve this linear programming problem, we want to fit the best straight line \( y = bx + a \) by minimizing the maximum deviation of all the observed values \( y_k \) from the predicted values \( \hat{y}_k = bx_k + a \). This can be formulated as a linear programming problem with the following constraints:

1. For each observed pair \((x_k, y_k)\), the deviation \( d_k \) between the observed value \( y_k \) and the predicted value \( bx_k + a \) is defined as \( d_k = |y_k - (bx_k + a)| \).
2. The objective is to minimize the maximum deviation \( D \), where \( D \geq d_k \) for all \( k \).

The problem can be formulated in linear programming terms by introducing auxiliary variables to handle the absolute values, and then solve it using linear programming techniques.

Let's write the mathematical model in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Linear Programming Formulation}

Given observed data \(\{(x_k, y_k)\}\) for \(k = 1, \ldots, K\), we want to fit a line \(y = bx + a\) such that we minimize the maximum deviation of the observed \(y_k\) from the predicted \(\hat{y}_k = bx_k + a\).

\textit{Variables:}
\begin{align*}
a & : \text{intercept of the fitted line} \\
b & : \text{slope of the fitted line} \\
d_k & : \text{deviation for each } k \\
D & : \text{maximum deviation to minimize}
\end{align*}

\textit{Objective:}
\[
\min D
\]

\textit{Subject to:}
\begin{align*}
d_k & \geq y_k - (bx_k + a), & \forall k = 1, \ldots, K \\
d_k & \geq -(y_k - (bx_k + a)), & \forall k = 1, \ldots, K \\
D & \geq d_k, & \forall k = 1, \ldots, K
\end{align*}

\end{document}
```

This formulation can be solved using linear programming solvers to find the values of \(a\) (intercept) and \(b\) (slope) that minimize the maximum deviation \(D\). The output will give you the best-fit line parameters.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Linear Programming Formulation}

Given observed data \(\{(x_k, y_k)\}\) for \(k = 1, \ldots, K\), we want to fit a line \(y = bx + a\) such that we minimize the maximum deviation of the observed \(y_k\) from the predicted \(\hat{y}_k = bx_k + a\).

\textit{Variables:}
\begin{align*}
a & : \text{intercept of the fitted line} \\
b & : \text{slope of the fitted line} \\
d_k & : \text{deviation for each } k \\
D & : \text{maximum deviation to minimize}
\end{align*}

\textit{Objective:}
\[
\min D
\]

\textit{Subject to:}
\begin{align*}
d_k & \geq y_k - (bx_k + a), & \forall k = 1, \ldots, K \\
d_k & \geq -(y_k - (bx_k + a)), & \forall k = 1, \ldots, K \\
D & \geq d_k, & \forall k = 1, \ldots, K
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'NumObs': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Load the data
data = {
    'NumObs': 19, 
    'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 
    'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]
}

#### Number of observations
num_obs = data['NumObs']
Y = data['Y']
X = data['X']

#### Create the problem
problem = pulp.LpProblem("Minimize_Maximum_Deviation", pulp.LpMinimize)

#### Decision variables
a = pulp.LpVariable('a', lowBound=None, upBound=None, cat='Continuous')
b = pulp.LpVariable('b', lowBound=None, upBound=None, cat='Continuous')
D = pulp.LpVariable('D', lowBound=0, cat='Continuous')
d = [pulp.LpVariable(f'd_{k}', lowBound=0, cat='Continuous') for k in range(num_obs)]

#### Objective function
problem += D, "Minimize_Max_Deviation"

#### Constraints
for k in range(num_obs):
    #### d_k >= y_k - (b*x_k + a)
    problem += d[k] >= Y[k] - (b * X[k] + a), f"Constraint_Upper_{k}"
    #### d_k >= -(y_k - (b*x_k + a))
    problem += d[k] >= -(Y[k] - (b * X[k] + a)), f"Constraint_Lower_{k}"
    #### D >= d_k
    problem += D >= d[k], f"Max_Deviation_Constraint_{k}"

#### Solve the problem
problem.solve()

#### Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```


