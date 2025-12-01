from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required
from app.decorators import admin_required
from app.models.user import User
from app.models.doctor import Doctor
from app.models.patient import Patient
from app.forms.admin_forms import SearchForm
from app import db

admin_search_bp = Blueprint('admin_search', __name__)

@admin_search_bp.route('/search', methods=['GET', 'POST'])
@login_required
@admin_required
def search():
    form = SearchForm()
    results = {'doctors': [], 'patients': []}
    
    if form.validate_on_submit():
        query = form.query.data
        search_type = form.search_type.data
        
        if search_type in ['all', 'doctors']:
            results['doctors'] = Doctor.query.filter(
                (Doctor.name.ilike(f'%{query}%')) | (Doctor.specialization.ilike(f'%{query}%'))
            ).all()
        
        if search_type in ['all', 'patients']:
            results['patients'] = Patient.query.filter(
                (Patient.name.ilike(f'%{query}%')) | (Patient.phone.ilike(f'%{query}%'))
            ).all()
    
    return render_template('admin/search.html', form=form, results=results)

@admin_search_bp.route('/users/<int:id>/toggle_status', methods=['POST'])
@login_required
@admin_required
def toggle_user_status(id):
    user = User.query.get_or_404(id)
    
    if user.role == 'admin':
        flash('Cannot deactivate admin accounts.', 'danger')
    else:
        user.is_active = not user.is_active
        db.session.commit()
        status = 'activated' if user.is_active else 'deactivated'
        flash(f'User {user.email} has been {status}.', 'success')
    
    return redirect(url_for('admin_search.search'))
