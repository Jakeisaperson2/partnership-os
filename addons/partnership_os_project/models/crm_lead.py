from odoo import fields, models


class Lead(models.Model):
    _inherit = 'crm.lead'

    project_count = fields.Integer(
        string='Projects',
        compute='_compute_project_count',
    )

    def _compute_project_count(self):
        for lead in self:
            lead.project_count = self.env['project.project'].search_count(
                [('opportunity_id', '=', lead.id)]
            )

    def action_view_linked_projects(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Partnership Projects',
            'res_model': 'project.project',
            'view_mode': 'kanban,list,form',
            'domain': [('opportunity_id', '=', self.id)],
            'context': {
                'default_opportunity_id': self.id,
                'default_partner_id': self.partner_id.id,
                'default_name': '[Partnership] ' + (self.name or ''),
            },
        }
