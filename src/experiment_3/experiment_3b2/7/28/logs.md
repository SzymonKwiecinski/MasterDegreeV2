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
To formulate this problem as a linear programming model, we need to minimize the sum of absolute deviations between the observed values and the predicted values on the line \( y = bx + a \). This can be set up by introducing auxiliary variables to represent the absolute deviations and then minimizing their sum.

**Linear Programming Model:**

Let:
- \( a \) be the intercept of the line.
- \( b \) be the slope of the line.
- \( e_k \) be the absolute deviation for each data point \( k \).

Objective:
Minimize the sum of absolute deviations \(\sum_{k=1}^{K} e_k\).

Subject to:
For each data point \( k \):
- \( e_k \geq y_k - (bx_k + a) \)
- \( e_k \geq -(y_k - (bx_k + a)) \)
- \( e_k \geq 0 \)

Here is the corresponding LaTeX representation of the linear programming formulation:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Linear Programming Model:}

\text{Let:}
\begin{itemize}
    \item \( a \) be the intercept of the line.
    \item \( b \) be the slope of the line.
    \item \( e_k \) be the absolute deviation for each data point \( k \).
\end{itemize}

\text{Objective:}
\[
\min \sum_{k=1}^{K} e_k
\]

\text{Subject to:}
\[
e_k \geq y_k - (bx_k + a), \quad \forall k = 1, \ldots, K
\]
\[
e_k \geq -(y_k - (bx_k + a)), \quad \forall k = 1, \ldots, K
\]
\[
e_k \geq 0, \quad \forall k = 1, \ldots, K
\]

\end{document}
```

This setup ensures that for each data point, the absolute deviation from the predicted line is captured and minimized collectively across all points. Solving this linear programming problem will yield the values of \( a \) (intercept) and \( b \) (slope) that define the best fit line minimizing the absolute deviations.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Linear Programming Model:}

\text{Let:}
\begin{itemize}
    \item \( a \) be the intercept of the line.
    \item \( b \) be the slope of the line.
    \item \( e_k \) be the absolute deviation for each data point \( k \).
\end{itemize}

\text{Objective:}
\[
\min \sum_{k=1}^{K} e_k
\]

\text{Subject to:}
\[
e_k \geq y_k - (bx_k + a), \quad \forall k = 1, \ldots, K
\]
\[
e_k \geq -(y_k - (bx_k + a)), \quad \forall k = 1, \ldots, K
\]
\[
e_k \geq 0, \quad \forall k = 1, \ldots, K
\]

\end{document}</MATH_MODEL>
<DATA>
{'K': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data from JSON format
data = json.loads('{"K": 19, "Y": [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], "X": [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}')

K = data['K']
Y = data['Y']
X = data['X']

#### Create the problem variable
problem = pulp.LpProblem("Minimize_Absolute_Deviation", pulp.LpMinimize)

#### Define variables
a = pulp.LpVariable("a", lowBound=None)
b = pulp.LpVariable("b", lowBound=None)
e = [pulp.LpVariable(f"e_{k}", lowBound=0) for k in range(K)]

#### Objective Function: Minimize the sum of e_k
problem += pulp.lpSum(e), "Objective"

#### Constraints
for k in range(K):
    problem += e[k] >= Y[k] - (b * X[k] + a), f"Upper_Deviation_Constraint_{k}"
    problem += e[k] >= -(Y[k] - (b * X[k] + a)), f"Lower_Deviation_Constraint_{k}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

