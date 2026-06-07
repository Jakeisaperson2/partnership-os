# PartnershipOS — Odoo 17.0 Community (Local Dev)

## Project Purpose

PartnershipOS is a purpose-built Business Development platform for Academic Medical Centers (AMCs),
built as a set of custom Odoo 17.0 Community addons. The platform manages industry partnerships,
sponsored research opportunities, licensing, corporate outreach, relationship management, project
execution, and financial tracking.

**Implementation rule:** All customizations live in `addons/` as Odoo modules. Never modify files
inside the Docker image — they are overwritten on every `docker compose pull`.

**Active database:** `odoo_dev`

---

## Repository Architecture

```
MM ERP/
├── docker-compose.yml          # Defines the db and web services
├── .env                        # Credentials (never commit this)
├── .gitignore
├── config/
│   └── odoo.conf               # Odoo server configuration file
├── addons/                     # All PartnershipOS custom modules
│   ├── partnership_os_base/    # Phase 1+6: navigation cleanup, brand colors
│   ├── partnership_os_crm/     # Phase 2+3: terminology, pipeline, AMC fields
│   ├── partnership_os_project/ # Phase 4: project auto-creation, opportunity link
│   └── partnership_os_reporting/ # Phase 5: BD dashboards (install separately)
├── backups/                    # Database dump files (gitignored)
├── README.md
└── CLAUDE.md                   # This file
```

### Services

| Service | Image | Port | Purpose |
|---------|-------|------|---------|
| `db` | `postgres:15` | (internal) | Persistent PostgreSQL database |
| `web` | `odoo:17.0` | `8069` | Odoo application server |

### Volumes

| Volume | Mount inside container | Purpose |
|--------|----------------------|---------|
| `odoo-db-data` | `/var/lib/postgresql/data` | All PostgreSQL data files |
| `odoo-web-data` | `/var/lib/odoo` | Odoo filestore (attachments, sessions) |
| `./config` | `/etc/odoo` | odoo.conf loaded at startup |
| `./addons` | `/mnt/extra-addons` | PartnershipOS custom modules |

---

## PartnershipOS Custom Modules

### Module dependency chain

```
partnership_os_base
    └── partnership_os_crm
            └── partnership_os_project
                    └── partnership_os_reporting
```

### `partnership_os_base`

**Depends on:** `web`, `base`, `mail`

**What it does:**
- Deactivates navigation for unused modules (Inventory, Manufacturing, POS, Website, Purchase,
  Email Marketing, Events, Surveys, Fleet, Lunch, Maintenance, Sales) via `post_init_hook`
- Injects brand color overrides (`#1B4F72` navy) into the SCSS primary variables bundle

**Key files:**
- `hooks.py` — `post_init_hook` that gracefully deactivates menus for any installed irrelevant modules
- `static/src/scss/branding.scss` — overrides `$o-brand-primary`, `$o-brand-odoo`, `$o-community-color`

---

### `partnership_os_crm`

**Depends on:** `partnership_os_base`, `crm`, `sales_team`

**What it does:**
- Replaces the 4 default CRM stages with the 9-stage partnership pipeline:
  1. Identified
  2. Outreach Initiated
  3. Introductory Meeting
  4. Opportunity Assessment
  5. Proposal Development
  6. Negotiation
  7. Agreement Executed *(is_won = True)*
  8. Active Project
  9. Completed *(folded)*
- Renames core terminology throughout the UI:

  | Before | After |
  |--------|-------|
  | CRM | Partnerships |
  | My Pipeline | My Partnerships |
  | Customers | Partner Organizations |
  | Salesperson | Partnership Manager |
  | Sales Team | BD Team |
  | Pipeline (report) | Partnership Pipeline |

- Hides the **Leads** menu (Opportunities only)
- Adds AMC-specific fields to opportunity records:
  - `therapeutic_area` — Char
  - `research_area` — Char
  - `service_category` — Selection (Sponsored Research, Licensing, Clinical Trial, Consulting, Data Sharing, Other)
  - `amc_partner_type` — Selection (Pharma, Biotech, MedTech, CRO, Foundation, Government, Academic, Other)
- Overrides kanban card to show Partner Organization instead of contact name
- Overrides search filters: "My Pipeline" → "My Partnerships", "Salesperson" → "Partnership Manager"

**Key files:**
- `models/crm_lead.py` — field string overrides + new AMC fields
- `data/partnership_stages.xml` — stage data (updates existing 4, creates 5 new)
- `data/menu_renames.xml` — `ir.ui.menu` record updates
- `views/crm_lead_views.xml` — form/kanban/search view inheritance
- `views/crm_team_views.xml` — team form/kanban label overrides

---

### `partnership_os_project`

**Depends on:** `partnership_os_crm`, `project`, `base_automation`

**What it does:**
- Adds `opportunity_id` (Many2one → `crm.lead`) to `project.project`
- Adds "Partnership Opportunity" column to the project list view
- Adds "Partnership Opportunity" field to the project form (Settings tab)
- Adds a **Projects** smart button on opportunity records (visible when projects exist)
- Installs an automation rule: when an opportunity's stage changes **to** "Agreement Executed",
  automatically creates a linked `project.project` (once — idempotent check prevents duplicates)

**Key files:**
- `models/project_project.py` — `opportunity_id` field
- `models/crm_lead.py` — `project_count` computed field + `action_view_linked_projects()`
- `data/automation_rules.xml` — `base.automation` record + `ir.actions.server` code action
- `views/crm_lead_views.xml` — Projects smart button
- `views/project_views.xml` — `opportunity_id` in project form and list

---

### `partnership_os_reporting`

**Depends on:** `partnership_os_project`, `account`, `spreadsheet_dashboard`

**Status:** Not yet installed — requires `spreadsheet_dashboard` to be installed in `odoo_dev` first.

**What it does:**
- Adds **BD Analytics** submenu under Partnerships → Reporting with three views:
  - **Revenue by Partner** — pivot/graph on `account.move.line` grouped by partner, by quarter
  - **Pipeline Forecast** — pivot/graph on open opportunities by stage and service category
  - **Closed Partnerships** — pivot/graph on won opportunities by partner and close quarter

**To install:**
```powershell
docker compose run --rm web odoo --db_host db --db_user odoo --db_password odoo `
    -d odoo_dev -i partnership_os_reporting --stop-after-init
docker compose restart web
```

---

## Startup Instructions

```powershell
# 1. Start all services
docker compose up -d

# 2. Tail logs to watch startup
docker compose logs -f web

# 3. Open the browser
#    http://localhost:8069
```

---

## Development Workflow

### Installing a PartnershipOS module for the first time

```powershell
docker compose run --rm web odoo --db_host db --db_user odoo --db_password odoo `
    -d odoo_dev -i <module_name> --stop-after-init
docker compose restart web
```

### Upgrading after editing a module

```powershell
docker compose run --rm web odoo --db_host db --db_user odoo --db_password odoo `
    -d odoo_dev -u <module_name> --stop-after-init
docker compose restart web
```

### Full reinstall of all three core modules

```powershell
docker compose run --rm web odoo --db_host db --db_user odoo --db_password odoo `
    -d odoo_dev -i partnership_os_base,partnership_os_crm,partnership_os_project --stop-after-init
docker compose restart web
```

### Adding a new custom field

1. Add the field to the relevant `models/*.py` file
2. Add it to the view in `views/*.xml` using `<inherit_id>` + xpath
3. Upgrade the module (see above) — Odoo handles the DB migration automatically

### Enabling Developer / Debug Mode

Option A — URL: append `?debug=assets` to any Odoo URL.

Option B — UI: Settings → General Settings → Developer Tools → Activate.

Option C — config: uncomment `dev_mode = assets` in `config/odoo.conf` and restart.

---

## Important Commands

```powershell
# Start
docker compose up -d

# Stop (keeps data)
docker compose down

# Destroy everything including volumes (WARNING: deletes all data)
docker compose down -v

# View web logs
docker compose logs -f web

# Open a shell inside the Odoo container
docker compose exec web bash

# Open a PostgreSQL prompt
docker compose exec db psql -U odoo -d odoo_dev

# List all databases
docker compose exec db psql -U odoo -d postgres -c "\l"

# Backup the database
docker compose exec db pg_dump -U odoo odoo_dev > backups/odoo_dev.dump

# Restore the database
docker compose exec -T db psql -U odoo -d odoo_dev < backups/odoo_dev.dump

# Pull updated images (then recreate)
docker compose pull
docker compose up -d --force-recreate
```

---

## Phases Completed / Remaining

| Phase | Description | Status |
|-------|-------------|--------|
| 1 | Navigation cleanup — hide irrelevant modules | ✅ Done |
| 2 | Terminology rename — Partnership language throughout | ✅ Done |
| 3 | CRM redesign — 9-stage pipeline, AMC fields | ✅ Done |
| 4 | Project integration — auto-create project on Agreement Executed | ✅ Done |
| 5 | Financial reporting — BD dashboards | ⏳ Module built, not yet installed |
| 6 | Branding — replace Odoo logo, login page | ❌ Not started |

---

## Configuration Reference

`config/odoo.conf` key options:

| Option | Current | Notes |
|--------|---------|-------|
| `addons_path` | `/mnt/extra-addons` | PartnershipOS modules dir |
| `data_dir` | `/var/lib/odoo` | Filestore location |
| `admin_passwd` | (none set) | Set before exposing to any network |
| `log_level` | `info` | `debug`, `info`, `warn`, `error`, `critical` |
| `workers` | `0` | 0 = single-process (dev mode) |
| `dev_mode` | (off) | Uncomment `dev_mode = assets` to enable |
