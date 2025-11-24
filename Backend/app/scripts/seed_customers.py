import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from Backend.app.core.db_setup import SessionLocal  # noqa: E402
from Backend.app.models.customer import Customer, CustomerMeasure  # noqa: E402
from Backend.app.models.measure import Measure  # noqa: E402
from Backend.app.core.enums import CareLevel, Gender  # noqa: E402
from sqlalchemy import select  # noqa: E402


# Swedish care measures with default durations (in minutes)
MEASURES = [
    {
        "name": "Dusch",
        "default_duration": 15,
        "text": "Hjälp med personlig hygien och dusch",
    },
    {"name": "Städ", "default_duration": 45, "text": "Städning av bostad"},
    {"name": "Tvätt", "default_duration": 30, "text": "Tvätt av kläder och textilier"},
    {
        "name": "Inköp",
        "default_duration": 60,
        "text": "Hjälp med inköp av mat och förnödenheter",
    },
    {
        "name": "Personlig Omvårdnad",
        "default_duration": 30,
        "text": "Personlig vård och omvårdnad",
    },
    {
        "name": "Mat/måltider",
        "default_duration": 30,
        "text": "Hjälp med matlagning och måltider",
    },
    {
        "name": "Annan insats",
        "default_duration": 30,
        "text": "Övriga insatser enligt beslut",
    },
    {"name": "Tillsyn", "default_duration": 15, "text": "Tillsyn och trygghetskontakt"},
]


# Customer profiles with realistic Swedish names and addresses
CUSTOMERS = [
    {
        "first_name": "Anna",
        "last_name": "Andersson",
        "key_number": 1001,
        "address": "Storgatan 12, 111 22 Stockholm",
        "care_level": CareLevel.LOW,
        "gender": Gender.FEMALE,
        "approved_hours": 5.0,
        "measures": [
            {
                "measure_name": "Inköp",
                "frequency": "WEEKLY",
                "days_of_week": ["Monday"],
                "occurrences_per_week": 1,
                "customer_duration": 75,
                "customer_notes": "Handlar på ICA Kvantum",
            }
        ],
    },
    {
        "first_name": "Erik",
        "last_name": "Johansson",
        "key_number": 1002,
        "address": "Kungsgatan 45, 411 19 Göteborg",
        "care_level": CareLevel.MEDIUM,
        "gender": Gender.MALE,
        "approved_hours": 20.0,
        "measures": [
            {
                "measure_name": "Inköp",
                "frequency": "WEEKLY",
                "days_of_week": ["Wednesday"],
                "occurrences_per_week": 1,
                "customer_duration": 60,
            },
            {
                "measure_name": "Städ",
                "frequency": "BIWEEKLY",
                "days_of_week": ["Friday"],
                "occurrences_per_week": 1,
                "customer_duration": 90,
                "customer_notes": "Hela lägenheten varannan vecka",
            },
            {
                "measure_name": "Tvätt",
                "frequency": "WEEKLY",
                "days_of_week": ["Thursday"],
                "occurrences_per_week": 1,
                "customer_duration": 30,
            },
        ],
    },
    {
        "first_name": "Margareta",
        "last_name": "Karlsson",
        "key_number": 1003,
        "address": "Linnégatan 8, 214 23 Malmö",
        "care_level": CareLevel.MEDIUM,
        "gender": Gender.FEMALE,
        "approved_hours": 35.0,
        "measures": [
            {
                "measure_name": "Mat/måltider",
                "frequency": "DAILY",
                "days_of_week": [
                    "Monday",
                    "Tuesday",
                    "Wednesday",
                    "Thursday",
                    "Friday",
                ],
                "occurrences_per_week": 5,
                "customer_duration": 30,
                "customer_notes": "Lunch och middag vardagar",
            },
            {
                "measure_name": "Inköp",
                "frequency": "WEEKLY",
                "days_of_week": ["Saturday"],
                "occurrences_per_week": 1,
                "customer_duration": 45,
            },
            {
                "measure_name": "Städ",
                "frequency": "WEEKLY",
                "days_of_week": ["Wednesday"],
                "occurrences_per_week": 1,
                "customer_duration": 60,
            },
        ],
    },
    {
        "first_name": "Lars",
        "last_name": "Nilsson",
        "key_number": 1004,
        "address": "Vasagatan 23, 753 20 Uppsala",
        "care_level": CareLevel.HIGH,
        "gender": Gender.MALE,
        "approved_hours": 75.0,
        "measures": [
            {
                "measure_name": "Personlig Omvårdnad",
                "frequency": "DAILY",
                "days_of_week": [
                    "Monday",
                    "Tuesday",
                    "Wednesday",
                    "Thursday",
                    "Friday",
                    "Saturday",
                    "Sunday",
                ],
                "occurrences_per_week": 7,
                "customer_duration": 20,
                "customer_notes": "Morgonhjälp varje dag",
            },
            {
                "measure_name": "Dusch",
                "frequency": "WEEKLY",
                "days_of_week": ["Tuesday", "Friday"],
                "occurrences_per_week": 2,
                "customer_duration": 15,
            },
            {
                "measure_name": "Mat/måltider",
                "frequency": "DAILY",
                "days_of_week": [
                    "Monday",
                    "Tuesday",
                    "Wednesday",
                    "Thursday",
                    "Friday",
                    "Saturday",
                    "Sunday",
                ],
                "occurrences_per_week": 7,
                "customer_duration": 25,
                "customer_notes": "Frukost och middag",
            },
            {
                "measure_name": "Inköp",
                "frequency": "WEEKLY",
                "days_of_week": ["Monday"],
                "occurrences_per_week": 1,
                "customer_duration": 60,
            },
        ],
    },
    {
        "first_name": "Ingrid",
        "last_name": "Svensson",
        "key_number": 1005,
        "address": "Drottninggatan 67, 252 21 Helsingborg",
        "care_level": CareLevel.LOW,
        "gender": Gender.FEMALE,
        "approved_hours": 8.0,
        "measures": [
            {
                "measure_name": "Inköp",
                "frequency": "WEEKLY",
                "days_of_week": ["Friday"],
                "occurrences_per_week": 1,
                "customer_duration": 90,
                "customer_notes": "Behöver hjälp med tunga kassar",
            },
            {
                "measure_name": "Tvätt",
                "frequency": "BIWEEKLY",
                "days_of_week": ["Tuesday"],
                "occurrences_per_week": 1,
                "customer_duration": 45,
            },
        ],
    },
    {
        "first_name": "Sven",
        "last_name": "Bergström",
        "key_number": 1006,
        "address": "Hantverkargatan 34, 703 61 Örebro",
        "care_level": CareLevel.MEDIUM,
        "gender": Gender.MALE,
        "approved_hours": 28.0,
        "measures": [
            {
                "measure_name": "Mat/måltider",
                "frequency": "DAILY",
                "days_of_week": ["Monday", "Wednesday", "Friday"],
                "occurrences_per_week": 3,
                "customer_duration": 35,
            },
            {
                "measure_name": "Städ",
                "frequency": "WEEKLY",
                "days_of_week": ["Thursday"],
                "occurrences_per_week": 1,
                "customer_duration": 60,
            },
            {
                "measure_name": "Inköp",
                "frequency": "WEEKLY",
                "days_of_week": ["Saturday"],
                "occurrences_per_week": 1,
                "customer_duration": 50,
            },
            {
                "measure_name": "Tillsyn",
                "frequency": "DAILY",
                "days_of_week": [
                    "Monday",
                    "Tuesday",
                    "Wednesday",
                    "Thursday",
                    "Friday",
                    "Saturday",
                    "Sunday",
                ],
                "occurrences_per_week": 7,
                "customer_duration": 10,
                "customer_notes": "Kvällstillsyn varje dag",
            },
        ],
    },
    {
        "first_name": "Birgitta",
        "last_name": "Lindberg",
        "key_number": 1007,
        "address": "Prästgatan 89, 602 24 Norrköping",
        "care_level": CareLevel.HIGH,
        "gender": Gender.FEMALE,
        "approved_hours": 85.0,
        "measures": [
            {
                "measure_name": "Personlig Omvårdnad",
                "frequency": "DAILY",
                "days_of_week": [
                    "Monday",
                    "Tuesday",
                    "Wednesday",
                    "Thursday",
                    "Friday",
                    "Saturday",
                    "Sunday",
                ],
                "occurrences_per_week": 7,
                "customer_duration": 30,
                "customer_notes": "Morgon- och kvällshjälp",
            },
            {
                "measure_name": "Dusch",
                "frequency": "WEEKLY",
                "days_of_week": ["Monday", "Thursday"],
                "occurrences_per_week": 2,
                "customer_duration": 20,
            },
            {
                "measure_name": "Mat/måltider",
                "frequency": "DAILY",
                "days_of_week": [
                    "Monday",
                    "Tuesday",
                    "Wednesday",
                    "Thursday",
                    "Friday",
                    "Saturday",
                    "Sunday",
                ],
                "occurrences_per_week": 7,
                "customer_duration": 30,
                "customer_notes": "Frukost, lunch och middag",
            },
            {
                "measure_name": "Städ",
                "frequency": "WEEKLY",
                "days_of_week": ["Wednesday"],
                "occurrences_per_week": 1,
                "customer_duration": 90,
            },
            {
                "measure_name": "Tvätt",
                "frequency": "WEEKLY",
                "days_of_week": ["Tuesday"],
                "occurrences_per_week": 1,
                "customer_duration": 45,
            },
            {
                "measure_name": "Inköp",
                "frequency": "WEEKLY",
                "days_of_week": ["Friday"],
                "occurrences_per_week": 1,
                "customer_duration": 60,
            },
        ],
    },
    {
        "first_name": "Gustav",
        "last_name": "Eriksson",
        "key_number": 1008,
        "address": "Järnvägsgatan 56, 172 45 Sundbyberg",
        "care_level": CareLevel.MEDIUM,
        "gender": Gender.MALE,
        "approved_hours": 42.0,
        "measures": [
            {
                "measure_name": "Mat/måltider",
                "frequency": "DAILY",
                "days_of_week": [
                    "Monday",
                    "Tuesday",
                    "Wednesday",
                    "Thursday",
                    "Friday",
                    "Saturday",
                    "Sunday",
                ],
                "occurrences_per_week": 7,
                "customer_duration": 25,
                "customer_notes": "Middag varje dag",
            },
            {
                "measure_name": "Dusch",
                "frequency": "WEEKLY",
                "days_of_week": ["Wednesday"],
                "occurrences_per_week": 1,
                "customer_duration": 15,
            },
            {
                "measure_name": "Städ",
                "frequency": "WEEKLY",
                "days_of_week": ["Friday"],
                "occurrences_per_week": 1,
                "customer_duration": 75,
            },
            {
                "measure_name": "Inköp",
                "frequency": "WEEKLY",
                "days_of_week": ["Thursday"],
                "occurrences_per_week": 1,
                "customer_duration": 55,
            },
            {
                "measure_name": "Tvätt",
                "frequency": "WEEKLY",
                "days_of_week": ["Monday"],
                "occurrences_per_week": 1,
                "customer_duration": 40,
            },
        ],
    },
    {
        "first_name": "Karin",
        "last_name": "Olsson",
        "key_number": 1009,
        "address": "Strandvägen 18, 903 27 Umeå",
        "care_level": CareLevel.LOW,
        "gender": Gender.FEMALE,
        "approved_hours": 12.0,
        "measures": [
            {
                "measure_name": "Inköp",
                "frequency": "WEEKLY",
                "days_of_week": ["Thursday"],
                "occurrences_per_week": 1,
                "customer_duration": 60,
            },
            {
                "measure_name": "Mat/måltider",
                "frequency": "WEEKLY",
                "days_of_week": ["Tuesday", "Friday"],
                "occurrences_per_week": 2,
                "customer_duration": 40,
                "customer_notes": "Matlagning två gånger i veckan",
            },
            {
                "measure_name": "Annan insats",
                "frequency": "WEEKLY",
                "days_of_week": ["Saturday"],
                "occurrences_per_week": 1,
                "customer_duration": 30,
                "customer_notes": "Hjälp med administration och räkningar",
            },
        ],
    },
    {
        "first_name": "Ove",
        "last_name": "Persson",
        "key_number": 1010,
        "address": "Kyrkogatan 91, 651 84 Karlstad",
        "care_level": CareLevel.HIGH,
        "gender": Gender.MALE,
        "approved_hours": 68.0,
        "measures": [
            {
                "measure_name": "Personlig Omvårdnad",
                "frequency": "DAILY",
                "days_of_week": [
                    "Monday",
                    "Tuesday",
                    "Wednesday",
                    "Thursday",
                    "Friday",
                    "Saturday",
                    "Sunday",
                ],
                "occurrences_per_week": 7,
                "customer_duration": 25,
                "customer_notes": "Morgonhjälp varje dag kl 07:00-08:00",
            },
            {
                "measure_name": "Dusch",
                "frequency": "WEEKLY",
                "days_of_week": ["Tuesday", "Friday"],
                "occurrences_per_week": 2,
                "customer_duration": 20,
            },
            {
                "measure_name": "Mat/måltider",
                "frequency": "DAILY",
                "days_of_week": [
                    "Monday",
                    "Tuesday",
                    "Wednesday",
                    "Thursday",
                    "Friday",
                ],
                "occurrences_per_week": 5,
                "customer_duration": 30,
                "customer_notes": "Frukost vardagar",
            },
            {
                "measure_name": "Inköp",
                "frequency": "WEEKLY",
                "days_of_week": ["Monday"],
                "occurrences_per_week": 1,
                "customer_duration": 50,
            },
            {
                "measure_name": "Tvätt",
                "frequency": "WEEKLY",
                "days_of_week": ["Wednesday"],
                "occurrences_per_week": 1,
                "customer_duration": 35,
            },
            {
                "measure_name": "Städ",
                "frequency": "BIWEEKLY",
                "days_of_week": ["Thursday"],
                "occurrences_per_week": 1,
                "customer_duration": 60,
            },
        ],
    },
]


def create_or_get_measures(db):
    """Create Swedish care measures if they don't exist."""
    measures_dict = {}

    for measure_data in MEASURES:
        stmt = select(Measure).where(Measure.name == measure_data["name"])
        existing_measure = db.execute(stmt).scalar_one_or_none()

        if existing_measure:
            print(f"✓ Measure '{measure_data['name']}' already exists")
            measures_dict[measure_data["name"]] = existing_measure
        else:
            new_measure = Measure(
                name=measure_data["name"],
                default_duration=measure_data["default_duration"],
                text=measure_data["text"],
                is_active=True,
                is_standard=True,
            )
            db.add(new_measure)
            db.commit()
            db.refresh(new_measure)
            measures_dict[measure_data["name"]] = new_measure
            print(f"✓ Created measure: {measure_data['name']}")

    return measures_dict


def create_customers_with_measures(db, measures_dict):
    """Create customers and their measure assignments."""
    created_customers = []

    for customer_data in CUSTOMERS:
        # Check if customer already exists
        stmt = select(Customer).where(
            Customer.key_number == customer_data["key_number"]
        )
        existing_customer = db.execute(stmt).scalar_one_or_none()

        if existing_customer:
            print(
                f"✓ Customer '{customer_data['first_name']} {customer_data['last_name']}' already exists"
            )
            continue

        # Create customer
        customer = Customer(
            first_name=customer_data["first_name"],
            last_name=customer_data["last_name"],
            key_number=customer_data["key_number"],
            address=customer_data["address"],
            care_level=customer_data["care_level"],
            gender=customer_data["gender"],
            approved_hours=customer_data["approved_hours"],
            is_active=True,
        )
        db.add(customer)
        db.commit()
        db.refresh(customer)

        print(
            f"✓ Created customer: {customer.first_name} {customer.last_name} ({customer.approved_hours}h/month)"
        )

        # Create customer measure assignments
        for measure_assignment in customer_data["measures"]:
            measure = measures_dict[measure_assignment["measure_name"]]

            customer_measure = CustomerMeasure(
                customer_id=customer.id,
                measure_id=measure.id,
                customer_duration=measure_assignment.get("customer_duration"),
                customer_notes=measure_assignment.get("customer_notes"),
                frequency=measure_assignment["frequency"],
                days_of_week=measure_assignment.get("days_of_week"),
                occurrences_per_week=measure_assignment.get("occurrences_per_week"),
            )
            db.add(customer_measure)
            print(
                f"  → Assigned measure: {measure_assignment['measure_name']} ({measure_assignment['frequency']})"
            )

        db.commit()
        created_customers.append(customer)

    return created_customers


def seed_customers():
    """Main function to seed customers and measures."""
    db = SessionLocal()

    try:
        print("\n" + "=" * 60)
        print("Starting customer and measure seeding...")
        print("=" * 60 + "\n")

        # Create or get measures
        print("Step 1: Creating Swedish care measures...")
        measures_dict = create_or_get_measures(db)
        print(f"\n✓ {len(measures_dict)} measures available\n")

        # Create customers with their measures
        print("Step 2: Creating customers with care needs...")
        customers = create_customers_with_measures(db, measures_dict)

        print("\n" + "=" * 60)
        print(f"✓ Successfully created {len(customers)} customers!")
        print("=" * 60 + "\n")

        # Summary
        print("Summary:")
        for customer_data in CUSTOMERS:
            print(
                f"  - {customer_data['first_name']} {customer_data['last_name']}: "
                f"{customer_data['approved_hours']}h/month, "
                f"{len(customer_data['measures'])} insatser ({customer_data['care_level'].value} care level)"
            )

    except Exception as e:
        print(f"❌ Error seeding customers: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_customers()
