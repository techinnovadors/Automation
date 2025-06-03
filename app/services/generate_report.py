from datetime import datetime
from weasyprint import HTML
import json
import os


def generate_financial_analysis_html(json_data: dict):
    """
    Generates an HTML string for the financial analysis report based on JSON data.
    Includes CSS for minimal page margins suitable for WeasyPrint.
    """
    analysis = json_data.get("financial_analysis", {})
    summary = analysis.get("overall_financial_summary", {}).get(
        "comparative_periods", [{}]
    )[0]
    ratios = analysis.get("detailed_ratio_analysis", {})
    deep_dive = analysis.get("specific_financial_deep_dive", {})

    # --- Overall Financial Summary ---
    current_fy = summary.get("current_fy_data", {})
    previous_fy = summary.get("previous_fy_data", {})
    assets_summary = summary.get("assets_summary", {})
    income_profitability_summary = summary.get("income_and_profitability_summary", {})
    liquidity_position = summary.get("liquidity_position", {})

    summary_html = f"""
    <div class="section">
        <h2>Overall Financial Summary</h2>
        <div class="subsection">
            <h3>{summary.get('comparison_years', 'FY Comparison')}</h3>

            <h4>Current FY Data ({summary.get('comparison_years', '').split(' vs ')[0] if 'vs' in summary.get('comparison_years', '') else 'Current FY'})</h4>
            <div class="data-point">
                <strong>Shareholders' Equity:</strong> {current_fy.get('shareholders_equity', {}).get('value', 'N/A')}
                <span class="note">{current_fy.get('shareholders_equity', {}).get('notes', '')}</span>
            </div>
            <div class="data-point">
                <strong>Equity Share Capital:</strong> {current_fy.get('equity_share_capital', {}).get('value', 'N/A')}
                <span class="note">{current_fy.get('equity_share_capital', {}).get('notes', '')}</span>
            </div>
            <div class="data-point">
                <strong>Total Debt:</strong> {current_fy.get('total_debt', {}).get('value', 'N/A')}
                <span class="note">{current_fy.get('total_debt', {}).get('notes', '')}</span>
            </div>
            <div class="data-point">
                <strong>Total Debt (Financing Ratio):</strong> {current_fy.get('total_debt', {}).get('financing_ratio', 'N/A')}
            </div>

            <h4>Previous FY Data ({summary.get('comparison_years', '').split(' vs ')[1] if 'vs' in summary.get('comparison_years', '') else 'Previous FY'})</h4>
            <div class="data-point">
                <strong>Shareholders' Equity:</strong> {previous_fy.get('shareholders_equity', {}).get('value', 'N/A')}
                <span class="note">{previous_fy.get('shareholders_equity', {}).get('notes', '')}</span>
            </div>
            <div class="data-point">
                <strong>Equity Share Capital:</strong> {previous_fy.get('equity_share_capital', {}).get('value', 'N/A')}
                <span class="note">{previous_fy.get('equity_share_capital', {}).get('notes', '')}</span>
            </div>
            <div class="data-point">
                <strong>Total Debt:</strong> {previous_fy.get('total_debt', {}).get('value', 'N/A')}
                <span class="note">{previous_fy.get('total_debt', {}).get('notes', '')}</span>
            </div>
            <div class="data-point">
                <strong>Total Debt (Financing Ratio):</strong> {previous_fy.get('total_debt', {}).get('financing_ratio', 'N/A')}
            </div>

            <h4>Assets Summary</h4>
            <div class="data-point">
                <strong>Total Assets:</strong> {assets_summary.get('total_assets', {}).get('value', 'N/A')}
                <span class="note">{assets_summary.get('total_assets', {}).get('notes', '')}</span>
            </div>
            <div class="data-point">
                <strong>Property, Plant & Equipment (net) notes:</strong> {assets_summary.get('property_plant_equipment_notes', 'N/A')}
            </div>
            <div class="data-point">
                <strong>Current Assets notes:</strong> {assets_summary.get('current_assets_notes', 'N/A')}
            </div>
            <div class="data-point">
                <strong>Cash & Bank Balances:</strong> {assets_summary.get('cash_and_bank_balances', 'N/A')}
            </div>
            <div class="data-point">
                <strong>Inventory:</strong> {assets_summary.get('inventory', 'N/A')}
            </div>

            <h4>Income & Profitability Summary</h4>
            <div class="data-point">
                <strong>Revenue from Operations:</strong> {income_profitability_summary.get('revenue_from_operations', {}).get('value', 'N/A')}
                <span class="note">{income_profitability_summary.get('revenue_from_operations', {}).get('notes', '')}</span>
            </div>
            <div class="data-point">
                <strong>Other Income notes:</strong> {income_profitability_summary.get('other_income_notes', 'N/A')}
            </div>
            <div class="data-point">
                <strong>Total Income notes:</strong> {income_profitability_summary.get('total_income_notes', 'N/A')}
            </div>
            <div class="data-point">
                <strong>Operating Expenses notes:</strong> {income_profitability_summary.get('operating_expenses_notes', 'N/A')}
            </div>
            <h4>Key Operating Expenses:</h4>
            <ul>
                {"".join([f'<li class="list-item">{item}</li>' for item in income_profitability_summary.get('key_operating_expenses', [])])}
            </ul>
            <div class="data-point">
                <strong>Finance Costs notes:</strong> {income_profitability_summary.get('finance_costs_notes', 'N/A')}
            </div>
            <div class="data-point">
                <strong>Depreciation notes:</strong> {income_profitability_summary.get('depreciation_notes', 'N/A')}
            </div>
            <div class="data-point">
                <strong>Net Profit After Tax:</strong> {income_profitability_summary.get('net_profit_after_tax', {}).get('value', 'N/A')}
                <span class="note">{income_profitability_summary.get('net_profit_after_tax', {}).get('notes', '')}</span>
            </div>
            <div class="data-point">
                <strong>Net Profit Margin:</strong> {income_profitability_summary.get('net_profit_margin', {}).get('value', 'N/A')}
                <span class="note">{income_profitability_summary.get('net_profit_margin', {}).get('notes', '')}</span>
            </div>
            <div class="data-point">
                <strong>Dividends:</strong> {income_profitability_summary.get('dividends', 'N/A')}
            </div>
            <div class="data-point">
                <strong>Tax Expense:</strong> {income_profitability_summary.get('tax_expense', 'N/A')}
            </div>

            <h4>Liquidity Position</h4>
            <div class="data-point">
                <strong>Current Ratio:</strong> {liquidity_position.get('current_ratio', 'N/A')}
                <span class="note">{liquidity_position.get('notes', '')}</span>
            </div>

            <h4>Overall Change Notes</h4>
            <p>{summary.get('overall_change_notes', 'N/A')}</p>
        </div>
    </div>
    """

    # --- Detailed Ratio Analysis ---
    ratio_analysis_html = """
    <div class="section ratio-analysis">
        <h2>Detailed Ratio Analysis</h2>
    """
    for ratio_type, ratios_list in ratios.items():
        ratio_analysis_html += f"<h3>{ratio_type.replace('_', ' ').title()}</h3>"
        for ratio in ratios_list:
            ratio_analysis_html += f"""
            <div class="subsection">
                <h4>{ratio.get('ratio_name', 'N/A')}</h4>
                <div class="data-point">
                    <strong>Calculation Formula:</strong> {ratio.get('calculation_formula', 'N/A')}
                </div>
                <div class="data-point">
                    <strong>Interpretation & Analysis:</strong> {ratio.get('interpretation_and_analysis', 'N/A')}
                </div>
            </div>
            """
    ratio_analysis_html += "</div>"

    # --- Specific Financial Deep Dive ---
    deep_dive_html = """
    <div class="section deep-dive">
        <h2>Specific Financial Deep Dive</h2>
    """
    for key, item in deep_dive.items():
        deep_dive_html += f"""
        <div class="subsection">
            <h4>{key.replace('_', ' ').title()}</h4>
            <div class="data-point">
                <strong>Assessment:</strong> {item.get('assessment', 'N/A')}
            </div>
            <div class="data-point">
                <strong>Details:</strong> {item.get('details', 'N/A')}
            </div>
            """
        # Add specific sub-fields if they exist
        if item.get("investments"):
            deep_dive_html += f"""
            <div class="data-point">
                <strong>Investments:</strong> {item.get('investments', 'N/A')}
            </div>
            """
        if item.get("loans_and_advances"):
            deep_dive_html += f"""
            <div class="data-point">
                <strong>Loans and Advances:</strong> {item.get('loans_and_advances', 'N/A')}
            </div>
            """
        if item.get("contingent_liabilities"):
            deep_dive_html += f"""
            <div class="data-point">
                <strong>Contingent Liabilities:</strong> {item.get('contingent_liabilities', 'N/A')}
            </div>
            """
        if item.get("conclusion"):
            deep_dive_html += f"""
            <div class="data-point">
                <strong>Conclusion:</strong> {item.get('conclusion', 'N/A')}
            </div>
            """
        deep_dive_html += "</div>"  # Close subsection
    deep_dive_html += "</div>"  # Close section

    # --- Full HTML Template with WeasyPrint specific CSS for margins ---
    html_template = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Financial Analysis Report</title>
        <style>
            /* --- WeasyPrint Specific Page Styling --- */
            @page {{
                margin: 5mm; /* Set all margins to a minimum value, e.g., 5mm */
            }}

            /* --- General Body and Container Styles --- */
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6;
                /* Important: Set body margin/padding to 0 to avoid double margins with @page */
                margin: 0;
                padding: 0;
                color: #333;
                background-color: #f4f4f4; /* This will be ignored in print media */
            }}
            .container {{
                max-width: 1000px; /* Max width for content */
                margin: 0 auto; /* Center the container, if there's extra space */
                background: #fff;
                padding: 20px; /* Add internal padding for content within the page */
                border-radius: 8px; /* Visual only, less relevant for print */
                box-shadow: 0 0 15px rgba(0,0,0,0.1); /* Visual only */
            }}

            /* --- Other existing styles --- */
            h1, h2, h3, h4 {{
                color: #2c3e50;
                border-bottom: 2px solid #3498db;
                padding-bottom: 10px;
                margin-top: 25px;
            }}
            h1 {{
                text-align: center;
                font-size: 2.2em;
                color: #3498db;
                border-bottom: 3px solid #3498db;
                padding-bottom: 15px;
                margin-bottom: 30px;
            }}
            h2 {{
                font-size: 1.8em;
                color: #2980b9;
            }}
            h3 {{
                font-size: 1.4em;
                color: #34495e;
                border-bottom: 1px solid #eee;
                padding-bottom: 5px;
                margin-top: 20px;
            }}
            h4 {{
                font-size: 1.2em;
                color: #4a6a8a;
                margin-top: 15px;
                margin-bottom: 5px;
            }}
            .section {{
                margin-bottom: 25px;
                padding: 15px;
                border: 1px solid #eee;
                border-radius: 5px;
                background-color: #fafafa;
            }}
            .subsection {{
                margin-bottom: 20px;
                padding: 10px;
                background-color: #ffffff;
                border-left: 4px solid #5cb85c;
                padding-left: 15px;
                border-radius: 3px;
            }}
            .data-point {{
                margin-bottom: 10px;
            }}
            .data-point strong {{
                color: #555;
                display: inline-block;
                width: 250px; /* Adjust as needed */
            }}
            .note {{
                font-style: italic;
                color: #666;
                margin-left: 260px; /* Align with data point values */
                display: block;
                margin-top: -5px;
                font-size: 0.9em;
            }}
            .list-item {{
                margin-left: 20px;
                list-style-type: disc;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 15px;
            }}
            th, td {{
                border: 1px solid #ddd;
                padding: 10px;
                text-align: left;
            }}
            th {{
                background-color: #f2f2f2;
                color: #333;
            }}
            .ratio-analysis .subsection {{
                border-left: 4px solid #f0ad4e;
            }}
            .deep-dive .subsection {{
                border-left: 4px solid #5bc0de;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Financial Analysis Report</h1>
            {summary_html}
            {ratio_analysis_html}
            {deep_dive_html}
        </div>
    </body>
    </html>
    """
    return html_template


def ensure_output_directory(directory_path: str) -> None:
    """
    Ensure the output directory exists, creating it if necessary.

    Args:
        directory_path (str): Path to the directory that should exist

    Raises:
        FileNotFoundError: If parent directory doesn't exist and can't be created
        PermissionError: If there's no permission to create the directory
        Exception: For other system-related errors
    """
    try:
        if not os.path.exists(directory_path):
            os.makedirs(directory_path, exist_ok=True)
    except FileNotFoundError as e:
        raise FileNotFoundError(
            f"Could not create output directory '{directory_path}': {str(e)}"
        )
    except PermissionError as e:
        raise PermissionError(
            f"No permission to create output directory '{directory_path}': {str(e)}"
        )
    except Exception as e:
        raise Exception(f"Error creating output directory '{directory_path}': {str(e)}")


def save_pdf(html_content: str, file_name: str):
    """
    Save HTML content as PDF using WeasyPrint.

    Args:
        html_content (str): HTML content to convert to PDF
        file_name (str): Name of the output PDF file

    Raises:
        FileNotFoundError: If the output directory doesn't exist
        PermissionError: If there's no permission to write to the directory
        ValueError: If the HTML content is invalid
        Exception: For other WeasyPrint or system-related errors
    """
    try:
        # Ensure output directory exists
        output_dir = os.path.dirname(file_name)
        ensure_output_directory(output_dir)

        # Generate PDF
        HTML(string=html_content, encoding="utf-8").write_pdf(file_name)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Could not create output directory: {str(e)}")
    except PermissionError as e:
        raise PermissionError(f"Permission denied when writing PDF file: {str(e)}")
    except ValueError as e:
        raise ValueError(f"Invalid HTML content: {str(e)}")
    except Exception as e:
        raise Exception(f"Error generating PDF: {str(e)}")


def generate_pdf(json_data: dict, file_name: str):
    """
    Generate a PDF report from JSON data.

    Args:
        json_data (dict): Financial analysis data in JSON format
        file_name (str): Base name for the output PDF file

    Returns:
        str: Path to the generated PDF file

    Raises:
        ValueError: If json_data is invalid or missing required fields
        FileNotFoundError: If output directory cannot be created
        PermissionError: If there's no permission to create/write to output directory
        Exception: For other errors during PDF generation
    """
    try:
        # Validate input data
        if not isinstance(json_data, dict):
            raise ValueError("json_data must be a dictionary")
        if not json_data.get("financial_analysis"):
            raise ValueError("json_data missing required 'financial_analysis' field")

        # Generate HTML content
        html_content = generate_financial_analysis_html(json_data)

        # Format filename and ensure output directory exists
        file_name = file_name.lower()
        file_name = file_name.replace(" ", "_")
        output_dir = "output_pdfs"
        ensure_output_directory(output_dir)

        output_path = f"{output_dir}/{file_name}-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.pdf"

        # Save PDF
        save_pdf(html_content, output_path)

        return output_path

    except ValueError as e:
        raise ValueError(f"Invalid input data: {str(e)}")
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Output directory error: {str(e)}")
    except PermissionError as e:
        raise PermissionError(f"Permission error: {str(e)}")
    except Exception as e:
        raise Exception(f"Error generating PDF report: {str(e)}")


# # # Your provided JSON data
# json_data = {
#     "financial_analysis": {
#         "overall_financial_summary": {
#             "comparative_periods": [
#                 {
#                     "comparison_years": "FY 2024-25 vs FY 2023-24",
#                     "current_fy_data": {
#                         "shareholders_equity": {
#                             "value": "18,252.53 lakhs",
#                             "notes": "↑ due to bonus issue of 11,114.82 lakhs and profit retention of 6,666.27 lakhs. <Balance Sheet 'Total Equity' = 18,252.53 lakhs> <Note 5>"
#                         },
#                         "equity_share_capital": {
#                             "value": "11,611.20 lakhs",
#                             "notes": "↑ due to a bonus issue of 11,114.82 lakhs. <Balance Sheet 'Share capital' = 11,611.20 lakhs> <Note 4>"
#                         },
#                         "total_debt": {
#                             "value": "7,257.01 lakhs",
#                             "notes": "↓ reflecting reduction in both long-term and short-term borrowings. <Total Debt = 7,257.01 lakhs (Long-term borrowings = 3,010.91 lakhs, Short-term borrowings = 4,246.10 lakhs)> <Note 6> <Note 10>",
#                             "financing_ratio": "22.69% of total assets"
#                         }
#                     },
#                     "previous_fy_data": {
#                         "shareholders_equity": {
#                             "value": "11,706.64 lakhs",
#                             "notes": "Strengthened by retained profit. <Balance Sheet 'Total Equity' = 11,706.64 lakhs>"
#                         },
#                         "equity_share_capital": {
#                             "value": "111.20 lakhs",
#                             "notes": "Consistent with prior periods. <Balance Sheet 'Share capital' = 111.20 lakhs>"
#                         },
#                         "total_debt": {
#                             "value": "10,218.75 lakhs",
#                             "notes": "Comprising both long-term and short-term obligations. <Total Debt = 10,218.75 lakhs (Long-term borrowings = 5,137.88 lakhs, Short-term borrowings = 5,080.87 lakhs)> <Note 6> <Note 10>",
#                             "financing_ratio": "34.03% of total assets"
#                         }
#                     },
#                     "assets_summary": {
#                         "total_assets": {
#                             "value": "31,972.01 lakhs",
#                             "notes": "Increased from 30,027.43 lakhs in FY 2023-24, primarily due to higher non-current investments. <Balance Sheet 'Total' = 31,972.01 lakhs; FY 2023-24 = 30,027.43 lakhs>"
#                         },
#                         "property_plant_equipment_notes": "Property, Plant & Equipment (net) showed a modest increase from 5,994.36 lakhs in FY 2023-24 to 6,214.91 lakhs in FY 2024-25, suggesting capital expenditures were largely offset by depreciation, maintaining asset base. <Balance Sheet 'Property, Plant & Equipment' = 6,214.91 lakhs; FY 2023-24 = 5,994.36 lakhs>",
#                         "current_assets_notes": "Total Current Assets slightly decreased from 14,500.66 lakhs to 14,154.03 lakhs, mainly due to a reduction in Cash & Bank Balances and Short-term loans and advances, despite an increase in Trade Receivables. <Balance Sheet 'Total Current assets' = 14,154.03 lakhs; FY 2023-24 = 14,500.66 lakhs>",
#                         "cash_and_bank_balances": "Cash & Bank Balances decreased from 3,015.44 lakhs to 2,374.04 lakhs, indicating cash utilization for operations or debt servicing rather than accumulation. <Balance Sheet 'Cash and bank balances' = 2,374.04 lakhs; FY 2023-24 = 3,015.44 lakhs>",
#                         "inventory": "Inventories remained a relatively small component, decreasing from 350.96 lakhs to 229.51 lakhs."
#                     },
#                     "income_and_profitability_summary": {
#                         "revenue_from_operations": {
#                             "value": "38,692.83 lakhs",
#                             "notes": "Revenue from Operations increased by 5.82% from 36,563.83 lakhs in FY 2023-24, reflecting growth in the company's services business. <Statement of Profit & Loss 'Revenue from Operations' = 38,692.83 lakhs; FY 2023-24 = 36,563.83 lakhs>"
#                         },
#                         "other_income_notes": "Other Income saw a slight increase from 477.70 lakhs to 494.87 lakhs, contributing modestly to overall income, with Profit on Sale of Investment increasing significantly. <Statement of Profit & Loss 'Other income' = 494.87 lakhs; FY 2023-24 = 477.70 lakhs>",
#                         "total_income_notes": "Total Income thus rose from 37,041.53 lakhs to 39,187.70 lakhs, driven primarily by revenue growth. <Statement of Profit & Loss 'Total Income' = 39,187.70 lakhs; FY 2023-24 = 37,041.53 lakhs>",
#                         "operating_expenses_notes": "Total Operating Expenses increased from 26,705.79 lakhs to 27,816.70 lakhs in line with higher activity levels, but relative to revenue, costs were managed effectively as evidenced by improved EBITDA margin. <Statement of Profit & Loss 'Total expenses (II)' = 27,816.70 lakhs; FY 2023-24 = 26,705.79 lakhs>",
#                         "key_operating_expenses": [
#                             "Cost of Services & Spare Parts Consumed: 19,493.48 lakhs (FY25) vs 18,545.85 lakhs (FY24). <Statement of Profit & Loss 'Cost of Services and spare parts consumed' = 19,493.48 lakhs; FY 2023-24 = 18,545.85 lakhs>",
#                             "Employee Benefit Expenses: 6,154.04 lakhs (FY25) vs 5,792.14 lakhs (FY24). <Statement of Profit & Loss 'Employee benefit expenses' = 6,154.04 lakhs; FY 2023-24 = 5,792.14 lakhs>",
#                             "Other Expenses: 2,169.18 lakhs (FY25) vs 2,367.81 lakhs (FY24). <Statement of Profit & Loss 'Other expenses' = 2,169.18 lakhs; FY 2023-24 = 2,367.81 lakhs>"
#                         ],
#                         "finance_costs_notes": "Finance Costs significantly decreased from 1,117.30 lakhs to 837.25 lakhs, reflecting reduced debt obligations and positively impacting profitability. <Statement of Profit & Loss 'Finance costs' = 837.25 lakhs; FY 2023-24 = 1,117.30 lakhs>",
#                         "depreciation_notes": "Depreciation & Amortisation Expense increased slightly from 935.95 lakhs to 1,003.46 lakhs. <Statement of Profit & Loss 'Depreciation and amortisation expense' = 1,003.46 lakhs; FY 2023-24 = 935.95 lakhs>",
#                         "net_profit_after_tax": {
#                             "value": "6,666.27 lakhs",
#                             "notes": "Profit for the year increased by 15.93% from 5,750.06 lakhs in FY 2023-24, demonstrating improved bottom-line performance. <Statement of Profit & Loss 'Profit / (Loss) for the year' = 6,666.27 lakhs; FY 2023-24 = 5,750.06 lakhs>"
#                         },
#                         "net_profit_margin": {
#                             "value": "17.23%",
#                             "notes": "The Net Profit Margin improved from 15.72% in FY 2023-24 to 17.23% in FY 2024-25, indicating enhanced overall efficiency. <Net Profit Margin = 17.23% (6,666.27 lakhs / 38,692.83 lakhs); FY 2023-24 = 15.72% (5,750.06 lakhs / 36,563.83 lakhs)>"
#                         },
#                         "dividends": "No proposed dividend was declared for FY 2024-25, allowing for full retention of profits to bolster reserves. <Note 5>",
#                         "tax_expense": "Total Tax Expense increased from 2,228.32 lakhs to 2,384.76 lakhs, commensurate with the higher taxable profit. <Statement of Profit & Loss 'Total tax expense' = 2,384.76 lakhs; FY 2023-24 = 2,228.32 lakhs>"
#                     },
#                     "liquidity_position": {
#                         "current_ratio": "FY 2024-25: 1.41x; FY 2023-24: 1.38x",
#                         "notes": "The Current Ratio improved slightly from 1.38x to 1.41x, indicating a marginally healthier short-term liquidity position, though still relatively tight. <Balance Sheet 'Total Current assets' = 14,154.03 lakhs; 'Total Current Liabilities' = 10,029.81 lakhs; FY 2023-24 'Total Current assets' = 14,500.66 lakhs; 'Total Current Liabilities' = 10,535.20 lakhs>"
#                     },
#                     "overall_change_notes": "Overall, FY 2024-25 saw strong operational performance leading to higher revenue and net profit. The company significantly reduced its debt burden and bolstered shareholders' equity through profit retention and a bonus issue. While liquidity saw a marginal improvement, the asset base increased, primarily driven by non-current investments. <Statement of Profit & Loss 'Revenue from Operations' = 38,692.83 lakhs; 'Profit / (Loss) for the year' = 6,666.27 lakhs> <Total Debt = 7,257.01 lakhs> <Balance Sheet 'Total Equity' = 18,252.53 lakhs> <Note 4> <Balance Sheet 'Total' = 31,972.01 lakhs>"
#                 }
#             ]
#         },
#         "detailed_ratio_analysis": {
#             "liquidity_ratios": [
#                 {
#                     "ratio_name": "Current Ratio",
#                     "calculation_formula": "Total Current Assets / Total Current Liabilities",
#                     "calculated_values": {
#                         "yearly_values": {}
#                     },
#                     "interpretation_and_analysis": "The Current Ratio improved from 1.38x in FY 2023-24 to 1.41x in FY 2024-25. This indicates a marginal improvement in the company's ability to cover its short-term obligations with its current assets, though still suggesting a relatively lean liquidity position. <Balance Sheet 'Total Current assets' = 14,154.03 lakhs; 'Total Current Liabilities' = 10,029.81 lakhs> <Balance Sheet 'Total Current assets' = 14,500.66 lakhs; 'Total Current Liabilities' = 10,535.20 lakhs>"
#                 },
#                 {
#                     "ratio_name": "Quick Ratio",
#                     "calculation_formula": "(Total Current Assets – Inventories) / Total Current Liabilities",
#                     "calculated_values": {
#                         "yearly_values": {}
#                     },
#                     "interpretation_and_analysis": "The Quick Ratio increased from 1.34x in FY 2023-24 to 1.39x in FY 2024-25. This suggests an improvement in the company's immediate liquidity, as it can cover current liabilities even without relying on inventory sales. The ratio remains healthy, indicating sufficient liquid assets. <Balance Sheet 'Total Current assets' = 14,154.03 lakhs; 'Inventories' = 229.51 lakhs; 'Total Current Liabilities' = 10,029.81 lakhs> <Balance Sheet 'Total Current assets' = 14,500.66 lakhs; 'Inventories' = 350.96 lakhs; 'Total Current Liabilities' = 10,535.20 lakhs>"
#                 }
#             ],
#             "solvency_ratios": [
#                 {
#                     "ratio_name": "Debt-to-Equity Ratio",
#                     "calculation_formula": "Total Debt / Total Equity",
#                     "calculated_values": {
#                         "yearly_values": {}
#                     },
#                     "interpretation_and_analysis": "The Debt-to-Equity Ratio significantly improved from 0.87x in FY 2023-24 to 0.40x in FY 2024-25. This substantial decrease indicates a strong strengthening of the company's capital structure, with a much larger proportion of assets now financed by equity rather than debt. This reduces financial risk and enhances borrowing capacity. <Total Debt = 7,257.01 lakhs (Long-term borrowings = 3,010.91 lakhs, Short-term borrowings = 4,246.10 lakhs); Balance Sheet 'Total Equity' = 18,252.53 lakhs> <Total Debt = 10,218.75 lakhs (Long-term borrowings = 5,137.88 lakhs, Short-term borrowings = 5,080.87 lakhs); Balance Sheet 'Total Equity' = 11,706.64 lakhs>"
#                 },
#                 {
#                     "ratio_name": "Total Debt to Total Assets Ratio",
#                     "calculation_formula": "Total Debt / Total Assets",
#                     "calculated_values": {
#                         "yearly_values": {}
#                     },
#                     "interpretation_and_analysis": "The Total Debt to Total Assets Ratio decreased from 0.34x in FY 2023-24 to 0.23x in FY 2024-25. This indicates a reduced reliance on debt to finance assets, signifying improved financial stability and lower leverage. <Total Debt = 7,257.01 lakhs; Balance Sheet 'Total' = 31,972.01 lakhs> <Total Debt = 10,218.75 lakhs; Balance Sheet 'Total' = 30,027.43 lakhs>"
#                 },
#                 {
#                     "ratio_name": "Interest Coverage Ratio",
#                     "calculation_formula": "EBITDA / Finance Costs",
#                     "calculated_values": {
#                         "yearly_values": {}
#                     },
#                     "interpretation_and_analysis": "The Interest Coverage Ratio significantly improved from 9.25x in FY 2023-24 to 13.58x in FY 2024-25. This strong increase indicates that the company's operating earnings (EBITDA) comfortably cover its finance costs, reflecting strong debt servicing capability and reduced risk. <Statement of Profit & Loss 'EBITDA' = 11,371.00 lakhs; 'Finance costs' = 837.25 lakhs> <Statement of Profit & Loss 'EBITDA' = 10,335.74 lakhs; 'Finance costs' = 1,117.30 lakhs>"
#                 }
#             ],
#             "profitability_ratios": [
#                 {
#                     "ratio_name": "Net Profit Margin",
#                     "calculation_formula": "Profit for the year / Revenue from Operations",
#                     "calculated_values": {
#                         "yearly_values": {}
#                     },
#                     "interpretation_and_analysis": "The Net Profit Margin increased from 15.72% in FY 2023-24 to 17.23% in FY 2024-25. This improvement demonstrates the company's enhanced ability to convert revenue into net profit, likely due to better operational efficiency and reduced finance costs. <Statement of Profit & Loss 'Profit / (Loss) for the year' = 6,666.27 lakhs; 'Revenue from Operations' = 38,692.83 lakhs> <Statement of Profit & Loss 'Profit / (Loss) for the year' = 5,750.06 lakhs; 'Revenue from Operations' = 36,563.83 lakhs>"
#                 },
#                 {
#                     "ratio_name": "EBITDA Margin",
#                     "calculation_formula": "EBITDA / Revenue from Operations",
#                     "calculated_values": {
#                         "yearly_values": {}
#                     },
#                     "interpretation_and_analysis": "The EBITDA Margin improved from 28.27% in FY 2023-24 to 29.39% in FY 2024-25. This indicates a healthy increase in operational profitability before accounting for interest, taxes, depreciation, and amortization, suggesting effective control over core operating expenses. <Statement of Profit & Loss 'EBITDA' = 11,371.00 lakhs; 'Revenue from Operations' = 38,692.83 lakhs> <Statement of Profit & Loss 'EBITDA' = 10,335.74 lakhs; 'Revenue from Operations' = 36,563.83 lakhs>"
#                 },
#                 {
#                     "ratio_name": "Return on Equity",
#                     "calculation_formula": "Profit for the year / Total Equity",
#                     "calculated_values": {
#                         "yearly_values": {}
#                     },
#                     "interpretation_and_analysis": "Return on Equity decreased from 49.12% in FY 2023-24 to 36.52% in FY 2024-25. While net profit increased, the substantial increase in total equity (due to the bonus issue and retained earnings) led to a dilution of the ratio. Despite the decrease, the ratio remains very strong, indicating efficient use of shareholders' capital to generate profit. <Statement of Profit & Loss 'Profit / (Loss) for the year' = 6,666.27 lakhs; Balance Sheet 'Total Equity' = 18,252.53 lakhs> <Statement of Profit & Loss 'Profit / (Loss) for the year' = 5,750.06 lakhs; Balance Sheet 'Total Equity' = 11,706.64 lakhs>"
#                 },
#                 {
#                     "ratio_name": "Return on Assets",
#                     "calculation_formula": "Profit for the year / Total Assets",
#                     "calculated_values": {
#                         "yearly_values": {}
#                     },
#                     "interpretation_and_analysis": "Return on Assets increased from 19.15% in FY 2023-24 to 20.85% in FY 2024-25. This indicates that the company is generating more profit for every unit of assets it employs, reflecting improved overall asset utilization and profitability. <Statement of Profit & Loss 'Profit / (Loss) for the year' = 6,666.27 lakhs; Balance Sheet 'Total' = 31,972.01 lakhs> <Statement of Profit & Loss 'Profit / (Loss) for the year' = 5,750.06 lakhs; Balance Sheet 'Total' = 30,027.43 lakhs>"
#                 }
#             ],
#             "efficiency_ratios": [
#                 {
#                     "ratio_name": "Inventory Turnover",
#                     "calculation_formula": "Cost of Services & Spare Parts Consumed / Inventories",
#                     "calculated_values": {
#                         "yearly_values": {}
#                     },
#                     "interpretation_and_analysis": "The Inventory Turnover ratio significantly increased from 52.84x in FY 2023-24 to 84.93x in FY 2024-25. This indicates a substantial improvement in inventory management and sales efficiency, suggesting that the company is selling its inventory much more quickly. <Statement of Profit & Loss 'Cost of Services and spare parts consumed' = 19,493.48 lakhs; Balance Sheet 'Inventories' = 229.51 lakhs> <Statement of Profit & Loss 'Cost of Services and spare parts consumed' = 18,545.85 lakhs; Balance Sheet 'Inventories' = 350.96 lakhs>"
#                 },
#                 {
#                     "ratio_name": "Trade Receivables Turnover",
#                     "calculation_formula": "Revenue from Operations / Trade Receivables",
#                     "calculated_values": {
#                         "yearly_values": {}
#                     },
#                     "interpretation_and_analysis": "The Trade Receivables Turnover decreased slightly from 8.56x in FY 2023-24 to 8.10x in FY 2024-25. This indicates a minor slowdown in the collection of receivables, meaning it took slightly longer to collect payments from customers. <Statement of Profit & Loss 'Revenue from Operations' = 38,692.83 lakhs; Balance Sheet 'Trade receivables' = 4,776.68 lakhs> <Statement of Profit & Loss 'Revenue from Operations' = 36,563.83 lakhs; Balance Sheet 'Trade receivables' = 4,272.15 lakhs>"
#                 },
#                 {
#                     "ratio_name": "Trade Payables Turnover",
#                     "calculation_formula": "Cost of Services & Spare Parts Consumed / Trade Payables",
#                     "calculated_values": {
#                         "yearly_values": {}
#                     },
#                     "interpretation_and_analysis": "The Trade Payables Turnover significantly decreased from 11.98x in FY 2023-24 to 6.35x in FY 2024-25. This suggests that the company is taking longer to pay its suppliers, indicating it is leveraging supplier credit more effectively or facing cash flow constraints. <Statement of Profit & Loss 'Cost of Services and spare parts consumed' = 19,493.48 lakhs; Note 11 'Trade payables Total' = 3,069.90 lakhs> <Statement of Profit & Loss 'Cost of Services and spare parts consumed' = 18,545.85 lakhs; Note 11 'Trade payables Total' = 1,548.08 lakhs>"
#                 }
#             ]
#         },
#         "specific_financial_deep_dive": {
#             "operating_margin_stability": {
#                 "assessment": "Stable with an improving trend.",
#                 "details": "The EBITDA margin has shown a positive trend, increasing from 28.27% in FY 2023-24 to 29.39% in FY 2024-25. This indicates enhanced operational efficiency and effective cost management relative to revenue growth. <Statement of Profit & Loss 'EBITDA' = 11,371.00 lakhs; 'Revenue from Operations' = 38,692.83 lakhs for FY 2024-25; 'EBITDA' = 10,335.74 lakhs; 'Revenue' = 36,563.83 lakhs for FY 2023-24>.",
#                 "data_availability": "sufficient_data_available",
#                 "inferred_details": None,
#                 "investments": None,
#                 "loans_and_advances": None,
#                 "contingent_liabilities": None,
#                 "conclusion": None
#             },
#             "other_income_scrutiny": {
#                 "assessment": "Present with a notable increase in non-recurring items.",
#                 "details": "Other income increased from 477.70 lakhs in FY 2023-24 to 494.87 lakhs in FY 2024-25. A key contributor to this increase is the 'Profit on Sale of Investment', which rose significantly from 137.83 lakhs in FY 2023-24 to 298.86 lakhs in FY 2024-25. Interest income from fixed deposits decreased, while dividend income increased. This suggests some non-core, one-off gains contribute to the overall other income. <Note 25 'Profit on Sale of Investment' = 298.86 lakhs; FY 2023-24 = 137.83 lakhs> <Note 25 'Interest income on fixed deposits with banks' = 147.23 lakhs; FY 2023-24 = 291.22 lakhs> <Note 25 'Dividend income' = 33.67 lakhs; FY 2023-24 = 7.52 lakhs>.",
#                 "data_availability": "sufficient_data_available",
#                 "inferred_details": None,
#                 "investments": None,
#                 "loans_and_advances": None,
#                 "contingent_liabilities": None,
#                 "conclusion": None
#             },
#             "earnings_quality_assessment": {
#                 "assessment": "Insufficient data available for full analysis (Cash Flow Statement not provided).",
#                 "details": "Insufficient data available for analysis (Cash Flow Statement not provided). Therefore, a direct comparison between 'Profit for the year' and 'Net Cash from Operating Activities' cannot be performed to assess earnings quality.",
#                 "data_availability": "insufficient_data_available_for_analysis (Cash Flow Statement not provided)",
#                 "inferred_details": None,
#                 "investments": None,
#                 "loans_and_advances": None,
#                 "contingent_liabilities": None,
#                 "conclusion": None
#             },
#             "working_capital_efficiency": {
#                 "assessment": "Improved inventory management, but receivables collection slightly slowed, and payable days extended.",
#                 "details": "Trade Receivables Turnover decreased from 8.56x in FY 2023-24 to 8.10x in FY 2024-25, implying Days Sales Outstanding (DSO) increased from approximately 42.64 days to 45.06 days. <Statement of Profit & Loss 'Revenue from Operations' = 38,692.83 lakhs; Balance Sheet 'Trade receivables' = 4,776.68 lakhs for FY 2024-25; 'Revenue from Operations' = 36,563.83 lakhs; 'Trade receivables' = 4,272.15 lakhs for FY 2023-24>. Trade Payables Turnover significantly decreased from 11.98x to 6.35x, indicating Days Payable Outstanding (DPO) extended from approximately 30.47 days to 57.48 days. <Statement of Profit & Loss 'Cost of Services and spare parts consumed' = 19,493.48 lakhs; Note 11 'Trade payables Total' = 3,069.90 lakhs for FY 2024-25; 'Cost of Services and spare parts consumed' = 18,545.85 lakhs; Note 11 'Trade payables Total' = 1,548.08 lakhs for FY 2023-24>. Inventory Turnover improved substantially. The extended DPO suggests the company is benefiting from longer payment terms from suppliers.",
#                 "data_availability": "sufficient_data_available",
#                 "inferred_details": None,
#                 "investments": None,
#                 "loans_and_advances": None,
#                 "contingent_liabilities": None,
#                 "conclusion": None
#             },
#             "related_party_transactions_and_leakage": {
#                 "assessment": "No significant concerns regarding related-party transactions.",
#                 "details": "Director Remuneration remained stable at 200.00 lakhs for both FY 2024-25 and FY 2023-24, which appears reasonable relative to the company's scale. <Note 27 'Remuneration to Directors' = 200.00 lakhs; FY 2023-24 = 200.00 lakhs>. Long-term loans to related parties were 975.38 lakhs in FY 2023-24 but are not present in FY 2024-25, suggesting repayment or reclassification. <Note 16 'Loans to related parties' = 975.38 lakhs for FY 2023-24>. Short-term loans to related parties are substantial at 2,994.25 lakhs in FY 2024-25 (slightly up from 2,975.72 lakhs in FY 2023-24). While sizable, these amounts are disclosed and do not immediately indicate disproportionate or non-arm's-length dealings without further context of the nature of these loans. <Note 22 'Loans to related parties' = 2,994.25 lakhs; FY 2023-24 = 2,975.72 lakhs>.",
#                 "data_availability": "sufficient_data_available",
#                 "inferred_details": None,
#                 "investments": None,
#                 "loans_and_advances": None,
#                 "contingent_liabilities": None,
#                 "conclusion": None
#             },
#             "debt_service_capability": {
#                 "assessment": "Strong and significantly improved.",
#                 "details": "The Interest Coverage Ratio was 13.58x in FY 2024-25, a significant improvement from 9.25x in FY 2023-24. This indicates that the company's operating profit (EBITDA) comfortably covers its finance costs by a large margin, signaling robust debt servicing capability and reduced financial risk. <Statement of Profit & Loss 'EBITDA' = 11,371.00 lakhs; 'Finance costs' = 837.25 lakhs for FY 2024-25; 'EBITDA' = 10,335.74 lakhs; 'Finance costs' = 1,117.30 lakhs for FY 2023-24>.",
#                 "data_availability": "sufficient_data_available",
#                 "inferred_details": None,
#                 "investments": None,
#                 "loans_and_advances": None,
#                 "contingent_liabilities": None,
#                 "conclusion": None
#             },
#             "reinvestment_strategy_capex": {
#                 "assessment": "Moderate CAPEX, likely reflecting a balance between maintenance and some expansion.",
#                 "details": "Net Property, Plant & Equipment (PPE) increased from 5,994.36 lakhs in FY 2023-24 to 6,214.91 lakhs in FY 2024-25. Depreciation for FY 2024-25 was 1,003.46 lakhs. Gross CAPEX for FY 2024-25 can be estimated as (6,214.91 – 5,994.36) + 1,003.46 = 1,224.01 lakhs. This level of CAPEX suggests more than just maintenance, indicating some investment in asset base expansion or modernization, supporting future revenue generation. <Note 14 'Property, Plant & Equipment' = 6,214.91 lakhs for FY 2024-25; 'Property, Plant & Equipment' = 5,994.36 lakhs for FY 2023-24> <Note 29 'Depreciation of property, plant and equipment' = 1,003.46 lakhs for FY 2024-25>.",
#                 "data_availability": "sufficient_data_available",
#                 "inferred_details": None,
#                 "investments": None,
#                 "loans_and_advances": None,
#                 "contingent_liabilities": None,
#                 "conclusion": None
#             },
#             "equity_changes_and_promoters": {
#                 "assessment": "Significant equity growth via bonus issue and retained earnings.",
#                 "details": "Paid-up Share Capital increased dramatically from 111.20 lakhs in FY 2023-24 to 11,611.20 lakhs in FY 2024-25, primarily due to a bonus issue of 11,114.82 lakhs. This bonus issue was funded from 'Reserves and surplus'. Additionally, the company retained Profit for the year of 6,666.27 lakhs, further bolstering its reserves. This indicates a strategic move to strengthen the equity base without external fresh capital infusion. <Note 4 'Share capital' = 11,611.20 lakhs; FY 2023-24 = 111.20 lakhs> <Note 5 'Utilised towards bonus shares' = 11,114.82 lakhs; 'Add : Profit for the year' = 6,666.27 lakhs>.",
#                 "data_availability": "sufficient_data_available",
#                 "inferred_details": None,
#                 "investments": None,
#                 "loans_and_advances": None,
#                 "contingent_liabilities": None,
#                 "conclusion": None
#             },
#             "non_core_exposure": {
#                 "assessment": "Significant non-current investments in subsidiaries, and substantial short-term related party loans.",
#                 "details": None,
#                 "data_availability": "insufficient_data_available_for_analysis for contingent liabilities details.",
#                 "inferred_details": None,
#                 "investments": "Non-current Investments increased from 5,510.54 lakhs to 9,480.84 lakhs. This includes substantial investments in subsidiary companies such as 'Investment in Traveltime City Bus Services (Nagpur) Private Limited' (2,300.00 lakhs) and 'Investment in Traveltime Mobility Services LLP' (5,318.85 lakhs), indicating strategic investments in related entities. <Note 15 'Non-current investment' = 9,480.84 lakhs; FY 2023-24 = 5,510.54 lakhs> <Note 15 'Investment in Traveltime City Bus Services (Nagpur) Private Limited' = 2,300.00 lakhs> <Note 15 'Investment in Traveltime Mobility Services LLP' = 5,318.85 lakhs>.",
#                 "loans_and_advances": "Long-term loans and advances to related parties were 975.38 lakhs in FY 2023-24 but show no balance in FY 2024-25. <Note 16 'Loans to related parties' = 975.38 lakhs for FY 2023-24>. Short-term loans to related parties remain substantial at 2,994.25 lakhs in FY 2024-25, consistent with 2,975.72 lakhs in FY 2023-24. These represent non-operating financial assets. <Note 22 'Loans to related parties' = 2,994.25 lakhs; FY 2023-24 = 2,975.72 lakhs>.",
#                 "contingent_liabilities": "Insufficient data available for contingent liabilities details.",
#                 "conclusion": "The company has significant non-core exposure through its investments in subsidiaries and ongoing short-term loans to related parties. While these are disclosed, the details of contingent liabilities which could represent off-balance sheet exposures, are not provided."
#             }
#         }
#     }
# }


# # Generate the HTML content
# html_output = generate_financial_analysis_html(json_data)

# # # Save the HTML to a file
# output_filename = "financial_analysis_report.html"
# with open(output_filename, "w", encoding="utf-8") as f:
#     f.write(html_output)

# print(f"HTML report saved to {os.path.abspath(output_filename)}")
# print("\nTo convert this HTML file to PDF:")
# print("1. Open 'financial_analysis_report.html' in your web browser.")
# print("2. Use your browser's print function (Ctrl+P or Cmd+P).")
# print("3. In the print dialog, select 'Save as PDF' or 'Print to PDF' as the destination.")
# print("\nAlternatively, for automated PDF generation in Python, you can use a library like WeasyPrint:")
# print("   - Install it: pip install WeasyPrint")
# print("   - You'll also need to install its system dependencies (e.g., on Ubuntu: sudo apt-get install build-essential python3-dev python3-pip python3-setuptools python3-wheel pango cairo libffi-dev shared-mime-info)")
# print("   - Then, in Python: from weasyprint import HTML; HTML(filename='financial_analysis_report.html').write_pdf('financial_analysis_report.pdf')")
