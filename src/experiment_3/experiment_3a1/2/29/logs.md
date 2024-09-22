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

Given the data points \((x_k, y_k)\) for \(k = 1, \ldots, K\), we seek to fit a line of the form \(y = bx + a\) that minimizes the maximum deviation of the observed values \(y_k\) from the predicted values \((bx_k + a)\).

\subsection*{Decision Variables}
\begin{align*}
b & : \text{slope of the fitted line} \\
a & : \text{intercept of the fitted line} \\
d_k & : \text{deviation for each observation } (k = 1, \ldots, K)
\end{align*}

\subsection*{Objective Function}
We want to minimize the maximum deviation:
\[
\min_{d_k} \quad D \quad \text{where} \quad D \geq d_k \quad \forall k
\]

Subject to:
\[
d_k \geq y_k - (bx_k + a) \quad \forall k
\]
\[
d_k \geq -(y_k - (bx_k + a)) \quad \forall k
\]

\subsection*{Constraints}
Thus, we can define the problem with the following constraints:
\begin{align*}
d_k & \geq y_k - (bx_k + a) & \forall k \\
d_k & \geq -(y_k - (bx_k + a)) & \forall k \\
D & \geq d_k & \forall k
\end{align*}

\subsection*{Output}
The output will be:
\[
\text{Output: } \{ \text{"intercept": } a, \text{"slope": } b \}
\]

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

Given the data points \((x_k, y_k)\) for \(k = 1, \ldots, K\), we seek to fit a line of the form \(y = bx + a\) that minimizes the maximum deviation of the observed values \(y_k\) from the predicted values \((bx_k + a)\).

\subsection*{Decision Variables}
\begin{align*}
b & : \text{slope of the fitted line} \\
a & : \text{intercept of the fitted line} \\
d_k & : \text{deviation for each observation } (k = 1, \ldots, K)
\end{align*}

\subsection*{Objective Function}
We want to minimize the maximum deviation:
\[
\min_{d_k} \quad D \quad \text{where} \quad D \geq d_k \quad \forall k
\]

Subject to:
\[
d_k \geq y_k - (bx_k + a) \quad \forall k
\]
\[
d_k \geq -(y_k - (bx_k + a)) \quad \forall k
\]

\subsection*{Constraints}
Thus, we can define the problem with the following constraints:
\begin{align*}
d_k & \geq y_k - (bx_k + a) & \forall k \\
d_k & \geq -(y_k - (bx_k + a)) & \forall k \\
D & \geq d_k & \forall k
\end{align*}

\subsection*{Output}
The output will be:
\[
\text{Output: } \{ \text{"intercept": } a, \text{"slope": } b \}
\]

\end{document}</MATH_MODEL>
<DATA>
{'NumObs': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Given data
data = '''{
    "NumObs": 19,
    "Y": [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3],
    "X": [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]
}'''

data_dict = json.loads(data)
NumObs = data_dict['NumObs']
Y = data_dict['Y']
X = data_dict['X']

#### Create the linear programming problem
problem = pulp.LpProblem("BestFitLine", pulp.LpMinimize)

#### Decision Variables
b = pulp.LpVariable("b", lowBound=None)  #### slope of the fitted line
a = pulp.LpVariable("a", lowBound=None)  #### intercept of the fitted line
D = pulp.LpVariable("D", lowBound=0)     #### maximum deviation

#### Deviation Variables
d = [pulp.LpVariable(f"d_{k}", lowBound=0) for k in range(NumObs)]

#### Objective Function: Minimize the maximum deviation
problem += D

#### Constraints
for k in range(NumObs):
    problem += d[k] >= Y[k] - (b * X[k] + a)
    problem += d[k] >= -(Y[k] - (b * X[k] + a))
    problem += D >= d[k]

#### Solve the problem
problem.solve()

#### Output the results
intercept = a.varValue
slope = b.varValue
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print(f'Output: {{ "intercept": {intercept}, "slope": {slope} }}')
```

