# Data dictionary — `sample_data/csv`

This document describes the synthetic CRM dataset under [`csv/`](csv/). Column names use **snake_case** (export-style). In a Salesforce org, standard object fields are typically **PascalCase** in the API (for example `owner_id` corresponds to `OwnerId`).

**IDs.** Record keys are 18-character strings with Salesforce-style 3-character key prefixes: `005` User, `001` Account, `00Q` Lead, `003` Contact, `006` Opportunity, `801` Order, `802` OrderItem, `00T` Task, `00U` Event.

**Booleans.** Stored as the strings `true` or `false` in the CSV; treat as Boolean when loading for analysis.

**Dates and times.** Calendar dates are `YYYY-MM-DD` strings. `event` start/end are ISO 8601 local-style date-time strings (for example `2022-12-04T08:00:00`).

**Polymorphic lookups (Task and Event).** `who_id` and `what_id` follow Salesforce’s Who/What pattern. For **Task** (`tasks.csv`), `who_id` is a **Lead** or **Contact** ID; `what_id` is an **Account** or **Opportunity** ID, or empty. For **Event** (`event.csv`), `who_id` is always a **Contact** ID; `what_id` is an **Account** or **Opportunity** ID.

---

## `user.csv` — User

Mimics the Salesforce **User** object: internal people who can own records, with a sales hierarchy (Director → Managers → BDR, SDR, AE) and attributes used for ownership and reporting. Some columns mirror common profile or custom org fields in a real deployment.

| Column | Data type | Description |
|--------|-----------|-------------|
| `id` | String (ID) | 18-character User record id (`005` prefix). |
| `first_name` | String | User’s first name. |
| `last_name` | String | User’s last name. |
| `name` | String | Full display name. |
| `title` | String | Job title (for example Director of Sales, Sales Manager, or role-specific rep title). |
| `role` | String | Simplified org role: Director, Manager, BDR, SDR, or AE. |
| `manager_id` | String (ID) or empty | 18-character User id of the direct manager; empty for the top of the hierarchy. |
| `department` | String | Department (for example Sales). |
| `email` | String | Work email address. |
| `is_active` | Boolean (as string) | Whether the user is active (`true` / `false`). |
| `hire_date` | Date | Hire date, `YYYY-MM-DD`. |

---

## `account.csv` — Account

Mimics the Salesforce **Account** object: company or organization records (customers, prospects, partners) with location, size, and ownership.

| Column | Data type | Description |
|--------|-----------|-------------|
| `id` | String (ID) | 18-character Account record id (`001` prefix). |
| `name` | String | Account (company) name. |
| `account_number` | String | Human-readable account number (for example `ACC-100000`). |
| `owner_id` | String (ID) | User id of the account owner. |
| `type` | String | Account classification: Customer, Prospect, or Partner. |
| `industry` | String | Industry category (for example Technology, Healthcare). |
| `annual_revenue` | Integer | Annual revenue, synthetic whole number. |
| `employee_count` | Integer | Approximate headcount. |
| `billing_city` | String | Billing address city. |
| `billing_state` | String | Billing address state (for example two-letter code). |
| `billing_country` | String | Billing address country. |
| `created_date` | Date | Record creation date, `YYYY-MM-DD`. |
| `is_active` | Boolean (as string) | Whether the account is considered active. |

---

## `lead.csv` — Lead

Mimics the Salesforce **Lead** object: unconverted prospect records. Conversion fields link to the Account, Contact, and Opportunity created when a lead is converted in the synthetic pipeline.

| Column | Data type | Description |
|--------|-----------|-------------|
| `id` | String (ID) | 18-character Lead record id (`00Q` prefix). |
| `first_name` | String | Lead’s first name. |
| `last_name` | String | Lead’s last name. |
| `company` | String | Company or account name for the lead. |
| `email` | String | Email address. |
| `phone` | String | Phone number (synthetic). |
| `status` | String | Lead status (for example Open, Working, Nurturing, Qualified). |
| `lead_source` | String | Source of the lead (for example Web, Outbound, Trade Show). |
| `owner_id` | String (ID) | User id of the lead owner. |
| `created_date` | Date | Record creation date, `YYYY-MM-DD`. |
| `is_converted` | Boolean (as string) | Whether the lead was converted in the generated scenario. |
| `converted_account_id` | String (ID) or empty | Account id when converted; empty if not converted. |
| `converted_contact_id` | String (ID) or empty | Contact id when a matching contact was created; empty otherwise. |
| `converted_opportunity_id` | String (ID) or empty | Opportunity id when created from this lead; empty when none. |

---

## `contact.csv` — Contact

Mimics the Salesforce **Contact** object: people tied to accounts. A subset of rows is aligned to converted leads (same name/source pattern); others are generated independently.

| Column | Data type | Description |
|--------|-----------|-------------|
| `id` | String (ID) | 18-character Contact record id (`003` prefix). |
| `account_id` | String (ID) | Parent Account id. |
| `owner_id` | String (ID) | User id of the contact owner. |
| `first_name` | String | Contact’s first name. |
| `last_name` | String | Contact’s last name. |
| `email` | String | Email address. |
| `phone` | String | Phone number (synthetic). |
| `title` | String | Job title (for example Director, Manager). |
| `department` | String | Department (for example Sales, Finance, IT). |
| `lead_source` | String | Attributed lead source, aligned when created from a lead. |
| `created_date` | Date | Record creation date, `YYYY-MM-DD`. |
| `is_primary` | Boolean (as string) | Whether this contact is marked primary for the account context. |

---

## `opportunity.csv` — Opportunity

Mimics the Salesforce **Opportunity** object: pipeline opportunities/deals, linked to an account and owner. `lead_source_id` references a lead when the row was built from a converted lead pool; the text field `lead_source` is a separate label in the generator.

| Column | Data type | Description |
|--------|-----------|-------------|
| `id` | String (ID) | 18-character Opportunity record id (`006` prefix). |
| `name` | String | Opportunity name. |
| `account_id` | String (ID) | Related Account id. |
| `owner_id` | String (ID) | User id of the opportunity owner. |
| `stage_name` | String | Stage (for example Prospecting, Qualification, Proposal, Negotiation, Closed Won, Closed Lost). |
| `amount` | Integer | Deal amount, synthetic whole number (currency not specified). |
| `probability` | Integer | Win probability, 0–100, aligned to stage. |
| `close_date` | Date | Expected or actual close date, `YYYY-MM-DD`. |
| `lead_source` | String | Marketing or channel label (synthetic; not always equal to the originating lead’s source). |
| `lead_source_id` | String (ID) or empty | Lead id when the opportunity was created from a converted lead; empty when not. |
| `created_date` | Date | Record creation date, `YYYY-MM-DD`. |

---

## `order.csv` — Order

Mimics the Salesforce **Order** object: commercial orders linked to an account, opportunity, and owner. The generator preferentially uses Closed Won opportunities, with a fallback to other opportunities if needed to reach the target row count.

| Column | Data type | Description |
|--------|-----------|-------------|
| `id` | String (ID) | 18-character Order record id (`801` prefix). |
| `order_number` | String | Human-readable order number (for example `ORD-200000`). |
| `account_id` | String (ID) | Bill-to or sold-to Account id. |
| `opportunity_id` | String (ID) | Source Opportunity id. |
| `owner_id` | String (ID) | User id of the order owner. |
| `status` | String | Order status (for example Draft, Activated, Fulfilled, Cancelled). |
| `effective_date` | Date | Date the order is effective, `YYYY-MM-DD`. |
| `total_amount` | Integer | Header-level total, synthetic whole number. |
| `contract_term_months` | Integer | Contract length in months (for example 12, 24, 36). |
| `created_date` | Date | Record creation date, `YYYY-MM-DD` (synthetic, often shortly before `effective_date`). |

---

## `order_items.csv` — OrderItem

Mimics the Salesforce **OrderItem** (order line item): product or service lines on an order, with quantity, list-style pricing, and discount. **Data note:** the generator sets `line_total` to `quantity * unit_price` and does **not** reduce the total by `discount_pct`. Use `discount_pct` as a separate analytic dimension; for a discounted line total, compute it yourself if required.

| Column | Data type | Description |
|--------|-----------|-------------|
| `id` | String (ID) | 18-character OrderItem record id (`802` prefix). |
| `order_id` | String (ID) | Parent Order id. |
| `product_code` | String | SKU or product code. |
| `product_name` | String | Product display name. |
| `quantity` | Integer | Number of units. |
| `unit_price` | Integer | Unit price, synthetic whole number. |
| `discount_pct` | Integer | Discount percentage, 0–20 in generation (0, 5, 10, 15, 20, etc.); not applied to `line_total` in this dataset. |
| `line_total` | Integer | Extended line amount in the file (`quantity` × `unit_price` in generation). |
| `service_start_date` | Date | Service or subscription start date, `YYYY-MM-DD`. |

---

## `tasks.csv` — Task

Mimics the Salesforce **Task** object: to-dos and activity records (calls, follow-ups, etc.) with `who_id` (person) and `what_id` (related record) polymorphic references.

| Column | Data type | Description |
|--------|-----------|-------------|
| `id` | String (ID) | 18-character Task record id (`00T` prefix). |
| `subject` | String | Short description of the task. |
| `type` | String | Task type (for example Email, Call, Follow-up, Discovery, Qualification). |
| `status` | String | Task status (for example Not Started, In Progress, Completed, Deferred). |
| `priority` | String | Priority (for example High, Normal, Low). |
| `owner_id` | String (ID) | User id of the task owner (Assigned To). |
| `who_id` | String (ID) | **Who** — related person: Lead id or Contact id. |
| `what_id` | String (ID) or empty | **What** — related non-person record: Account id or Opportunity id; may be empty. |
| `activity_date` | Date | Due or activity date, `YYYY-MM-DD`. |
| `is_closed` | Boolean (as string) | Whether the task is closed. |
| `created_date` | Date | Record creation date, `YYYY-MM-DD`. |

---

## `event.csv` — Event

Mimics the Salesforce **Event** object: scheduled meetings and calendar blocks. `who_id` is always a Contact; `what_id` is an Account or Opportunity.

| Column | Data type | Description |
|--------|-----------|-------------|
| `id` | String (ID) | 18-character Event record id (`00U` prefix). |
| `subject` | String | Event title. |
| `type` | String | Event type (for example Meeting, Demo, Onsite Visit, QBR, Executive Review). |
| `owner_id` | String (ID) | User id of the event owner. |
| `who_id` | String (ID) | **Who** — related Contact id. |
| `what_id` | String (ID) | **What** — related Account id or Opportunity id. |
| `location` | String | Where the event takes place (for example Zoom, Onsite, Phone). |
| `start_datetime` | DateTime | Event start, ISO 8601 local-style string. |
| `end_datetime` | DateTime | Event end, ISO 8601 local-style string. |
| `is_all_day_event` | Boolean (as string) | All-day flag; synthetic data uses `false`. |
| `created_date` | Date | Record creation date, `YYYY-MM-DD`. |
