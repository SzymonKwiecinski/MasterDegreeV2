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

\section*{Linear Programming Model for Best Fit Line}

Given a set of observed values \( y_k \) and \( x_k \) for \( k = 1, \ldots, K \), we aim to fit the best straight line described by the equation:

\[
y = bx + a
\]

where \( a \) is the intercept and \( b \) is the slope of the line. The objective is to minimize the maximum deviation of all the observed values of \( y \) from the predicted values based on the linear relationship.

Let:

- \( y_k \) be the observed values.
- \( x_k \) be the corresponding values.
- \( \epsilon_k \) be the deviation for each observed value, defined as:

\[
\epsilon_k = y_k - (bx_k + a)
\]

We then formulate the problem as follows:

\subsection*{Objective Function}

Minimize the maximum deviation:

\[
\min \, t
\]

subject to the constraints:

\[
y_k - (bx_k + a) \leq t \quad \forall k = 1, \ldots, K
\]
\[
-(y_k - (bx_k + a)) \leq t \quad \forall k = 1, \ldots, K
\]

\subsection*{Linear Programming Formulation}

We summarize the linear programming model:

\begin{align*}
\text{Minimize} \quad & t \\
\text{Subject to} \quad & y_k - bx_k - a \leq t, \quad k = 1, \ldots, K \\
& -y_k + bx_k + a \leq t, \quad k = 1, \ldots, K \\
& b \in \mathbb{R}, \\
& a \in \mathbb{R}, \\
& t \geq 0.
\end{align*}

\subsection*{Output}

The output of this optimization problem will yield the values for:

\begin{align*}
\text{intercept} & = a, \\
\text{slope} & = b.
\end{align*}

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

\section*{Linear Programming Model for Best Fit Line}

Given a set of observed values \( y_k \) and \( x_k \) for \( k = 1, \ldots, K \), we aim to fit the best straight line described by the equation:

\[
y = bx + a
\]

where \( a \) is the intercept and \( b \) is the slope of the line. The objective is to minimize the maximum deviation of all the observed values of \( y \) from the predicted values based on the linear relationship.

Let:

- \( y_k \) be the observed values.
- \( x_k \) be the corresponding values.
- \( \epsilon_k \) be the deviation for each observed value, defined as:

\[
\epsilon_k = y_k - (bx_k + a)
\]

We then formulate the problem as follows:

\subsection*{Objective Function}

Minimize the maximum deviation:

\[
\min \, t
\]

subject to the constraints:

\[
y_k - (bx_k + a) \leq t \quad \forall k = 1, \ldots, K
\]
\[
-(y_k - (bx_k + a)) \leq t \quad \forall k = 1, \ldots, K
\]

\subsection*{Linear Programming Formulation}

We summarize the linear programming model:

\begin{align*}
\text{Minimize} \quad & t \\
\text{Subject to} \quad & y_k - bx_k - a \leq t, \quad k = 1, \ldots, K \\
& -y_k + bx_k + a \leq t, \quad k = 1, \ldots, K \\
& b \in \mathbb{R}, \\
& a \in \mathbb{R}, \\
& t \geq 0.
\end{align*}

\subsection*{Output}

The output of this optimization problem will yield the values for:

\begin{align*}
\text{intercept} & = a, \\
\text{slope} & = b.
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'NumObs': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data as a JSON string
data_json = '{"NumObs": 19, "Y": [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], "X": [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}'
data = json.loads(data_json)

#### Extract data
K = data['NumObs']
Y = data['Y']
X = data['X']

#### Create a linear programming problem
problem = pulp.LpProblem("BestFitLine", pulp.LpMinimize)

#### Variables
b = pulp.LpVariable("slope", lowBound=None)  #### Slope
a = pulp.LpVariable("intercept", lowBound=None)  #### Intercept
t = pulp.LpVariable("max_deviation", lowBound=0)  #### Maximum deviation

#### Objective function
problem += t, "Minimize_Max_Deviation"

#### Constraints
for k in range(K):
    problem += Y[k] - (b * X[k] + a) <= t, f"Upper_Bound_Constraint_{k+1}"
    problem += -(Y[k] - (b * X[k] + a)) <= t, f"Lower_Bound_Constraint_{k+1}"

#### Solve the problem
problem.solve()

#### Output results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print(f'Intercept (a): {pulp.value(a)}')
print(f'Slope (b): {pulp.value(b)}')
```

