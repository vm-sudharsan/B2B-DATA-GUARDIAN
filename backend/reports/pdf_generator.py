"""
Professional PDF Report Generator for B2B Customer Data Quality
Generates comprehensive before/after comparison reports
"""
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, 
    Spacer, PageBreak, Image, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas
from datetime import datetime
import pandas as pd
from typing import Dict, List
from io import BytesIO
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')


class B2BDataQualityReport:
    """Generate professional PDF reports for B2B data quality"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1e40af'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#1e40af'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='MetricValue',
            parent=self.styles['Normal'],
            fontSize=32,
            textColor=colors.HexColor('#059669'),
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
    
    def generate_report(
        self,
        original_data: pd.DataFrame,
        cleaned_data: pd.DataFrame,
        report_metrics: Dict,
        fixes: List[Dict],
        output_path: str
    ):
        """Generate comprehensive PDF report"""
        
        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18,
        )
        
        story = []
        
        # Title Page
        story.extend(self._create_title_page(report_metrics))
        story.append(PageBreak())
        
        # Executive Summary
        story.extend(self._create_executive_summary(report_metrics))
        story.append(PageBreak())
        
        # Data Quality Metrics
        story.extend(self._create_metrics_section(report_metrics))
        story.append(PageBreak())
        
        # Before/After Comparison
        story.extend(self._create_comparison_section(original_data, cleaned_data))
        story.append(PageBreak())
        
        # Duplicate Analysis
        story.extend(self._create_duplicate_analysis(report_metrics, fixes))
        story.append(PageBreak())
        
        # Data Quality Issues
        story.extend(self._create_issues_section(fixes))
        story.append(PageBreak())
        
        # Recommendations
        story.extend(self._create_recommendations(report_metrics))
        
        # Build PDF
        doc.build(story, onFirstPage=self._add_header_footer, onLaterPages=self._add_header_footer)
        
        return output_path
    
    def _create_title_page(self, metrics: Dict) -> List:
        """Create professional title page"""
        elements = []
        
        # Title
        elements.append(Spacer(1, 2*inch))
        title = Paragraph("B2B Customer Data Quality Report", self.styles['CustomTitle'])
        elements.append(title)
        elements.append(Spacer(1, 0.5*inch))
        
        # Subtitle
        subtitle = Paragraph(
            f"Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}",
            self.styles['Normal']
        )
        elements.append(subtitle)
        elements.append(Spacer(1, 1*inch))
        
        # Key Metrics Box
        quality_score = metrics.get('overall_quality_score', 0)
        score_color = self._get_score_color(quality_score)
        
        score_data = [
            ['Overall Data Quality Score'],
            [f'{quality_score:.1f}%'],
            [self._get_quality_label(quality_score)]
        ]
        
        score_table = Table(score_data, colWidths=[4*inch])
        score_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('FONTNAME', (0, 1), (-1, 1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 1), (-1, 1), 48),
            ('TEXTCOLOR', (0, 1), (-1, 1), score_color),
            ('FONTSIZE', (0, 2), (-1, 2), 12),
            ('BOX', (0, 0), (-1, -1), 2, colors.HexColor('#1e40af')),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#eff6ff')),
            ('PADDING', (0, 0), (-1, -1), 20),
        ]))
        
        elements.append(score_table)
        elements.append(Spacer(1, 0.5*inch))
        
        # Summary Stats
        stats_data = [
            ['Total Records', str(metrics.get('records', 0))],
            ['Duplicates Found', str(metrics.get('duplicate_rows', 0))],
            ['Issues Fixed', str(metrics.get('offline_fixes', 0) + metrics.get('online_fixes', 0))],
            ['Manual Review Needed', str(metrics.get('manual_review', 0))]
        ]
        
        stats_table = Table(stats_data, colWidths=[2.5*inch, 1.5*inch])
        stats_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('FONTNAME', (1, 0), (-1, -1), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f9fafb')),
            ('PADDING', (0, 0), (-1, -1), 10),
        ]))
        
        elements.append(stats_table)
        
        return elements
    
    def _create_executive_summary(self, metrics: Dict) -> List:
        """Create executive summary section"""
        elements = []
        
        elements.append(Paragraph("Executive Summary", self.styles['SectionHeader']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Summary text
        quality_score = metrics.get('overall_quality_score', 0)
        total_records = metrics.get('records', 0)
        duplicates = metrics.get('duplicate_rows', 0)
        issues_fixed = metrics.get('offline_fixes', 0) + metrics.get('online_fixes', 0)
        
        summary_text = f"""
        This report provides a comprehensive analysis of your B2B customer data quality. 
        We processed <b>{total_records} customer records</b> and identified various data quality issues.
        <br/><br/>
        <b>Key Findings:</b><br/>
        • Overall data quality score: <b>{quality_score:.1f}%</b> ({self._get_quality_label(quality_score)})<br/>
        • Duplicate records detected: <b>{duplicates}</b><br/>
        • Issues automatically fixed: <b>{issues_fixed}</b><br/>
        • Records requiring manual review: <b>{metrics.get('manual_review', 0)}</b><br/>
        <br/>
        The system has automatically cleaned and standardized your data, removing duplicates 
        and fixing common data quality issues. A detailed breakdown of all changes is provided 
        in the following sections.
        """
        
        elements.append(Paragraph(summary_text, self.styles['Normal']))
        
        return elements
    
    def _create_metrics_section(self, metrics: Dict) -> List:
        """Create detailed metrics section"""
        elements = []
        
        elements.append(Paragraph("Data Quality Metrics", self.styles['SectionHeader']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Metrics table
        metrics_data = [
            ['Metric', 'Count', 'Percentage'],
            ['Total Records', str(metrics.get('records', 0)), '100%'],
            ['Missing Fields', str(metrics.get('missing_fields', 0)), 
             f"{(metrics.get('missing_fields', 0) / max(metrics.get('records', 1), 1) * 100):.1f}%"],
            ['Invalid Formats', str(metrics.get('invalid_fields', 0)),
             f"{(metrics.get('invalid_fields', 0) / max(metrics.get('records', 1), 1) * 100):.1f}%"],
            ['Duplicate Records', str(metrics.get('duplicate_rows', 0)),
             f"{(metrics.get('duplicate_rows', 0) / max(metrics.get('records', 1), 1) * 100):.1f}%"],
            ['Standardized Fields', str(metrics.get('standardized_fields', 0)),
             f"{(metrics.get('standardized_fields', 0) / max(metrics.get('records', 1), 1) * 100):.1f}%"],
        ]
        
        if metrics.get('ai_powered'):
            metrics_data.extend([
                ['Anomalies Detected', str(metrics.get('anomalies_detected', 0)),
                 f"{(metrics.get('anomalies_detected', 0) / max(metrics.get('records', 1), 1) * 100):.1f}%"],
                ['Low Confidence Predictions', str(metrics.get('low_confidence_predictions', 0)),
                 f"{(metrics.get('low_confidence_predictions', 0) / max(metrics.get('records', 1), 1) * 100):.1f}%"],
            ])
        
        metrics_table = Table(metrics_data, colWidths=[3*inch, 1.5*inch, 1.5*inch])
        metrics_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')]),
            ('PADDING', (0, 0), (-1, -1), 8),
        ]))
        
        elements.append(metrics_table)
        
        return elements
    
    def _create_comparison_section(self, original: pd.DataFrame, cleaned: pd.DataFrame) -> List:
        """Create before/after comparison"""
        elements = []
        
        elements.append(Paragraph("Before & After Comparison", self.styles['SectionHeader']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Sample comparison (first 5 records)
        comparison_text = Paragraph(
            "Below is a sample comparison showing the first 5 records before and after cleaning:",
            self.styles['Normal']
        )
        elements.append(comparison_text)
        elements.append(Spacer(1, 0.1*inch))
        
        # Show key columns only
        key_columns = ['company_name', 'person_name', 'email', 'phone', 'job_title']
        available_columns = [col for col in key_columns if col in original.columns]
        
        if available_columns:
            # Before table
            elements.append(Paragraph("<b>BEFORE (Original Data):</b>", self.styles['Normal']))
            before_data = [available_columns]
            for idx in range(min(5, len(original))):
                row = [str(original.iloc[idx][col])[:30] for col in available_columns]
                before_data.append(row)
            
            before_table = Table(before_data, colWidths=[1.2*inch] * len(available_columns))
            before_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#fee2e2')),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('PADDING', (0, 0), (-1, -1), 4),
            ]))
            elements.append(before_table)
            elements.append(Spacer(1, 0.2*inch))
            
            # After table
            elements.append(Paragraph("<b>AFTER (Cleaned Data):</b>", self.styles['Normal']))
            after_data = [available_columns]
            for idx in range(min(5, len(cleaned))):
                row = [str(cleaned.iloc[idx][col])[:30] for col in available_columns]
                after_data.append(row)
            
            after_table = Table(after_data, colWidths=[1.2*inch] * len(available_columns))
            after_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#d1fae5')),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('PADDING', (0, 0), (-1, -1), 4),
            ]))
            elements.append(after_table)
        
        return elements
    
    def _create_duplicate_analysis(self, metrics: Dict, fixes: List[Dict]) -> List:
        """Create duplicate analysis section"""
        elements = []
        
        elements.append(Paragraph("Duplicate Records Analysis", self.styles['SectionHeader']))
        elements.append(Spacer(1, 0.2*inch))
        
        duplicate_count = metrics.get('duplicate_rows', 0)
        
        if duplicate_count > 0:
            dup_text = f"""
            Found <b>{duplicate_count} duplicate records</b> in your customer database. 
            Duplicates were identified using advanced ML algorithms that compare multiple fields 
            including names, emails, phone numbers, and company information.
            <br/><br/>
            <b>Impact:</b> Duplicate records can lead to:<br/>
            • Inaccurate reporting and analytics<br/>
            • Wasted marketing spend<br/>
            • Poor customer experience<br/>
            • Compliance issues<br/>
            """
            elements.append(Paragraph(dup_text, self.styles['Normal']))
        else:
            elements.append(Paragraph("✓ No duplicate records found. Your data is clean!", self.styles['Normal']))
        
        return elements
    
    def _create_issues_section(self, fixes: List[Dict]) -> List:
        """Create data quality issues section"""
        elements = []
        
        elements.append(Paragraph("Data Quality Issues Fixed", self.styles['SectionHeader']))
        elements.append(Spacer(1, 0.2*inch))
        
        if fixes:
            # Group fixes by type
            fix_types = {}
            for fix in fixes[:50]:  # Show first 50
                field = fix.get('field', 'Unknown')
                if field not in fix_types:
                    fix_types[field] = []
                fix_types[field].append(fix)
            
            for field, field_fixes in fix_types.items():
                elements.append(Paragraph(f"<b>{field.upper()}:</b>", self.styles['Normal']))
                
                fix_data = [['Original', 'Corrected', 'Confidence', 'Mode']]
                for fix in field_fixes[:10]:  # Show first 10 per field
                    fix_data.append([
                        str(fix.get('original', ''))[:25],
                        str(fix.get('suggested', ''))[:25],
                        f"{fix.get('confidence', 0):.2f}",
                        fix.get('processing_mode', 'N/A')
                    ])
                
                fix_table = Table(fix_data, colWidths=[1.5*inch, 1.5*inch, 1*inch, 1*inch])
                fix_table.setStyle(TableStyle([
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 9),
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#eff6ff')),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                    ('PADDING', (0, 0), (-1, -1), 6),
                ]))
                elements.append(fix_table)
                elements.append(Spacer(1, 0.1*inch))
        else:
            elements.append(Paragraph("No issues found. Your data quality is excellent!", self.styles['Normal']))
        
        return elements
    
    def _create_recommendations(self, metrics: Dict) -> List:
        """Create recommendations section"""
        elements = []
        
        elements.append(Paragraph("Recommendations", self.styles['SectionHeader']))
        elements.append(Spacer(1, 0.2*inch))
        
        quality_score = metrics.get('overall_quality_score', 0)
        
        recommendations = []
        
        if quality_score < 70:
            recommendations.append("• Implement data validation rules at the point of entry")
            recommendations.append("• Conduct regular data quality audits")
            recommendations.append("• Train staff on data entry best practices")
        
        if metrics.get('duplicate_rows', 0) > 0:
            recommendations.append("• Implement duplicate detection before data entry")
            recommendations.append("• Establish a master data management process")
        
        if metrics.get('missing_fields', 0) > metrics.get('records', 1) * 0.1:
            recommendations.append("• Make critical fields mandatory in your CRM")
            recommendations.append("• Implement data enrichment services")
        
        if metrics.get('manual_review', 0) > 0:
            recommendations.append(f"• Review {metrics.get('manual_review', 0)} records flagged for manual verification")
        
        if not recommendations:
            recommendations.append("• Maintain current data quality standards")
            recommendations.append("• Continue regular data quality monitoring")
        
        rec_text = "<br/>".join(recommendations)
        elements.append(Paragraph(rec_text, self.styles['Normal']))
        
        return elements
    
    def _add_header_footer(self, canvas, doc):
        """Add header and footer to each page"""
        canvas.saveState()
        
        # Header
        canvas.setFont('Helvetica', 9)
        canvas.setFillColor(colors.grey)
        canvas.drawString(inch, letter[1] - 0.5*inch, "B2B Data Quality Report")
        canvas.drawRightString(letter[0] - inch, letter[1] - 0.5*inch, 
                              datetime.now().strftime('%Y-%m-%d'))
        
        # Footer
        canvas.drawString(inch, 0.5*inch, "Confidential - For Internal Use Only")
        canvas.drawRightString(letter[0] - inch, 0.5*inch, f"Page {doc.page}")
        
        canvas.restoreState()
    
    def _get_score_color(self, score: float) -> colors.Color:
        """Get color based on quality score"""
        if score >= 85:
            return colors.HexColor('#059669')  # Green
        elif score >= 70:
            return colors.HexColor('#2563eb')  # Blue
        elif score >= 50:
            return colors.HexColor('#d97706')  # Orange
        else:
            return colors.HexColor('#dc2626')  # Red
    
    def _get_quality_label(self, score: float) -> str:
        """Get quality label based on score"""
        if score >= 85:
            return "Excellent"
        elif score >= 70:
            return "Good"
        elif score >= 50:
            return "Fair"
        else:
            return "Needs Improvement"
