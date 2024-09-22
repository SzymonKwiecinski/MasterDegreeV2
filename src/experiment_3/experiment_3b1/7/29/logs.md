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

\section*{Linear Programming Model for Best-Fit Line}

Let us define our model for fitting the best straight line \( y = bx + a \) to the given datasets \((x_k, y_k)\) for \( k = 1, 2, \ldots, K \).

\subsection*{Variables}
\begin{align*}
a & \quad \text{(intercept)} \\
b & \quad \text{(slope)} \\
d_k & \quad \text{(deviation for each observation)} \quad \text{for } k = 1, \ldots, K
\end{align*}

\subsection*{Objective}
We want to minimize the maximum deviation between the observed values \( y_k \) and the predicted values \( \hat{y}_k = bx_k + a \). Our objective can be formulated as:
\[
\text{Minimize } D
\]
where
\[
D \geq |y_k - (bx_k + a)| \quad \text{for } k = 1, 2, \ldots, K
\]

\subsection*{Constraints}
The constraints for our model can be expressed as:
\[
y_k - (bx_k + a) \leq D \quad \text{for } k = 1, \ldots, K
\]
\[
-(y_k - (bx_k + a)) \leq D \quad \text{for } k = 1, \ldots, K
\]

\subsection*{Complete Model}
Putting everything together, the complete linear programming model is:

\[
\text{Minimize } D
\]

Subject to:
\[
y_k - (bx_k + a) \leq D, \quad k = 1, 2, \ldots, K
\]
\[
-(y_k - (bx_k + a)) \leq D, \quad k = 1, 2, \ldots, K
\]

\subsection*{Output Variables}
After solving the above linear programming model, the output will be:
\[
\text{Output: } 
\begin{cases}
\text{intercept} = a \\
\text{slope} = b
\end{cases}
\]

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

\section*{Linear Programming Model for Best-Fit Line}

Let us define our model for fitting the best straight line \( y = bx + a \) to the given datasets \((x_k, y_k)\) for \( k = 1, 2, \ldots, K \).

\subsection*{Variables}
\begin{align*}
a & \quad \text{(intercept)} \\
b & \quad \text{(slope)} \\
d_k & \quad \text{(deviation for each observation)} \quad \text{for } k = 1, \ldots, K
\end{align*}

\subsection*{Objective}
We want to minimize the maximum deviation between the observed values \( y_k \) and the predicted values \( \hat{y}_k = bx_k + a \). Our objective can be formulated as:
\[
\text{Minimize } D
\]
where
\[
D \geq |y_k - (bx_k + a)| \quad \text{for } k = 1, 2, \ldots, K
\]

\subsection*{Constraints}
The constraints for our model can be expressed as:
\[
y_k - (bx_k + a) \leq D \quad \text{for } k = 1, \ldots, K
\]
\[
-(y_k - (bx_k + a)) \leq D \quad \text{for } k = 1, \ldots, K
\]

\subsection*{Complete Model}
Putting everything together, the complete linear programming model is:

\[
\text{Minimize } D
\]

Subject to:
\[
y_k - (bx_k + a) \leq D, \quad k = 1, 2, \ldots, K
\]
\[
-(y_k - (bx_k + a)) \leq D, \quad k = 1, 2, \ldots, K
\]

\subsection*{Output Variables}
After solving the above linear programming model, the output will be:
\[
\text{Output: } 
\begin{cases}
\text{intercept} = a \\
\text{slope} = b
\end{cases}
\]

\end{document}</MATH_MODEL>
<DATA>
{'NumObs': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Given data
data_json = """{'NumObs': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}"""
data = json.loads(data_json.replace("'", '"'))

#### Model setup
num_obs = data['NumObs']
Y = data['Y']
X = data['X']

#### Define the problem
problem = pulp.LpProblem("Best_Fit_Line", pulp.LpMinimize)

#### Variables
a = pulp.LpVariable("a", cat="Continuous")
b = pulp.LpVariable("b", cat="Continuous")
D = pulp.LpVariable("D", lowBound=0, cat="Continuous")  #### D is non-negative

#### Constraints
for k in range(num_obs):
    problem += Y[k] - (b * X[k] + a) <= D
    problem += -(Y[k] - (b * X[k] + a)) <= D

#### Objective
problem += D

#### Solve the problem
problem.solve()

#### Output results
print(f'Intercept (a): {a.varValue}, Slope (b): {b.varValue}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

