from flask import (
    Blueprint, current_app, redirect, render_template, request, flash, url_for
)
import sendgrid
from sendgrid.helpers.mail import *
from app.db import get_db

bp = Blueprint('mail', __name__, url_prefix="/")

@bp.route('/', methods=['GET'])
def index():
    search_query = request.args.get('search')
    db, c = get_db()
    
    if search_query is None:
        c.execute("SELECT * FROM email")
    else:
        c.execute("SELECT * from email WHERE content like %s", ('%' + search_query + '%',))
        
    mails = c.fetchall()
    return render_template('mails/index.html', mails=mails)

@bp.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        email = request.form.get('email')
        subject = request.form.get('subject')
        content = request.form.get('content')
        errors = []
        
        if not email:
            errors.append('Email es obligatorio')
        if not subject:
            errors.append('Asunto es obligatorio')
        if not content:
            errors.append('Contenido es obligatorio')

        if len(errors) == 0:
            try:
                send(email, subject, content)
                db, c = get_db()
                c.execute("INSERT INTO email (email, subject, content) VALUES (%s, %s, %s)", (email, subject, content))
                db.commit()
                return redirect(url_for('mail.index'))
            except Exception as e:
                flash(f'Error al guardar el correo: {e}')
        else:
            for error in errors:
                flash(error)

    return render_template('mails/create.html')

def send(to, subject, content):
    try:
        sg = sendgrid.SendGridAPIClient(api_key=current_app.config['SENDGRID_KEY'])
        from_email = Email(current_app.config['FROM_EMAIL'])
        to_email = To(to)
        content = Content('text/plain', content)
        mail = Mail(from_email, to_email, subject, content)
        response = sg.client.mail.send.post(request_body=mail.get())
        
        if response.status_code != 202:
            print(f"Error al enviar el correo: {response.status_code}")
    except Exception as e:
        print(f"Error en SendGrid: {e}")
