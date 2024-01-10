
class User:
    # required fields to create a user
    firstName = None
    lastName = None
    centerName = None
    centerId = None
    uniqueName = None
    email = None
    password = None
    isAdmin = False

    # not mandatory fields
    img = None
    city = None
    state = None
    country = "INDIA"
    phone = None
    fullName = None


class AIIMSJDPUser:
    centerName = "AIIMS JODHPUR"
    centerId = "AIIMS_JDP"
    allowedPermissions = [
        {
            "recordStethoscope": False,
            "showSuspectedLungCancer": True
        }
    ]

    city = "jodhpur"
    state = "rajasthan"
    country = "INDIA"
    fullName = None


class CompanyUser:
    centerName = "DIY Healthcare"
    centerId = "DIYH_GGN"

    city = "gurugram"
    state = "haryana"
    country = "INDIA"
    fullName = None

class TESTUser:
    centerName = "Test User"
    centerId = "test_user"
    allowedPermissions = [
        {
            "recordStethoscope": True,
            "showSuspectedLungCancer": False
        }
    ]

    city = "test"
    state = "test"
    country = "INDIA"
    fullName = None

class DrAshvendraUser:
    centerName = "Dr Ashvendra Chawla"
    centerId = "DR_CHAWLA"

    city = "hisar"
    state = "haryana"
    country = "INDIA"
    fullName = None