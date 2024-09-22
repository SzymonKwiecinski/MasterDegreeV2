# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP

PROBLEM INFO: 

- Consider a rocket that travels along a straight path. 
- Let \var{x_t}, \var{v_t}, and \var{a_t} be the position, velocity, and acceleration, respectively, of the rocket at time \var{t}.
- By discretizing time and by taking the time increment to be unity, we obtain an approximate discrete-time model of the form 
    
    \var{x_{t+1}} = \var{x_t} + \var{v_t}
    \var{v_{t+1}} = \var{v_t} + \var{a_t}

- We assume that the acceleration \var{a_t} is under our control, as it is determined by the rocket thrust.
- In a rough model, the magnitude |\var{a_t}| of the accelera­tion can be assumed to be proportional to the rate of fuel consumption at time \var{t}.
- Suppose that we have \var{x_0} and \var{v_0} as the initial position and velocity, respectively, of the rocket.
- We wish the rocket to take off and reach a target position \var{x_T} with speed \var{v_T} at time \var{T}.
- Furthermore, we wish to accomplish this in an economical fashion, that is, by using as little fuel as possible.


INPUT FORMAT: 

{
    "x_0": x_0,
    "v_0": v_0,
    "x_T": x_T,
    "v_T": v_T,
    "T": T
}

OBJECTIVE: The objective is to minimize the maximum thrust required, which is max_t |a_t|. 

OUTPUT INFO:

- key "x" contains a list of the positions of the rocket at each time step from 0 to \var{T}
- key "v" contains a list of the velocities of the rocket at each time step from 0 to \var{T}
- key "a" contains a list of the accelerations of the rocket at each time step from 0 to \var{T}
- key "fuel_spend" contains the total fuel spent by the rocket

OUTPUT FORMAT:

{
    "x": [x_i for i in 1, ..., T],
    "v": [v_i for i in 1, ..., T],
    "a": [a_i for i in 1, ..., T],
    "fuel_spend": fuel_spent,
}


</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Rocket Movement Optimization Problem}

\textbf{Variables:}
\begin{itemize}
    \item $\var{x_t}$: Position of the rocket at time $t$
    \item $\var{v_t}$: Velocity of the rocket at time $t$
    \item $\var{a_t}$: Acceleration (thrust) of the rocket at time $t$
\end{itemize}

\textbf{Discrete-Time Model:}
\begin{align}
    \var{x_{t+1}} &= \var{x_t} + \var{v_t} \quad \text{(1)} \\
    \var{v_{t+1}} &= \var{v_t} + \var{a_t} \quad \text{(2)}
\end{align}

\textbf{Parameters:}
\begin{itemize}
    \item Initial position: $\var{x_0}$
    \item Initial velocity: $\var{v_0}$
    \item Target position: $\var{x_T}$
    \item Target velocity: $\var{v_T}$
    \item Time duration: $T$
\end{itemize}

\textbf{Objective:}
Minimize the maximum thrust required:
\[
\text{minimize } Z = \max_{t} |\var{a_t}|
\]

\textbf{Constraints:}
\begin{align}
    \var{x_0} &= x_0 \quad \text{(initial condition)} \\
    \var{v_0} &= v_0 \quad \text{(initial condition)} \\
    \var{x_T} &= \var{x_T} \quad \text{(target position)} \\
    \var{v_T} &= \var{v_T} \quad \text{(target velocity)} \\
    \var{x_{t+1}} &= \var{x_t} + \var{v_t}, \quad t = 0, 1, \ldots, T-1 \quad \text{(1)} \\
    \var{v_{t+1}} &= \var{v_t} + \var{a_t}, \quad t = 0, 1, \ldots, T-1 \quad \text{(2)}
\end{align}

\textbf{Output:}
\begin{itemize}
    \item Key "x" contains: $\{ \var{x_i} \;|\; i = 0, 1, \ldots, T \}$
    \item Key "v" contains: $\{ \var{v_i} \;|\; i = 0, 1, \ldots, T \}$
    \item Key "a" contains: $\{ \var{a_i} \;|\; i = 0, 1, \ldots, T \}$
    \item Key "fuel\_spend" contains the total fuel spent by the rocket
\end{itemize}

\textbf{Output Format:}
\begin{verbatim}
{
    "x": [x_i for i in 0, ..., T],
    "v": [v_i for i in 0, ..., T],
    "a": [a_i for i in 0, ..., T],
    "fuel_spend": fuel_spent,
}
\end{verbatim}

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

\section*{Rocket Movement Optimization Problem}

\textbf{Variables:}
\begin{itemize}
    \item $\var{x_t}$: Position of the rocket at time $t$
    \item $\var{v_t}$: Velocity of the rocket at time $t$
    \item $\var{a_t}$: Acceleration (thrust) of the rocket at time $t$
\end{itemize}

\textbf{Discrete-Time Model:}
\begin{align}
    \var{x_{t+1}} &= \var{x_t} + \var{v_t} \quad \text{(1)} \\
    \var{v_{t+1}} &= \var{v_t} + \var{a_t} \quad \text{(2)}
\end{align}

\textbf{Parameters:}
\begin{itemize}
    \item Initial position: $\var{x_0}$
    \item Initial velocity: $\var{v_0}$
    \item Target position: $\var{x_T}$
    \item Target velocity: $\var{v_T}$
    \item Time duration: $T$
\end{itemize}

\textbf{Objective:}
Minimize the maximum thrust required:
\[
\text{minimize } Z = \max_{t} |\var{a_t}|
\]

\textbf{Constraints:}
\begin{align}
    \var{x_0} &= x_0 \quad \text{(initial condition)} \\
    \var{v_0} &= v_0 \quad \text{(initial condition)} \\
    \var{x_T} &= \var{x_T} \quad \text{(target position)} \\
    \var{v_T} &= \var{v_T} \quad \text{(target velocity)} \\
    \var{x_{t+1}} &= \var{x_t} + \var{v_t}, \quad t = 0, 1, \ldots, T-1 \quad \text{(1)} \\
    \var{v_{t+1}} &= \var{v_t} + \var{a_t}, \quad t = 0, 1, \ldots, T-1 \quad \text{(2)}
\end{align}

\textbf{Output:}
\begin{itemize}
    \item Key "x" contains: $\{ \var{x_i} \;|\; i = 0, 1, \ldots, T \}$
    \item Key "v" contains: $\{ \var{v_i} \;|\; i = 0, 1, \ldots, T \}$
    \item Key "a" contains: $\{ \var{a_i} \;|\; i = 0, 1, \ldots, T \}$
    \item Key "fuel\_spend" contains the total fuel spent by the rocket
\end{itemize}

\textbf{Output Format:}
\begin{verbatim}
{
    "x": [x_i for i in 0, ..., T],
    "v": [v_i for i in 0, ..., T],
    "a": [a_i for i in 0, ..., T],
    "fuel_spend": fuel_spent,
}
\end{verbatim}

\end{document}</MATH_MODEL>
<DATA>
{'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data from JSON
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}
x0 = data['X0']
v0 = data['V0']
xT = data['XT']
vT = data['VT']
T = data['T']

#### Problem Definition
problem = pulp.LpProblem("Rocket Movement Optimization", pulp.LpMinimize)

#### Variables
x = pulp.LpVariable.dicts("x", range(T + 1), lowBound=None)  #### Position
v = pulp.LpVariable.dicts("v", range(T + 1), lowBound=None)  #### Velocity
a = pulp.LpVariable.dicts("a", range(T), lowBound=None)       #### Acceleration

#### Objective Function: Minimize the maximum thrust required
max_thrust = pulp.LpVariable("max_thrust", lowBound=0)
problem += max_thrust

#### Constraints
problem += (x[0] == x0, "Initial position")
problem += (v[0] == v0, "Initial velocity")
problem += (x[T] == xT, "Target position")
problem += (v[T] == vT, "Target velocity")

for t in range(T):
    problem += (x[t + 1] == x[t] + v[t], f"Position constraint at time {t}")
    problem += (v[t + 1] == v[t] + a[t], f"Velocity constraint at time {t}")
    problem += (a[t] <= max_thrust, f"Thrust constraint at time {t}")
    problem += (a[t] >= -max_thrust, f"Negative thrust constraint at time {t}")

#### Solve the problem
problem.solve()

#### Extract outputs
result = {
    "x": [x[i].varValue for i in range(T + 1)],
    "v": [v[i].varValue for i in range(T + 1)],
    "a": [a[i].varValue for i in range(T)],
    "fuel_spend": pulp.value(max_thrust)
}

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

#### Print result in JSON format
print(json.dumps(result, indent=2))
```

