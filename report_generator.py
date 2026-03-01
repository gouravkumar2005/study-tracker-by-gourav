try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
    from reportlab.lib.units import inch
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

from datetime import datetime
import sqlite3

class ReportGenerator:
    def __init__(self, db_name='study_tracker.db'):
        self.db_name = db_name
        self.enabled = REPORTLAB_AVAILABLE
    
    def generate_student_report(self, username, output_file='report.pdf'):
        """Generate comprehensive PDF report"""
        if not self.enabled:
            raise Exception("ReportLab not installed. Install: pip install reportlab")
        
        doc = SimpleDocTemplate(output_file, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()
        
        # Title
        title = Paragraph(f"<b>Study Report - {username}</b>", styles['Title'])
        story.append(title)
        story.append(Spacer(1, 0.3*inch))
        
        # Date
        date_text = Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", styles['Normal'])
        story.append(date_text)
        story.append(Spacer(1, 0.3*inch))
        
        # Get data
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        
        # Summary stats
        c.execute('''SELECT COUNT(*), SUM(hours), AVG(focus_score), SUM(warnings)
                     FROM study_sessions WHERE username=?''', (username,))
        stats = c.fetchone()
        
        summary_data = [
            ['Metric', 'Value'],
            ['Total Sessions', str(stats[0] or 0)],
            ['Total Hours', f"{stats[1] or 0:.1f}h"],
            ['Average Focus', f"{stats[2] or 0:.1f}%"],
            ['Total Warnings', str(stats[3] or 0)]
        ]
        
        summary_table = Table(summary_data)
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(Paragraph("<b>Summary Statistics</b>", styles['Heading2']))
        story.append(Spacer(1, 0.2*inch))
        story.append(summary_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Recent sessions
        c.execute('''SELECT date, hours, focus_score, warnings
                     FROM study_sessions WHERE username=?
                     ORDER BY date DESC LIMIT 10''', (username,))
        sessions = c.fetchall()
        
        if sessions:
            session_data = [['Date', 'Hours', 'Focus', 'Warnings']]
            for session in sessions:
                session_data.append([
                    session[0],
                    f"{session[1]:.1f}h",
                    f"{session[2] or 0:.0f}%",
                    str(session[3] or 0)
                ])
            
            session_table = Table(session_data)
            session_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(Paragraph("<b>Recent Sessions</b>", styles['Heading2']))
            story.append(Spacer(1, 0.2*inch))
            story.append(session_table)
        
        conn.close()
        
        # Build PDF
        doc.build(story)
        return output_file
    
    def generate_weekly_report(self, username, output_file='weekly_report.pdf'):
        """Generate weekly summary report"""
        # Similar to above but for weekly data
        return self.generate_student_report(username, output_file)
