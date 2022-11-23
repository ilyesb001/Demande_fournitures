from odoo import api,models,fields

class DemandeFournitures(models.Model):
    _name = 'demande.fournitures'
    nom = fields.Char('Reference')
    state = fields.Selection(
        [('brouillons','brouillons'),('annuler','annuler'),('fait','fait')],
        'Etat'
    )
    #relation Many2one avec hr.employee
    employer_id = fields.Many2one('hr.employee',string='employé' )

    #hr related fields

    employer = fields.Char('Employer',
    related='employer_id.name',readonly=True)

    societe = fields.Many2one(
    related='employer_id.company_id',readonly=True)

    direction = fields.Many2one(
    related='employer_id.department_id',readonly=True)

    responsable = fields.Many2one(
    related='employer_id.parent_id')


    #relation Many2one avec purchase
    cat_id = fields.Many2one('product.template',string='categorie' )

    #hr related fields
    categ = fields.Many2one(
    related='cat_id.categ_id')
    #date fields
    date_demande = fields.Date('date de demande')
    date_validation = fields.Date('date de validation')
    date_fin = fields.Date('date de fin')

