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
To formulate this problem as a linear programming model, we need to minimize the maximum deviation between observed and predicted values based on the linear relationship \( y = bx + a \).

Objective Function:
- Minimize the maximum deviation \( d \).

Constraints:
- For each given pair \((x_k, y_k)\), the absolute deviation between the observed \( y_k \) and the predicted value \( bx_k + a \) should not exceed \( d \).

Let's define the constraints for each data point \((x_k, y_k)\):
- \( y_k - (bx_k + a) \leq d \)
- \( (bx_k + a) - y_k \leq d \)

In these constraints, \( b \) is the slope, \( a \) is the intercept, and \( d \) is the variable we are minimizing.

Here's how the formulation looks in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

\textbf{Objective:}
\[
\min \, d
\]

\textbf{Subject to:}
\[
y_k - (bx_k + a) \leq d, \quad k = 1, 2, \ldots, K
\]
\[
(bx_k + a) - y_k \leq d, \quad k = 1, 2, \ldots, K
\]

\textbf{Variables:}
\[
a \, (\text{intercept}), \quad b \, (\text{slope}), \quad d \, (\text{maximum deviation})
\]

\end{document}
```

This mathematical formulation can be solved using linear programming techniques to find the values of \( a \) and \( b \) that minimize the maximum deviation \( d \).

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

\textbf{Objective:}
\[
\min \, d
\]

\textbf{Subject to:}
\[
y_k - (bx_k + a) \leq d, \quad k = 1, 2, \ldots, K
\]
\[
(bx_k + a) - y_k \leq d, \quad k = 1, 2, \ldots, K
\]

\textbf{Variables:}
\[
a \, (\text{intercept}), \quad b \, (\text{slope}), \quad d \, (\text{maximum deviation})
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

#### Number of observations
K = data['NumObs']

#### Create the Linear Programming problem
problem = pulp.LpProblem("Minimize_Maximum_Deviation", pulp.LpMinimize)

#### Variables
a = pulp.LpVariable('a', lowBound=None, upBound=None, cat='Continuous')
b = pulp.LpVariable('b', lowBound=None, upBound=None, cat='Continuous')
d = pulp.LpVariable('d', lowBound=0, upBound=None, cat='Continuous')

#### Objective function
problem += d

#### Constraints
for k in range(K):
    x_k = data['X'][k]
    y_k = data['Y'][k]
    problem += y_k - (b * x_k + a) <= d
    problem += (b * x_k + a) - y_k <= d

#### Solve the problem
problem.solve()

#### Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

