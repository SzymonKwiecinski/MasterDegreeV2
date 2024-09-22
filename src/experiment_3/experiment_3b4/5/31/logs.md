# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: MIP
PROBLEM INFO:

- A number of power stations are committed to meeting the following electricity load demands over a day.
- Period \var{t} of a day has demand \var{demand_{t}}.
- There are several types of generating unit available: the number of \var{k}-th type units is \var{num_{k}}.
- Type \var{k} generator has to work between a minimum level \var{minlevel_{k}} and a maximum level \var{maxlevel_{k}}. 
- There is an hourly cost of running each type \var{k} generator at minimum level \var{runcost_{k}}. 
- In addition, there is an extra hourly cost \var{extracost_{k}} for each megawatt at which a type \var{k} unit is operated above the minimum level. 
- Starting up a type \var{k} generator also involves a cost \var{startcost_{k}}.


INPUT FORMAT:

{
    "demand": [demand_{t} for t in 1,...,T],
    "num": [num_{k} for in 1,...,K],
    "minlevel": [minlevel_{k} for in 1,...,K],
    "maxlevel": [minlevel_{k} for in 1,...,K],
    "runcost": [runcost_{k} for in 1,...,K],
    "extracost": [extracost_{k} for in 1,...,K],
    "startcost": [startcost_{k} for in 1,...,K]
}


OBJECTIVE: Which generators should be working in which periods of the day to minimize total cost?

OUTPUT INFO:

- \var{numon} represents the number of generators of each type that are on in each period

OUTPUT FORMAT:

{
    "numon": [[numon_{k, t} for t in 1,...,T] for k in 1,...,K]
}
</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
To formulate this problem as a Mixed Integer Programming (MIP) model, we will define binary variables to determine which generators are turned on during each period, as well as continuous variables for the power they produce.

Let's define the decision variables:
- \( x_{k,t} \): The number of type \( k \) generators that are running in period \( t \).
- \( y_{k,t} \): 1 if at least one generator of type \( k \) is started up in period \( t \), 0 otherwise.
- \( p_{k,t} \): The power output above the minimum level for generators of type \( k \) in period \( t \).

The objective is to minimize the total cost, including running costs, extra costs for additional power, and start-up costs.

Here is the mathematical model in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Mathematical Model}

\subsection*{Parameters}
\begin{align*}
T & : \text{Number of periods} \\
K & : \text{Number of generator types} \\
\text{demand}_t & : \text{Electricity demand in period } t \\
\text{num}_k & : \text{Number of generators of type } k \\
\text{minlevel}_k & : \text{Minimum power output of type } k \text{ generator} \\
\text{maxlevel}_k & : \text{Maximum power output of type } k \text{ generator} \\
\text{runcost}_k & : \text{Hourly cost of running a type } k \text{ generator at minimum level} \\
\text{extracost}_k & : \text{Extra hourly cost per MW above minimum for type } k \text{ generator} \\
\text{startcost}_k & : \text{Cost to start up a type } k \text{ generator}
\end{align*}

\subsection*{Decision Variables}
\begin{align*}
x_{k, t} & : \text{Number of type } k \text{ generators running in period } t \\
y_{k, t} & : \begin{cases} 
1, & \text{if at least one generator of type } k \text{ is started in period } t \\
0, & \text{otherwise}
\end{cases} \\
p_{k, t} & : \text{Power output above minimum level for type } k \text{ in period } t
\end{align*}

\subsection*{Objective Function}
Minimize the total cost:
\[
\sum_{t=1}^{T} \sum_{k=1}^{K} \left( x_{k, t} \cdot \text{runcost}_k + p_{k, t} \cdot \text{extracost}_k + y_{k, t} \cdot \text{startcost}_k \right)
\]

\subsection*{Constraints}
\begin{align}
\sum_{k=1}^{K} \left( x_{k, t} \cdot \text{minlevel}_k + p_{k, t} \right) & \geq \text{demand}_t, & \forall t = 1,\ldots,T \\
0 \leq p_{k,t} & \leq (x_{k,t} \cdot (\text{maxlevel}_k - \text{minlevel}_k)), & \forall k = 1,\ldots,K, \forall t = 1,\ldots,T \\
0 \leq x_{k,t} & \leq \text{num}_k, & \forall k = 1,\ldots,K, \forall t = 1,\ldots,T \\
y_{k,t} & \geq x_{k,t} - x_{k,t-1}, & \forall k = 1,\ldots,K, \forall t = 1,\ldots,T
\end{align}

\end{document}
```

This model accounts for the minimum generation levels of each type of generator, their maximum output capability, and the costs associated with starting and running generators above their minimum output levels. The constraints ensure that demand is met in each period, and that the number of generators on is constrained by the available number. A change from off to on is captured by the \( y_{k,t} \) variables, which incurs the start-up cost.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Mathematical Model}

\subsection*{Parameters}
\begin{align*}
T & : \text{Number of periods} \\
K & : \text{Number of generator types} \\
\text{demand}_t & : \text{Electricity demand in period } t \\
\text{num}_k & : \text{Number of generators of type } k \\
\text{minlevel}_k & : \text{Minimum power output of type } k \text{ generator} \\
\text{maxlevel}_k & : \text{Maximum power output of type } k \text{ generator} \\
\text{runcost}_k & : \text{Hourly cost of running a type } k \text{ generator at minimum level} \\
\text{extracost}_k & : \text{Extra hourly cost per MW above minimum for type } k \text{ generator} \\
\text{startcost}_k & : \text{Cost to start up a type } k \text{ generator}
\end{align*}

\subsection*{Decision Variables}
\begin{align*}
x_{k, t} & : \text{Number of type } k \text{ generators running in period } t \\
y_{k, t} & : \begin{cases} 
1, & \text{if at least one generator of type } k \text{ is started in period } t \\
0, & \text{otherwise}
\end{cases} \\
p_{k, t} & : \text{Power output above minimum level for type } k \text{ in period } t
\end{align*}

\subsection*{Objective Function}
Minimize the total cost:
\[
\sum_{t=1}^{T} \sum_{k=1}^{K} \left( x_{k, t} \cdot \text{runcost}_k + p_{k, t} \cdot \text{extracost}_k + y_{k, t} \cdot \text{startcost}_k \right)
\]

\subsection*{Constraints}
\begin{align}
\sum_{k=1}^{K} \left( x_{k, t} \cdot \text{minlevel}_k + p_{k, t} \right) & \geq \text{demand}_t, & \forall t = 1,\ldots,T \\
0 \leq p_{k,t} & \leq (x_{k,t} \cdot (\text{maxlevel}_k - \text{minlevel}_k)), & \forall k = 1,\ldots,K, \forall t = 1,\ldots,T \\
0 \leq x_{k,t} & \leq \text{num}_k, & \forall k = 1,\ldots,K, \forall t = 1,\ldots,T \\
y_{k,t} & \geq x_{k,t} - x_{k,t-1}, & \forall k = 1,\ldots,K, \forall t = 1,\ldots,T
\end{align}

\end{document}</MATH_MODEL>
<DATA>
{'demand': [15000, 30000, 25000, 40000, 27000], 'num': [12, 10, 5], 'minlevel': [850, 1250, 1500], 'maxlevel': [2000, 1750, 4000], 'runcost': [1000, 2600, 3000], 'extracost': [2.0, 1.3, 3.0], 'startcost': [2000, 1000, 500]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
data = {
    'demand': [15000, 30000, 25000, 40000, 27000],
    'num': [12, 10, 5],
    'minlevel': [850, 1250, 1500],
    'maxlevel': [2000, 1750, 4000],
    'runcost': [1000, 2600, 3000],
    'extracost': [2.0, 1.3, 3.0],
    'startcost': [2000, 1000, 500]
}

T = len(data['demand'])
K = len(data['num'])

#### Initialize the problem
problem = pulp.LpProblem("Generator_Scheduling", pulp.LpMinimize)

#### Decision Variables
x = pulp.LpVariable.dicts("x", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat=pulp.LpInteger)
y = pulp.LpVariable.dicts("y", ((k, t) for k in range(K) for t in range(T)), cat=pulp.LpBinary)
p = pulp.LpVariable.dicts("p", ((k, t) for k in range(K) for t in range(T)), lowBound=0)

#### Objective function
problem += pulp.lpSum(
    x[k, t] * data['runcost'][k] + 
    p[k, t] * data['extracost'][k] + 
    y[k, t] * data['startcost'][k]
    for k in range(K) for t in range(T)
)

#### Constraints
#### Demand satisfaction
for t in range(T):
    problem += pulp.lpSum(x[k, t] * data['minlevel'][k] + p[k, t] for k in range(K)) >= data['demand'][t]

#### Power output limits
for k in range(K):
    for t in range(T):
        problem += p[k, t] <= x[k, t] * (data['maxlevel'][k] - data['minlevel'][k])
        problem += x[k, t] <= data['num'][k]

#### Start-up conditions
for k in range(K):
    for t in range(1, T):
        problem += y[k, t] >= x[k, t] - x[k, t - 1]

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

