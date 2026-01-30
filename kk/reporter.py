import pandas as pd
from fpdf import FPDF
import datetime
import os

class Reporter:
    @staticmethod
    def generate_csv_report(data: list, filename: str = "report.csv"):
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)
        return filename

    @staticmethod
    def generate_pdf_report(data: list, filename: str = "report.pdf"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(200, 10, txt="Security & Monitoring Bot Report", ln=True, align='C')
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"Generated on: {datetime.datetime.now()}", ln=True, align='C')
        pdf.ln(10)

        for entry in data:
            # Simple PDF layout for entries
            text = f"[{entry.get('timestamp')}] {entry.get('exchange')}: {entry.get('status')}"
            pdf.multi_cell(0, 10, txt=text)
            pdf.ln(2)

        pdf.output(filename)
        return filename
