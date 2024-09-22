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

\section*{Linear Programming Model for Fitting a Line}

Given a set of corresponding values \( (x_k, y_k) \) for \( k = 1, 2, \ldots, K \), we aim to fit the best straight line of the form \( y = bx + a \) by minimizing the maximum deviation of the observed \( y \) values from the predicted values of the linear relationship.

We define the deviation for each observed value as follows:

\[
d_k = y_k - (bx_k + a)
\]

The objective is to minimize the maximum absolute deviation across all observations:

\[
\text{Minimize } D = \max_{k=1,\ldots,K} |d_k| = \max_{k=1,\ldots,K} |y_k - (bx_k + a)|
\]

To express this as a linear programming problem, we introduce auxiliary variables \( D^+ \) and \( D^- \) to represent the positive and negative deviations, respectively:

\[
d_k \leq D^+ \quad \forall k
\]
\[
-d_k \leq D^- \quad \forall k
\]

Thus, our problem can be reformulated as:

\[
\text{Minimize } D^+ + D^-
\]

Subject to the following constraints:

\[
y_k - (bx_k + a) \leq D^+ \quad \forall k
\]
\[
-(y_k - (bx_k + a)) \leq D^- \quad \forall k
\]

In addition, we can consider the relationships of the deviations explicitly:

\[
D^+ \geq 0, \quad D^- \geq 0
\]

The final model can be summarized as:

\[
\begin{aligned}
& \text{Minimize}\quad D^+ + D^- \\
& \text{subject to} \\
& y_k - (bx_k + a) \leq D^+ \quad \forall k \\
& -(y_k - (bx_k + a)) \leq D^- \quad \forall k \\
& D^+ \geq 0, \quad D^- \geq 0 \\
\end{aligned}
\]

The output of the model will be as follows:

\[
\{ \text{intercept}: a, \text{slope}: b \}
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

\section*{Linear Programming Model for Fitting a Line}

Given a set of corresponding values \( (x_k, y_k) \) for \( k = 1, 2, \ldots, K \), we aim to fit the best straight line of the form \( y = bx + a \) by minimizing the maximum deviation of the observed \( y \) values from the predicted values of the linear relationship.

We define the deviation for each observed value as follows:

\[
d_k = y_k - (bx_k + a)
\]

The objective is to minimize the maximum absolute deviation across all observations:

\[
\text{Minimize } D = \max_{k=1,\ldots,K} |d_k| = \max_{k=1,\ldots,K} |y_k - (bx_k + a)|
\]

To express this as a linear programming problem, we introduce auxiliary variables \( D^+ \) and \( D^- \) to represent the positive and negative deviations, respectively:

\[
d_k \leq D^+ \quad \forall k
\]
\[
-d_k \leq D^- \quad \forall k
\]

Thus, our problem can be reformulated as:

\[
\text{Minimize } D^+ + D^-
\]

Subject to the following constraints:

\[
y_k - (bx_k + a) \leq D^+ \quad \forall k
\]
\[
-(y_k - (bx_k + a)) \leq D^- \quad \forall k
\]

In addition, we can consider the relationships of the deviations explicitly:

\[
D^+ \geq 0, \quad D^- \geq 0
\]

The final model can be summarized as:

\[
\begin{aligned}
& \text{Minimize}\quad D^+ + D^- \\
& \text{subject to} \\
& y_k - (bx_k + a) \leq D^+ \quad \forall k \\
& -(y_k - (bx_k + a)) \leq D^- \quad \forall k \\
& D^+ \geq 0, \quad D^- \geq 0 \\
\end{aligned}
\]

The output of the model will be as follows:

\[
\{ \text{intercept}: a, \text{slope}: b \}
\]

\end{document}</MATH_MODEL>
<DATA>
{'NumObs': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
data = {
    'NumObs': 19,
    'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3],
    'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]
}

#### Problem definition
problem = pulp.LpProblem("Line_Fitting_Problem", pulp.LpMinimize)

#### Variables
a = pulp.LpVariable('a', lowBound=None, cat='Continuous')
b = pulp.LpVariable('b', lowBound=None, cat='Continuous')
D_plus = pulp.LpVariable('D_plus', lowBound=0, cat='Continuous')
D_minus = pulp.LpVariable('D_minus', lowBound=0, cat='Continuous')

#### Objective function: Minimize D_plus + D_minus
problem += D_plus + D_minus

#### Constraints
for k in range(data['NumObs']):
    x_k = data['X'][k]
    y_k = data['Y'][k]
    problem += y_k - (b * x_k + a) <= D_plus, f"Constraint_Positive_Deviation_{k}"
    problem += -(y_k - (b * x_k + a)) <= D_minus, f"Constraint_Negative_Deviation_{k}"

#### Solve
problem.solve()

#### Print solution
print(f'Optimal Intercept (a): {pulp.value(a)}')
print(f'Optimal Slope (b): {pulp.value(b)}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

