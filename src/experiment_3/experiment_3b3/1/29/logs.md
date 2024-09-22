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

We want to fit a straight line of the form:
\[
y = bx + a
\]
where \(a\) is the intercept and \(b\) is the slope. The objective is to minimize the maximum deviation of the observed values of \(y\) from the values predicted by the linear relationship. 

Let:
\[
\text{Deviation}_{k} = y_{k} - (bx_{k} + a)
\]
for \(k = 1, \ldots, K\).

To formulate this as a linear programming problem, we introduce a variable \(M\) to represent the maximum deviation. The linear programming model can be expressed as follows:

\subsection*{Objective Function}
Minimize \(M\)

\subsection*{Subject to}
\[
y_{k} - (bx_{k} + a) \leq M \quad \forall k = 1, \ldots, K
\]
\[
-(y_{k} - (bx_{k} + a)) \leq M \quad \forall k = 1, \ldots, K
\]

\subsection*{Variable Constraints}
\[
a \in \mathbb{R}, \quad b \in \mathbb{R}, \quad M \geq 0
\]

\subsection*{Output}
The output of the model will provide the best fitted line parameters:
\begin{itemize}
    \item Intercept: \(a\)
    \item Slope: \(b\)
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

\section*{Linear Programming Model for Line Fitting}

We want to fit a straight line of the form:
\[
y = bx + a
\]
where \(a\) is the intercept and \(b\) is the slope. The objective is to minimize the maximum deviation of the observed values of \(y\) from the values predicted by the linear relationship. 

Let:
\[
\text{Deviation}_{k} = y_{k} - (bx_{k} + a)
\]
for \(k = 1, \ldots, K\).

To formulate this as a linear programming problem, we introduce a variable \(M\) to represent the maximum deviation. The linear programming model can be expressed as follows:

\subsection*{Objective Function}
Minimize \(M\)

\subsection*{Subject to}
\[
y_{k} - (bx_{k} + a) \leq M \quad \forall k = 1, \ldots, K
\]
\[
-(y_{k} - (bx_{k} + a)) \leq M \quad \forall k = 1, \ldots, K
\]

\subsection*{Variable Constraints}
\[
a \in \mathbb{R}, \quad b \in \mathbb{R}, \quad M \geq 0
\]

\subsection*{Output}
The output of the model will provide the best fitted line parameters:
\begin{itemize}
    \item Intercept: \(a\)
    \item Slope: \(b\)
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'NumObs': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from the problem
data = {
    'NumObs': 19,
    'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3],
    'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]
}

#### Create a Linear Programming problem
problem = pulp.LpProblem("Line_Fitting", pulp.LpMinimize)

#### Decision Variables
a = pulp.LpVariable('a', lowBound=None, upBound=None, cat='Continuous')
b = pulp.LpVariable('b', lowBound=None, upBound=None, cat='Continuous')
M = pulp.LpVariable('M', lowBound=0, upBound=None, cat='Continuous')

#### Objective Function
problem += M, "Minimize_Maximum_Deviation"

#### Constraints
for k in range(data['NumObs']):
    y_k = data['Y'][k]
    x_k = data['X'][k]
    #### y_k - (b * x_k + a) <= M
    problem += y_k - (b * x_k + a) <= M, f"Upper_Deviation_Constraint_{k}"
    #### -(y_k - (b * x_k + a)) <= M
    problem += -(y_k - (b * x_k + a)) <= M, f"Lower_Deviation_Constraint_{k}"

#### Solve the problem
problem.solve()

#### Results
print(f'Intercept (a): {pulp.value(a)}')
print(f'Slope (b): {pulp.value(b)}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

