from io import BytesIO
from django.template.loader import render_to_string
from django.core.files.base import ContentFile
from weasyprint import HTML

def generate_and_save_pdf(financial_model_instance, context):
    """
    Renders an HTML template with context and saves it as a PDF 
    to the FileField of a FinantialModels instance.
    """

    
    html_string = render_to_string('site/financeiros/report/report_template.html', context)
    
    
    pdf_file_bytes = HTML(string=html_string).write_pdf()
    pdf_buffer = BytesIO(pdf_file_bytes)
    pdf_buffer.seek(0)
    print(f"Length of pdf_file_bytes: {len(pdf_file_bytes)}")

    pdf_content_file = ContentFile(pdf_buffer.read()) # Read all bytes into ContentFile
    pdf_content_file.seek(0) 

    file_name = f"black_scholes_report_{financial_model_instance.id}.pdf"
    try:
        financial_model_instance.report.save(file_name, pdf_content_file, save=True)
    except Exception as e:
        print('er',e)
        raise e
