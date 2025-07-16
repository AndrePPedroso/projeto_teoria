from django.template.loader import render_to_string
from django.core.files.base import ContentFile
from weasyprint import HTML

def generate_and_save_pdf(financial_model_instance, context):
    """
    Renders an HTML template with context and saves it as a PDF 
    to the FileField of a FinantialModels instance.
    """

    
    html_string = render_to_string('site/financeiros/report/report_template.html', context)
    
    pdf_file = HTML(string=html_string).write_pdf()
    
    # Create a Django ContentFile
    pdf_content = ContentFile(pdf_file)
    
    # Define a filename
    file_name = f"black_scholes_report_{financial_model_instance.id}.pdf"
    
    # Save the ContentFile to the model's FileField
    financial_model_instance.report.save(file_name, pdf_content, save=True)
