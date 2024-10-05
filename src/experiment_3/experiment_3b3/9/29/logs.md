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

Given a set of observed values \( (x_k, y_k) \) for \( k = 1, 2, \ldots, K \), we want to fit the best straight line \( y = bx + a \) by minimizing the maximum deviation of the observed values \( y_k \) from the predicted values \( \hat{y}_k = bx_k + a \).

\subsection*{Variables}
Let:
\begin{itemize}
    \item \( a \) be the intercept of the fitted line.
    \item \( b \) be the slope of the fitted line.
    \item \( d_k \) be the deviation for each observation \( k \), defined as \( d_k = y_k - (bx_k + a) \).
\end{itemize}

\subsection*{Objective Function}
We want to minimize the maximum deviation:
\[
\text{Minimize } D
\]
subject to:
\[
d_k \leq D \quad \forall k
\]
\[
-d_k \leq D \quad \forall k
\]

\subsection*{Constraints}
The deviations are defined as:
\[
d_k = y_k - (bx_k + a) \quad \forall k
\]

This leads to the following set of linear constraints:
\[
y_k - bx_k - a \leq D \quad \forall k
\]
\[
-bx_k - a + y_k \leq D \quad \forall k
\]

\subsection*{Final Model}
The complete linear programming model can be summarized as follows:

\begin{align*}
\text{Minimize} \quad & D \\
\text{subject to} \quad & y_k - bx_k - a \leq D, \quad \forall k \\
& -bx_k - a + y_k \leq D, \quad \forall k \\
& D \geq 0 \\
& a \in \mathbb{R}, \quad b \in \mathbb{R}, \quad D \in \mathbb{R}
\end{align*}

\subsection*{Output}
The output of this model will yield:
\begin{itemize}
    \item \( \text{intercept} = a \)
    \item \( \text{slope} = b \)
\end{itemize}

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

Given a set of observed values \( (x_k, y_k) \) for \( k = 1, 2, \ldots, K \), we want to fit the best straight line \( y = bx + a \) by minimizing the maximum deviation of the observed values \( y_k \) from the predicted values \( \hat{y}_k = bx_k + a \).

\subsection*{Variables}
Let:
\begin{itemize}
    \item \( a \) be the intercept of the fitted line.
    \item \( b \) be the slope of the fitted line.
    \item \( d_k \) be the deviation for each observation \( k \), defined as \( d_k = y_k - (bx_k + a) \).
\end{itemize}

\subsection*{Objective Function}
We want to minimize the maximum deviation:
\[
\text{Minimize } D
\]
subject to:
\[
d_k \leq D \quad \forall k
\]
\[
-d_k \leq D \quad \forall k
\]

\subsection*{Constraints}
The deviations are defined as:
\[
d_k = y_k - (bx_k + a) \quad \forall k
\]

This leads to the following set of linear constraints:
\[
y_k - bx_k - a \leq D \quad \forall k
\]
\[
-bx_k - a + y_k \leq D \quad \forall k
\]

\subsection*{Final Model}
The complete linear programming model can be summarized as follows:

\begin{align*}
\text{Minimize} \quad & D \\
\text{subject to} \quad & y_k - bx_k - a \leq D, \quad \forall k \\
& -bx_k - a + y_k \leq D, \quad \forall k \\
& D \geq 0 \\
& a \in \mathbb{R}, \quad b \in \mathbb{R}, \quad D \in \mathbb{R}
\end{align*}

\subsection*{Output}
The output of this model will yield:
\begin{itemize}
    \item \( \text{intercept} = a \)
    \item \( \text{slope} = b \)
\end{itemize}

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

#### Define the LP problem
problem = pulp.LpProblem("Linear_Regression_MinMax_Deviation", pulp.LpMinimize)

#### Decision variables
a = pulp.LpVariable('a', lowBound=None)  #### Intercept
b = pulp.LpVariable('b', lowBound=None)  #### Slope
D = pulp.LpVariable('D', lowBound=0)     #### Maximum deviation

#### Objective function
problem += D, "Minimize_Max_Deviation"

#### Constraints
for k in range(data['NumObs']):
    y_k = data['Y'][k]
    x_k = data['X'][k]
    #### Constraints for each observation
    problem += y_k - b * x_k - a <= D, f"Pos_Deviation_{k}"
    problem += -b * x_k - a + y_k <= D, f"Neg_Deviation_{k}"

#### Solve the problem
problem.solve()

#### Results
print(f'Intercept (a): {pulp.value(a)}')
print(f'Slope (b): {pulp.value(b)}')
print(f'Maximum Deviation (D): {pulp.value(D)}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

