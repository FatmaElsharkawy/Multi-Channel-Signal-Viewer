from fpdf import FPDF
import numpy as np
from datetime import datetime

class ReportGenerator:
    def __init__(self):
        self.statistics = {}
        self.snapshots = []

    def generate_report(self, filename="report.pdf"):
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_title("Signal Viewer Report")
        
        # Add Title and Header
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(200, 10, txt="Signal Viewer Report", ln=True, align="C")
        pdf.set_font("Arial", "I", 12)
        pdf.cell(200, 10, txt=f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align="C")
        
        # Add Statistics Section with Styling
        pdf.ln(15)
        pdf.set_font("Arial", "B", 14)
        pdf.set_text_color(0, 51, 102)  # Dark blue for section header
        pdf.cell(200, 10, txt="Statistics Summary", ln=True, align="L")
        
        # Draw a horizontal line
        pdf.set_draw_color(0, 51, 102)  # Matching line color
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(5)
        
        # Table Header with Background Fill Color
        pdf.set_fill_color(200, 220, 255)
        pdf.set_font("Arial", "B", 12)
        pdf.cell(100, 10, "Statistic", border=1, align="C", fill=True)
        pdf.cell(90, 10, "Value", border=1, align="C", fill=True)
        pdf.ln(10)
        
        # Table Body with alternating row colors for better readability
        pdf.set_font("Arial", "", 11)
        fill = False
        for key, value in self.statistics.items():
            pdf.cell(100, 10, str(key), border=1, align="C", fill=fill)
            pdf.cell(90, 10, f"{value:.2f}" if isinstance(value, float) else str(value), border=1, align="C", fill=fill)
            pdf.ln(10)
            fill = not fill  # Toggle fill for alternating row colors
        
        # Add Snapshots Section with Header
        pdf.ln(15)
        pdf.set_font("Arial", "B", 14)
        pdf.set_text_color(0, 51, 102)
        pdf.cell(200, 10, txt="Signal Snapshots", ln=True, align="L")
        
        # Draw a horizontal line for the snapshots section
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(5)
        
        # Insert each snapshot with titles and underlined Graph titles
        for idx, snapshot in enumerate(self.snapshots):
            pdf.add_page()  # New page for each snapshot to avoid clutter
            pdf.set_font("Arial", "B", 12)
            pdf.set_text_color(0, 0, 0)  # Reset text color to black for content
            pdf.cell(200, 10, txt=f"Graph {idx + 1}", ln=True, align="L")
            pdf.line(10, pdf.get_y(), 200, pdf.get_y())  # Underline the graph title
            pdf.ln(5)
            pdf.image(snapshot, x=15, w=180, h=100)
        
        # Add Footer with Page Number
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.alias_nb_pages()
        pdf.set_y(-15)
        pdf.set_font("Arial", "I", 8)
        pdf.cell(0, 10, f"Page {pdf.page_no()}/{{nb}}", 0, 0, "C")
        
        # Save the PDF
        pdf.output(filename)

    def calculate_statistics(self, signal):
        self.statistics = {
            "Mean": np.mean(signal),
            "STD": np.std(signal),
            "Min": np.min(signal),
            "Max": np.max(signal),
            "Duration": len(signal)
        }

    def add_snapshot(self, graph_filename):
        self.snapshots.append(graph_filename)
