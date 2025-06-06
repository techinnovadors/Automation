SUMMARY_PROMPT = """
Perform a comprehensive financial analysis of a company based on its provided Provisional Balance Sheet and Provisional Statement of Profit & Loss for two comparative fiscal years (e.g., current year and previous year).

Your analysis should be structured as follows, with detailed instructions for each section:

1.  **Executive Summary:**
    *   **Objective:** Provide a high-level, concise overview of the company's financial performance and position across the two fiscal years.
    *   **Content:**
        *   Summarize the most significant changes in revenue, expenses, profitability, assets, and liabilities.
        *   Highlight key drivers behind these changes (e.g., major shifts in sales, significant investments, changes in debt levels).
        *   Briefly state the overall financial health and any critical challenges or strengths identified.
        *   Include a consolidated financial highlights table comparing key metrics (e.g., Total Revenue, Total Expenses, Profit Before Tax, Profit for the Period, Total Equity and Liabilities, Total Assets) for both years, along with absolute and percentage changes.

2.  **Company Overview and Financial Periods:**
    *   **Objective:** Clearly identify the entity being analyzed and the specific financial periods covered by the statements.
    *   **Content:**
        *   State the full legal name of the company.
        *   Specify the exact "As at" dates for the Balance Sheet (e.g., March 31, 20XX) and "Year ended" dates for the Statement of Profit & Loss for both the current and previous fiscal years.

3.  **Analysis of Financial Position (Balance Sheet):**
    *   **Objective:** Provide a detailed examination of the company's assets, liabilities, and equity at specific points in time, identifying significant changes and their implications.
    *   **Overall Comparison:**
        *   Compare the total equity and liabilities and total assets for both periods.
        *   Discuss the overall growth or contraction of the company's financial scale.
        *   Include a consolidated balance sheet summary table showing major categories (e.g., Total Shareholder's Funds, Total Non-Current Liabilities, Total Current Liabilities, Total Non-Current Assets, Total Current Assets) for both years, with absolute and percentage changes.
    *   **Shareholder's Funds:**
        *   Analyze changes in Share Capital (e.g., new share issuance, buybacks) and their impact on the number of shares and total value.
        *   Examine changes in Reserves and Surplus, specifically detailing movements in Securities Premium Account (indicating share issuance premium), General Reserve, and Surplus (retained earnings, net profit impact).
        *   Include a breakdown table for Shareholder's Funds components.
    *   **Non-Current Liabilities:**
        *   Focus on Long-term Borrowings: Identify significant new loans or changes in existing ones (e.g., term loans, vehicle loans, unsecured loans from directors/shareholders). Discuss the implications of increased or decreased long-term debt.
        *   Analyze Deferred Tax Liabilities: Note any significant changes or stability.
        *   Include a breakdown table for Long-term Borrowings, distinguishing between non-current and current maturities where applicable.
    *   **Current Liabilities:**
        *   Analyze Short-term Borrowings: Differentiate between new short-term loans and current maturities of long-term debt. Discuss the impact on short-term liquidity.
        *   Examine Trade Payables: Discuss whether changes indicate extended payment terms, increased purchases, or cash flow management strategies.
        *   Analyze Other Current Liabilities: Pay attention to items like "Advances from customers" and interpret what changes signify (e.g., new order pipeline, revenue recognition).
        *   Review Short-term Provisions: Note any significant increases or decreases.
    *   **Non-Current Assets:**
        *   Focus on Property, Plant and Equipment (PPE) and Capital Work-in-Progress (CWIP): Discuss significant additions or disposals, linking them to investment strategies and their potential impact on future operations and depreciation.
        *   Analyze Non-current Investments: Note any strategic investments in equity or other instruments.
        *   Review Other Non-current Assets: Identify any notable changes.
    *   **Current Assets:**
        *   Analyze Inventories: Break down into raw materials, work-in-progress, and finished goods. Discuss whether changes reflect production efficiency, sales trends, or strategic stocking.
        *   Examine Trade Receivables: Discuss changes in relation to revenue, indicating collection efficiency or credit policy adjustments.
        *   Analyze Cash & Cash Equivalents: Discuss the overall cash position, including balances with banks and fixed deposits. Interpret whether cash is being consumed by operations or investments.
        *   Review Short-term Loans & Advances: Pay attention to "Advance to suppliers" and discuss implications for working capital.
        *   Include a breakdown table for Key Working Capital Components (Inventories, Trade Receivables, Trade Payables, Advances from Customers, Short-term Loans & Advances, Cash & Cash Equivalents).

4.  **Analysis of Financial Performance (Statement of Profit & Loss):**
    *   **Objective:** Provide a detailed examination of the company's revenues and expenses over the fiscal year, assessing operational efficiency and profitability.
    *   **Overall Comparison:**
        *   Compare Total Revenue, Total Expenses, Profit Before Tax (PBT), and Profit for the Period for both years.
        *   Discuss the overall trend in profitability and the proportionality of expense changes to revenue changes.
        *   Include a consolidated statement of profit & loss summary table.
    *   **Revenue Analysis:**
        *   Analyze **Revenue from Operations**: Break down into primary components like "Sale of Products" and "Sale of Services." Identify which segment is driving overall revenue changes.
        *   Analyze **Other Operating Revenues**: Detail components such as "Scrap Sales," "Fluctuation of Currency," and "Freight Charges Receipts." Discuss their contribution and any unusual trends.
        *   Analyze **Other Income**: Detail components like "Interest From FDR," "Miscellaneous Income," and "Profit on sale of asset." Discuss their stability and significance to overall income.
        *   Include a breakdown table for Revenue from Operations.
    *   **Expense Analysis:**
        *   Analyze **Cost of Materials Consumed**: Discuss whether this cost scaled proportionally with changes in sales/production. Detail changes in opening stock, purchases, and closing stock of raw materials.
        *   Analyze **Changes in Inventories of Finished Goods, WIP and Stock in Trade**: Interpret the impact of inventory movements on the cost of goods sold.
        *   Analyze **Manufacturing Expenses**: Detail changes in key components like "Labor Charges," "Consumables," "Power & Fuel," and "Repairing Machinery." Discuss whether these costs are fixed/variable and their impact on operational efficiency.
        *   Analyze **Employee Benefits Expense**: Detail changes in "Salary, Bonus, and Allowances," "Director's Remuneration," and "Staff Welfare Expenses." Discuss workforce cost rigidity.
        *   Analyze **Finance Costs**: Detail changes in "Interest to Term Loans," "Bank Charges," and "Loan Processing Charges." Directly link these to changes in long-term borrowings and discuss their impact on profitability.
        *   Analyze **Depreciation & Amortization Expense**: Discuss the increase/decrease in relation to asset additions/disposals.
        *   Analyze **Other Expenses**: Break down into "Office & Administrative Expenses" and "Selling & Distribution Expenses." Detail significant changes in sub-components (e.g., "Consultancy Charges," "Professional Fees," "Bad Debts Written Off," "Sales Commission," "Bank Guarantee Revoked," "Exhibition Expenses"). Discuss cost control efforts and any one-time or unusual expenses.
        *   Include a breakdown table for Key Expense Categories.

5.  **Key Financial Trends and Multi-layered Interpretations:**
    *   **Objective:** Synthesize findings from both the Balance Sheet and Profit & Loss Statement to identify overarching financial trends and their interconnectedness.
    *   **Content:**
        *   Discuss the relationship between investment decisions (asset growth, debt) and their impact on profitability (finance costs, depreciation).
        *   Analyze working capital efficiency (e.g., trade receivables, advances to suppliers, cash position) in the context of revenue and expense trends.
        *   Assess the company's cost structure (fixed vs. variable costs) and its ability to adapt to changes in revenue.
        *   Identify any strategic decisions (e.g., major capital projects, new loans) and their immediate and potential long-term financial implications.
        *   Provide a holistic view of the company's financial narrative.

6.  **Conclusion and Recommendations:**
    *   **Objective:** Summarize the overall financial health and performance and provide actionable insights.
    *   **Content:**
        *   Concisely reiterate the most critical financial findings.
        *   Offer specific, actionable recommendations for areas requiring further investigation or strategic consideration (e.g., sales and market strategy, operational efficiency, capital expenditure review, working capital management, debt sustainability).

**General Instructions:**
*   **Accuracy:** Ensure all numerical data extracted from the document is accurately presented.
*   **Citations:** Cite all information directly extracted from the document using the provided snippet IDs (e.g.[1]).
*   **Clarity and Professionalism:** Maintain a clear, concise, and professional writing style throughout the analysis.
*   **Comparative Analysis:** Emphasize year-over-year comparisons and discuss the absolute and percentage changes for all relevant financial line items.
*   **Interpretation:** Go beyond merely stating numbers; interpret what the changes signify for the company's financial health, operational efficiency, and strategic direction.

Sources and related content
"""
