# Customer Seed Script Documentation

## Overview

This script seeds the database with Swedish care measures and 10 fictional customers with varying care needs.

## What Gets Created

### Swedish Care Measures (Insatser)

The script creates 8 standard Swedish care measures:

1. **Dusch** - Shower assistance (15 min default)
2. **Städ** - Cleaning (45 min default)
3. **Tvätt** - Laundry (30 min default)
4. **Inköp** - Shopping assistance (60 min default)
5. **Personlig Omvårdnad** - Personal care (30 min default)
6. **Mat/måltider** - Meal preparation (30 min default)
7. **Annan insats** - Other services (30 min default)
8. **Tillsyn** - Supervision/check-in (15 min default)

### Customer Profiles

#### Low Care Need (3 customers)

- **Anna Andersson** (5h/month): Shopping 1x/week
- **Ingrid Svensson** (8h/month): Shopping weekly + laundry biweekly
- **Karin Olsson** (12h/month): Shopping + meals 2x/week + admin help

#### Medium Care Need (4 customers)

- **Erik Johansson** (20h/month): Shopping, cleaning biweekly, laundry weekly
- **Margareta Karlsson** (35h/month): Meals 5x/week, shopping, cleaning
- **Sven Bergström** (28h/month): Meals 3x/week, cleaning, shopping, daily supervision
- **Gustav Eriksson** (42h/month): Daily meals, shower weekly, cleaning, shopping, laundry

#### High Care Need (3 customers)

- **Lars Nilsson** (75h/month): Daily morning help, meals 7x/week, showers 2x/week, shopping
- **Birgitta Lindberg** (85h/month): Daily personal care, meals 7x/week, showers 2x/week, cleaning, laundry, shopping
- **Ove Persson** (68h/month): Daily morning help, meals 5x/week, showers 2x/week, shopping, laundry, cleaning biweekly

## How to Run

### Prerequisites

1. Activate the Python virtual environment
2. Ensure database is running and migrations are up to date
3. Database connection must be configured in `.env` file

### Execute the script

```bash
python -m Backend.app.scripts.seed_customers
```

## Script Features

### Idempotent Execution

- The script checks for existing measures and customers before creating them
- Safe to run multiple times without creating duplicates
- Uses `key_number` to identify existing customers

### Data Structure

Each customer is created with:

- Basic info: first_name, last_name, key_number, address
- Care level: LOW, MEDIUM, or HIGH
- Gender: MALE or FEMALE
- Approved hours per month
- Multiple measure assignments with:
  - Frequency: DAILY, WEEKLY, or BIWEEKLY
  - Days of week: Specific days when measure should be performed
  - Occurrences per week: Number of times per week
  - Custom duration: Overrides measure's default duration
  - Notes: Customer-specific instructions

## Database Tables Affected

1. `measures` - Swedish care measures
2. `customers` - Customer profiles
3. `customer_measures` - Relationships between customers and measures

## Verification

After running the script, you should see:

- 8 measures created/verified
- 10 customers created
- Customer-measure relationships established

Check the database:

```sql
SELECT COUNT(*) FROM measures;  -- Should be at least 8
SELECT COUNT(*) FROM customers;  -- Should be at least 10
SELECT COUNT(*) FROM customer_measures;  -- Should be 44 total assignments
```

## Example Output

```
============================================================
Starting customer and measure seeding...
============================================================

Step 1: Creating Swedish care measures...
✓ Created measure: Dusch
✓ Created measure: Städ
...

✓ 8 measures available

Step 2: Creating customers with care needs...
✓ Created customer: Anna Andersson (5.0h/month)
  → Assigned measure: Inköp (WEEKLY)
...

============================================================
✓ Successfully created 10 customers!
============================================================
```

## Notes

- All measures are marked as `is_standard=True` and `is_active=True`
- All customers are marked as `is_active=True`
- Time of day preferences are not set by the script (users configure in frontend)
- Customer key_numbers range from 1001-1010
