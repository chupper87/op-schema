from typing import List
from datetime import datetime, date as date_type, timezone

from sqlalchemy import (
    ForeignKey,
    Integer,
    String,
    Float,
    Boolean,
    DateTime,
    Date,
    func,
    Text,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from Backend.app.schemas.schemas import (
    RoleType,
    CareLevel,
    ShiftType,
    VisitStatus,
    AbsenceType,
)


####################################################################################


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)


class Token(Base):
    __tablename__ = "tokens"

    # Token information
    token: Mapped[str] = mapped_column(String, unique=True, index=True)

    created: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )

    # Relationships
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="tokens")


class Employee(Base):
    __tablename__ = "employee"

    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    phone: Mapped[str] = mapped_column(String(15), unique=True, nullable=False)
    gender: Mapped[str] = mapped_column(String(10), nullable=True)
    birth_date: Mapped[str] = mapped_column(
        String(8), nullable=True
    )  # Format: YYYYMMDD

    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    role: Mapped[str] = mapped_column(String(20), nullable=False)

    employment_type: Mapped[str] = mapped_column(String(20), nullable=True)
    employment_degree: Mapped[int] = mapped_column(Integer, nullable=True)
    weekly_hours: Mapped[int] = mapped_column(Integer, nullable=True)
    vacation_days: Mapped[int] = mapped_column(Integer, nullable=True)
    is_summer_worker: Mapped[bool] = mapped_column(
        Boolean, nullable=True, default=False
    )
    start_date: Mapped[date_type] = mapped_column(Date, nullable=True)
    end_date: Mapped[date_type] = mapped_column(Date, nullable=True)

    created: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    updated: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    schedules: Mapped[List["ScheduleEmployee"]] = relationship(
        back_populates="employee"
    )
    care_visits: Mapped[List["EmployeeCareVisit"]] = relationship(
        back_populates="employee"
    )
    absences: Mapped[List["Absence"]] = relationship(back_populates="employee")

    @property
    def role_enum(self) -> RoleType:
        return RoleType(self.role)

    @role_enum.setter
    def role_enum(self, value: RoleType):
        self.role = value.value

    def __repr__(self) -> str:
        return f"<Employee {self.first_name} {self.last_name}>"


class User(Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(Text, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)

    created: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    updated: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=False)
    employee: Mapped["Employee"] = relationship("Employee")
    tokens: Mapped[List["Token"]] = relationship(back_populates="user")

    @property
    def full_name(self) -> str:
        return f"{self.employee.first_name} {self.employee.last_name}"

    @property
    def role(self) -> str:
        return self.employee.role

    @property
    def schedules(self):
        """Returnerar alla scheman för användaren via den anställda."""
        return [se.schedule for se in self.employee.schedules]

    def __repr__(self) -> str:
        return f"<User {self.username}>"


class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    key_number: Mapped[str] = mapped_column(String(50), nullable=False)
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    care_level: Mapped[str] = mapped_column(String(20), nullable=True)
    gender: Mapped[str] = mapped_column(String(10), nullable=True)
    approved_hours: Mapped[float | None] = mapped_column(
        Float, nullable=True, default=None
    )
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    created: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now()
    )

    # Relationships
    schedules: Mapped[List["ScheduleCustomer"]] = relationship(
        back_populates="customer"
    )
    measures: Mapped[List["CustomerMeasure"]] = relationship(back_populates="customer")

    @property
    def care_level_enum(self) -> CareLevel:
        return CareLevel(self.care_level)

    def __repr__(self) -> str:
        return f"<Customer {self.first_name} {self.last_name}>"


class Measure(Base):
    __tablename__ = "measures"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    default_duration: Mapped[int] = mapped_column(Integer, nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=True)
    time_of_day: Mapped[str] = mapped_column(String(20), nullable=True)
    time_flexibility: Mapped[str] = mapped_column(String(20), nullable=True)

    created: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now()
    )

    # Relationships
    care_visits: Mapped[List["MeasureCareVisit"]] = relationship(
        back_populates="measure"
    )
    schedules: Mapped[List["ScheduleMeasure"]] = relationship(back_populates="measure")
    customers: Mapped[List["CustomerMeasure"]] = relationship(back_populates="measure")

    def __repr__(self) -> str:
        return f"<Measure {self.name}>"


class CareVisit(Base):
    __tablename__ = "care_visits"

    date: Mapped[date_type] = mapped_column(Date, nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)
    duration: Mapped[int] = mapped_column(Integer, nullable=False)
    notes: Mapped[str] = mapped_column(String(255), nullable=True)

    created: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )

    schedule_id: Mapped[int] = mapped_column(ForeignKey("schedules.id"), nullable=False)
    schedule: Mapped["Schedule"] = relationship(
        "Schedule", back_populates="care_visits"
    )
    measures: Mapped[List["MeasureCareVisit"]] = relationship(
        back_populates="care_visit"
    )
    employees: Mapped[List["EmployeeCareVisit"]] = relationship(
        back_populates="care_visit"
    )

    @property
    def status_enum(self) -> VisitStatus:
        return VisitStatus(self.status)

    @status_enum.setter
    def status_enum(self, value: VisitStatus):
        self.status = value.value

    def __repr__(self) -> str:
        return f"<CareVisit {self.date}>"


class Schedule(Base):
    __tablename__ = "schedules"

    date: Mapped[date_type] = mapped_column(Date, nullable=False)
    shift: Mapped[str] = mapped_column(String(20), nullable=False)

    employees: Mapped[List["ScheduleEmployee"]] = relationship(
        back_populates="schedule"
    )
    measures: Mapped[List["ScheduleMeasure"]] = relationship(back_populates="schedule")
    customers: Mapped[List["ScheduleCustomer"]] = relationship(
        back_populates="schedule"
    )
    care_visits: Mapped[List["CareVisit"]] = relationship(back_populates="schedule")

    created: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )

    @property
    def shift_enum(self) -> ShiftType:
        return ShiftType(self.shift)

    @shift_enum.setter
    def shift_enum(self, value: ShiftType):
        self.shift = value.value

    def __repr__(self) -> str:
        return f"<Schedule {self.date}>"


class Absence(Base):
    __tablename__ = "absences"

    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=False)
    start_date: Mapped[date_type] = mapped_column(Date, nullable=False)
    end_date: Mapped[date_type] = mapped_column(Date, nullable=False)
    absence_type: Mapped[str] = mapped_column(String(20), nullable=False)
    notes: Mapped[str] = mapped_column(String(255), nullable=True)
    hours: Mapped[int] = mapped_column(Integer, nullable=True)

    created: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )

    employee: Mapped["Employee"] = relationship(back_populates="absences")

    @property
    def absence_type_enum(self) -> AbsenceType:
        return AbsenceType(self.absence_type)

    @absence_type_enum.setter
    def absence_type_enum(self, value: AbsenceType):
        self.absence_type = value.value

    def __repr__(self) -> str:
        return f"<Absence {self.employee.first_name} {self.employee.last_name}: {self.absence_type} {self.start_date} - {self.end_date}>"


class ScheduleArchive(Base):
    __tablename__ = "schedule_archives"

    original_schedule_id: Mapped[int] = mapped_column(Integer, nullable=False)
    original_date: Mapped[date_type] = mapped_column(Date, nullable=False)
    shift: Mapped[str] = mapped_column(String(20), nullable=False)

    employee_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    customer_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    measure_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    visit_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    completed_visit_count: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0
    )
    canceled_visit_count: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0
    )

    employees_data: Mapped[str] = mapped_column(Text, nullable=True)
    customers_data: Mapped[str] = mapped_column(Text, nullable=True)
    measures_data: Mapped[str] = mapped_column(Text, nullable=True)
    visits_data: Mapped[str] = mapped_column(Text, nullable=True)

    archived_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    original_created: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    notes: Mapped[str] = mapped_column(Text, nullable=True)

    def __repr__(self) -> str:
        return f"<ScheduleArchive {self.original_date} (original_id={self.original_schedule_id})>"


# =====================================================================================================
#                                      Junction tables


class ScheduleMeasure(Base):
    __tablename__ = "schedule_measure"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    schedule_id: Mapped[int] = mapped_column(ForeignKey("schedules.id"), nullable=False)
    measure_id: Mapped[int] = mapped_column(ForeignKey("measures.id"), nullable=False)

    time_of_day: Mapped[str] = mapped_column(String(20), nullable=True)
    custom_duration: Mapped[int] = mapped_column(Integer, nullable=True)
    notes: Mapped[str] = mapped_column(String(255), nullable=True)

    created: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )

    #
    schedule: Mapped["Schedule"] = relationship(back_populates="measures")
    measure: Mapped["Measure"] = relationship(back_populates="schedules")

    def __repr__(self) -> str:
        time_info = f" ({self.time_of_day})" if self.time_of_day else ""
        return f"<ScheduleMeasure {self.measure.name}{time_info}>"


class ScheduleCustomer(Base):
    __tablename__ = "schedule_customer"

    schedule_id: Mapped[int] = mapped_column(
        ForeignKey("schedules.id"), primary_key=True
    )
    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customers.id"), primary_key=True
    )

    schedule: Mapped["Schedule"] = relationship(back_populates="customers")
    customer: Mapped["Customer"] = relationship(back_populates="schedules")


class MeasureCareVisit(Base):
    __tablename__ = "measure_care_visit"

    measure_id: Mapped[int] = mapped_column(ForeignKey("measures.id"), primary_key=True)
    care_visit_id: Mapped[int] = mapped_column(
        ForeignKey("care_visits.id"), primary_key=True
    )

    measure: Mapped["Measure"] = relationship(back_populates="care_visits")
    care_visit: Mapped["CareVisit"] = relationship(back_populates="measures")

    def __repr__(self) -> str:
        return f"<MeasureCareVisit {self.measure.name} {self.care_visit.date}>"


class EmployeeCareVisit(Base):
    __tablename__ = "employee_care_visit"

    employee_id: Mapped[int] = mapped_column(
        ForeignKey("employees.id"), primary_key=True
    )
    care_visit_id: Mapped[int] = mapped_column(
        ForeignKey("care_visits.id"), primary_key=True
    )

    is_primary: Mapped[bool] = mapped_column(Boolean, default=False)
    notes: Mapped[str] = mapped_column(String(255), nullable=True)

    created: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )

    employee: Mapped["Employee"] = relationship(back_populates="care_visits")
    care_visit: Mapped["CareVisit"] = relationship(back_populates="employees")

    def __repr__(self) -> str:
        return f"<EmployeeCareVisit {self.employee.first_name} {self.employee.last_name} - {self.care_visit.date}>"


class CustomerMeasure(Base):
    __tablename__ = "customer_measures"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    customer_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("customers.id"), nullable=False
    )
    measure_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("measures.id"), nullable=False
    )
    customer_duration: Mapped[int] = mapped_column(Integer, nullable=True)
    customer_frequency: Mapped[str] = mapped_column(String(50), nullable=True)
    customer_notes: Mapped[str] = mapped_column(Text, nullable=True)

    customer_time_of_day: Mapped[str] = mapped_column(String(20), nullable=True)
    customer_time_flexibility: Mapped[str] = mapped_column(String(20), nullable=True)
    schedule_info: Mapped[str] = mapped_column(Text, nullable=True)

    created: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now()
    )

    customer: Mapped["Customer"] = relationship("Customer", back_populates="measures")
    measure: Mapped["Measure"] = relationship("Measure", back_populates="customers")

    def __repr__(self) -> str:
        return f"<CustomerMeasure customer_id={self.customer_id} measure_id={self.measure_id}>"


class ScheduleEmployee(Base):
    __tablename__ = "schedule_employee"

    schedule_id: Mapped[int] = mapped_column(
        ForeignKey("schedules.id"), primary_key=True
    )
    employee_id: Mapped[int] = mapped_column(
        ForeignKey("employees.id"), primary_key=True
    )

    schedule: Mapped["Schedule"] = relationship(back_populates="employees")
    employee: Mapped["Employee"] = relationship(back_populates="schedules")
