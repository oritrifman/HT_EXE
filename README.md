# Heat Transfer Simulation

A PySide6 desktop application that simulates heat conduction between two bodies,
written for the course "Physics in the Computer".

## Features

- Two bodies with adjustable temperature (candle sliders), mass and heat capacity
- Live simulation with a timer: temperatures, colors and sliders update every step
- Material selection (copper, aluminum, iron, gold, glass, water) or manual heat capacity
- Heaters with adjustable power (kW) for each body
- Automatic stop when the temperatures are equal
- Graph window: plot the temperature of each body over time, clear the graph
- Export of the full experiment to a CSV file that opens in Excel
- About window and a warm Hanukkah theme (`style.qss`)

## Physics

Each time step `dt`:

- Heat current: `I1 = sigma * (T2 - T1)`
- Heat added to body 1: `dQ1 = I1 * dt` (body 2 gets `-dQ1`)
- Temperature change: `dT = dQ / (m * c)`

Units: heat capacity in kJ/kg°C, conductivity and heater power in kW/°C and kW.

## Files

| File | Content |
|---|---|
| `Main.py` | Main window and the simulation (`HeatTransfer`) |
| `Body.py` | The `Body` class with the `add_heat` method |
| `graph_window.py` | Graph window with matplotlib and CSV export |
| `about_window.py` | About window |
| `candle_slider.py` | Candle-shaped slider with a flickering flame |
| `style.qss` | Style sheet for all the windows |

## How to run