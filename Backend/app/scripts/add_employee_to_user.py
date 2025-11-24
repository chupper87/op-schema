import sys
from pathlib import Path
from datetime import date

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from Backend.app.core.db_setup import SessionLocal  # noqa: E402
from Backend.app.models.auth import User  # noqa: E402
from Backend.app.models.employee import Employee  # noqa: E402
from Backend.app.core.enums import RoleType, Gender  # noqa: E402


def add_employee_to_user(username: str):
    """
    Add Employee record to an existing User.
    Prompts for employee details interactively.
    """
    db = SessionLocal()

    try:
        # Find user by username
        user = db.query(User).filter(User.username == username).first()

        if not user:
            print(f"Error: User '{username}' not found")
            return None

        # Check if employee already exists
        if user.employee:
            print(f"Error: User '{username}' already has an employee record")
            return None

        print(f"Creating employee record for user: {username}")

        # Prompt for employee details
        print("\nEnter employee details:")
        first_name = input("First name: ").strip()
        last_name = input("Last name: ").strip()
        phone = input("Phone (e.g., 0700000000): ").strip()

        # Gender selection
        print("\nSelect gender:")
        print("1. Male")
        print("2. Female")
        print("3. Unspecified")
        gender_choice = input("Choice (1-3): ").strip()
        gender_map = {"1": Gender.MALE, "2": Gender.FEMALE, "3": Gender.UNSPECIFIED}
        gender = gender_map.get(gender_choice, Gender.UNSPECIFIED)

        # Role selection
        print("\nSelect role:")
        print("1. Admin")
        print("2. Assistant Nurse")
        print("3. Care Assistant")
        role_choice = input("Choice (1-3): ").strip()
        role_map = {
            "1": RoleType.ADMIN,
            "2": RoleType.ASSISTANT_NURSE,
            "3": RoleType.CARE_ASSISTANT,
        }
        role = role_map.get(role_choice, RoleType.ADMIN)

        # Birth date
        birth_year = int(input("Birth year (e.g., 1990): ").strip())
        birth_month = int(input("Birth month (1-12): ").strip())
        birth_day = int(input("Birth day (1-31): ").strip())
        birth_date = date(birth_year, birth_month, birth_day)

        return user, first_name, last_name, phone, gender, role, birth_date

    finally:
        db.close()


def create_employee_record(username: str):
    """
    Main function to create employee for a user.
    """
    result = add_employee_to_user(username)

    if result is None:
        return

    user, first_name, last_name, phone, gender, role, birth_date = result

    # Create Employee object
    db = SessionLocal()
    try:
        employee = Employee(
            user_id=user.id,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            gender=gender,
            role=role,
            birth_date=birth_date,
        )

        db.add(employee)
        db.commit()
        db.refresh(employee)

        print("\n✓ Employee record created successfully!")
        print(f"  Name: {first_name} {last_name}")
        print(f"  Role: {role.value}")

    except Exception as e:
        db.rollback()
        print(f"\n✗ Error creating employee: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python add_employee_to_user.py <username>")
        print("Example: python add_employee_to_user.py admin")
        sys.exit(1)

    username = sys.argv[1]
    create_employee_record(username)
