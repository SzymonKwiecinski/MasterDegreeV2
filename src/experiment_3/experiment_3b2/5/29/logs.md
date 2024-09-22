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
To address this problem, we need to formulate a linear programming model that minimizes the maximum deviation of the observed values of \( y \) from the predicted values given by the equation \( y = bx + a \).

Let's denote the variables:
- \( a \) as the intercept of the line.
- \( b \) as the slope of the line.
- \( d \) as the maximum deviation, which we aim to minimize.

The problem can be formulated as follows:

**Objective Function:**
Minimize \( d \).

**Constraints:**
For each observation \( k \):
\[
y_k - (bx_k + a) \leq d
\]
\[
(bx_k + a) - y_k \leq d
\]

This ensures that the deviation \( |y_k - (bx_k + a)| \) does not exceed \( d \).

Here is the complete LP formulation in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective:} Minimize the maximum deviation \( d \).

\textbf{Decision Variables:}
\[
\begin{aligned}
    &a \quad \text{(intercept of the line)} \\
    &b \quad \text{(slope of the line)} \\
    &d \quad \text{(maximum deviation)}
\end{aligned}
\]

\textbf{Objective Function:}
\[
\min d
\]

\textbf{Constraints:}
For each \( k = 1, \ldots, K \):
\[
\begin{aligned}
    &y_k - (bx_k + a) \leq d \\
    &(bx_k + a) - y_k \leq d
\end{aligned}
\]

\textbf{Conclusion:}

By solving this linear programming model, we can obtain the values of \( a \) (intercept) and \( b \) (slope) that fit the best straight line to the data by minimizing the maximum deviation.

\end{document}
```

This formulation leverages linear programming to address the problem of finding the best fit line under the criterion of minimizing the maximum absolute deviation. This type of fitting is known as Chebyshev or Minimax fitting.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective:} Minimize the maximum deviation \( d \).

\textbf{Decision Variables:}
\[
\begin{aligned}
    &a \quad \text{(intercept of the line)} \\
    &b \quad \text{(slope of the line)} \\
    &d \quad \text{(maximum deviation)}
\end{aligned}
\]

\textbf{Objective Function:}
\[
\min d
\]

\textbf{Constraints:}
For each \( k = 1, \ldots, K \):
\[
\begin{aligned}
    &y_k - (bx_k + a) \leq d \\
    &(bx_k + a) - y_k \leq d
\end{aligned}
\]

\textbf{Conclusion:}

By solving this linear programming model, we can obtain the values of \( a \) (intercept) and \( b \) (slope) that fit the best straight line to the data by minimizing the maximum deviation.

\end{document}</MATH_MODEL>
<DATA>
{'NumObs': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Given data in JSON format
data_json = '{"NumObs": 19, "Y": [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], "X": [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}'
data = json.loads(data_json)

#### Number of observations
K = data['NumObs']
X = data['X']
Y = data['Y']

#### Create the linear programming problem
problem = pulp.LpProblem("Minimize_Max_Deviation", pulp.LpMinimize)

#### Decision Variables
a = pulp.LpVariable("a", lowBound=None)  #### intercept
b = pulp.LpVariable("b", lowBound=None)  #### slope
d = pulp.LpVariable("d", lowBound=0)     #### maximum deviation

#### Objective Function: minimize d
problem += d, "Objective"

#### Constraints
for k in range(K):
    problem += Y[k] - (b * X[k] + a) <= d, f"Upper_Deviation_Constraint_{k+1}"
    problem += (b * X[k] + a) - Y[k] <= d, f"Lower_Deviation_Constraint_{k+1}"

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

