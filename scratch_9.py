import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
from collections import defaultdict
import re
from datetime import datetime
import threading
import os

chrome_options = Options()
chrome_options.add_argument("--headless")

def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "_", name)

# Selenium function
def run_selenium_cycle():
    while True:
        driver = webdriver.Chrome(options=chrome_options)
        try:
            print(f"\n🔁 Selenium Cycle Started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            driver.get("http://wcms.whildc.com/wcms/")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "UserName")))

            driver.find_element(By.NAME, "UserName").send_keys("40354")
            driver.find_element(By.NAME, "Password").send_keys("40354@54")
            driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]").click()

            WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Reports') or contains(text(), 'Logout')]")))

            # Tally Report Page Access for Functional Issues
            driver.get("http://wcms.whildc.com/wcms/Report/TallyReport")
            time.sleep(3)

            dropdown = Select(driver.find_element(By.ID, "Type"))
            dropdown.select_by_visible_text("FUQC")
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "btnSave"))).click()
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "table tbody tr")))

            time.sleep(2)

            rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
            raw_data = []
            model_issue_data = defaultdict(lambda: defaultdict(int))
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            for row in rows:
                cols = row.find_elements(By.TAG_NAME, "td")
                if len(cols) >= 4:
                    serial = cols[0].text.strip()
                    model_name = cols[1].text.strip()
                    issue = cols[2].text.strip()
                    quantity = int(cols[3].text.strip())
                    raw_data.append([timestamp, serial, model_name, issue, quantity])
                    model_issue_data[model_name][issue] += quantity

            # Save to tally_report.csv (append)
            file_exists = os.path.isfile('tally_report.csv')
            with open('tally_report.csv', 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                if not file_exists:
                    writer.writerow(["Timestamp", "Serial", "Model Name", "Issue", "Quantity"])
                writer.writerows(raw_data)
            print("📁 Data appended to tally_report.csv")

            # Save to tally_report_2.csv (overwrite)
            with open('tally_report_2.csv', 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["Timestamp", "Serial", "Model Name", "Issue", "Quantity"])
                writer.writerows(raw_data)
            print("📁 Data written to tally_report_2.csv")

            # Tally Report Page Access for Aesthetic Issues
            driver.get("http://wcms.whildc.com/wcms/Report/TallyReport")
            time.sleep(3)

            dropdown = Select(driver.find_element(By.ID, "Type"))
            dropdown.select_by_visible_text("ASTQC")
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "btnSave"))).click()
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "table tbody tr")))

            time.sleep(2)

            rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
            raw_data = []
            model_issue_data = defaultdict(lambda: defaultdict(int))
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            for row in rows:
                cols = row.find_elements(By.TAG_NAME, "td")
                if len(cols) >= 4:
                    serial = cols[0].text.strip()
                    model_name = cols[1].text.strip()
                    issue = cols[2].text.strip()
                    quantity = int(cols[3].text.strip())
                    raw_data.append([timestamp, serial, model_name, issue, quantity])
                    model_issue_data[model_name][issue] += quantity

            # Save to tally_report_AST.csv (append)
            file_exists = os.path.isfile('tally_report_AST.csv')
            with open('tally_report_AST.csv', 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                if not file_exists:
                    writer.writerow(["Timestamp", "Serial", "Model Name", "Issue", "Quantity"])
                writer.writerows(raw_data)
            print("📁 Data appended to tally_report_AST.csv")

            # Save to tally_report_2_AST.csv (overwrite)
            with open('tally_report_2_AST.csv', 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["Timestamp", "Serial", "Model Name", "Issue", "Quantity"])
                writer.writerows(raw_data)
            print("📁 Data written to tally_report_2_AST.csv")

            # Checked Data ===
            driver.get("http://wcms.whildc.com/wcms/Report/ProductionQcFaultScenerio")
            time.sleep(4)

            try:
                search_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Search')]"))
                )
                search_button.click()
            except:
                print("⚠️ Search button not found or not clickable.")

            # Extract checked data
            rows = driver.find_elements(By.CSS_SELECTOR, "#QcProductionData tbody tr")
            data = []
            for row in rows:
                cols = row.find_elements(By.TAG_NAME, "td")
                if len(cols) >= 4:
                    project = cols[1].text.strip()
                    checked = cols[3].text.strip().replace(',', '')
                    try:
                        checked = int(checked)
                    except:
                        checked = 0
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    data.append((project, checked, timestamp))

            # === Append checked data to CSV file ===
            csv_file_path = "checked.csv"

            # Create a DataFrame with the new data
            new_df = pd.DataFrame(data, columns=["Project", "Checked", "Timestamp"])

            # Overwrite the 'checked.csv' file with the new data
            new_df.to_csv(csv_file_path, index=False)

            print("✅ Data written to 'checked.csv' (overwritten)")

            # === Calculate Issue Percentages ===
            # Get total checked quantity per model from checked.csv
            checked_data = pd.read_csv("checked.csv")
            total_checked = checked_data.groupby("Project")["Checked"].sum()

            # Load tally report###########################################################################################

            common_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Process first file (tally_report_2.csv)
            df1 = pd.read_csv("tally_report_2.csv")
            df1['Timestamp'] = common_timestamp  # Set the common timestamp
            df1 = df1.dropna(subset=['Timestamp'])

            # Calculate percentage for each issue
            df1['Checked Quantity'] = df1['Model Name'].map(total_checked)
            df1['Percentage'] = df1['Quantity'] / df1['Checked Quantity'] * 100

            # Save to trend_percentage.csv (append)
            df1 = df1[['Timestamp', 'Model Name', 'Issue', 'Percentage']]
            df1.to_csv("trend_percentage.csv", mode='a', header=not os.path.isfile('trend_percentage.csv'), index=False)

            # Process second file (tally_report_2_AST.csv)
            df1 = pd.read_csv("tally_report_2_AST.csv")
            df1['Timestamp'] = common_timestamp  # Set the same common timestamp
            df1 = df1.dropna(subset=['Timestamp'])

            # Calculate percentage for each issue
            df1['Checked Quantity'] = df1['Model Name'].map(total_checked)
            df1['Percentage'] = df1['Quantity'] / df1['Checked Quantity'] * 100

            # Save to trend_percentage.csv (append)
            df1 = df1[['Timestamp', 'Model Name', 'Issue', 'Percentage']]
            df1.to_csv("trend_percentage.csv", mode='a', header=False,
                       index=False)  # Skip header for subsequent appends

            print("✅ Data appended to 'trend_percentage.csv' with the same timestamp for both datasets")

#############################################



            print("📁 Data appended to trend_percentage.csv")

        except Exception as e:
            print(f"❌ Error: {e}")
        finally:
            driver.quit()
            print("⏳ Waiting 30s...\n")
            time.sleep(30)

# Fault Issue Summary Dashboard
def run_summary_dashboard():
    app = dash.Dash(__name__)
    app.title = "Fault Issue Summary Dashboard"

    app.layout = html.Div([
        html.H1("📊 Fault Issue Summary Dashboard (Russel)", style={"textAlign": "center"}),
        dcc.Dropdown(id='model-dropdown', placeholder="Select models", multi=True),
        html.Div(id='graphs-container'),
        html.Div(id='last-updated', style={'textAlign': 'center', 'marginTop': '10px', 'color': 'gray'})
    ])

    @app.callback(
        [Output('model-dropdown', 'options'),
         Output('model-dropdown', 'value')],
        Input('model-dropdown', 'value')
    )
    def update_model_dropdown(_):
        df = pd.read_csv("tally_report_2.csv")
        models = df["Model Name"].unique()
        return [{"label": model, "value": model} for model in models], models.tolist()

    @app.callback(
        [Output('graphs-container', 'children'),
         Output('last-updated', 'children')],
        Input('model-dropdown', 'value')
    )
    def update_charts(models, grouped=None):
        # Read and group first CSV
        df1 = pd.read_csv("tally_report_2.csv")
        filtered1 = df1[df1["Model Name"].isin(models)]
        grouped1 = filtered1.groupby(["Model Name", "Issue"])["Quantity"].sum().reset_index()

        # Read and group second CSV
        df2 = pd.read_csv("tally_report_2_AST.csv")
        filtered2 = df2[df2["Model Name"].isin(models)]
        grouped2 = filtered2.groupby(["Model Name", "Issue"])["Quantity"].sum().reset_index()

        # Combine the grouped data
        combined = pd.concat([grouped1, grouped2])
        grouped = combined.groupby(["Model Name", "Issue"])["Quantity"].sum().reset_index()

        # Create charts
        graphs = []
        for model in models:
            model_data = grouped[grouped["Model Name"] == model]

            if not model_data.empty:
                model_data = model_data.copy()  # Optional but helps clarity
                model_data.loc[:, "Issue"] = model_data["Issue"].astype(str)
                fig = px.bar(model_data, x="Issue", y="Quantity",
                             title=f"Issue Summary - {model}",
                             color="Issue", text_auto=True)
                fig.update_layout(xaxis_tickangle=-45)
                graphs.append(dcc.Graph(figure=fig))
            else:
                graphs.append(html.Div(f"No data for model: {model}"))

        last_updated = f"Last updated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}"
        return graphs, last_updated

    app.run(port=8050, debug=True, use_reloader=False)
# Fault Trend Over Time Dashboard
def run_trend_dashboard():
    app = dash.Dash(__name__)
    app.title = "Fault Trend Over Time Dashboard"

    app.layout = html.Div([
        html.H1("📈 Fault Trend Over Time (Russel)", style={"textAlign": "center"}),
        html.Div(id='trend-graphs-container')
    ])

    @app.callback(
        Output('trend-graphs-container', 'children'),
        Input('trend-graphs-container', 'id')  # dummy input to trigger once
    )
    def update_trend_charts(_):
        # Read both CSV files
        df1 = pd.read_csv("tally_report.csv")
        df2 = pd.read_csv("tally_report_AST.csv")

        # Convert Timestamp to datetime and clean invalid timestamps
        df1['Timestamp'] = pd.to_datetime(df1['Timestamp'], errors='coerce')
        df2['Timestamp'] = pd.to_datetime(df2['Timestamp'], errors='coerce')
        df1 = df1.dropna(subset=['Timestamp'])
        df2 = df2.dropna(subset=['Timestamp'])

        # Combine both dataframes
        df = pd.concat([df1, df2], ignore_index=True)

        charts = []

        # Create charts for each model
        for model in df["Model Name"].unique():
            model_df = df[df["Model Name"] == model]

            # Group data by Timestamp and Issue, and sum the Quantity for each Issue at each Timestamp
            grouped = model_df.groupby(["Timestamp", "Issue"])["Quantity"].sum().reset_index()

            # Sort the issues by Quantity in descending order (optional, but doesn't affect line plot order)
            grouped_sorted = grouped.sort_values(by="Quantity", ascending=False)

            # Create the line plot for each issue
            fig = px.line(
                grouped_sorted,
                x="Timestamp", y="Quantity", color="Issue",
                title=f"Trend Over Time - {model}",
                labels={"Quantity": "Fault Count", "Timestamp": "Time", "Issue": "Issue"},
                markers=True
            )

            fig.update_layout(
                xaxis_title="Time",
                yaxis_title="Quantity",
                legend_title="Issue",
                xaxis=dict(tickformat='%Y-%m-%d %H:%M:%S'),
                yaxis=dict(automargin=True)
            )

            charts.append(dcc.Graph(figure=fig))

        return charts

    app.run(port=8051, debug=True, use_reloader=False)

# Fault Issue Percentage Over Time Dashboard
def run_percentage_dashboard():
    app = dash.Dash(__name__)
    app.title = "Fault Issue Percentage Over Time Dashboard"

    app.layout = html.Div([
        html.H1("📉 Fault Issue Percentage Over Time", style={"textAlign": "center"}),
        html.Div(id='percentage-graphs-container'),

        dcc.Interval(
            id="interval-component",
            interval=5 * 1000,  # Update every 5 seconds
            n_intervals=0
        )

    ])

    @app.callback(
        Output('percentage-graphs-container', 'children'),
        Input('percentage-graphs-container', 'id')  # dummy input to trigger once
    )
    def update_percentage_charts(_):
        # Read the trend percentage data
        df = pd.read_csv("trend_percentage.csv")

        charts = []

        # Create charts for each model
        for model in df["Model Name"].unique():
            model_df = df[df["Model Name"] == model]

            # Group data by Timestamp and Issue, and calculate the percentage
            grouped = model_df.groupby(["Timestamp", "Issue"])["Percentage"].mean().reset_index()

            # Create the line plot for each issue
            fig = px.line(
                grouped,
                x="Timestamp", y="Percentage", color="Issue",
                title=f"Percentage Trend Over Time - {model}",
                labels={"Percentage": "Fault Percentage", "Timestamp": "Time", "Issue": "Issue"},
                markers=True
            )

            fig.update_layout(
                xaxis_title="Time",
                yaxis_title="Percentage",
                legend_title="Issue",
                xaxis=dict(tickformat='%Y-%m-%d %H:%M:%S'),
                yaxis=dict(automargin=True)
            )

            charts.append(dcc.Graph(figure=fig))

        return charts

    app.run(port=8052, debug=True, use_reloader=False)  # Change this line from run_server to run

if __name__ == "__main__":
    # Run Selenium cycle in a separate thread
    selenium_thread = threading.Thread(target=run_selenium_cycle, daemon=True)
    selenium_thread.start()

    # Run all three dashboards
    summary_thread = threading.Thread(target=run_summary_dashboard, daemon=True)
    trend_thread = threading.Thread(target=run_trend_dashboard, daemon=True)
    percentage_thread = threading.Thread(target=run_percentage_dashboard, daemon=True)

    summary_thread.start()
    trend_thread.start()
    percentage_thread.start()

    # Keep the main thread alive
    summary_thread.join()
    trend_thread.join()
    percentage_thread.join()
