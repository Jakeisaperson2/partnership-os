# PartnershipOS

**A partnership and business-development platform for academic medical centers, built as custom modules on Odoo 17 Community.** It turns Odoo's general-purpose CRM into a tool for managing industry partnerships, sponsored research, licensing deals, and the projects that follow them.

![Odoo](https://img.shields.io/badge/Odoo-17.0_Community-714B67?logo=odoo&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-4169E1?logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker_Compose-2496ED?logo=docker&logoColor=white)
![License: LGPL-3](https://img.shields.io/badge/License-LGPL--3-blue.svg)

---

## Why

Off-the-shelf CRMs are built for sales teams selling products. Academic medical center BD teams work differently: long partnership cycles, research agreements, licensing, and hand-offs into funded projects. PartnershipOS reshapes Odoo around that workflow instead of making the team fit a sales tool.

## Features

- **9-stage partnership pipeline**: Identified → Outreach → Intro Meeting → Assessment → Proposal → Negotiation → Agreement Executed → Active Project → Completed
- **Domain-specific fields**: therapeutic area, research area, service category (sponsored research, licensing, clinical trial…), and partner type (pharma, biotech, MedTech, CRO, foundation…)
- **Partnership terminology throughout**: "CRM" becomes *Partnerships*, "Customers" become *Partner Organizations*, "Salesperson" becomes *Partnership Manager*
- **Automatic project creation**: moving a deal to *Agreement Executed* creates a linked project (idempotent), and opportunities show a smart button to their projects
- **BD analytics**: revenue by partner, pipeline forecast, and closed partnerships by quarter
- **Streamlined UI**: hides unused ERP apps (inventory, manufacturing, POS…) and applies custom branding

## Modules

All customization lives in `addons/` as installable Odoo modules, layered in a dependency chain:

| Module | Purpose |
|---|---|
| [`partnership_os_base`](addons/partnership_os_base) | Navigation cleanup and brand styling |
| [`partnership_os_crm`](addons/partnership_os_crm) | Pipeline stages, AMC fields, terminology, view overrides |
| [`partnership_os_project`](addons/partnership_os_project) | Opportunity ↔ project link and auto-creation rule |
| [`partnership_os_reporting`](addons/partnership_os_reporting) | BD dashboards (pivot and graph views) |

```
partnership_os_base → partnership_os_crm → partnership_os_project → partnership_os_reporting
```

## Quick Start

**Requires:** [Docker Desktop](https://www.docker.com/products/docker-desktop/), with port 8069 free.

```bash
git clone https://github.com/Jakeisaperson2/partnership-os.git
cd partnership-os
cp .env.example .env          # then set your own Postgres password
docker compose up -d
```

Open **http://localhost:8069** and create a database (for example `odoo_dev`). Then install the modules:

```bash
docker compose run --rm web odoo --db_host db --db_user odoo --db_password <your-password> \
  -d odoo_dev -i partnership_os_base,partnership_os_crm,partnership_os_project --stop-after-init
docker compose restart web
```

After editing a module, upgrade it with `-u <module_name>` in place of `-i`.

## Project Structure

```
partnership-os/
├── docker-compose.yml     # Postgres 15 + Odoo 17 services
├── .env.example           # Database credential template
├── config/odoo.conf       # Odoo server configuration
├── addons/                # PartnershipOS custom modules
│   └── partnership_os_*/  # models/, views/, data/, __manifest__.py
└── backups/               # Local database dumps (gitignored)
```

## Common Commands

| Task | Command |
|---|---|
| Start | `docker compose up -d` |
| Stop (keep data) | `docker compose down` |
| Full reset | `docker compose down -v` |
| Logs | `docker compose logs -f web` |
| Backup | `docker compose exec db pg_dump -U odoo odoo_dev > backups/odoo_dev.dump` |

## Roadmap

- [x] Navigation cleanup, terminology, and pipeline redesign
- [x] Project integration and automation
- [ ] Install and polish the reporting dashboards
- [ ] Full rebranding (logo and login page)

## License

[LGPL-3.0](LICENSE), matching the Odoo Community module license declared in each manifest.
