# This blueprint handles configuration of the logged-in users' dashboard with correct information.

# Imports -------------------------------------------------------------------------------------------------

from flask import Blueprint, render_template

from flask_login import current_user, login_required

# Blueprint Configuration --------------------------------------------------------------------------------


dashboard_bp = Blueprint(
    'dashboard_bp',  # Name we want to assign to our Blueprint for Flask's internal routing purposes.
    __name__,
    template_folder='templates'
)


# Shared Routes ------------------------------------------------------------------------------------------

@dashboard_bp.route('/dashboard', methods=['GET'])
@login_required
def dashboard():

    return render_template(
        'dashboard/dashboard_layout.html',
        title=' Dashboard ~ MiWell'
    )


# User Dashboard ---------------------------------------------------------------------------------------

@dashboard_bp.route('/dashboard/your_progress', methods=['GET'])
@login_required
def user_progress():

    # print(current_user.user_authentication) FOR MANUAL DEBUGGING.

    return render_template(
        'dashboard/user_dash/user_progress.html',
        title=' Your Progress ~ MiWell'
    )


@dashboard_bp.route('/dashboard/your_tools', methods=['GET'])
@login_required
def user_tools():
    return render_template(
        'dashboard/user_dash/user_tools.html',
        title=' Mindfulness Tools ~ MiWell'
    )


# Psychiatrist Dashboard ------------------------------------------------------------------------------

@dashboard_bp.route('/dashboard/my_patients', methods=['GET'])
@login_required
def my_patients():
    return render_template(
        'dashboard/psych_dash/my_patients.html',
        title=' My Patients ~ MiWell'
    )


@dashboard_bp.route('/dashboard/psychiatrist_tools', methods=['GET'])
@login_required
def psychiatrist_tools():
    return render_template(
        'dashboard/psych_dash/psychiatrist_tools.html',
        title=' psychiatrist Tools ~ MiWell'
    )
