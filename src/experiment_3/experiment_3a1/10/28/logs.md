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
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Linear Regression}

Let \( y_k \) be the \( k \)-th observed value of \( y \) and \( x_k \) be the \( k \)-th observed value of \( x \), for \( k = 1, 2, \ldots, K \). We aim to fit the best straight line given by the equation

\[
y = bx + a
\]

where \( b \) is the slope and \( a \) is the intercept. The objective is to minimize the sum of absolute deviations between observed values and predicted values.

Define the deviation for each observation as

\[
d_k = y_k - (bx_k + a)
\]

Our objective function is to minimize the total absolute deviation, expressed as:

\[
\text{Minimize } \sum_{k=1}^{K} |d_k|
\]

To handle the absolute values, we introduce non-negative variables \( e_k \) such that:

\[
d_k \leq e_k \quad \text{and} \quad -d_k \leq e_k \quad \text{for } k = 1, 2, \ldots, K
\]

This allows us to rewrite our objective function as:

\[
\text{Minimize } \sum_{k=1}^{K} e_k
\]

Thus, the complete linear programming model can be formulated as follows:

\begin{align*}
\text{Minimize } & \sum_{k=1}^{K} e_k \\
\text{subject to } & y_k - (bx_k + a) \leq e_k, \quad k = 1, \ldots, K \\
& -(y_k - (bx_k + a)) \leq e_k, \quad k = 1, \ldots, K \\
& e_k \geq 0, \quad k = 1, \ldots, K \\
& b \text{ and } a \text{ are unrestricted in sign.}
\end{align*}

After solving this linear programming problem, the values of \( a \) and \( b \) will provide the slope and intercept of the fitted line, respectively.

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

\section*{Linear Programming Model for Linear Regression}

Let \( y_k \) be the \( k \)-th observed value of \( y \) and \( x_k \) be the \( k \)-th observed value of \( x \), for \( k = 1, 2, \ldots, K \). We aim to fit the best straight line given by the equation

\[
y = bx + a
\]

where \( b \) is the slope and \( a \) is the intercept. The objective is to minimize the sum of absolute deviations between observed values and predicted values.

Define the deviation for each observation as

\[
d_k = y_k - (bx_k + a)
\]

Our objective function is to minimize the total absolute deviation, expressed as:

\[
\text{Minimize } \sum_{k=1}^{K} |d_k|
\]

To handle the absolute values, we introduce non-negative variables \( e_k \) such that:

\[
d_k \leq e_k \quad \text{and} \quad -d_k \leq e_k \quad \text{for } k = 1, 2, \ldots, K
\]

This allows us to rewrite our objective function as:

\[
\text{Minimize } \sum_{k=1}^{K} e_k
\]

Thus, the complete linear programming model can be formulated as follows:

\begin{align*}
\text{Minimize } & \sum_{k=1}^{K} e_k \\
\text{subject to } & y_k - (bx_k + a) \leq e_k, \quad k = 1, \ldots, K \\
& -(y_k - (bx_k + a)) \leq e_k, \quad k = 1, \ldots, K \\
& e_k \geq 0, \quad k = 1, \ldots, K \\
& b \text{ and } a \text{ are unrestricted in sign.}
\end{align*}

After solving this linear programming problem, the values of \( a \) and \( b \) will provide the slope and intercept of the fitted line, respectively.

\end{document}</MATH_MODEL>
<DATA>
{'K': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data
data = json.loads('{"K": 19, "Y": [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], "X": [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}')

K = data['K']
Y = data['Y']
X = data['X']

#### Create the problem variable
problem = pulp.LpProblem("Linear_Regression_Problem", pulp.LpMinimize)

#### Define variables
a = pulp.LpVariable("a", lowBound=None)  #### Intercept
b = pulp.LpVariable("b", lowBound=None)  #### Slope
e = pulp.LpVariable.dicts("e", range(K), lowBound=0)  #### Deviation variables

#### Objective function: Minimize the sum of e_k
problem += pulp.lpSum(e[k] for k in range(K))

#### Constraints
for k in range(K):
    problem += Y[k] - (b * X[k] + a) <= e[k]  #### d_k <= e_k
    problem += -(Y[k] - (b * X[k] + a)) <= e[k]  #### -d_k <= e_k

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

