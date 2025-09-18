from enum import Enum


class RoleType(str, Enum):
    EMPLOYEE = "employee"
    ADMIN = "admin"
    ASSISTANT_NURSE = "assistant_nurse"
    CARE_ASSISTANT = "care_assistant"
    USER = "user"


class CareLevel(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class ShiftType(str, Enum):
    MORNING = "MORNING"
    DAY = "DAY"
    EVENING = "EVENING"
    NIGHT = "NIGHT"


class AbsenceType(str, Enum):
    SICK = "sick"
    VAB = "vab"
    VACATION = "vacation"
    PARENTAL_LEAVE = "parental_leave"
    LEAVE_OF_ABSCENCE = "leave_of_absence"


class VisitStatus(str, Enum):
    PLANNED = "planned"
    COMPLETED = "completed"
    CANCELED = "canceled"
    NO_SHOW = "no_show"
    PARTIALLY_COMPLETED = "partially_completed"
    RESCHEDULED = "rescheduled"


class TimeOfDay(str, Enum):
    MORNING = "morning"
    DAY = "day"
    EVENING = "evening"
    NIGHT = "night"


class TimeFlexibility(str, Enum):
    STRICT = "strict"
    STANDARD = "standard"
    FLEXIBLE = "flexible"


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    UNSPECIFIED = "unspecified"
