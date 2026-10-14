# Radioactive Decay Simulator

A simple Python command-line program that simulates radioactive decay over time.
Built as a personal project while preparing for a nuclear engineering degree.

## What it does

- Lets the user choose a language (Korean or English)
- Lets the user pick one of 6 common radioactive isotopes — or enter a custom half-life:
  - Uranium-238
  - Uranium-235
  - Plutonium-239
  - Cesium-137
  - Carbon-14
  - Iodine-131
- Calculates how much of the original material remains over a chosen time span, using the standard decay formula:

  N(t) = N0 * (1/2)^(t / half-life)

- Prints a text summary and shows a graph of the decay curve using matplotlib

## How to run it

1. Make sure Python is installed.
2. Install the required library:

   ```
   pip install matplotlib
   ```

3. Run the program:

   ```
   python radioactive_decay_simulator.py
   ```

4. Follow the prompts: choose a language, pick an element (or enter a custom half-life), enter the initial number of atoms, and enter how many years to simulate.

## Example

Choosing Cesium-137 (half-life ≈ 30.17 years) with 1,000,000 initial atoms over a 100-year span shows the amount drop to roughly 1/8 of the original by the end of the simulation.

## Tech used

- Python 3
- matplotlib

## Why I built this

I'm a high school student planning to study nuclear engineering, and I wanted a small hands-on project that connects basic physics (radioactive decay) with programming. This was also my first time using Git and GitHub.
