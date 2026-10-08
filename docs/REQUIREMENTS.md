# ACME Salary Management — Requirements

## User Story

> As the HR Manager of ACME, I want to manage salary data for 10,000 employees across multiple countries via a web application, so that I can stop relying on Excel sheets and quickly answer questions about how the organisation pays people.

---

## Scope & Features

### Employee Management
- Create, view, edit, and delete employee records
- Fields: name, email, employee code, job title, department, country, currency, annual salary (local currency), hire date
- Validation: salary must be positive, email unique and valid, hire date not in the future, currency must match the employee's country

### Employee List
- Paginated table (server-side, 25 rows per page)
- Search by name, email, or employee code
- Filter by country, job title, department — sort by any column
- Salary displayed in local currency with correct formatting

### Insights
- Org-wide: total headcount, average and median salary (USD)
- By country: headcount, min / max / average / median in local currency and USD
- By job title: same stats in USD, with optional country filter
- Salary distribution histogram (10 buckets, USD)
- All USD figures use a fixed exchange rates table (as of 2024-01-01)

### Supporting
- Seed script: 10,000 deterministic employees across 10 countries
- REST API with auto-generated docs (`/docs`)
- Health endpoint: status + employee count

---

## Deliberately Left Out

| Feature | Reason |
|---|---|
| Authentication / roles | Single user. Adds complexity with no value here. Next step. |
| Payroll, tax, payslips | Different problem domain — this is salary *data management*. |
| Bonus, equity, benefits | One clear number (base annual salary) keeps scope clean. |
| Salary history / audit log | Valuable but complex. Next step. |
| Live currency rates | Fixed rates are deterministic and testable. |
| CSV / Excel import | One-time migration concern. Out of scope. |
| Department breakdown in Insights | On the roadmap. |

---

## Success Measures

- Employee list of 10,000 paginates with < 300ms API response
- Insights page answers pay-by-country and pay-by-job-title in one view
- Seed runs in under 10 seconds
- All core tests pass with coverage reported
