{
    'name': "Hospital Management System",
    'summary': "Hospital Management Module",
    'description': """ This Hospital Management Module is useful for Maintained the Patients record""",
    'author': 'Aetos Technologies',
    'company': 'Aetos Technologies',
    'maintainer': 'Aetos Technologies',
    'website': "https://aetostechnologies.com/",
    'category': 'Health',
    'version': '18.0.1.0.0',
    'depends': ['base','web'],
    'data': [
        'security/ir.model.access.csv',
        'views/patient_views.xml',
        'views/appointment_views.xml',
        'views/doctor_views.xml',
        'views/template_controller.xml',
        'views/assets.xml',



    ],
    'assets': {
        'web.assets_frontend': [
            '/hospital/static/src/css/custom.css',
            '/hospital/static/src/js/custom.js',
        ],
    'web.assets_backend': [
        '/hospital/static/src/component/listview/listview.css',
        '/hospital/static/src/component/listview/listview.js',
        '/hospital/static/src/component/listview/listview.xml',
        '/hospital/static/src/component/formview/formview.js',
        '/hospital/static/src/component/formview/formview.xml',
        '/hospital/static/src/component/formview/formview.css',

        '/hospital/static/src/component/doclist/doclist.css',
        '/hospital/static/src/component/doclist/doclist.js',
        '/hospital/static/src/component/doclist/doclist.xml',
        '/hospital/static/src/component/docform/docform.xml',
        '/hospital/static/src/component/docform/docform.js',
        '/hospital/static/src/component/docform/docform.css',

        '/hospital/static/src/component/appointmentformview/appointmentformview.css',
        '/hospital/static/src/component/appointmentformview/appointmentformview.js',
        '/hospital/static/src/component/appointmentformview/appointmentformview.xml',
        '/hospital/static/src/component/appointmentlistview/appointmentlistview.css',
        '/hospital/static/src/component/appointmentlistview/appointmentlistview.js',
        '/hospital/static/src/component/appointmentlistview/appointmentlistview.xml',

    ],
},
'application': True,
'images': ['static/description/icon.png'],
}


