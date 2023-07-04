from flask import Flask, request, jsonify
from database import Database
from patient import Patient

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
            # Return the response as JSON if a patient is found
            return jsonify(response), 200
        # return a 404 if patient is not in database
        else:
            return jsonify({'message':'Patient not found'}), 404
    else:
        return jsonify({'message': 'Database connection error'}), 500




if __name__ == '__main__':
    app.run(port=5003)


