"""
Created by: David Edwards
Contact: david.j.edwards.de@gmail.com
Date: 2026-04-24

This script generates sample data for a Salesforce like organization.
The data is generated in a CSV format and can be imported into a database or work directly from the CSV files.

The data is generated for a single sales org with the following entities:
- Users
- Accounts
- Leads
- Contacts
- Opportunities
- Orders
- Order Items
- Tasks
- Events

This script was generated with the help of Codex 5.3.  
"""


import csv
import os
import random
import string
from collections import Counter
from datetime import date, datetime, timedelta


SEED = 42
random.seed(SEED)


COUNTS = {
    "users": 275,
    "accounts": 10000,
    "leads": 14000,
    "contacts": 18500,
    "opportunities": 16000,
    "orders": 9200,
    "order_items": 41400,
    "tasks": 110000,
    "events": 38000,
}


# Resolve to sample_data/csv so generation works from any working directory
_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.normpath(os.path.join(_BASE_DIR, "..", "csv"))


ID_PREFIX = {
    "user": "005",
    "account": "001",
    "lead": "00Q",
    "contact": "003",
    "opportunity": "006",
    "order": "801",
    "order_item": "802",
    "task": "00T",
    "event": "00U",
}


USED_IDS = set()


def sf_id(prefix: str) -> str:
    alphabet = string.ascii_uppercase + string.ascii_lowercase + string.digits
    while True:
        rest = "".join(random.choice(alphabet) for _ in range(15))
        record_id = prefix + rest
        if record_id not in USED_IDS:
            USED_IDS.add(record_id)
            return record_id


def write_csv(filename, rows, fieldnames):
    path = f"{BASE_DIR}/{filename}"
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


FIRST_NAMES = [
    "Aaliyah", "Adriana", "Akira", "Alex", "Amina", "Andre", "Anika", "Bao",
    "Camila", "Carmen", "Casey", "Daniel", "DeShawn", "Diego", "Elias", "Emerson",
    "Fatima", "Gabriel", "Haruto", "Imani", "Jada", "Jamal", "Javier", "Jihoon",
    "Jordan", "Kai", "Kavya", "Keisha", "Leila", "Liam", "Lucia", "Malik",
    "Maya", "Mei", "Miguel", "Nia", "Noah", "Omar", "Priya", "Quinn",
    "Riley", "Saanvi", "Sofia", "Tariq", "Taylor", "Ximena", "Yara", "Zuri",
]

LAST_NAMES = [
    "Abebe", "Ali", "Alvarez", "Anderson", "Baker", "Banerjee", "Brown", "Chen",
    "Clark", "Cruz", "Davis", "Diaz", "Edwards", "Garcia", "Gonzalez", "Green",
    "Gupta", "Hall", "Hernandez", "Ibrahim", "Jackson", "Johnson", "Khan", "Kim",
    "Lee", "Lewis", "Lopez", "Martinez", "Miller", "Mitchell", "Moore", "Nguyen",
    "Patel", "Perez", "Robinson", "Rodriguez", "Sanchez", "Singh", "Smith", "Taylor",
    "Thomas", "Thompson", "Walker", "Washington", "Williams", "Wilson", "Wong", "Wright",
]

COMPANY_PREFIX = [
    "Acme", "Summit", "Northstar", "Pinnacle", "Evergreen", "BlueSky", "Vertex", "Lighthouse",
    "Ironwood", "Clearwater", "Redwood", "Nimbus", "Stratus", "Cobalt", "Oakridge", "Harbor",
]

COMPANY_SUFFIX = [
    "Technologies", "Logistics", "Health", "Financial", "Retail", "Manufacturing", "Consulting",
    "Systems", "Energy", "Foods", "Media", "Labs", "Software", "Partners", "Group", "Services",
]

CITIES = [
    ("San Francisco", "CA", "US"), ("New York", "NY", "US"), ("Austin", "TX", "US"),
    ("Chicago", "IL", "US"), ("Seattle", "WA", "US"), ("Denver", "CO", "US"),
    ("Boston", "MA", "US"), ("Atlanta", "GA", "US"), ("Miami", "FL", "US"),
    ("Phoenix", "AZ", "US"), ("Nashville", "TN", "US"), ("Charlotte", "NC", "US"),
    ("Portland", "OR", "US"), ("Minneapolis", "MN", "US"), ("Dallas", "TX", "US"),
    ("Los Angeles", "CA", "US"), ("San Diego", "CA", "US"), ("Philadelphia", "PA", "US"),
]

LEAD_SOURCES = ["Web", "Partner Referral", "Trade Show", "Outbound", "Inbound", "Event"]
INDUSTRIES = ["Technology", "Healthcare", "Financial Services", "Retail", "Manufacturing", "Education"]
TASK_TYPES = ["Email", "Call", "Follow-up", "Discovery", "Qualification"]
EVENT_TYPES = ["Meeting", "Demo", "Onsite Visit", "QBR", "Executive Review"]
OPP_STAGES = ["Prospecting", "Qualification", "Proposal", "Negotiation", "Closed Won", "Closed Lost"]
ORDER_STATUS = ["Draft", "Activated", "Fulfilled", "Cancelled"]
PRODUCTS = [
    ("SKU-CRM-100", "CRM Platform Seat"),
    ("SKU-ANL-210", "Analytics Add-on"),
    ("SKU-SVC-300", "Professional Services Pack"),
    ("SKU-INT-410", "Integration Connector"),
    ("SKU-SUP-500", "Premium Support"),
]


def rand_date(start: date, end: date) -> date:
    days = (end - start).days
    return start + timedelta(days=random.randint(0, days))


def build_users():
    users = []
    today = date.today()

    director_id = sf_id(ID_PREFIX["user"])
    users.append({
        "id": director_id,
        "first_name": "Jami",
        "last_name": "Green",
        "name": "Jami Green",
        "title": "Director of Sales",
        "role": "Director",
        "manager_id": "",
        "department": "Sales",
        "email": "jami.green@fakeco.example",
        "is_active": "true",
        "hire_date": str(today - timedelta(days=1500)),
    })

    total_frontline = COUNTS["users"] - 1
    manager_count = max((total_frontline + 9) // 10, 1)
    frontline_count = total_frontline - manager_count

    managers = []
    for i in range(manager_count):
        fn = random.choice(FIRST_NAMES)
        ln = random.choice(LAST_NAMES)
        uid = sf_id(ID_PREFIX["user"])
        managers.append(uid)
        users.append({
            "id": uid,
            "first_name": fn,
            "last_name": ln,
            "name": f"{fn} {ln}",
            "title": "Sales Manager",
            "role": "Manager",
            "manager_id": director_id,
            "department": "Sales",
            "email": f"{fn.lower()}.{ln.lower()}.{i}@fakeco.example",
            "is_active": "true",
            "hire_date": str(today - timedelta(days=random.randint(700, 2200))),
        })

    role_targets = {
        "BDR": int(round(frontline_count * 0.30)),
        "SDR": int(round(frontline_count * 0.30)),
    }
    role_targets["AE"] = frontline_count - role_targets["BDR"] - role_targets["SDR"]

    role_pool = []
    for role, n in role_targets.items():
        role_pool.extend([role] * n)
    random.shuffle(role_pool)

    frontline = []
    for i in range(frontline_count):
        fn = random.choice(FIRST_NAMES)
        ln = random.choice(LAST_NAMES)
        uid = sf_id(ID_PREFIX["user"])
        frontline.append(uid)
        mgr = managers[i % manager_count]
        role = role_pool[i]
        title = {
            "BDR": "Business Development Representative",
            "SDR": "Sales Development Representative",
            "AE": "Account Executive",
        }[role]
        users.append({
            "id": uid,
            "first_name": fn,
            "last_name": ln,
            "name": f"{fn} {ln}",
            "title": title,
            "role": role,
            "manager_id": mgr,
            "department": "Sales",
            "email": f"{fn.lower()}.{ln.lower()}.{i + 1000}@fakeco.example",
            "is_active": "true",
            "hire_date": str(today - timedelta(days=random.randint(30, 1800))),
        })

    manager_reports = Counter(u["manager_id"] for u in users if u["role"] in {"BDR", "SDR", "AE"})
    assert max(manager_reports.values()) <= 10
    assert len(users) == COUNTS["users"]
    return users, director_id, managers, frontline


def weighted_owner(frontline_users, user_by_id, distribution):
    buckets = {"BDR": [], "SDR": [], "AE": []}
    for uid in frontline_users:
        buckets[user_by_id[uid]["role"]].append(uid)
    selected_role = random.choices(list(distribution.keys()), weights=list(distribution.values()), k=1)[0]
    return random.choice(buckets[selected_role])


def build_accounts(frontline_users, user_by_id):
    rows = []
    for i in range(COUNTS["accounts"]):
        city, state, country = random.choice(CITIES)
        owner_id = weighted_owner(frontline_users, user_by_id, {"BDR": 30, "SDR": 30, "AE": 40})
        name = f"{random.choice(COMPANY_PREFIX)} {random.choice(COMPANY_SUFFIX)} {i + 1}"
        created = rand_date(date(2021, 1, 1), date(2025, 12, 31))
        rows.append({
            "id": sf_id(ID_PREFIX["account"]),
            "name": name,
            "account_number": f"ACC-{100000 + i}",
            "owner_id": owner_id,
            "type": random.choice(["Customer", "Prospect", "Partner"]),
            "industry": random.choice(INDUSTRIES),
            "annual_revenue": random.randint(500000, 50000000),
            "employee_count": random.randint(10, 5000),
            "billing_city": city,
            "billing_state": state,
            "billing_country": country,
            "created_date": str(created),
            "is_active": random.choice(["true", "true", "true", "false"]),
        })
    return rows


def build_leads(frontline_users, user_by_id, accounts):
    rows = []
    converted_ids = []
    account_ids = [a["id"] for a in accounts]
    for i in range(COUNTS["leads"]):
        fn = random.choice(FIRST_NAMES)
        ln = random.choice(LAST_NAMES)
        owner_id = weighted_owner(frontline_users, user_by_id, {"BDR": 45, "SDR": 45, "AE": 10})
        created = rand_date(date(2022, 1, 1), date(2025, 12, 31))
        converted = random.random() < 0.52
        cid = sf_id(ID_PREFIX["lead"])
        converted_account_id = random.choice(account_ids) if converted else ""
        rows.append({
            "id": cid,
            "first_name": fn,
            "last_name": ln,
            "company": f"{random.choice(COMPANY_PREFIX)} {random.choice(COMPANY_SUFFIX)}",
            "email": f"{fn.lower()}.{ln.lower()}.{i}@lead.example",
            "phone": f"+1-555-{random.randint(100, 999)}-{random.randint(1000, 9999)}",
            "status": random.choice(["Open", "Working", "Nurturing", "Qualified"]),
            "lead_source": random.choice(LEAD_SOURCES),
            "owner_id": owner_id,
            "created_date": str(created),
            "is_converted": "true" if converted else "false",
            "converted_account_id": converted_account_id,
            "converted_contact_id": "",
            "converted_opportunity_id": "",
        })
        if converted:
            converted_ids.append(cid)
    return rows, set(converted_ids)


def build_contacts(frontline_users, user_by_id, accounts, leads, converted_lead_ids):
    rows = []
    account_ids = [a["id"] for a in accounts]
    leads_by_id = {l["id"]: l for l in leads}

    converted_contacts_to_create = int(round(COUNTS["contacts"] * 0.35))
    converted_candidates = list(converted_lead_ids)
    random.shuffle(converted_candidates)
    converted_used = converted_candidates[:converted_contacts_to_create]

    lead_to_contact = {}
    for lid in converted_used:
        lead = leads_by_id[lid]
        cid = sf_id(ID_PREFIX["contact"])
        lead_to_contact[lid] = cid
        created = rand_date(date(2022, 1, 1), date(2025, 12, 31))
        rows.append({
            "id": cid,
            "account_id": lead["converted_account_id"] or random.choice(account_ids),
            "owner_id": lead["owner_id"],
            "first_name": lead["first_name"],
            "last_name": lead["last_name"],
            "email": lead["email"].replace("@lead.example", "@contact.example"),
            "phone": lead["phone"],
            "title": random.choice(["Manager", "Director", "VP", "Individual Contributor"]),
            "department": random.choice(["Sales", "Operations", "IT", "Finance"]),
            "lead_source": lead["lead_source"],
            "created_date": str(created),
            "is_primary": random.choice(["true", "false", "false"]),
        })

    remaining = COUNTS["contacts"] - len(rows)
    for i in range(remaining):
        fn = random.choice(FIRST_NAMES)
        ln = random.choice(LAST_NAMES)
        created = rand_date(date(2021, 1, 1), date(2025, 12, 31))
        owner_id = weighted_owner(frontline_users, user_by_id, {"BDR": 30, "SDR": 30, "AE": 40})
        rows.append({
            "id": sf_id(ID_PREFIX["contact"]),
            "account_id": random.choice(account_ids),
            "owner_id": owner_id,
            "first_name": fn,
            "last_name": ln,
            "email": f"{fn.lower()}.{ln.lower()}.{i}@contact.example",
            "phone": f"+1-555-{random.randint(100, 999)}-{random.randint(1000, 9999)}",
            "title": random.choice(["Manager", "Director", "VP", "Individual Contributor"]),
            "department": random.choice(["Sales", "Operations", "IT", "Finance"]),
            "lead_source": random.choice(LEAD_SOURCES),
            "created_date": str(created),
            "is_primary": random.choice(["true", "false", "false"]),
        })

    return rows, lead_to_contact


def build_opportunities(frontline_users, user_by_id, accounts, leads, converted_lead_ids):
    rows = []
    account_ids = [a["id"] for a in accounts]
    converted_leads = [l for l in leads if l["id"] in converted_lead_ids]
    random.shuffle(converted_leads)
    converted_limit = int(round(COUNTS["opportunities"] * 0.55))

    lead_to_opp = {}
    for i in range(COUNTS["opportunities"]):
        from_lead = i < converted_limit and i < len(converted_leads)
        lead = converted_leads[i] if from_lead else None
        opp_id = sf_id(ID_PREFIX["opportunity"])
        role_dist = {"BDR": 10, "SDR": 10, "AE": 80}
        owner_id = weighted_owner(frontline_users, user_by_id, role_dist)
        owner_role = user_by_id[owner_id]["role"]

        if owner_role == "AE":
            stage = random.choices(OPP_STAGES, weights=[8, 12, 18, 17, 33, 12], k=1)[0]
        else:
            stage = random.choices(OPP_STAGES, weights=[12, 18, 26, 18, 10, 16], k=1)[0]

        created = rand_date(date(2022, 1, 1), date(2025, 12, 31))
        close_date = created + timedelta(days=random.randint(15, 180))

        account_id = lead["converted_account_id"] if lead and lead["converted_account_id"] else random.choice(account_ids)
        lead_source_id = lead["id"] if lead else ""
        if lead:
            lead_to_opp[lead["id"]] = opp_id

        rows.append({
            "id": opp_id,
            "name": f"{random.choice(COMPANY_PREFIX)} Expansion {i + 1}",
            "account_id": account_id,
            "owner_id": owner_id,
            "stage_name": stage,
            "amount": random.randint(5000, 250000),
            "probability": {
                "Prospecting": 10, "Qualification": 25, "Proposal": 50,
                "Negotiation": 70, "Closed Won": 100, "Closed Lost": 0
            }[stage],
            "close_date": str(close_date),
            "lead_source": random.choice(LEAD_SOURCES),
            "lead_source_id": lead_source_id,
            "created_date": str(created),
        })
    return rows, lead_to_opp


def build_orders(opportunities):
    rows = []
    closed_won = [o for o in opportunities if o["stage_name"] == "Closed Won"]
    random.shuffle(closed_won)
    source = closed_won[:COUNTS["orders"]]
    if len(source) < COUNTS["orders"]:
        fallback = opportunities[: COUNTS["orders"] - len(source)]
        source.extend(fallback)

    for i, opp in enumerate(source):
        activated = rand_date(date(2022, 1, 1), date(2025, 12, 31))
        status = random.choices(ORDER_STATUS, weights=[8, 20, 62, 10], k=1)[0]
        rows.append({
            "id": sf_id(ID_PREFIX["order"]),
            "order_number": f"ORD-{200000 + i}",
            "account_id": opp["account_id"],
            "opportunity_id": opp["id"],
            "owner_id": opp["owner_id"],
            "status": status,
            "effective_date": str(activated),
            "total_amount": random.randint(3000, 300000),
            "contract_term_months": random.choice([12, 24, 36]),
            "created_date": str(activated - timedelta(days=random.randint(1, 14))),
        })
    return rows


def build_order_items(orders):
    rows = []
    order_ids = [o["id"] for o in orders]
    generated = 0
    idx = 0
    while generated < COUNTS["order_items"]:
        order_id = order_ids[idx % len(order_ids)]
        idx += 1
        sku, product_name = random.choice(PRODUCTS)
        quantity = random.randint(1, 40)
        unit_price = random.randint(50, 5000)
        rows.append({
            "id": sf_id(ID_PREFIX["order_item"]),
            "order_id": order_id,
            "product_code": sku,
            "product_name": product_name,
            "quantity": quantity,
            "unit_price": unit_price,
            "discount_pct": random.choice([0, 0, 5, 10, 15, 20]),
            "line_total": quantity * unit_price,
            "service_start_date": str(rand_date(date(2022, 1, 1), date(2025, 12, 31))),
        })
        generated += 1
    return rows


def build_tasks(frontline_users, user_by_id, accounts, contacts, opportunities, leads):
    rows = []
    account_ids = [a["id"] for a in accounts]
    contact_ids = [c["id"] for c in contacts]
    opp_ids = [o["id"] for o in opportunities]
    lead_ids = [l["id"] for l in leads]

    for i in range(COUNTS["tasks"]):
        owner_id = weighted_owner(frontline_users, user_by_id, {"BDR": 40, "SDR": 40, "AE": 20})
        who_type = random.choices(["lead", "contact"], weights=[45, 55], k=1)[0]
        what_type = random.choices(["account", "opportunity", "none"], weights=[45, 45, 10], k=1)[0]
        due = rand_date(date(2022, 1, 1), date(2026, 1, 31))
        rows.append({
            "id": sf_id(ID_PREFIX["task"]),
            "subject": f"{random.choice(TASK_TYPES)} - {random.choice(['Intro', 'Follow-up', 'Next Steps', 'Renewal'])}",
            "type": random.choice(TASK_TYPES),
            "status": random.choice(["Not Started", "In Progress", "Completed", "Deferred"]),
            "priority": random.choice(["High", "Normal", "Low"]),
            "owner_id": owner_id,
            "who_id": random.choice(lead_ids if who_type == "lead" else contact_ids),
            "what_id": "" if what_type == "none" else random.choice(account_ids if what_type == "account" else opp_ids),
            "activity_date": str(due),
            "is_closed": random.choice(["true", "false"]),
            "created_date": str(due - timedelta(days=random.randint(1, 30))),
        })
    return rows


def build_events(frontline_users, user_by_id, accounts, contacts, opportunities):
    rows = []
    account_ids = [a["id"] for a in accounts]
    contact_ids = [c["id"] for c in contacts]
    opp_ids = [o["id"] for o in opportunities]

    for i in range(COUNTS["events"]):
        owner_id = weighted_owner(frontline_users, user_by_id, {"BDR": 20, "SDR": 35, "AE": 45})
        who_id = random.choice(contact_ids)
        what_type = random.choices(["account", "opportunity"], weights=[40, 60], k=1)[0]
        start_date = rand_date(date(2022, 1, 1), date(2026, 1, 31))
        start_dt = datetime.combine(start_date, datetime.min.time()) + timedelta(hours=random.randint(8, 16))
        duration = random.choice([30, 45, 60, 90])
        end_dt = start_dt + timedelta(minutes=duration)
        rows.append({
            "id": sf_id(ID_PREFIX["event"]),
            "subject": f"{random.choice(EVENT_TYPES)} - {random.choice(['Discovery', 'Roadmap', 'Executive', 'Renewal'])}",
            "type": random.choice(EVENT_TYPES),
            "owner_id": owner_id,
            "who_id": who_id,
            "what_id": random.choice(account_ids if what_type == "account" else opp_ids),
            "location": random.choice(["Zoom", "Teams", "Onsite", "Phone"]),
            "start_datetime": start_dt.isoformat(),
            "end_datetime": end_dt.isoformat(),
            "is_all_day_event": "false",
            "created_date": str(start_date - timedelta(days=random.randint(1, 21))),
        })
    return rows


def update_lead_conversions(leads, lead_to_contact, lead_to_opp):
    for lead in leads:
        lid = lead["id"]
        if lid in lead_to_contact:
            lead["is_converted"] = "true"
            lead["converted_contact_id"] = lead_to_contact[lid]
            lead["converted_opportunity_id"] = lead_to_opp.get(lid, "")


def validate(users, accounts, leads, contacts, opportunities, orders, order_items, tasks, events):
    users_set = {r["id"] for r in users}
    account_set = {r["id"] for r in accounts}
    lead_set = {r["id"] for r in leads}
    contact_set = {r["id"] for r in contacts}
    opp_set = {r["id"] for r in opportunities}
    order_set = {r["id"] for r in orders}

    for row in accounts:
        assert row["owner_id"] in users_set
    for row in leads:
        assert row["owner_id"] in users_set
        if row["converted_account_id"]:
            assert row["converted_account_id"] in account_set
        if row["converted_contact_id"]:
            assert row["converted_contact_id"] in contact_set
        if row["converted_opportunity_id"]:
            assert row["converted_opportunity_id"] in opp_set
    for row in contacts:
        assert row["owner_id"] in users_set
        assert row["account_id"] in account_set
    for row in opportunities:
        assert row["owner_id"] in users_set
        assert row["account_id"] in account_set
        if row["lead_source_id"]:
            assert row["lead_source_id"] in lead_set
    for row in orders:
        assert row["account_id"] in account_set
        assert row["opportunity_id"] in opp_set
        assert row["owner_id"] in users_set
    for row in order_items:
        assert row["order_id"] in order_set
    for row in tasks:
        assert row["owner_id"] in users_set
        assert (row["who_id"] in lead_set) or (row["who_id"] in contact_set)
        if row["what_id"]:
            assert (row["what_id"] in account_set) or (row["what_id"] in opp_set)
    for row in events:
        assert row["owner_id"] in users_set
        assert row["who_id"] in contact_set
        assert (row["what_id"] in account_set) or (row["what_id"] in opp_set)

    jami = [u for u in users if u["name"] == "Jami Green" and u["role"] == "Director"]
    assert len(jami) == 1
    director_id = jami[0]["id"]
    managers = [u for u in users if u["role"] == "Manager"]
    for m in managers:
        assert m["manager_id"] == director_id
    reports = Counter(u["manager_id"] for u in users if u["role"] in {"BDR", "SDR", "AE"})
    assert max(reports.values()) <= 10

    roles = Counter(u["role"] for u in users if u["role"] in {"BDR", "SDR", "AE"})
    frontline_total = sum(roles.values())
    assert frontline_total > 0
    assert abs((roles["BDR"] / frontline_total) - 0.30) <= 0.02
    assert abs((roles["SDR"] / frontline_total) - 0.30) <= 0.02
    assert abs((roles["AE"] / frontline_total) - 0.40) <= 0.02

    account_owner_roles = Counter()
    user_lookup = {u["id"]: u for u in users}
    for a in accounts:
        role = user_lookup[a["owner_id"]]["role"]
        if role in {"BDR", "SDR", "AE"}:
            account_owner_roles[role] += 1
    account_total = sum(account_owner_roles.values())
    assert abs((account_owner_roles["BDR"] / account_total) - 0.30) <= 0.03
    assert abs((account_owner_roles["SDR"] / account_total) - 0.30) <= 0.03
    assert abs((account_owner_roles["AE"] / account_total) - 0.40) <= 0.03

    closed_won = [o for o in opportunities if o["stage_name"] == "Closed Won"]
    cw_roles = Counter(user_lookup[o["owner_id"]]["role"] for o in closed_won)
    ae_won = cw_roles["AE"]
    non_ae_won = cw_roles["BDR"] + cw_roles["SDR"] + cw_roles["Manager"] + cw_roles["Director"]
    assert ae_won > non_ae_won


def main():
    users, _, _, frontline = build_users()
    user_by_id = {u["id"]: u for u in users}
    accounts = build_accounts(frontline, user_by_id)
    leads, converted_lead_ids = build_leads(frontline, user_by_id, accounts)
    contacts, lead_to_contact = build_contacts(frontline, user_by_id, accounts, leads, converted_lead_ids)
    opportunities, lead_to_opp = build_opportunities(frontline, user_by_id, accounts, leads, converted_lead_ids)
    update_lead_conversions(leads, lead_to_contact, lead_to_opp)
    orders = build_orders(opportunities)
    order_items = build_order_items(orders)
    tasks = build_tasks(frontline, user_by_id, accounts, contacts, opportunities, leads)
    events = build_events(frontline, user_by_id, accounts, contacts, opportunities)

    validate(users, accounts, leads, contacts, opportunities, orders, order_items, tasks, events)

    write_csv(
        "user.csv",
        users,
        [
            "id", "first_name", "last_name", "name", "title", "role", "manager_id",
            "department", "email", "is_active", "hire_date",
        ],
    )
    write_csv(
        "account.csv",
        accounts,
        [
            "id", "name", "account_number", "owner_id", "type", "industry",
            "annual_revenue", "employee_count", "billing_city", "billing_state",
            "billing_country", "created_date", "is_active",
        ],
    )
    write_csv(
        "lead.csv",
        leads,
        [
            "id", "first_name", "last_name", "company", "email", "phone", "status",
            "lead_source", "owner_id", "created_date", "is_converted",
            "converted_account_id", "converted_contact_id", "converted_opportunity_id",
        ],
    )
    write_csv(
        "contact.csv",
        contacts,
        [
            "id", "account_id", "owner_id", "first_name", "last_name", "email",
            "phone", "title", "department", "lead_source", "created_date", "is_primary",
        ],
    )
    write_csv(
        "opportunity.csv",
        opportunities,
        [
            "id", "name", "account_id", "owner_id", "stage_name", "amount",
            "probability", "close_date", "lead_source", "lead_source_id", "created_date",
        ],
    )
    write_csv(
        "order.csv",
        orders,
        [
            "id", "order_number", "account_id", "opportunity_id", "owner_id", "status",
            "effective_date", "total_amount", "contract_term_months", "created_date",
        ],
    )
    write_csv(
        "order_items.csv",
        order_items,
        [
            "id", "order_id", "product_code", "product_name", "quantity", "unit_price",
            "discount_pct", "line_total", "service_start_date",
        ],
    )
    write_csv(
        "tasks.csv",
        tasks,
        [
            "id", "subject", "type", "status", "priority", "owner_id", "who_id",
            "what_id", "activity_date", "is_closed", "created_date",
        ],
    )
    write_csv(
        "event.csv",
        events,
        [
            "id", "subject", "type", "owner_id", "who_id", "what_id", "location",
            "start_datetime", "end_datetime", "is_all_day_event", "created_date",
        ],
    )

    counts = {
        "user.csv": len(users),
        "account.csv": len(accounts),
        "lead.csv": len(leads),
        "contact.csv": len(contacts),
        "opportunity.csv": len(opportunities),
        "order.csv": len(orders),
        "order_items.csv": len(order_items),
        "tasks.csv": len(tasks),
        "event.csv": len(events),
    }
    print("Generated files and row counts:")
    for k, v in counts.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
