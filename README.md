# 🌌 Advanced 3D Astrodynamics & Orbital Simulation Suite

A high-precision, multi-physics orbital mechanics simulation suite developed in **Python**, designed to model complex satellite trajectories under realistic space environment perturbations.

## 🚀 Key Engineering & Physics Features
1. **Numerical Integration (RK4):** Implements 4th-Order Runge-Kutta integration to ensure superior long-term orbital energy stability and high precision compared to basic Euler methods.
2. **Earth's Oblateness ($J2$ Perturbation):** Accounts for the equatorial bulge, modeling nodal precession and apsidal shifts accurately in 3D space.
3. **Atmospheric Drag & Decay:** Incorporates an exponential atmospheric density model ($\rho = \rho_0 e^{-h/H}$) to simulate orbital decay in Low Earth Orbit (LEO).
4. **Orbital Maneuvers / Thrust:** Simulates active prograde rocket burns (`Orbit Raising`) for orbital transfer mechanics.
5. **3D Visualization:** Generates full 3D interactive plots with true orbital inclination angles around an oblate Earth model using NumPy and Matplotlib.

## 🛠️ Tech Stack
* **Language:** Python 3.x
* **Libraries:** NumPy, Matplotlib (3D/2D plotting)

## ⚙️ Installation & Quick Start

Clone the repository and run the simulation locally:

```bash
# Clone the repository
git clone https://github.com/saif-ali-obayes/Advanced-Orbital-Simulator.git

# Navigate to project directory
cd Advanced-Orbital-Simulator

# Install required dependencies
pip install numpy matplotlib

# Run the 3D orbital simulation
python orbital_simulater.py
```

📊 Visualizations & Results
3d_orbital_simulation.png : Full 3D inclined orbit incorporating all perturbations and maneuvers.
rk4_orbital_simulation.png : High-precision orbital tracking via RK4.
thrust_orbital_simulation.png : Orbit raising visualization via active prograde thrust.
