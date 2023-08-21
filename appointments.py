from datetime import datetime

class Appointments:
    """
    1.   appointmentID: A unique identifier for each appointment (primary key)
    2.  patientID: A foreign key referencing the Patient table to associate the appointment with a specific patient.
    3.  appointmentDateTime: The date and time of the appointment.
    4.  doctorID: A foreign key referencing a Doctor table to associate the appointment with a specific doctor or healthcare professional.
    5.  appointmentType: A column indicating the type of appointment, such as "check-up," "follow-up," or "consultation."
    6.  duration: The duration of the appointment (e.g., in minutes or hours).
    7.  status: A column to track the status of the appointment, such as "scheduled," "confirmed," "canceled," or "completed."
    8.  reason: An optional column to capture the reason for the appointment or any additional notes.
    9.  createdAt: The timestamp indicating when the appointment was created.
    10.  UpdatedAt: The timestamp indicating the last modification of the appointment record.
    """

    def __init__(self, appointmentId, patientID, appointmentDateTime, doctorID, appointmentType, duration, status, reason,
                 createdAt=None, updatedAt=None):
        self.appointmentId = appointmentId
        self.patientID = patientID
        self.appointmentDateTime = appointmentDateTime
        self.doctorID = doctorID
        self.appointmentType = appointmentType
        self.duration = duration
        self.status = status
        self.reason = reason
        self.createdAt = createdAt or datetime.now()
        self.updatedAt = updatedAt or datetime.now()








