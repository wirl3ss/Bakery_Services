# User

class UsernameAlreadyExistsError(Exception):
    pass

class EmailAlreadyExistsError(Exception):
    pass

class UserAlreadyExistsError(Exception):
    pass

class UserNotFoundError(Exception):
    pass

class UnableToUpdateUserError(Exception):
    pass

class UnableToDeleteUserError(Exception):
    pass

# Student

class StudentAlreadyExistsError(Exception):
    pass

class StudentNotFoundError(Exception):
    pass

class UnableToDeleteStudentError(Exception):
    pass

# School

class SchoolNameAlreadyExistsError(Exception):
    pass

class SchoolAddressAlreadyExistsError(Exception):
    pass

class SchoolNotFoundError(Exception):
    pass

class UnableToDeleteSchoolError(Exception):
    pass