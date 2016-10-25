from wscoc_directory import app
from flask import render_template, request, jsonify
from forms import EmailForm

@app.route('/')
def index():

    return render_template('layout.html')

@app.route('/email')
def email():
    form = EmailForm()

    return render_template('email.html', form=form)

@app.route('/fixed', methods=['POST'])
def fixed():
    extras = []
    master_list = set(request.form['id_master'].split('\n'))
    contacts_list = set(request.form['id_contacts'].split('\n'))
    full_group_list = set()
    for i in range(1,6):
        group_list = set(request.form['id_group_%d' % i].split('\n'))
        extra_list = group_list.difference(master_list)
        full_group_list = full_group_list | group_list
        text = '\n'.join(extra_list)
        extras.append({
            'label_id':'id_group%d_extra_label' % i,
            'textarea_id':'id_group%d_extra' % i,
            'id':'%d' % i,
            'text':text
        })
    unassigned = {'text':'\n'.join(master_list.difference(full_group_list))}
    contacts_missing = {'text':'\n'.join(master_list.difference(contacts_list))}
    contacts_extra = {'text':'\n'.join(contacts_list.difference(master_list))}

    #TODO: We should always redirect on a post
    return render_template('fixed.html', extras=extras, unassigned=unassigned, contacts_extra=contacts_extra, contacts_missing=contacts_missing)

@app.route('/_clean_email_lists', methods=['POST'])
def _clean_email_lists():
    request.get_json()
    v = jsonify(
        group1_extra=[''],
        group2_extra=[''],
        group3_extra=[''],
        group4_extra=[''],
        group5_extra=[''],
        unassigned=['']
    )
    return v