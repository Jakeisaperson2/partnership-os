# MM ERP — Odoo 17.0 Community (Local)

A Docker-based local instance of [Odoo 17.0 Community Edition](https://github.com/odoo/odoo)
for evaluation and development.

---

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running
- Ports **8069** free on your machine

---

## Installation

```powershell
# Clone or download this project, then open a terminal in the project folder.
# No additional installation steps — Docker handles everything.
```

---

## Startup

```powershell
docker compose up -d
```

The first run downloads the `odoo:17.0` and `postgres:15` images (~1–2 GB total).
Wait about 30–60 seconds, then open:

**http://localhost:8069**

---

## First-Time Database Setup

Odoo opens a **Create Database** form on first visit.

| Field | Recommended value |
|-------|------------------|
| Master Password | (leave blank for local dev, or set in `config/odoo.conf`) |
| Database Name | `odoo_dev` (any name you like) |
| Email | Your login email |
| Password | Your login password |
| Language | English (or your preferred language) |
| Country | Your country |
| Demo data | Check this box to load sample records for evaluation |

Click **Create Database**. Odoo installs its base module (~1–2 min) and then
redirects you to the login screen.

---

## Installing Modules

### Via the web interface (recommended for evaluation)

1. Log in as the administrator.
2. Go to **Settings → General Settings** → scroll to bottom → **Activate Developer Mode**.
3. Open the **Apps** menu from the top bar.
4. Click **Update Apps List** (first time only).
5. Search for the module (e.g., "CRM") and click **Install**.

### Via the command line

```powershell
docker compose run --rm web odoo `
    --db_host db --db_user odoo --db_password odoo `
    -d odoo_dev -i crm,sale_management,project,contacts,discuss `
    --stop-after-init
```

Replace `odoo_dev` with your database name and the `-i` list with the module
technical names you want.

---

## Upgrading Modules

After updating a module's source code, upgrade it so Odoo re-applies changes:

```powershell
docker compose run --rm web odoo `
    --db_host db --db_user odoo --db_password odoo `
    -d odoo_dev -u <module_name> `
    --stop-after-init
```

---

## Shutdown

```powershell
# Stop containers, keep all data intact
docker compose down
```

```powershell
# Stop AND delete all data (full reset — irreversible)
docker compose down -v
```

---

## Backup and Restore

### Backup via the Odoo web UI (easiest)

1. Go to **http://localhost:8069/web/database/manager**
2. Click **Backup** next to your database.
3. Choose **ZIP** format (includes filestore attachments).
4. Save the downloaded file.

### Backup via command line

```powershell
# Dump the database to a file in the backups/ folder
docker compose exec db pg_dump -U odoo odoo_dev > backups\odoo_dev.dump
```

### Restore via the Odoo web UI

1. Go to **http://localhost:8069/web/database/manager**
2. Click **Restore Database**.
3. Upload the ZIP file and give the restored database a name.

### Restore via command line

```powershell
# Create the database first, then restore
docker compose exec db createdb -U odoo odoo_dev_restored
Get-Content backups\odoo_dev.dump | docker compose exec -T db psql -U odoo odoo_dev_restored
```

---

## Viewing Logs

```powershell
# Follow live logs from Odoo
docker compose logs -f web

# Follow live logs from PostgreSQL
docker compose logs -f db
```

---

## Troubleshooting

### The browser shows "Bad Gateway" or nothing loads

The Odoo container is still starting. Wait 30 seconds and refresh. Check logs:

```powershell
docker compose logs web
```

### Port 8069 is already in use

Stop whatever is using it, or change the port mapping in `docker-compose.yml`:

```yaml
ports:
  - "8070:8069"   # maps host port 8070 → container port 8069
```

Then access Odoo at **http://localhost:8070**.

### "Connection refused" to the database

The `db` container may not be healthy yet. The `healthcheck` in `docker-compose.yml`
makes the web container wait, but you can check manually:

```powershell
docker compose ps
```

Both `db` and `web` should show `Up` or `healthy`.

### Forgot admin password

Reset it from the database manager page:
1. Go to **http://localhost:8069/web/database/manager**
2. Click **Set Master Password** if prompted.
3. Then use **http://localhost:8069/odoo/action-base_setup.setup_config_wizard_act**
   → or via the Settings → Users menu to change the admin user's password.

Alternatively, reset via shell:

```powershell
docker compose exec web odoo shell -d odoo_dev --db_host db --db_user odoo --db_password odoo
```

Then inside the Odoo shell:

```python
env['res.users'].browse(2).write({'password': 'newpassword'})
env.cr.commit()
exit()
```

### Complete reset (start fresh)

```powershell
docker compose down -v
docker compose up -d
```

This deletes all data and volumes. The next browser visit shows the database
creation form again.

---

## Project Structure

```
MM ERP/
├── docker-compose.yml     # Service definitions
├── .env                   # Credentials (never commit to git)
├── config/
│   └── odoo.conf          # Odoo server options
├── addons/                # Place custom modules here later
├── backups/               # Database dumps (gitignored)
├── README.md              # This file
└── CLAUDE.md              # Developer reference
```

---

## Community vs Enterprise Modules

**All modules in this setup are Community Edition (free).**

Key Community apps available to install:

| App | Technical name |
|-----|---------------|
| CRM | `crm` |
| Sales | `sale_management` |
| Purchase | `purchase` |
| Inventory | `stock` |
| Accounting / Invoicing | `account` |
| Project | `project` |
| Contacts | `contacts` |
| Discuss (Messaging) | `discuss` |
| Employees | `hr` |
| Manufacturing | `mrp` |
| Helpdesk | `helpdesk` |
| Website | `website` |
| eCommerce | `website_sale` |
| Point of Sale | `point_of_sale` |

Enterprise-only features (require a paid Odoo subscription and the Enterprise
repository) include: Studio, Sign, IoT Box, advanced accounting reports,
full payroll, Social Marketing, and WhatsApp integration.
