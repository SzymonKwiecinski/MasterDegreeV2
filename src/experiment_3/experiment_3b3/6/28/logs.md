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
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Best Fit Line}

Let \( y_k \) be the observed value for the \( k \)-th data point and \( x_k \) be the corresponding value for the \( k \)-th data point, where \( k = 1, \ldots, K \). We aim to fit a linear equation of the form:

\[
y = bx + a
\]

where \( a \) is the intercept and \( b \) is the slope of the line. We want to minimize the sum of absolute deviations between the observed values \( y_k \) and the predicted values \( bx_k + a \).

\subsection*{Objective Function}

We need to minimize the total absolute deviation:

\[
\text{Minimize} \quad \sum_{k=1}^{K} |y_k - (bx_k + a)|
\]

To handle the absolute values, we introduce auxiliary variables \( e_k \) such that:

\[
e_k \geq y_k - (bx_k + a) \quad \text{and} \quad e_k \geq -(y_k - (bx_k + a))
\]

This translates our objective into a linear programming format as follows:

\[
\text{Minimize} \quad \sum_{k=1}^{K} e_k
\]

\subsection*{Constraints}

The model includes the following constraints:

\[
e_k \geq y_k - (bx_k + a), \quad \forall k = 1, \ldots, K
\]

\[
e_k \geq -(y_k - (bx_k + a)), \quad \forall k = 1, \ldots, K
\]

\subsection*{Variables}

The decision variables are:

- \( a \): intercept of the fitted line
- \( b \): slope of the fitted line
- \( e_k \): absolute deviations for each data point

\subsection*{Output}

After solving the linear programming problem, the outputs are:

\begin{itemize}
    \item "intercept": \( a \)
    \item "slope": \( b \)
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

\section*{Linear Programming Model for Best Fit Line}

Let \( y_k \) be the observed value for the \( k \)-th data point and \( x_k \) be the corresponding value for the \( k \)-th data point, where \( k = 1, \ldots, K \). We aim to fit a linear equation of the form:

\[
y = bx + a
\]

where \( a \) is the intercept and \( b \) is the slope of the line. We want to minimize the sum of absolute deviations between the observed values \( y_k \) and the predicted values \( bx_k + a \).

\subsection*{Objective Function}

We need to minimize the total absolute deviation:

\[
\text{Minimize} \quad \sum_{k=1}^{K} |y_k - (bx_k + a)|
\]

To handle the absolute values, we introduce auxiliary variables \( e_k \) such that:

\[
e_k \geq y_k - (bx_k + a) \quad \text{and} \quad e_k \geq -(y_k - (bx_k + a))
\]

This translates our objective into a linear programming format as follows:

\[
\text{Minimize} \quad \sum_{k=1}^{K} e_k
\]

\subsection*{Constraints}

The model includes the following constraints:

\[
e_k \geq y_k - (bx_k + a), \quad \forall k = 1, \ldots, K
\]

\[
e_k \geq -(y_k - (bx_k + a)), \quad \forall k = 1, \ldots, K
\]

\subsection*{Variables}

The decision variables are:

- \( a \): intercept of the fitted line
- \( b \): slope of the fitted line
- \( e_k \): absolute deviations for each data point

\subsection*{Output}

After solving the linear programming problem, the outputs are:

\begin{itemize}
    \item "intercept": \( a \)
    \item "slope": \( b \)
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'K': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
data = {'K': 19, 
        'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 
        'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}

K = data['K']
Y = data['Y']
X = data['X']

#### Problem
problem = pulp.LpProblem("Best_Fit_Line", pulp.LpMinimize)

#### Decision Variables
a = pulp.LpVariable('Intercept', lowBound=None, upBound=None, cat='Continuous')
b = pulp.LpVariable('Slope', lowBound=None, upBound=None, cat='Continuous')
e = [pulp.LpVariable(f'e_{k}', lowBound=0, cat='Continuous') for k in range(K)]

#### Objective Function
problem += pulp.lpSum(e), "Minimize_Sum_of_Absolute_Deviations"

#### Constraints
for k in range(K):
    problem += e[k] >= Y[k] - (b * X[k] + a), f"Constraint_positive_deviation_{k}"
    problem += e[k] >= -(Y[k] - (b * X[k] + a)), f"Constraint_negative_deviation_{k}"

#### Solve the problem
problem.solve()

#### Output
intercept = pulp.value(a)
slope = pulp.value(b)

print(f"Intercept: {intercept}, Slope: {slope} (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")
```

