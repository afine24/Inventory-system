# Inventory-system

## Description

This project was created for my mom to help her keep track of what she has in her kitchen and to aid in restocking. It is designed to be easily maintainable and as simple to use as possible so anybody who walks into the kitchen can figure it out without needing to ask for help.

## Hardware

As for the hardware needed, i tried to keep it as simple as possible, you will need the following if you want to build this yourself:

- [Raspberry Pi 4 B](https://www.canakit.com/raspberry-pi-4-4gb.html)
- [16x2 I2C lcd display](https://www.amazon.com/SunFounder-Serial-Module-Display-Arduino/dp/B019K5X53O)
- [4x4 matrix keypad](https://a.co/d/04VNssab)
- [Symbol LS2208 barcode scanner (or similar), in serial mode](https://a.co/d/0bTYwDl1)
- assorted breadboard wires

I will eventually also put a link to a 3d printable case for the device but as of right now it is WIP.

## Setup

the steps below will allow you to run the code. Please note that is is not finished, but all are welcome to contribute (see Contributing below)

1. from the Pi's terminal, run `git clone https://github.com/afine24/Inventory-system.git inventorySystem` to copy all code into the Pi
2. then run 
   ```
   cd inventorySystem
   chmod 755 run.sh
   ./run.sh
   ```
   and enter your sudo password if prompted

## Contributing

if you would like to contribute you are welcome to do so but i may be slow with accepting PR's because i dont check github regularly.
