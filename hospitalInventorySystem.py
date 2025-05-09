import tkinter as tk
from tkinter import scrolledtext
import random
import pandas as pd
import matplotlib.pyplot as plt

# Constants
MAX_FIRST_FLOOR = 10
MAX_BASEMENT = 30
REVIEW_PERIOD = 6
INITIAL_FIRST_FLOOR = 4
INITIAL_BASEMENT = 30

# Demand Distribution (probabilities and ranges for random numbers)
demand_distribution = [(1, 0.1, (0, 10)),
                       (2, 0.15, (11, 25)),
                       (3, 0.35, (26, 60)),
                       (4, 0.2, (61, 80)),
                       (5, 0.2, (81, 100))]

# Lead Time Distribution (probabilities and ranges for random numbers)
lead_time_distribution = [(1, 0.4, (0, 40)),
                          (2, 0.35, (41, 75)),
                          (3, 0.25, (76, 100))]

# Function to run the inventory simulation
def run_inventory_simulation():
    global inventory_log  # So it can be accessed globally for the log
    first_floor_inventory = INITIAL_FIRST_FLOOR
    basement_inventory = INITIAL_BASEMENT
    inventory_log = []
    shortage_count = 0
    order_count = 0
    total_demand = 0
    total_lead_time = 0
    order_delivery_days_left = 0  # Tracks how many days until the next order arrives

    for cycle in range(1, 21):
        for day in range(1, REVIEW_PERIOD + 1):
            beginning_inventory_first_floor = first_floor_inventory
            beginning_inventory_basement = basement_inventory

            # Generate daily demand
            demand, demand_random_number = generate_demand()
            total_demand += demand

            # Handle demand
            if first_floor_inventory >= demand:
                first_floor_inventory -= demand
                shortage_quantity = 0
            else:
                shortfall_to_10 = MAX_FIRST_FLOOR - first_floor_inventory
                transfer_quantity = min(shortfall_to_10, basement_inventory)
                first_floor_inventory += transfer_quantity
                basement_inventory -= transfer_quantity

                demand_left = demand - first_floor_inventory
                if first_floor_inventory >= demand:
                    first_floor_inventory -= demand
                    shortage_quantity = 0
                else:
                    first_floor_inventory = 0
                    remaining_demand = demand_left
                    if basement_inventory >= remaining_demand:
                        basement_inventory -= remaining_demand
                        shortage_quantity = 0
                    else:
                        shortage_quantity = remaining_demand - basement_inventory
                        basement_inventory = 0

            if shortage_quantity > 0:
                shortage_count += shortage_quantity

            # Handle incoming orders
            if order_delivery_days_left > 0:
                order_delivery_days_left -= 1
                if order_delivery_days_left == 0:
                    refill_amount = MAX_BASEMENT - basement_inventory
                    basement_inventory += refill_amount

            ending_inventory_first_floor = first_floor_inventory
            ending_inventory_basement = basement_inventory

            inventory_log.append({
                'Cycle': cycle,
                'Day': day,
                'Beginning First Floor Inventory': beginning_inventory_first_floor,
                'Beginning Basement Inventory': beginning_inventory_basement,
                'Demand': demand,
                'Demand Random Number': demand_random_number,
                'Ending First Floor Inventory': ending_inventory_first_floor,
                'Ending Basement Inventory': ending_inventory_basement,
                'Shortage Quantity': shortage_quantity,
                'Order Quantity': 0,
                'Lead Time': '-',
                'Days Until Order Arrives': order_delivery_days_left if order_delivery_days_left > 0 else '-'
            })

        if basement_inventory < MAX_BASEMENT:
            refill_amount = MAX_BASEMENT - basement_inventory
            lead_time, lead_time_random_number = generate_lead_time()
            order_delivery_days_left = lead_time if lead_time != '-' else 0
            total_lead_time += lead_time
            order_count += 1
            inventory_log[-1]['Order Quantity'] = refill_amount
            inventory_log[-1]['Lead Time'] = order_delivery_days_left
            inventory_log[-1]['Days Until Order Arrives'] = order_delivery_days_left

    df_inventory_log = pd.DataFrame(inventory_log)
    average_ending_first_floor = df_inventory_log['Ending First Floor Inventory'].mean()
    average_ending_basement = df_inventory_log['Ending Basement Inventory'].mean()
    average_demand = total_demand / (REVIEW_PERIOD * 20)
    average_lead_time = total_lead_time / order_count if order_count > 0 else 0

    result_summary = (
        f"Average Ending Units in First Floor Inventory: {average_ending_first_floor:.2f}\n"
        f"Average Ending Units in Basement Inventory: {average_ending_basement:.2f}\n"
        f"Total Shortages: {shortage_count}\n"
        f"Average Demand per Day: {average_demand:.2f}\n"
        f"Average Lead Time: {average_lead_time:.2f} days\n"
        f"Number of Orders Placed: {order_count}\n"
    )

    return result_summary, df_inventory_log, average_demand, average_lead_time

def generate_demand():
    random_number = random.randint(0, 100)
    for demand, _, range_ in demand_distribution:
        if range_[0] <= random_number <= range_[1]:
            return demand, random_number

def generate_lead_time():
    random_number = random.randint(0, 100)
    for lead_time, _, range_ in lead_time_distribution:
        if range_[0] <= random_number <= range_[1]:
            return lead_time, random_number
    return '-', '-'

def display_results():
    result_summary, df_inventory_log, _, _ = run_inventory_simulation()
    result_textbox.delete('1.0', tk.END)
    result_textbox.insert(tk.END, result_summary)

    log_textbox.delete('1.0', tk.END)
    log_textbox.insert(tk.END, df_inventory_log.to_string(index=False))

def run_multiple_simulations():
    total_average_demand = 0
    total_average_lead_time = 0
    num_simulations = 30

    for _ in range(num_simulations):
        _, _, average_demand, average_lead_time = run_inventory_simulation()
        total_average_demand += average_demand
        total_average_lead_time += average_lead_time

    overall_average_demand = total_average_demand / num_simulations
    overall_average_lead_time = total_average_lead_time / num_simulations

    multi_sim_result = (
        f"Results from {num_simulations} Simulations:\n"
        f"Average of Average Demand: {overall_average_demand:.2f}\n"
        f"Average of Average Lead Time: {overall_average_lead_time:.2f} days\n"
    )

    result_textbox.delete('1.0', tk.END)
    result_textbox.insert(tk.END, multi_sim_result)

def plot_histogram(data, x_label, y_label, title, bins=None, color=None):
    plt.figure(figsize=(10, 6))
    plt.hist(data, bins=bins, edgecolor='black', alpha=0.7, color=color)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.grid(axis='y', alpha=0.75)
    plt.show()

def plot_demand_distribution():
    demand_data = [entry['Demand'] for entry in inventory_log]
    plot_histogram(demand_data, 'Demand', 'Frequency', 'Demand Distribution', bins=range(1, 7), color='blue')

def plot_lead_time_distribution():
    lead_times = [entry['Lead Time'] for entry in inventory_log if entry['Lead Time'] != '-']
    plot_histogram(lead_times, 'Lead Time (Days)', 'Frequency', 'Lead Time Distribution', bins=range(1, 5), color='green')

def plot_inventory_levels():
    first_floor_levels = [entry['Ending First Floor Inventory'] for entry in inventory_log]
    basement_levels = [entry['Ending Basement Inventory'] for entry in inventory_log]
    plot_histogram(first_floor_levels, 'Inventory Level', 'Frequency', 'First Floor Inventory Levels', bins=range(0, 12, 2), color='orange')
    plot_histogram(basement_levels, 'Inventory Level', 'Frequency', 'Basement Inventory Levels', bins=range(0, 32, 5), color='purple')

def plot_shortage_distribution():
    shortages = [entry['Shortage Quantity'] for entry in inventory_log if entry['Shortage Quantity'] > 0]
    plot_histogram(shortages, 'Shortage Quantity', 'Frequency', 'Shortage Quantity Distribution', bins=range(0, 12, 2), color='red')

def plot_order_frequency():
    order_counts = [entry['Order Quantity'] for entry in inventory_log if entry['Order Quantity'] > 0]
    cycles = [entry['Cycle'] for entry in inventory_log if entry['Order Quantity'] > 0]
    plt.figure(figsize=(10, 6))
    plt.bar(cycles, order_counts, color='skyblue', edgecolor='black')
    plt.xlabel('Cycle')
    plt.ylabel('Orders Placed')
    plt.title('Order Frequency by Cycle')
    plt.grid(axis='y', alpha=0.75)
    plt.show()

# the GUI application window
root = tk.Tk()
root.title("Inventory Simulation")
root.state('zoomed')  # Fullscreen window

header_label = tk.Label(root, text="Inventory Simulation Results", font=("Arial", 16))
header_label.pack(pady=10)

run_button = tk.Button(root, text="Run Simulation", command=display_results)
run_button.pack(pady=10)

multi_sim_button = tk.Button(root, text="Run 30 Simulations", command=run_multiple_simulations)
multi_sim_button.pack(pady=10)

result_label = tk.Label(root, text="Summary of Results", font=("Arial", 14))
result_label.pack(pady=5)

result_textbox = scrolledtext.ScrolledText(root, height=6)
result_textbox.pack(fill=tk.BOTH, expand=True, pady=5)

log_label = tk.Label(root, text="Inventory Log", font=("Arial", 14))
log_label.pack(pady=5)

log_textbox = scrolledtext.ScrolledText(root, wrap=tk.NONE)
log_textbox.pack(fill=tk.BOTH, expand=True, pady=5)


#buttons for histograms
hist_button_frame = tk.Frame(root)
hist_button_frame.pack(pady=10)

tk.Button(hist_button_frame, text="Demand Distribution", command=plot_demand_distribution).grid(row=0, column=0, padx=5)
tk.Button(hist_button_frame, text="Lead Time Distribution", command=plot_lead_time_distribution).grid(row=0, column=1, padx=5)
tk.Button(hist_button_frame, text="Inventory Levels", command=plot_inventory_levels).grid(row=0, column=2, padx=5)
tk.Button(hist_button_frame, text="Shortage Distribution", command=plot_shortage_distribution).grid(row=0, column=3, padx=5)
tk.Button(hist_button_frame, text="Order Frequency", command=plot_order_frequency).grid(row=0, column=4, padx=5)

root.mainloop()
