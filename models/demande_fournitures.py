import base64
from logging import warning
from odoo import api,models,fields,_
from odoo.exceptions import UserError
from datetime import datetime, timedelta
from odoo.modules.module import get_module_resource


class DemandeFournitures(models.Model):
    _name = 'demande.fournitures'
    _rec_name = 'reference'
    reference = fields.Char('Demande No.', default='REF',readonly=True)
    _inherit = ['mail.thread']

    @api.model
    def _default_image(self):
        image_path = get_module_resource('demande_fournitures', 'static/img', 'default_image.png')
        return base64.b64encode(open(image_path, 'rb').read())

    fields_image = fields.Image(default=_default_image)
    img2 = fields.Image(string='test')
    state = fields.Selection(
        [('brouillons','Brouillons'),('annuler','Annuler'),('fait','Fait'),('envoyer','Envoyer'),('valider','Valider par responsable'),
        ('valider2','Valider par gds'),('refuser','Refuser par responsable'),
        ('refuser2','Refuser par gds')],
        'Etat',default='brouillons'
    )
    etat = fields.Selection(
           [('brouillons','Brouillons'),('annuler','Annuler'),('fait','Fait'),('envoyer','Envoyer'),('valider','Valider par responsable'),
        ('valider2','Valider par gds'),('refuser','Refuser par responsable'),
        ('refuser2','Refuser par gds')],string = 'etats',default='brouillons')
    #relation Many2one avec hr.employee
    employer_id = fields.Many2one('hr.employee',string='Employer',required=True,
    )
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
    cat_id = fields.Many2one('product.category',string='Catégorie',required=True )

    #hr related fields

    #date fields
    date_demande = fields.Date('Date de demande',
    compute ='_d_demande')
    date_validation = fields.Date('Date de validation responsable',
    readonly=True)
    date_fin = fields.Date('Date de validation GDS',
    readonly=True)
    #one2many
    fournitures_lines_ids = fields.One2many("fournitures.lines","demande_fournitures_id")



    @api.model
    
    def allowed_transition (self,old_state,new_state):
        allowed = [
         ('brouillons','envoyer'),
         ('brouillons','annuler'),
         ('envoyer','refuser'),
         ('envoyer','refuser2'),        
         ('envoyer','valider'),        
         ('envoyer','valider2'),
         ('valider','valider2'),
         ('valider','refuser2'),        
        ]
        
        return (old_state,new_state) in allowed
    
    def change_state(self, new_state):
        for record in self:
            if record.allowed_transition(record.state,new_state):
                record.state = new_state
            else:
                msg = _('moving from %s to %s is not allowed' ) %(record.state, new_state)
                raise UserError(msg)

    def make_valide2(self):
        # self.change_state('valider2')
        self.date_fin= fields.Datetime.today()
        if (self.employer_id.user_id.partner_id.id):
            notification_ids = [((0, 0, {
           'res_partner_id': self.employer_id.user_id.partner_id.id,
           'notification_type': 'inbox'}))]
            # use_id = self.env.user.id
            message = ("Bonjour,Votre demande de fourniture a été validé par le gds ")
            channel_id=self.env['mail.channel'].sudo().search([('name','=','Picking Validated')])
                # find if a channel was opened for this user before

            channel = self.env['mail.channel'].sudo().search([

                    ('name', '=', 'Picking Validated'),

                ],

                limit=1,

                )



            if not channel:

                    # create a new channel

                    channel = self.env['mail.channel'].with_context(mail_create_nosubscribe=True).sudo().create({

                        'channel_partner_ids': [(4, self.employer_id.user_id.id), (4, odoobot_id)],

                        'public': 'private',

                        'channel_type': 'chat',

                        'email_send': False,

                        'name': f'Picking Validated',

                        'display_name': f'Picking Validated',

                    })

            channel_id=self.env['mail.channel'].sudo().search([('name','=','Picking Validated')])

            channel_id.message_post(author_id=self.employer_id.user_id.partner_id.id,
                            body=(message),
                            message_type='comment',
                            #subtype_xmlid="mail.mt_comment",
                            notification_ids=notification_ids,
                            partner_ids=[self.employer_id.user_id.partner_id.id],
                            subtype="mail.mt_comment",
                            #notify_by_email=False,
                            )
        else : 
            notification_ids = [((0, 0, {
           'res_partner_id': self.employer_id.parent_id.user_id.partner_id.id,
           'notification_type': 'inbox'}))]
            # use_id = self.env.user.id
            message = ("Bonjour,Votre demande de fourniture a été validé par le gds ")
            channel_id=self.env['mail.channel'].sudo().search([('name','=','Picking Validated')])
                # find if a channel was opened for this user before

            channel = self.env['mail.channel'].sudo().search([

                    ('name', '=', 'Picking Validated'),

                ],

                limit=1,

                )



            if not channel:

                    # create a new channel

                    channel = self.env['mail.channel'].with_context(mail_create_nosubscribe=True).sudo().create({

                        'channel_partner_ids': [(4, self.employer_id.parent_id.user_id.id), (4, odoobot_id)],

                        'public': 'private',

                        'channel_type': 'chat',

                        'email_send': False,

                        'name': f'Picking Validated',

                        'display_name': f'Picking Validated',

                    })

            channel_id=self.env['mail.channel'].sudo().search([('name','=','Picking Validated')])

            channel_id.message_post(author_id=self.employer_id.parent_id.user_id.partner_id.id,
                            body=(message),
                            message_type='comment',
                            #subtype_xmlid="mail.mt_comment",
                            notification_ids=notification_ids,
                            partner_ids=[self.employer_id.parent_id.user_id.partner_id.id],
                            subtype="mail.mt_comment",
                            #notify_by_email=False,
                            )


        # CREATING IN PURCHASE 
        warning('***********************')
        product =[]
        for rec in self: 
            for item in rec.fournitures_lines_ids:
                line1 = (0, 0, {
            'product_id': item.article.id,
            'product_qty': item.qte,
        })
                product.append(line1)
                
            self.env['purchase.requisition'].create({
                    'name': rec.reference,
                    'line_ids': product,
                })
                




    def make_valide(self):
        self.change_state('valider')
        self.date_validation= fields.Datetime.today()


    def make_annuler(self):
        self.change_state('annuler')

    def make_refuser(self):
        self.change_state('refuser')

    def make_refuser2(self):
            self.change_state('refuser2')

    def make_envoyer(self):
        self.change_state('envoyer')

    @api.model
    def create(self, vals):
        vals['reference'] = self.env['ir.sequence'].next_by_code('demande.fournitures')
        return super(DemandeFournitures, self).create(vals)
    
    
    def unlink(self):
        warning(self.env.context)
        if (self.state=='brouillons'):
            ret = super(DemandeFournitures,self).unlink()
        else :
            raise models.ValidationError('Vous pouvez pas supprimer cette demande')
            
        return ret


    def write(self, vals):
        return super(DemandeFournitures, self).write(vals)

    
    @api.depends('date_demande')
    def _d_demande(self):
        for record in self :
            record.date_demande = fields.Datetime.now()


#PRINT REPORT FUNCTION

    def action_print_report(self):
        return self.env.ref('demande_fournitures.action_fourniture_id_card').report_action(self.id)
            

class FournituresLines(models.Model):

    _name="fournitures.lines"
    article = fields.Many2one("product.product", string="Article",required=True)
    qte = fields.Integer("Quantité")
    demande_fournitures_id = fields.Many2one('demande.fournitures',required=True)

    @api.constrains('qte')
    def _check_release_date(self):
        for record in self:
            if (record.qte==0):
                raise models.ValidationError('La quantité doit etre superieur a zero'
                )
