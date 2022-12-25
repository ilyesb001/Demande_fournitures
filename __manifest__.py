{
'name': "Demande fournitures",
'summary': "faire des demandes de fournitures",
'description': """
Manage Library
==============
""",
'author': "ilyes belbahi",
'website': "http://www.example.com",
'category': 'Fournitures',
'version': '13.0.1',
'depends': ['base','hr','purchase','mail'],
'images': ['static/img/default_image.png'],
'data': ['security/ir.model.access.csv','security/groups.xml','security/security_rules.xml','data/data.xml','views/views.xml',
'report/report.xml','report/demande_fournitures_template.xml','views/external_layout.xml'
],

'demo': ['demo.xml'],
}
