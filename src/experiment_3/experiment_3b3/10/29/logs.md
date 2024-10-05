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

Given a set of observed values \(y_k\) and corresponding \(x_k\) values for \(k = 1, \ldots, K\), the objective is to fit a straight line \(y = bx + a\) such that the maximum deviation from the observed values is minimized.

\subsection*{Model Parameters}
Let:
\begin{itemize}
    \item \(y_k\) be the observed value at \(k\)-th observation, where \(k = 1, \ldots, K\)
    \item \(x_k\) be the corresponding value at \(k\)-th observation
    \item \(a\) be the intercept of the line
    \item \(b\) be the slope of the line
    \item \(d_k\) be the deviation for the \(k\)-th observation
\end{itemize}

\subsection*{Objective Function}
Minimize the maximum deviation:
\[
\min \max_{k=1, \ldots, K} d_k
\]

\subsection*{Deviations}
The deviation \(d_k\) is defined as:
\[
d_k \geq y_k - (bx_k + a) \quad \forall k
\]
\[
d_k \geq -(y_k - (bx_k + a)) \quad \forall k
\]

\subsection*{Linear Programming Formulation}
The linear programming model can thus be formulated as:

\textbf{Minimize:}
\[
D
\]

\textbf{Subject to:}
\begin{align*}
    d_k & \geq y_k - (bx_k + a) \quad \forall k = 1, \ldots, K \\
    d_k & \geq -(y_k - (bx_k + a)) \quad \forall k = 1, \ldots, K \\
    d_k & \leq D \quad \forall k = 1, \ldots, K
\end{align*}

\textbf{Variables:}
\begin{itemize}
    \item \(D\) - maximum deviation
    \item \(a\) - intercept
    \item \(b\) - slope
    \item \(d_k\) - deviation for each observation
\end{itemize}

\subsection*{Output}
The output of the model will provide:
\begin{itemize}
    \item \textbf{Intercept:} \(a\)
    \item \textbf{Slope:} \(b\)
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

Given a set of observed values \(y_k\) and corresponding \(x_k\) values for \(k = 1, \ldots, K\), the objective is to fit a straight line \(y = bx + a\) such that the maximum deviation from the observed values is minimized.

\subsection*{Model Parameters}
Let:
\begin{itemize}
    \item \(y_k\) be the observed value at \(k\)-th observation, where \(k = 1, \ldots, K\)
    \item \(x_k\) be the corresponding value at \(k\)-th observation
    \item \(a\) be the intercept of the line
    \item \(b\) be the slope of the line
    \item \(d_k\) be the deviation for the \(k\)-th observation
\end{itemize}

\subsection*{Objective Function}
Minimize the maximum deviation:
\[
\min \max_{k=1, \ldots, K} d_k
\]

\subsection*{Deviations}
The deviation \(d_k\) is defined as:
\[
d_k \geq y_k - (bx_k + a) \quad \forall k
\]
\[
d_k \geq -(y_k - (bx_k + a)) \quad \forall k
\]

\subsection*{Linear Programming Formulation}
The linear programming model can thus be formulated as:

\textbf{Minimize:}
\[
D
\]

\textbf{Subject to:}
\begin{align*}
    d_k & \geq y_k - (bx_k + a) \quad \forall k = 1, \ldots, K \\
    d_k & \geq -(y_k - (bx_k + a)) \quad \forall k = 1, \ldots, K \\
    d_k & \leq D \quad \forall k = 1, \ldots, K
\end{align*}

\textbf{Variables:}
\begin{itemize}
    \item \(D\) - maximum deviation
    \item \(a\) - intercept
    \item \(b\) - slope
    \item \(d_k\) - deviation for each observation
\end{itemize}

\subsection*{Output}
The output of the model will provide:
\begin{itemize}
    \item \textbf{Intercept:} \(a\)
    \item \textbf{Slope:} \(b\)
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

#### Parameters
K = data['NumObs']
Y = data['Y']
X = data['X']

#### Problem
problem = pulp.LpProblem('LinearRegressionMinMaxDeviation', pulp.LpMinimize)

#### Variables
a = pulp.LpVariable('Intercept', lowBound=None, upBound=None, cat='Continuous')
b = pulp.LpVariable('Slope', lowBound=None, upBound=None, cat='Continuous')
D = pulp.LpVariable('MaxDeviation', lowBound=0, cat='Continuous')
d = [pulp.LpVariable(f'Deviation_{k}', lowBound=0, cat='Continuous') for k in range(K)]

#### Objective
problem += D, "Minimize_Maximum_Deviation"

#### Constraints
for k in range(K):
    #### d_k >= y_k - (bx_k + a)
    problem += d[k] >= Y[k] - (b * X[k] + a), f"Deviation_Pos_{k}"
    #### d_k >= -(y_k - (bx_k + a))
    problem += d[k] >= -(Y[k] - (b * X[k] + a)), f"Deviation_Neg_{k}"
    #### d_k <= D
    problem += d[k] <= D, f"Max_Deviation_{k}"

#### Solve
problem.solve()

#### Output
print(f"Intercept (a): {pulp.value(a)}")
print(f"Slope (b): {pulp.value(b)}")
print(f"(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")
```

