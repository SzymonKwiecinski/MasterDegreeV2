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
To construct an appropriate linear programming model to fit the 'best' straight line to the given data while minimizing the maximum deviation from the observed values, we employ the minimax criterion. The model can be expressed as follows:

Objective: Minimize the maximum deviation (let's denote this deviation as `D`). The linear equation to be fitted is \( y = bx + a \), where \( a \) is the intercept and \( b \) is the slope.

Given:
- \( y_k \) and \( x_k \) for \( k = 1, 2, \ldots, K \).

Objective Function and Constraints:
- Minimize \( D \)
- Subject to:
    \[
    -(bx_k + a - y_k) \leq D, \quad k = 1, \ldots, K
    \]
    \[
    bx_k + a - y_k \leq D, \quad k = 1, \ldots, K
    \]

Below is the corresponding LaTeX code for the linear programming:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Best Fit Line}

\begin{align*}
\text{Objective:} \quad & \min D \\
\text{Subject to:} \quad & -(b x_k + a - y_k) \leq D, \quad k = 1, \ldots, K \\
                        & b x_k + a - y_k \leq D, \quad k = 1, \ldots, K \\
\end{align*}

Where:
\begin{itemize}
    \item \( a \) is the intercept of the line,
    \item \( b \) is the slope of the line,
    \item \( D \) is the maximum deviation to be minimized.
\end{itemize}

\end{document}
```

The above constraints ensure that the absolute deviation between the observed values and the values predicted by the line is kept within a minimized maximum bound `D`. Solving this LP will give the values for `a` (intercept) and `b` (slope).

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

\begin{align*}
\text{Objective:} \quad & \min D \\
\text{Subject to:} \quad & -(b x_k + a - y_k) \leq D, \quad k = 1, \ldots, K \\
                        & b x_k + a - y_k \leq D, \quad k = 1, \ldots, K \\
\end{align*}

Where:
\begin{itemize}
    \item \( a \) is the intercept of the line,
    \item \( b \) is the slope of the line,
    \item \( D \) is the maximum deviation to be minimized.
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'NumObs': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data provided in JSON format
data = json.loads('{"NumObs": 19, "Y": [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], "X": [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}')

#### Number of observations
K = data['NumObs']
Y = data['Y']
X = data['X']

#### Create the linear programming problem
problem = pulp.LpProblem("Best_Fit_Line", pulp.LpMinimize)

#### Variables: slope (b), intercept (a), and the maximum deviation (D)
b = pulp.LpVariable("b", lowBound=None)  #### slope
a = pulp.LpVariable("a", lowBound=None)  #### intercept
D = pulp.LpVariable("D", lowBound=0)     #### maximum deviation

#### Objective function: minimize D
problem += D, "Minimize_Max_Deviation"

#### Constraints for the model
for k in range(K):
    problem += -(b * X[k] + a - Y[k]) <= D, f"Lower_Bound_Constraint_{k}"
    problem += (b * X[k] + a - Y[k]) <= D, f"Upper_Bound_Constraint_{k}"

#### Solve the problem
problem.solve()

#### Output the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

