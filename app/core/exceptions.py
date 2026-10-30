class DomainError(Exception):
    status_code: int = 400

    def __init__(self, message: str = "A domain error occurred"):
        self.message = message
        super().__init__(self.message)

# User Errors
class UsernameAlreadyExistsError(DomainError):
    status_code = 409
class EmailAlreadyExistsError(DomainError):
    status_code = 409
class UserAlreadyExistsError(DomainError):
    status_code = 409
class UserNotFoundError(DomainError):
    status_code = 404
class UnableToUpdateUserError(DomainError):
    status_code = 400
class UnableToDeleteUserError(DomainError):
    status_code = 400

# Student Errors
class StudentAlreadyExistsError(DomainError):
    status_code = 409
class StudentNotFoundError(DomainError):
    status_code = 404
class UnableToUpdateStudentError(DomainError):
    status_code = 400
class UnableToDeleteStudentError(DomainError):
    status_code = 400

# School
class SchoolNameAlreadyExistsError(DomainError):
    status_code = 409
class SchoolAddressAlreadyExistsError(DomainError):
    status_code = 409
class SchoolNotFoundError(DomainError):
    status_code = 404
class UnableToUpdateSchoolError(DomainError):
    status_code = 400
class UnableToDeleteSchoolError(DomainError):
    status_code = 400

# Shop
class ShopAlreadyExistsError(DomainError):
    status_code = 409
class ShopNotFoundError(DomainError):
    status_code = 404
class UnableToDeleteShopError(DomainError):
    status_code = 400

# Product
class ProductAlreadyExistsError(DomainError):
    status_code = 409
class ProductNotFoundError(DomainError):
    status_code = 404
class UnableToUpdateProductError(DomainError):
    status_code = 400
class UnableToDeleteProductError(DomainError):
    status_code = 400

# Order
class UnableToCreateOrderError(DomainError):
    status_code = 400
class OrderNotFoundError(DomainError):
    status_code = 404
class UnableToUpdateOrderError(DomainError):
    status_code = 400
class UnableToDeleteOrderError(DomainError):
    status_code = 400

# WeeklySchedule
class WeeklyScheduleAlreadyExistsError(DomainError):
    status_code = 409
class UnableToCreateWeeklyScheduleError(DomainError):
    status_code = 400
class WeeklyScheduleNotFoundError(DomainError):
    status_code = 404
class UnableToUpdateWeeklyScheduleError(DomainError):
    status_code = 400
class UnableToDeleteWeeklyScheduleError(DomainError):
    status_code = 400

# CalendarException
class CalendarExceptionAlreadyExistsError(DomainError):
    status_code = 409
class UnableToCreateCalendarExceptionError(DomainError):
    status_code = 400
class CalendarExceptionNotFoundError(DomainError):
    status_code = 404
class UnableToUpdateCalendarExceptionError(DomainError):
    status_code = 400
class UnableToDeleteCalendarExceptionError(DomainError):
    status_code = 400