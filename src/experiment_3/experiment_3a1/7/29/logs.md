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

Given a set of observations, where the \textit{k}-th value of \( y \) is denoted as \( y_k \) and the \textit{k}-th value of \( x \) is denoted as \( x_k \), the objective is to fit a straight line in the form of \( y = bx + a \) while minimizing the maximum deviation of the observed \( y \) values from the predicted values.

Let:

\[
y_k = b x_k + a + e_k
\]

where \( e_k \) represents the deviation for each observation. The goal is to minimize the maximum of these deviations:

\[
\min \max_{k=1, \ldots, K} |e_k|
\]

This can be formulated using the following constraints:

1. Define \( e_k^+ \) and \( e_k^- \) such that:
   \[
   e_k = e_k^+ - e_k^-
   \]
   with \( e_k^+, e_k^- \geq 0 \).

2. The deviations can be expressed as:
   \[
   e_k^+ \geq y_k - (b x_k + a) \quad \forall k
   \]
   \[
   e_k^- \geq -(y_k - (b x_k + a)) \quad \forall k
   \]

The optimization problem can now be stated as:

\[
\text{Minimize } M
\]

subject to:

\[
e_k^+ \leq M \quad \forall k
\]

\[
e_k^- \leq M \quad \forall k
\]

\[
e_k^+ \geq y_k - (b x_k + a) \quad \forall k
\]

\[
e_k^- \geq -(y_k - (b x_k + a)) \quad \forall k
\]

\[
M \geq 0
\]

\noindent where \( a \) is the intercept and \( b \) is the slope of the fitted line.

\subsection*{Output}
The output will be:

\[
\{
    \text{"intercept"}: a,
    \text{"slope"}: b
\}
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

Given a set of observations, where the \textit{k}-th value of \( y \) is denoted as \( y_k \) and the \textit{k}-th value of \( x \) is denoted as \( x_k \), the objective is to fit a straight line in the form of \( y = bx + a \) while minimizing the maximum deviation of the observed \( y \) values from the predicted values.

Let:

\[
y_k = b x_k + a + e_k
\]

where \( e_k \) represents the deviation for each observation. The goal is to minimize the maximum of these deviations:

\[
\min \max_{k=1, \ldots, K} |e_k|
\]

This can be formulated using the following constraints:

1. Define \( e_k^+ \) and \( e_k^- \) such that:
   \[
   e_k = e_k^+ - e_k^-
   \]
   with \( e_k^+, e_k^- \geq 0 \).

2. The deviations can be expressed as:
   \[
   e_k^+ \geq y_k - (b x_k + a) \quad \forall k
   \]
   \[
   e_k^- \geq -(y_k - (b x_k + a)) \quad \forall k
   \]

The optimization problem can now be stated as:

\[
\text{Minimize } M
\]

subject to:

\[
e_k^+ \leq M \quad \forall k
\]

\[
e_k^- \leq M \quad \forall k
\]

\[
e_k^+ \geq y_k - (b x_k + a) \quad \forall k
\]

\[
e_k^- \geq -(y_k - (b x_k + a)) \quad \forall k
\]

\[
M \geq 0
\]

\noindent where \( a \) is the intercept and \( b \) is the slope of the fitted line.

\subsection*{Output}
The output will be:

\[
\{
    \text{"intercept"}: a,
    \text{"slope"}: b
\}
\]

\end{document}</MATH_MODEL>
<DATA>
{'NumObs': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import numpy as np

#### Data input
data = {
    'NumObs': 19, 
    'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 
    'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]
}

#### Problem definition
problem = pulp.LpProblem("Best_Fit_Line", pulp.LpMinimize)

#### Variables
a = pulp.LpVariable("a", lowBound=None)  #### Intercept
b = pulp.LpVariable("b", lowBound=None)  #### Slope
M = pulp.LpVariable("M", lowBound=0)     #### Maximum deviation
e_plus = [pulp.LpVariable(f"e_plus_{k}", lowBound=0) for k in range(data['NumObs'])]
e_minus = [pulp.LpVariable(f"e_minus_{k}", lowBound=0) for k in range(data['NumObs'])]

#### Objective function
problem += M, "Minimize_Max_Deviation"

#### Constraints
for k in range(data['NumObs']):
    problem += e_plus[k] >= data['Y'][k] - (b * data['X'][k] + a), f"Pos_Deviation_{k}"
    problem += e_minus[k] >= -(data['Y'][k] - (b * data['X'][k] + a)), f"Neg_Deviation_{k}"
    problem += e_plus[k] <= M, f"Max_Pos_Deviation_{k}"
    problem += e_minus[k] <= M, f"Max_Neg_Deviation_{k}"

#### Solve the problem
problem.solve()

#### Output results
intercept = a.varValue
slope = b.varValue
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print({'intercept': intercept, 'slope': slope})
```

