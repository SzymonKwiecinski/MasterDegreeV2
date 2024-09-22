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

\section*{Linear Programming Model for Line Fitting}

Given a set of values \( \{x_k\}_{k=1}^K \) and \( \{y_k\}_{k=1}^K \), the goal is to fit the best straight line defined by the equation 

\[
y = bx + a
\]

such that we minimize the maximum deviation of the observed values \( y_k \) from the predicted values.

\subsection*{Variables}
Let:
- \( a \) be the intercept of the fitted line.
- \( b \) be the slope of the fitted line.
- \( d_k \) be the deviation for each observation defined as \( d_k = y_k - (bx_k + a) \).

\subsection*{Objective Function}
We want to minimize the maximum deviation, which can be formalized as:

\[
\text{Minimize} \quad t
\]

subject to:

\[
d_k \leq t \quad \forall k = 1, \ldots, K
\]
\[
-d_k \leq t \quad \forall k = 1, \ldots, K
\]

This ensures that the absolute value of the deviation \( |d_k| \) does not exceed \( t \).

\subsection*{Constraints}
The deviations can be expressed in terms of \( a \) and \( b \):

\[
d_k = y_k - (bx_k + a) \quad \forall k = 1, \ldots, K
\]

The complete linear programming model can now be structured as follows:

\subsection*{Linear Program}
\begin{align*}
\text{Minimize} & \quad t \\
\text{Subject to} & \quad y_k - (bx_k + a) \leq t \quad \forall k = 1, \ldots, K \\
                  & \quad -(y_k - (bx_k + a)) \leq t \quad \forall k = 1, \ldots, K \\
                  & \quad a \in \mathbb{R}, \quad b \in \mathbb{R}, \quad t \geq 0
\end{align*}

\subsection*{Output}
The result of this linear programming model will yield:
\begin{itemize}
    \item \texttt{intercept} = \( a \)
    \item \texttt{slope} = \( b \)
\end{itemize}

The solution of this model provides the intercept and slope of the best-fit line minimizing the maximum deviation from the observed values.

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

\section*{Linear Programming Model for Line Fitting}

Given a set of values \( \{x_k\}_{k=1}^K \) and \( \{y_k\}_{k=1}^K \), the goal is to fit the best straight line defined by the equation 

\[
y = bx + a
\]

such that we minimize the maximum deviation of the observed values \( y_k \) from the predicted values.

\subsection*{Variables}
Let:
- \( a \) be the intercept of the fitted line.
- \( b \) be the slope of the fitted line.
- \( d_k \) be the deviation for each observation defined as \( d_k = y_k - (bx_k + a) \).

\subsection*{Objective Function}
We want to minimize the maximum deviation, which can be formalized as:

\[
\text{Minimize} \quad t
\]

subject to:

\[
d_k \leq t \quad \forall k = 1, \ldots, K
\]
\[
-d_k \leq t \quad \forall k = 1, \ldots, K
\]

This ensures that the absolute value of the deviation \( |d_k| \) does not exceed \( t \).

\subsection*{Constraints}
The deviations can be expressed in terms of \( a \) and \( b \):

\[
d_k = y_k - (bx_k + a) \quad \forall k = 1, \ldots, K
\]

The complete linear programming model can now be structured as follows:

\subsection*{Linear Program}
\begin{align*}
\text{Minimize} & \quad t \\
\text{Subject to} & \quad y_k - (bx_k + a) \leq t \quad \forall k = 1, \ldots, K \\
                  & \quad -(y_k - (bx_k + a)) \leq t \quad \forall k = 1, \ldots, K \\
                  & \quad a \in \mathbb{R}, \quad b \in \mathbb{R}, \quad t \geq 0
\end{align*}

\subsection*{Output}
The result of this linear programming model will yield:
\begin{itemize}
    \item \texttt{intercept} = \( a \)
    \item \texttt{slope} = \( b \)
\end{itemize}

The solution of this model provides the intercept and slope of the best-fit line minimizing the maximum deviation from the observed values.

\end{document}</MATH_MODEL>
<DATA>
{'NumObs': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Input data
data = json.loads('{"NumObs": 19, "Y": [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], "X": [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}')

#### Extracting data
num_obs = data['NumObs']
Y = data['Y']
X = data['X']

#### Create the linear programming problem
problem = pulp.LpProblem("LineFitting", pulp.LpMinimize)

#### Variables
a = pulp.LpVariable("a", None)
b = pulp.LpVariable("b", None)
t = pulp.LpVariable("t", lowBound=0)

#### Objective function
problem += t

#### Constraints
for k in range(num_obs):
    problem += Y[k] - (b * X[k] + a) <= t
    problem += -(Y[k] - (b * X[k] + a)) <= t

#### Solve the problem
problem.solve()

#### Output results
intercept = a.varValue
slope = b.varValue

print(f'Intercept: {intercept}')
print(f'Slope: {slope}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

