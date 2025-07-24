import base64
from io import BytesIO
from django.template.loader import render_to_string
from django.core.files.base import ContentFile
from weasyprint import HTML
from django.contrib.staticfiles import finders
from io import BytesIO
from django.template.loader import render_to_string
from django.core.files.base import ContentFile
from weasyprint import HTML

def generate_and_save_pdf(financial_model_instance, context):
    path_to_image = finders.find('app_teoria/assets/logoEng2.png')
    
    if path_to_image:
        with open(path_to_image, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            logo_data_uri = f"data:image/png;base64,{encoded_string}"
            context['logo_image'] = logo_data_uri
    else:
        context['logo_image'] = None
    
    html_string = render_to_string('site/financeiros/report/report_template.html', context)
    
    
    pdf_file_bytes = HTML(string=html_string).write_pdf()
    pdf_buffer = BytesIO(pdf_file_bytes)
    pdf_buffer.seek(0)
    print(f"Length of pdf_file_bytes: {len(pdf_file_bytes)}")

    pdf_content_file = ContentFile(pdf_buffer.read()) 
    pdf_content_file.seek(0) 

    file_name = f"black_scholes_report_{financial_model_instance.id}.pdf"
    try:
        financial_model_instance.report.save(file_name, pdf_content_file, save=True)
    except Exception as e:
        print('er',e)
        raise e


def generate_and_save_pdf_mcs(financial_model_instance, context):
    path_to_image = finders.find('app_teoria/assets/logoEng2.png')
    
    if path_to_image:
        with open(path_to_image, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            logo_data_uri = f"data:image/png;base64,{encoded_string}"
            context['logo_image'] = logo_data_uri
    else:
        context['logo_image'] = None

    html_string = render_to_string('site/financeiros/report/report_mcs.html', context)
    
    
    pdf_file_bytes = HTML(string=html_string).write_pdf()
    pdf_buffer = BytesIO(pdf_file_bytes)
    pdf_buffer.seek(0)
    print(f"Length of pdf_file_bytes: {len(pdf_file_bytes)}")

    pdf_content_file = ContentFile(pdf_buffer.read()) #
    pdf_content_file.seek(0) 

    file_name = f"black_scholes_report_{financial_model_instance.id}.pdf"
    try:
        financial_model_instance.report.save(file_name, pdf_content_file, save=True)
    except Exception as e:
        print('er',e)
        raise e
