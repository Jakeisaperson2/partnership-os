from odoo import fields, models


class Project(models.Model):
    _inherit = 'project.project'

    opportunity_id = fields.Many2one(
        comodel_name='crm.lead',
        string='Partnership Opportunity',
        domain=[('type', '=', 'opportunity')],
        ondelete='set null',
        index=True,
    )
