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
To fit the best straight line \( y = bx + a \) to the provided data points while minimizing the sum of absolute deviations, we need to formulate this problem as a linear programming problem. We'll introduce auxiliary variables to capture the absolute deviations and minimize their sum.

Here is the mathematical formulation for the problem using Linear Programming. The problem is formulated as:

Minimize:
\[
\sum_{k=1}^{K} |y_k - (bx_k + a)|
\]

This objective can be transformed by introducing auxiliary variables \( z_k \) such that:

\[
z_k \geq y_k - (bx_k + a)
\]
\[
z_k \geq -(y_k - (bx_k + a))
\]

The objective then becomes minimizing:

\[
\sum_{k=1}^{K} z_k
\]

Now, we provide the complete formulation in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\title{Linear Programming Formulation for Fitting a Line}
\author{}
\date{}
\maketitle

Given a set of data points \((x_k, y_k)\) for \(k=1,\ldots,K\), the objective is to fit a line \(y = bx + a\) to these points by minimizing the sum of absolute deviations between observed and predicted values of \(y\).

\section*{Mathematical Model}

\textbf{Objective:}

\[
\min \sum_{k=1}^{K} z_k
\]

\textbf{Subject to:}

For each \(k = 1, \ldots, K\):
\[
z_k \geq y_k - (bx_k + a)
\]
\[
z_k \geq -(y_k - (bx_k + a))
\]

Where:
- \( z_k \) is the auxiliary variable representing the absolute deviation for the \(k\)-th data point.
- \( y_k \) is the observed value.
- \( x_k \) is the corresponding \(x\) value.
- \( a \) is the intercept of the line.
- \( b \) is the slope of the line.

The decision variables are:
- The intercept \(a\)
- The slope \(b\)
- The auxiliary variables \(z_k\) for each \(k\).

\end{document}
```

This formulation will help determine the optimal \(a\) (intercept) and \(b\) (slope) that minimize the total deviation from the observed \(y\) values. The output will be the fitted line's intercept and slope.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\title{Linear Programming Formulation for Fitting a Line}
\author{}
\date{}
\maketitle

Given a set of data points \((x_k, y_k)\) for \(k=1,\ldots,K\), the objective is to fit a line \(y = bx + a\) to these points by minimizing the sum of absolute deviations between observed and predicted values of \(y\).

\section*{Mathematical Model}

\textbf{Objective:}

\[
\min \sum_{k=1}^{K} z_k
\]

\textbf{Subject to:}

For each \(k = 1, \ldots, K\):
\[
z_k \geq y_k - (bx_k + a)
\]
\[
z_k \geq -(y_k - (bx_k + a))
\]

Where:
- \( z_k \) is the auxiliary variable representing the absolute deviation for the \(k\)-th data point.
- \( y_k \) is the observed value.
- \( x_k \) is the corresponding \(x\) value.
- \( a \) is the intercept of the line.
- \( b \) is the slope of the line.

The decision variables are:
- The intercept \(a\)
- The slope \(b\)
- The auxiliary variables \(z_k\) for each \(k\).

\end{document}</MATH_MODEL>
<DATA>
{'K': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Parse the given data
data = {'K': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}

K = data['K']
Y = data['Y']
X = data['X']

#### Define the LP problem
problem = pulp.LpProblem("Line_Fitting", pulp.LpMinimize)

#### Decision variables
a = pulp.LpVariable('a', lowBound=None)
b = pulp.LpVariable('b', lowBound=None)
z = [pulp.LpVariable(f'z_{k}', lowBound=0) for k in range(K)]

#### Objective function
problem += pulp.lpSum(z)

#### Constraints
for k in range(K):
    problem += z[k] >= (Y[k] - (b * X[k] + a))
    problem += z[k] >= -(Y[k] - (b * X[k] + a))

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

