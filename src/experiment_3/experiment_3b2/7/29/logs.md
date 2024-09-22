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
To address this problem, we need to fit a straight line \( y = bx + a \) through the given data points by minimizing the maximum deviation of all observed values from this linear relationship. This is a linear programming problem that can be formulated using the Chebyshev approximation approach.

Here is the mathematical model presented in LaTeX format:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Line Fitting}

\subsection*{Problem Description}
Given a set of data points \((x_k, y_k)\) for \(k = 1, \ldots, K\), the objective is to fit a line \(y = bx + a\) such that the maximum deviation of observed values \(y_k\) from their predicted values on the line is minimized.

\subsection*{Mathematical Formulation}

\textbf{Variables:}
\begin{align*}
a & \text{ - Intercept of the line} \\
b & \text{ - Slope of the line} \\
d & \text{ - Maximum deviation}
\end{align*}

\textbf{Objective Function:}
\[ 
\text{Minimize } d 
\]

\textbf{Subject to Constraints:}
\begin{align*}
y_k - (bx_k + a) & \leq d, \quad \forall k = 1, \ldots, K \\
(bx_k + a) - y_k & \leq d, \quad \forall k = 1, \ldots, K
\end{align*}

This formulation ensures that the maximum deviation \(d\) is minimized for all data points, effectively reducing the maximum error of the observed values from the fitted line.

\end{document}
```

This linear programming model can be solved using any LP solver to obtain the values for \(a\) (intercept) and \(b\) (slope), which will minimize the maximum deviation across all data points.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Line Fitting}

\subsection*{Problem Description}
Given a set of data points \((x_k, y_k)\) for \(k = 1, \ldots, K\), the objective is to fit a line \(y = bx + a\) such that the maximum deviation of observed values \(y_k\) from their predicted values on the line is minimized.

\subsection*{Mathematical Formulation}

\textbf{Variables:}
\begin{align*}
a & \text{ - Intercept of the line} \\
b & \text{ - Slope of the line} \\
d & \text{ - Maximum deviation}
\end{align*}

\textbf{Objective Function:}
\[ 
\text{Minimize } d 
\]

\textbf{Subject to Constraints:}
\begin{align*}
y_k - (bx_k + a) & \leq d, \quad \forall k = 1, \ldots, K \\
(bx_k + a) - y_k & \leq d, \quad \forall k = 1, \ldots, K
\end{align*}

This formulation ensures that the maximum deviation \(d\) is minimized for all data points, effectively reducing the maximum error of the observed values from the fitted line.

\end{document}</MATH_MODEL>
<DATA>
{'NumObs': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from JSON
data = {
    'NumObs': 19,
    'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3],
    'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]
}

#### Number of observations
K = data['NumObs']
Y = data['Y']
X = data['X']

#### Create a linear programming problem
problem = pulp.LpProblem("LineFitting", pulp.LpMinimize)

#### Variables
a = pulp.LpVariable("Intercept", lowBound=None)
b = pulp.LpVariable("Slope", lowBound=None)
d = pulp.LpVariable("MaxDeviation", lowBound=0)

#### Objective Function
problem += d, "MinimizeMaxDeviation"

#### Constraints
for k in range(K):
    problem += Y[k] - (b * X[k] + a) <= d, f"UpperBoundConstraint_{k+1}"
    problem += (b * X[k] + a) - Y[k] <= d, f"LowerBoundConstraint_{k+1}"

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

