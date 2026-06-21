<div align="center">

# Unique ID Checker & Generator

**A Python tool to generate and verify unique device IDs for Android devices.**

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-GPL%203.0-green)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Android-yellow)]()
[![Stars](https://img.shields.io/github/stars/SirYadav1/Unique-id-checker-generator?style=social)]()

---

</div>

## What it does

Combines **ANDROID_ID**, **Board Name**, **Model**, and **Manufacturer** to generate a **SHA-256 hashed unique ID** — no root required.

## Features

- Generate a unique, consistent device ID
- Verify if a given ID matches the current device
- Works without root access
- Interactive CLI with colored output
- Lightweight — single dependency (`colorama`)

## Installation

```bash
git clone https://github.com/SirYadav1/Unique-id-checker-generator.git
cd Unique-id-checker-generator
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

```
========================================
  UNIQUE DEVICE ID VERIFICATION TOOL
========================================
1. Generate ID
2. Verify ID
3. Exit
========================================
Enter your choice (1/2/3):
```

**Generate** — creates a SHA-256 hash from your device info.

**Verify** — checks if an entered ID matches the current device.

## How it works

```
ANDROID_ID + Board + Model + Manufacturer
              |
        SHA-256 Hash
              |
      Unique Device ID
```

## Contributing

Fork, improve, and submit a PR. All contributions welcome.

## Contact

- GitHub: [@SirYadav1](https://github.com/SirYadav1)
- Email: siryadav@internet.ru
- Telegram: [@SirYadav]

---

<div align="center">

**Made by SirYadav1**

</div>
