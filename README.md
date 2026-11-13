# School-Monitor

Automated Python project for collecting your own weekly attendance records from the Clickedu school portal and sending a private summary to Telegram.

Designed for a self-hosted Linux server and scheduled with systemd.

> **Status:** Initial project scaffold. Clickedu authentication and attendance extraction are intentionally not implemented yet: the exact school portal URL, login flow, and attendance-page structure must be confirmed first.

## Features planned

- Sign in to your school's Clickedu portal using a locally stored configuration.
- Retrieve attendance records for the current school week.
- Send a formatted report to a private Telegram chat every Friday.
- Run as a systemd oneshot service and timer.
- Keep credentials, logs, and local state out of Git.

## Requirements

- Python 3.11+
- Linux server with systemd
- Chromium dependencies supported by Playwright
- A Telegram bot and its private chat ID
- Your school's Clickedu URL and an account permitted to view the attendance records

## Setup

```bash
git clone https://github.com/Michaecode/School-Monitor.git
cd School-Monitor

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium

cp school-monitor.conf.example .school-monitor.conf
chmod 600 .school-monitor.conf
```

Edit `.school-monitor.conf` with your own values. Never commit this file or share its contents.

## Configuration

The local configuration file uses INI format:

- `[clickedu]`: school portal URL and account credentials
- `[telegram]`: bot token and private chat ID
- `[settings]`: timezone and browser settings

## Run

```bash
.venv/bin/python bot.py
```

The initial scaffold validates configuration and reports which integration still needs implementation. It does not attempt to log in or send fabricated attendance data.

## systemd

Copy the unit templates from `deploy/systemd/` to your user systemd directory, replace the example paths/user if needed, then enable the timer:

```bash
mkdir -p ~/.config/systemd/user
cp deploy/systemd/school-monitor.service ~/.config/systemd/user/
cp deploy/systemd/school-monitor.timer ~/.config/systemd/user/

systemctl --user daemon-reload
systemctl --user enable --now school-monitor.timer
```

The timer is configured for Fridays at 18:00 in the server's local timezone. Enable lingering if the job must run while your user is logged out:

```bash
sudo loginctl enable-linger "$USER"
```

Check execution with:

```bash
systemctl --user list-timers
journalctl --user -u school-monitor.service
```

## Privacy and security

- Use only your own account and information you are authorized to access.
- Keep `.school-monitor.conf` readable only by its owner (`chmod 600`).
- Do not commit credentials, Telegram tokens, browser profiles, logs, or attendance exports.
- Avoid logging passwords, session cookies, or unnecessary personal information.

## Development status

- [x] Project structure and configuration loader
- [x] Telegram message sender
- [x] Attendance report formatter
- [x] systemd service and Friday timer templates
- [ ] Confirm Clickedu portal URL and login flow
- [ ] Implement and test attendance extraction
- [ ] Add duplicate-report protection and automated tests
