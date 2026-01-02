# sentinel-logistics-command

<img width="1533" height="717" alt="image" src="https://github.com/user-attachments/assets/bab17315-fd79-4547-af4d-493b50e7e07c" />

# 🛡️ Sentinel: Crisis Logistics Command

**Submission for:** AI for Good Hackathon 2025-26

**Challenge:** Inventory Heatmap & Stock-Out Alerts for Essential Goods

## 🚀 The Vision

In humanitarian crises, logistics data is often fragmented across separate silos—inventory, demand, and procurement. **Sentinel** bridges these gaps by transforming static data into a **Self-Healing Supply Chain**. It moves beyond simple "dashboards" to provide a predictive, AI-augmented command center that ensures life-saving supplies reach those in need before a stock-out occurs.

## 🛠️ Tech Stack (The Snowflake "All-In" Approach)

Sentinel is built natively and entirely within the Snowflake ecosystem to ensure maximum data privacy and performance:

* **Engine:** **Snowflake Dynamic Tables** for real-time stream processing of stock-health metrics.
* **Intelligence:** **Snowflake Cortex AI** (`TRY_COMPLETE`) for tactical supply chain briefings and model resiliency.
* **App Layer:** **Streamlit in Snowflake** for a bi-directional, transactional user interface.
* **Analytics:** **Snowpark Python** for complex "Safety Buffer" calculations and data transformations.
* **Governance:** **Snowflake Horizon** principles for secure, row-level access to sensitive NGO data.

## 💡 Key Innovation: The "Safety Buffer"

Unlike traditional inventory counts, Sentinel calculates a **Predictive Safety Buffer**:



This metric tells a logistics officer not just what they have, but **how many days they have until a total stock-out**, accounting for the time it takes for a new shipment to arrive.

## 🌟 Features

* **Live Risk Heatmap:** Instant visual identification of "Redline" crisis items.
* **AI-Driven Rebalancing:** Cortex AI suggests moving surplus stock from safe zones to crisis zones, reducing waste and procurement costs.
* **Closed-Loop Transactions:** A "Write-Back" architecture that allows users to approve emergency reorders and log incoming shipments directly into the Snowflake ledger from the UI.
* **Interactive Visualization:** Altair-powered gap analysis for at-a-glance tactical awareness.

## 📂 Repository Structure

* `streamlit_app.py`: The core application logic and UI.
* `snowflake_setup.sql`: Backend DDL/DML for tables and Dynamic Table configurations.
* `manifest.csv`: Sample data structure for reproduction.

## 🏁 Impact

By automating the "Insight-to-Action" loop, Sentinel reduces human error in spreadsheet calculations and provides 24/7 monitoring of essential goods, ensuring that no medical facility runs out of life-saving supplies due to a data delay.

---
