from odoo import fields, models


class Lead(models.Model):
    _inherit = 'crm.lead'

    # ── Terminology overrides ────────────────────────────────────────────────
    user_id = fields.Many2one('res.users', string='Partnership Manager')
    team_id = fields.Many2one('crm.team', string='BD Team')
    expected_revenue = fields.Monetary(string='Estimated Opportunity Value')

    # ── AMC-specific fields ──────────────────────────────────────────────────
    therapeutic_area = fields.Char(string='Therapeutic Area')
    research_area = fields.Char(string='Research Area')
    service_category = fields.Selection(
        selection=[
            ('sponsored_research', 'Sponsored Research'),
            ('licensing', 'Licensing & Technology Transfer'),
            ('clinical_trial', 'Clinical Trial'),
            ('consulting', 'Scientific Consulting'),
            ('data_sharing', 'Data Sharing Agreement'),
            ('other', 'Other'),
        ],
        string='Service Category',
    )
    amc_partner_type = fields.Selection(
        selection=[
            ('pharma', 'Pharmaceutical'),
            ('biotech', 'Biotechnology'),
            ('medtech', 'Medical Device / MedTech'),
            ('cro', 'CRO / Research Organization'),
            ('foundation', 'Foundation / Non-Profit'),
            ('government', 'Government / Federal'),
            ('academic', 'Academic Institution'),
            ('other', 'Other'),
        ],
        string='Partner Type',
    )
