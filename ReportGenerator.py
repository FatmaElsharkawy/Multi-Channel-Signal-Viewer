from fpdf import FPDF
import numpy as np

class ReportGenerator:
    def __init__(self):
        
        self.statistics = {}
        self.snapshots = []
        
    def generate_report(self, filename="report.pdf"):
        
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        
        #Add Title
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Signal Viewer Report", ln=True, align="C")
        
        #Add Statistics Table
        pdf.ln(10)
        pdf.set_font("Arial", size=10)
        pdf.cell(200, 10, txt="Statistics", ln=True, align="L")
        
        #Create a table
        pdf.set_font("Arial", size=10)
        col_width = pdf.w / 4.5
        row_height = pdf.font_size + 2
        
        #Table Header
        pdf.cell(col_width, row_height, "Statistics", border=1)    
        pdf.cell(col_width, row_height, "Value", border=1)
        pdf.ln(row_height)
        
        #Table Body
        for key, value in self.statistics.items():
            pdf.cell(col_width, row_height, str(key), border=1)
            pdf.cell(col_width, row_height, str(value), border=1)
            pdf.ln(row_height)
            
        #Add Snapshot
        pdf.ln(10)
        pdf.set_font("Arial", size=10)
        pdf.cell(200, 10, txt="Glued Signal Graphs", ln=True, align="L")
        
        for idx, snapshot in enumerate(self.snapshots):
            pdf.ln(10)
            pdf.set_font("Arial", 'I', 12)
            pdf.cell(200, 10, txt=f"Graph {idx + 1}", ln=True)   
            
        # Insert graph directly into PDF 
        pdf.image(snapshot, x=10, w=180)
            
        #Save PDF
        pdf.output(filename)
        
    def calculate_statistics(self, signal):
        mean_val = np.mean(signal)
        std_val = np.std(signal)
        min_val = np.min(signal)
        max_val = np.max(signal)
        duration = len(signal)

        self.statistics = {
            "Mean": mean_val,
            "STD": std_val,
            "Min": min_val,
            "Max": max_val,
            "Duration": duration
        }
    
    
    def add_snapshot(self, graph_filename):
        self.snapshots.append(graph_filename)
        
        
        
