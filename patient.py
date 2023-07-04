from datetime import datetime

class Patient:
    def __init__(self, id, firstName, lastName, dob, mobileNumber, accountNumber, streetAddress, city, state, postCode,
                 createdAt=None, updatedAt=None):
        self.id = id
        self.firstName = str(firstName)
        self.lastName = str(lastName)
        self.dob = datetime.strptime(str(dob), "%Y-%m-%d").date()
        self.mobileNumber = str(mobileNumber)
        self.accountNum = str(accountNumber)
        self.streetAddress = str(streetAddress)
        self.city = str(city)
        self.state = str(state)
        self.postCode = str(postCode)

        if createdAt:
            self.createdAt = datetime.strptime(str(createdAt), "%Y-%m-%d %H:%M:%S")
        else:
            self.createdAt = datetime.now()

        if updatedAt:
            self.updatedAt = datetime.strptime(str(updatedAt), "%Y-%m-%d %H:%M:%S")
        else:
            self.updatedAt = datetime.now()
