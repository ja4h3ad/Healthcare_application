from flask import Flask, request, jsonify
from database import Database
from patient import Patient
from datetime import datetime
from appt_mappings import duration_mapping, status_mapping, reason_mapping
# load imports
import os
from os.path import join, dirname
from dotenv import load_dotenv
import vonage
dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

app = Flask(__name__)


# Endpoint to receive the webhook
@app.route('/patient', methods=['GET'])
def patient_webhook():
    print("Reached the webhook function")
    phone_number = request.args.get('phone_number')
    print("Phone number:", phone_number)

    database = Database()
    conn = database.connect()
    if conn is not None:
        cursor = conn.cursor()
        print("You have made a SQL connection")
        query = f"SELECT * FROM patientData WHERE mobileNumber = '{phone_number}'"
        cursor.execute(query)
        patient_data = cursor.fetchone()
        if patient_data:
            patient = Patient(*patient_data)
            print(f"Patient: {patient}")
            # Create a response dictionary with patient data
            response = {
                'message': 'Patient found',
                'patient': {
                    'id': patient.id,
                    'firstName': patient.firstName,
                    'lastName': patient.lastName,
                    'dob': str(patient.dob),
                    'mobileNumber': patient.mobileNumber,
                    'accountNumber': patient.accountNum,
                    'streetAddress': patient.streetAddress,
                    'city': patient.city,
                    'state': patient.state,
                    'postCode': patient.postCode,
                    'createdAt': str(patient.createdAt),
                    'updatedAt': str(patient.updatedAt)
                }
            }
            # Check for existing appointments
            appointments = database.get_patient_appointments(patient.id)
            if appointments:
                appointment_info = []
                for appointment in appointments:
                    appointment_date_time = appointment[2]
                    appointment_date = appointment_date_time.strftime("%Y-%m-%d")
                    appointment_time = appointment_date_time.strftime("%H:%M:%S")

                    appointment_info.append({
                        'appointmentId': appointment[0],
                        'appointmentDate': appointment_date,
                        'appointmentTime': appointment_time,
                        'doctorID': appointment[3],
                        'appointmentType': appointment[4],
                        'duration': appointment[5],
                        'status': appointment[6],
                        'reason': appointment[7],
                        'createdAt': str(appointment[8]),
                        'updatedAt': str(appointment[9])
                    })
                response['appointments'] = appointment_info


            # Return the response as JSON if a patient is found
            return jsonify(response), 200
        # return a 404 if patient is not in database
        else:
            return jsonify({'message':'Patient not found'}), 404
    else:
        return jsonify({'message': 'Database connection error'}), 500



# Endpoint to create the appointment
# Endpoint to create the appointment
@app.route('/create_appointment', methods=['POST'])
def create_appointment():
    print("Reached the webhook function")
    appointment_data = request.get_json()
    patientID = appointment_data.get('patient_id')
    phone_number = appointment_data.get('phone_number')
    appointmentType = appointment_data.get('appointment_type')
    appointmentDate = appointment_data.get('appointment_date')
    appointmentTime = appointment_data.get('appointment_time')
    print(appointmentTime)
    appointmentRoute = appointment_data.get('appointment_route')
    appointmentDuration = appointment_data.get('appointment_duration')
    appointmentStatus = appointment_data.get('appointment_status')
    appointmentReason = appointment_data.get('appointment_reason')

    # Parse the appointmentTime into a datetime object
    appointmentTime_datetime = datetime.strptime(appointmentTime, '%H:%M:%S')

    # Convert appointmentDate to datetime.date object
    appointmentDate = datetime.strptime(appointmentDate, '%Y-%m-%d').date()

    # Combine date and time to create appointmentDateTime
    appointmentDateTime = datetime.combine(appointmentDate, appointmentTime_datetime.time())

    print(appointmentDateTime)  # Verify that appointmentDateTime is created correctly
    # # Combine date and time to create appointmentDateTime
    # appointmentDateTime = datetime.strptime(appointmentDate + ' ' + appointmentTime, '%Y-%m-%d %H:%M:%S')


    # Query the doctorData table to find the matching provider based on the appointment_route designator
    if appointmentRoute == 'Physician':
        query = "SELECT * FROM doctorData LIMIT 1"
    else:
        query = "SELECT * FROM doctorData LIMIT 4, 1"  # Get the 5th entry

    # Create a new appointment in the database using the Database class
    database = Database()
    conn = database.connect()
    if conn is not None:
        cursor = conn.cursor()
        print("You have made a SQL connection")

        # Execute the query to get the service provider
        cursor.execute(query)

        # Get the service provider from the result
        provider = cursor.fetchone()

        if provider:
            query = "INSERT INTO appointments (appointmentDateTime, patientID, doctorID, appointmentType, duration, status, reason) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            values = (
                appointmentDateTime,
                patientID,
                provider[0],
                appointmentType,
                appointmentDuration,
                appointmentStatus,
                appointmentReason,
            )
            cursor.execute(query, values)
            conn.commit()

            # Create a response dictionary with appointment data
            response = {
                'message': 'Appointment created successfully',
                'appointment': {
                    'appointment_id': cursor.lastrowid,  # Retrieve the last inserted ID
                    'appointment_date': appointmentDate,
                    'appointment_time': appointmentTime,
                    'patient_id': patientID,
                    'doctor_id': provider[0],  # Assuming the provider ID is in the first column
                    'doctor_first_name': provider[1],
                    'doctor_last_name': provider[2],
                    'appointment_type': appointmentType,
                    'duration': appointmentDuration,  # Replace with actual duration value
                    'status': appointmentStatus,  # Replace with actual status value
                    'reason': appointmentReason,  # Replace with actual reason value
                    'created_at': str(datetime.now()),
                    'updated_at': str(datetime.now())
                }
            }

            cursor.close()
            conn.close()

            return jsonify(response), 200

    return jsonify({'message': 'Invalid appointment route'}), 400


# App routes for Vonage Meetings API
# fetch the Vonage Application ID from .env - this is important to generate the JWT
VONAGE_APPLICATION_ID = os.environ.get("VONAGE_APPLICATION_ID")
# fetch the private key path generated from the project settings from .env - this is important to generate the JWT
VONAGE_APPLICATION_PRIVATE_KEY_PATH = os.environ.get("VONAGE_APPLICATION_PRIVATE_KEY_PATH")

# # create meeting room theme based on service provider name
# @app.route("/create_meeting_theme")
# def create_meeting_room():
#     main_color = #f3f6f4
#     brand_text =
#     return



if __name__ == '__main__':
    app.run(port=5003)

