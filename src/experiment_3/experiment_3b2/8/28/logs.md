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
To solve this problem, we need to fit a linear model to the data points such that the sum of the absolute deviations of the observed values from the predicted values is minimized. This is a typical Linear Programming problem that can be formulated as follows:

Let:
- \( y_k \) be the observed values.
- \( x_k \) be the predictor values.
- \( a \) be the intercept of the line.
- \( b \) be the slope of the line.
- \( e_k \) be the absolute error for each data point \( k \).

The objective is to minimize the sum of absolute deviations, which can be expressed as:

\[
\min \sum_{k=1}^{K} e_k
\]

Subject to the constraints:
\[
y_k - (bx_k + a) \leq e_k, \quad \forall k = 1, \ldots, K
\]
\[
-(y_k - (bx_k + a)) \leq e_k, \quad \forall k = 1, \ldots, K
\]

This ensures that \( e_k \) is the absolute deviation for each observation.

Here is the LaTeX code for the mathematical model:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Formulation}

Given:
\begin{itemize}
    \item Observed values \( y_k \) for \( k = 1, \ldots, K \)
    \item Predictor values \( x_k \) for \( k = 1, \ldots, K \)
\end{itemize}

Objective:
\[
\min \sum_{k=1}^{K} e_k
\]

Subject to:
\begin{align*}
    y_k - (bx_k + a) & \leq e_k, \quad \forall k = 1, \ldots, K \\
    -(y_k - (bx_k + a)) & \leq e_k, \quad \forall k = 1, \ldots, K
\end{align*}

Where:
\begin{itemize}
    \item \( a \) is the intercept
    \item \( b \) is the slope
    \item \( e_k \) is the absolute deviation for each \( k \)
\end{itemize}

Output:
\begin{itemize}
    \item \texttt{intercept}: \texttt{a}
    \item \texttt{slope}: \texttt{b}
\end{itemize}

\end{document}
```

The solution to this linear programming problem will provide the best fitting line in terms of minimizing the sum of the absolute deviations from the observed data points.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Formulation}

Given:
\begin{itemize}
    \item Observed values \( y_k \) for \( k = 1, \ldots, K \)
    \item Predictor values \( x_k \) for \( k = 1, \ldots, K \)
\end{itemize}

Objective:
\[
\min \sum_{k=1}^{K} e_k
\]

Subject to:
\begin{align*}
    y_k - (bx_k + a) & \leq e_k, \quad \forall k = 1, \ldots, K \\
    -(y_k - (bx_k + a)) & \leq e_k, \quad \forall k = 1, \ldots, K
\end{align*}

Where:
\begin{itemize}
    \item \( a \) is the intercept
    \item \( b \) is the slope
    \item \( e_k \) is the absolute deviation for each \( k \)
\end{itemize}

Output:
\begin{itemize}
    \item \texttt{intercept}: \texttt{a}
    \item \texttt{slope}: \texttt{b}
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'K': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data input
data = json.loads('{"K": 19, "Y": [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], "X": [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}')
K = data['K']
Y = data['Y']
X = data['X']

#### Problem definition
problem = pulp.LpProblem("Linear_Programming_Problem", pulp.LpMinimize)

#### Variables
a = pulp.LpVariable('a', lowBound=None)  #### intercept
b = pulp.LpVariable('b', lowBound=None)  #### slope
e = [pulp.LpVariable(f'e_{k}', lowBound=0) for k in range(K)]  #### absolute deviations

#### Objective function
problem += pulp.lpSum(e), "Total_Absolute_Deviation"

#### Constraints
for k in range(K):
    problem += Y[k] - (b * X[k] + a) <= e[k], f"Upper_Bound_Constraint_{k}"
    problem += -(Y[k] - (b * X[k] + a)) <= e[k], f"Lower_Bound_Constraint_{k}"

#### Solve the problem
problem.solve()

#### Output results
intercept = a.varValue
slope = b.varValue
print(f'Intercept: {intercept}, Slope: {slope}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

