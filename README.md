# pgAdmin4 Service

An old-school utility script for deploying a local [pgAdmin4](https://www.pgadmin.org/) web interface, optimized for offline and non-root environments.  
This project automates setup, patching, and running, making it especially suitable for individual use or in restrictive environments.

---

## Features

- **Runs without root access** (except for systemd installation).
- **Offline support** after initial dependency download/setup.
- **Custom patching** for compatibility.
- **Easily adjustable** network bind address, port, and data directories via environment variables.
- **Optional systemd integration** for persistent/auto-start web service.

---

## Getting Started

### 1. Initial Setup

For the first usage, **initialize the environment** by running:

```sh
./manage.py init
```
This will:
- Create a Python virtual environment.
- Install dependencies from `requirements.txt`.
- Patch necessary python libraries (e.g. SQLAlchemy for use with pysqlite3).
- Copy a local configuration file for pgAdmin4.

### 2. Start the Server

Launch the web app:

```sh
./manage.py start
```

- On first launch, you'll be prompted to set up the initial pgAdmin4 web login (email & password).

#### [Advanced] Custom Options

- **IP Address:** Set `IP` env variable (default: `0.0.0.0`)
- **Port:** Set `PORT` env variable (default: `5050`)
- **pgAdmin4 Data Path:** Set `BASE_DIR` env variable (default: script location)

Example:

```sh
IP=127.0.0.1 PORT=5555 BASE_DIR=/desired/path ./manage.py start
```

---

## Commands

- **`init`**  
  Set up the environment (venv, install, patching, config).

- **`start [--daemon]`**  
  Start the pgAdmin4 web UI. All extra arguments pass through to gunicorn.

- **`patch`**  
  Run all necessary patching steps individually.

- **`patch_sqlalchemy` / `patch_config_local`**  
  Run one of the patches alone.

- **`install_systemd`**  
  Install a systemd service unit for this pgAdmin4 instance (requires root, will prompt for sudo).  
  Edits `/etc/systemd/system/pgadmin4.service` and enables/starts the service.

---

## Example Usages

```sh
# Initialize environment
./manage.py init

# Start pgAdmin4 web UI
./manage.py start

# With custom environment
IP=127.0.0.1 PORT=8080 ./manage.py start

# Patch manually (if needed)
./manage.py patch

# Install systemd unit (as root)
sudo ./manage.py install_systemd
```

---

## File Structure

- `manage.py` - Main utility script
- `requirements.txt` - Python dependencies
- `config_local.py` - pgAdmin4 configuration override
- `etc/systemd/system/pgadmin4.service` - Example systemd unit file

---

## Systemd Integration

To run pgAdmin4 as a persistent system service:

```sh
sudo ./manage.py install_systemd
```

- This will copy/edit the service file and reload systemd.
- The service can then be managed using `systemctl`:
    - `sudo systemctl start pgadmin4`
    - `sudo systemctl enable pgadmin4`
    - `sudo systemctl status pgadmin4`

---

## Troubleshooting

- **Dependencies**: Make sure Python 3 and pip are available on your system.
- **Permissions**: Only systemd installation requires root.
- **Environment variables**: Custom paths/network binds by exporting `IP`, `PORT`, `BASE_DIR` as needed.

---

## Source Code Reference

The full source for `manage.py` is included in this repository for reference and further customization.

---

## License

MIT

---

**Happy hacking!**  
For issues or contributions, please open a PR or issue on this repository.
