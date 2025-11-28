# BT-SSH-Device-Manager

A Python tool for discovering Bluetooth Low Energy (BLE) devices and establishing SSH connections for remote management.

## Features

*   Scans for nearby BLE devices.
*   Connects to a specified BLE device (requires specific GATT profile knowledge for actual interaction).
*   Manages SSH connections using username/password or key-based authentication.
*   Executes remote commands via SSH.

## Prerequisites

You need Python 3.8+ installed.

Install the required libraries using pip:

```bash
pip install bleak paramiko

Or with python3:
