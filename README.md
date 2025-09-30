 Smart Meter Energy Consumption Analytics 🔌⚡  

This project analyzes Smart Meter electricity consumption data using Python and Power BI.  
It shows how data can be cleaned, stored, and visualized to identify patterns in energy usage.  

---

 📊 Features  
✔ Data Cleaning with Python (handled missing values, anomalies)  
✔ SQLite Database for storing cleaned data  
✔ Power BI Dashboard with:  
- KPI Cards: Total Consumption, Average Consumption, Anomaly Count  
- Line Chart with 7-day Rolling Average  
- Region-wise Consumption (Bar Chart)  
- Customer-wise Consumption  
- Anomalies Table with highlights  
- Interactive Slicers (Date, Region, Status)  

---

🛠 Tools Used  
- Python (pandas, sqlite3) – for data cleaning & storage  
- Power BI – for dashboard & visualization  
GitHub – for hosting portfolio  

---

 📂 Project Structure  
SmartMeter-Analytics-Project/
│
├── data/
│ ├── Raw_Smart_Meter_Data.csv
│ ├── Clean_Smart_Meter_Data.csv
│ ├── Anomalies.csv
│ └── smart_meter.db
│
├── scripts/
│ └── Data_cleaning.py
│
├── dashboard/
│ ├── Smart_Meter_Consumption.pbix
│ └── DASHBOARD_SCREENSHOT.png
│
└── README.md

---

🚀 How to Run  
1. Run `scripts/Data_cleaning.py` → this cleans raw data & saves files.  
2. Open `dashboard/Smart_Meter_Consumption.pbix` in Power BI.  
3. Explore the dashboard with filters and charts.  

---

 📸 Dashboard Preview  

![Dashboard](dashboard/DASHBOARD_SCREENSHOT.png)
