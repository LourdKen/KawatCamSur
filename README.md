# KawatCamSur

A student prototype for discovering sports partners and sports venues in
Camarines Sur.

## Planned features

- User registration and profiles
- Sports partner recommendations using Content-Based Filtering
- Sports venue directory and OpenStreetMap view
- User-submitted venue recommendations
- Moderator approval workflow
- Role-based access control required by the course project

## Technology

- Python
- Flet
- SQLite
- Flet Map / OpenStreetMap

## Setup

1. Install Python.
2. Open this folder in VS Code.
3. Create and activate a virtual environment:

   ```powershell
   py -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

4. Install dependencies:

   ```powershell
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

5. Start the starter application:

   ```powershell
   python main.py
   ```

## Project notes

This folder is a starter structure, not a completed secure application.
Complete the required security implementation, tests, and documentation
with your group. Follow your instructor's restrictions on AI assistance,
especially for security-sensitive code and required security documents.

Use fictional demo data only. Add required OpenStreetMap attribution when
displaying map tiles, and follow the tile provider's usage policy.
