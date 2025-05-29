# Hospital Inventory Simulation

This Python application simulates inventory management for a hospital's two-level storage system (First Floor and Basement). It uses probabilistic demand and lead time distributions to model restocking and shortages over multiple review cycles.

## Features

- Simulates daily demand and inventory adjustments over 20 cycles with 6-day review periods.
- Tracks shortages, orders, and lead times.
- Supports running single or multiple (30) simulations to analyze performance variability.
- Provides detailed inventory logs.
- Visualizes demand, lead time, inventory levels, shortages, and order frequency using matplotlib histograms.
- Simple Tkinter GUI for running simulations and displaying results.

## How It Works

- Demand and lead time are randomly generated based on predefined probability distributions.
- Orders are placed when basement inventory falls below maximum capacity, with lead time delays.
- Inventory is transferred from basement to first floor to meet demand before registering shortages.
- Results include average inventory levels, total shortages, average demand, lead time, and order counts.

## Usage

Run the Python script to launch the GUI. Use buttons to:

- Run a single simulation and view summary and log.
- Run 30 simulations and view averaged results.
- Display histograms for demand, lead time, inventory, shortages, and order frequency.

## Requirements

- Python 3.x
- tkinter (usually included with Python)
- pandas
- matplotlib



