# This script contains the logic which pairs a patient to a psychiatrist upon registration.

# Imports -------------------------------------------------------------------------------------
from os import abort

from sqlalchemy import func

from flaskr import db
from flaskr.register.models import Psychiatrist, Patient


# Define Function ------------------------------------------------------------------------------

def psychiatrist_assign_function():
    # We assign each patient a new psychiatrist upon registering an account.
    # A patient should not be able to register if no psychiatrists are registered in  system.

    count_psychiatrists = db.session.query(
        func.count(Psychiatrist.bacp_number))  # Counts the number of psychiatrists in our database.

    print('\n------------------------------------- START SQL RAW QUERY -------------------------------------\n')
    print(count_psychiatrists)  # Outputs the raw SQL query to the terminal.
    print('\n------------------------------------- END SQL RAW QUERY -------------------------------------\n')

    count_patients = db.session.query(
        func.count(Patient.username))  # Counts the number of patients in our database.

    print('\n------------------------------------- START SQL RAW QUERY -------------------------------------\n')
    print(count_patients)  # Outputs the raw SQL query to the terminal.
    print('\n------------------------------------- END SQL RAW QUERY -------------------------------------\n')

    #  SELECT COUNT(bacp_number) AS num_psychiatrists
    #  FROM psychiatrist_table;

    (number_of_psychiatrists, ) = count_psychiatrists.one()  # Here, we unpack the tuple which our query returns.
    print(f"The number of psychiatrists is: {number_of_psychiatrists}")

    (number_of_patients, ) = count_patients.one()
    print(f"The number of patients is: {number_of_patients}")

    if number_of_psychiatrists == 0:

        print("\nThere are no psychiatrists currently in our table!\n")

        chosen_psychiatrist = None

        # If there is only one psychiatrist, or no patients, the logic below won't work.

    elif number_of_psychiatrists == 1 or number_of_patients == 0:

        # In this case, we just want to assign a value to the first available psychiatrist.

        (only_psychiatrist,) = db.session.query(Psychiatrist.bacp_number).first()

        print(f'\nThe first available psychiatrist is: {only_psychiatrist}')

        chosen_psychiatrist = only_psychiatrist

    else:  # We are free to assign the user a psychiatrist.
        # To prevent overworking psychiatrists, we assign our patient to the psychiatrist with the least # of patients.

        # The following query searches for the psychiatrist with the least number of patients assigned to them.

        psych_search = db.session.query(Patient.psychiatrist_id, func.count(Patient.psychiatrist_id))  # Step 1
        psych_search = psych_search.group_by(Patient.psychiatrist_id)  # Step 2


        print('\n------------------------------------- START SQL RAW QUERY -------------------------------------\n')
        print(psych_search)  # Outputs the raw SQL query to our terminal.
        print('\n------------------------------------- END SQL RAW QUERY -------------------------------------\n')

        # SELECT patient.psych_id, COUNT(Patient.username)
        # FROM patient_table
        # GROUP_BY bacp_number

        chosen_psychiatrist = psych_search.all()

        print(f'\nThe psychiatrist with the least number of people assigned to them is: {chosen_psychiatrist}')

    print(f'\nThe chosen psychiatrist is: {chosen_psychiatrist}.\n')

    return chosen_psychiatrist
