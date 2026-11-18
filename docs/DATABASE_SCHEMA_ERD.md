# Relational Database Schema & Entity-Relationship Diagram (ERD)
## Real Estate Decision Intelligence Platform (Apex Realty AI)

### 1. Entity-Relationship Diagram (Mermaid)

```mermaid
erDiagram
    users ||--o{ business_profiles : owns
    users ||--o{ human_approvals : reviews
    analysis_reports ||--o{ human_approvals : stages
    analysis_reports ||--o{ agent_execution_logs : generates
    properties ||--o{ site_visits : hosts
    properties ||--o{ deals : transacts
    leads ||--o{ site_visits : requests
    leads ||--o{ deals : signs

    users {
        int id PK
        string email UK
        string hashed_password
        string full_name
        string role
        boolean is_active
        datetime created_at
    }

    business_profiles {
        int id PK
        int user_id FK
        string company_name
        string industry
        int team_size
        string business_goals
        datetime updated_at
    }

    properties {
        string property_id PK
        string property_type
        string city
        string locality
        int bedrooms
        float area_sqft
        float asking_price
        date listing_date
        string listing_status
        datetime created_at
    }

    leads {
        string lead_id PK
        string lead_name
        string property_type_interest
        string city
        string lead_source
        date inquiry_date
        float budget_min
        float budget_max
        string lead_status
        string phone
        datetime created_at
    }

    site_visits {
        string visit_id PK
        string lead_id FK
        string property_id FK
        date visit_date
        string visit_feedback
        string visit_outcome
        string agent_id
        datetime created_at
    }

    deals {
        string deal_id PK
        string lead_id FK
        string property_id FK
        date deal_date
        string deal_status
        float sale_price
        float commission_rate
        string agent_id
        datetime created_at
    }

    agent_performance {
        string performance_id PK
        string agent_id
        string period_month
        int calls_made
        int visits_conducted
        int deals_closed
        float customer_rating
        float marketing_spend
        datetime created_at
    }

    expenses {
        string expense_id PK
        date expense_date
        string project_id
        string category
        float amount
        string vendor
        datetime created_at
    }

    analysis_reports {
        int id PK
        string title
        string industry
        string period_start
        string period_end
        text summary
        json kpis_json
        json agent_insights_json
        json strategic_plan_json
        json verification_details_json
        string verification_status
        float confidence_score
        string verified_by
        float execution_time_seconds
        datetime created_at
    }

    agent_execution_logs {
        int id PK
        int report_id FK
        string run_id
        string agent_name
        string agent_role
        string step_name
        string status
        text log_message
        json metrics_snapshot
        datetime created_at
    }

    human_approvals {
        int id PK
        int report_id FK
        string action_key
        string title
        text description
        string category
        string financial_impact
        string risk_level
        string status
        text decision_reason
        string reviewed_by
        datetime reviewed_at
        datetime created_at
    }
```

---

### 2. Table-by-Table Schema Dictionary

| Table Name | Primary Key | Foreign Keys | Row Count | Purpose & Description |
|:---|:---|:---|:---:|:---|
| `properties` | `property_id` | None | 1,200 | Stores property listings with attributes: bedrooms, square footage, asking price, locality, and status (Available, Sold, Pending). |
| `leads` | `lead_id` | None | 1,800 | Customer inquiries across 6 acquisition channels (Campaign, Referral, Social Media, Walk-in, Portal, Website). |
| `site_visits` | `visit_id` | `lead_id`, `property_id` | 1,200 | Physical inspection logs with customer feedback and outcome (Offer Expected, Second Visit, Follow-up, No Interest). |
| `deals` | `deal_id` | `lead_id`, `property_id` | 600 | Real estate transaction negotiations with agreed sale price, broker commission rate, and status (Closed Won, Closed Lost, Under Negotiation). |
| `agent_performance` | `performance_id` | None | 300 | Monthly broker productivity telemetry: outbound calls, visits completed, deals closed, customer ratings, marketing spend. |
| `expenses` | `expense_id` | None | 500 | Operational expenses categorized by Advertising, Maintenance, Legal, Brokerage, Travel, and Office Rent. |
| `users` | `id` | None | Variable | Platform authentication accounts with salted BCrypt passwords and Role-Based Access Control (`admin`, `manager`, `analyst`, `agent`). |
| `business_profiles` | `id` | `user_id` | Variable | Agency corporate parameters, target revenue goals, team size, and geographical market focus. |
| `analysis_reports` | `id` | None | Variable | Multi-agent execution deliverables containing JSON metrics, agent insights, strategic plans, and verification stamps. |
| `agent_execution_logs` | `id` | `report_id` | Variable | Step-by-step audit trail of CrewAI agent thought processes, tools invoked, and intermediate data outputs. |
| `human_approvals` | `id` | `report_id` | Variable | Consequential strategic actions staged by the Strategy Agent, requiring manager authorization before execution. |
