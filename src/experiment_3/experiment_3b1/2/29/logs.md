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

\section*{Linear Programming Model for Linear Regression}

Given a set of observed values \( (x_k, y_k) \) for \( k = 1, \ldots, K \), we want to fit the best straight line represented by the equation:

\[
y = bx + a
\]

where \( a \) is the intercept and \( b \) is the slope. The objective is to minimize the maximum deviation of all observed values of \( y \) from the predicted values given by the linear relationship.

Define \( e_k = y_k - (bx_k + a) \) as the deviation of the observed value from the predicted value. Our goal is to minimize the maximum absolute deviation:

\[
\text{Minimize} \quad T
\]

subject to:

\[
e_k \leq T \quad \forall k = 1, \ldots, K
\]
\[
-e_k \leq T \quad \forall k = 1, \ldots, K
\]

This can be expressed as:

\[
y_k - (bx_k + a) \leq T \quad \forall k
\]
\[
-(y_k - (bx_k + a)) \leq T \quad \forall k
\]

Rearranging the constraints gives:

\[
bx_k + a + T \geq y_k \quad \forall k
\]
\[
bx_k + a - T \leq y_k \quad \forall k
\]

This leads us to the following Linear Programming formulation:

\begin{align*}
\text{Minimize} \quad & T \\
\text{subject to} \quad & bx_k + a + T \geq y_k, \quad \forall k = 1, \ldots, K \\
& bx_k + a - T \leq y_k, \quad \forall k = 1, \ldots, K \\
& T \geq 0
\end{align*}

The output of the model will provide the values for \( a \) (intercept) and \( b \) (slope) that define the best-fitting line.

\textbf{Output Format:}
\begin{verbatim}
{
    "intercept": a,
    "slope": b
}
\end{verbatim}

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

Given a set of observed values \( (x_k, y_k) \) for \( k = 1, \ldots, K \), we want to fit the best straight line represented by the equation:

\[
y = bx + a
\]

where \( a \) is the intercept and \( b \) is the slope. The objective is to minimize the maximum deviation of all observed values of \( y \) from the predicted values given by the linear relationship.

Define \( e_k = y_k - (bx_k + a) \) as the deviation of the observed value from the predicted value. Our goal is to minimize the maximum absolute deviation:

\[
\text{Minimize} \quad T
\]

subject to:

\[
e_k \leq T \quad \forall k = 1, \ldots, K
\]
\[
-e_k \leq T \quad \forall k = 1, \ldots, K
\]

This can be expressed as:

\[
y_k - (bx_k + a) \leq T \quad \forall k
\]
\[
-(y_k - (bx_k + a)) \leq T \quad \forall k
\]

Rearranging the constraints gives:

\[
bx_k + a + T \geq y_k \quad \forall k
\]
\[
bx_k + a - T \leq y_k \quad \forall k
\]

This leads us to the following Linear Programming formulation:

\begin{align*}
\text{Minimize} \quad & T \\
\text{subject to} \quad & bx_k + a + T \geq y_k, \quad \forall k = 1, \ldots, K \\
& bx_k + a - T \leq y_k, \quad \forall k = 1, \ldots, K \\
& T \geq 0
\end{align*}

The output of the model will provide the values for \( a \) (intercept) and \( b \) (slope) that define the best-fitting line.

\textbf{Output Format:}
\begin{verbatim}
{
    "intercept": a,
    "slope": b
}
\end{verbatim}

\end{document}</MATH_MODEL>
<DATA>
{'NumObs': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data
data = {
    'NumObs': 19,
    'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3],
    'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]
}

#### Create LP problem
problem = pulp.LpProblem("Linear_Regression_LP", pulp.LpMinimize)

#### Variables
a = pulp.LpVariable("a", lowBound=None)  #### intercept
b = pulp.LpVariable("b", lowBound=None)  #### slope
T = pulp.LpVariable("T", lowBound=0)     #### maximum deviation

#### Constraints
for k in range(data['NumObs']):
    problem += (b * data['X'][k] + a + T >= data['Y'][k], f"UpperBound_{k}")
    problem += (b * data['X'][k] + a - T <= data['Y'][k], f"LowerBound_{k}")

#### Objective
problem += T

#### Solve the problem
problem.solve()

#### Output
output = {
    "intercept": a.varValue,
    "slope": b.varValue
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

