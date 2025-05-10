# Retiro Park Simulation

A simulation of visitor behavior in Madrid's Retiro Park, modeling movement patterns, activities, and time-based events.

## Overview

This project simulates the daily life of Retiro Park in Madrid. Visitors enter the park at specific times, participate in various activities, and leave based on their preferences and the park's schedule. The simulation includes realistic modeling of visitor movement, activity selection, and park operations from opening (6:00 AM) until closing (10:00 PM).

## Architecture

The simulation follows an object-oriented approach with several key components:

### Core Components

- **RetiroPark**: The main class that initializes and orchestrates the simulation
- **TimeManager**: Controls the passage of time in the simulation with a configurable time scale
- **Visitor**: Represents individual park visitors with unique behaviors and preferences
- **Activities**: Various activities available in the park (sports, boat/bike rentals, cafes, etc.)

### Event System

The simulation uses an event-driven architecture where:
- TimeManager broadcasts time events ("open", "close")
- Components (visitors, activities) react to these events accordingly
- Visitors make decisions based on time of day, their preferences, and available activities

### Threading Model

- **TimeManager**: Runs in its own thread to update the simulation time
- **Visitors**: Each visitor runs in a separate thread for independent behavior
- **GUI**: Runs in the main thread to display the simulation state

### Database Integration

Simple SQLite database integration tracks:
- Visitor entries and exits
- Activity participation
- Usage statistics for analysis

## Features

- **Time Simulation**: Configurable time acceleration to run a full day quickly
- **Visitor Behavior Modeling**: Different visitor personas with unique preferences
- **Visual Representation**: 2D visualization of visitors moving through the park
- **Activity System**: Various activities with different durations and appeal
- **Natural Exit**: Simulation properly ends when all visitors have exited
- **Analytics**: Comprehensive metrics collection

## Running the Simulation

1. Ensure you have Python 3.6+ installed
2. Install required dependencies: `pip install -r requirements.txt`
3. Run the simulation: `python RetiroPark.py`
4. After the simulation completes:
   - Activate the database with SQLite3: `sqlite3 retiro.db`
   - The database will contain all simulation data for analysis
   - Run `python Metrics/run_all_metrics.py` to generate analytics and reports
   - View the metrics output for insights on visitor behavior and activity patterns

## Controls

- **Close Simulation Button**: Located in the top-left corner, allows immediate termination
- The simulation pauses when all visitors have left

### Threading

The simulation uses Python's threading library to model concurrent visitor behaviors. Each visitor operates independently but shares access to park activities.

### GUI

Built with Tkinter, the GUI displays:
- A map of Retiro Park with visitor positions
- Current time and day
- Active visitors (red dots) and those who have exited (blue dots)

### Time Management

TimeManager controls the simulation's time flow:
- Park opens at 6:00 AM
- Activities close at 10:00 PM 
- Time advances in configurable increments

### Analytics

The project includes a metrics system that analyzes simulation data:
- **Activity popularity** across different times of day
- **Visitor behavior patterns** based on personas
- **Facility usage** statistics for optimization
- **Sports and cafe metrics** for specific venue analysis

## Project Structure

```
retiro-park-simulation/
├── Activities/              # Activity classes and factories
│   ├── activity.py          # Base activity class
│   ├── activity_factory.py  # Creates all available activities
│   ├── Renting/             # Rental activities (bikes, boats)
│   └── Sports/              # Sports activities
├── Metrics/                 # Analytics and reporting tools
│   ├── activity_metrics.py  # Analysis of activity participation
│   ├── visitors_metrics.py  # Visitor behavior analysis
│   ├── sport_metrics.py     # Sports facilities usage metrics
│   ├── cafe_metrics.py      # Cafe and restaurant analytics
│   └── run_all_metrics.py   # Unified metrics runner
├── Time_manager.py          # Manages simulation time
├── Visitor.py               # Visitor class definition
├── Visitor_Factory.py       # Creates visitors with different personas
├── RetiroPark.py            # Main simulation controller
├── UI/                      # User interface components
│   ├── gui.py               # Main GUI implementation
│   ├── park_map.py          # Park map coordinate system
│   └── retiro.jpg           # Park background image
├── Utils/                   # Utility functions
│   ├── database.py          # Database operations
│   └── logger.py            # Logging functionality
├── retiro.db                # SQLite database for simulation data (added when simulation has been run)
└── requirements.txt         # Project dependencies
```