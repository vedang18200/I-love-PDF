import os
from django.shortcuts import render
from django.http import HttpResponse, FileResponse
from django.conf import settings
from django.core.files.storage import default_storage
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from PIL import Image

# Helper function to save uploaded files
def save_uploaded_file(uploaded_file):
    file_path = os.path.join(settings.MEDIA_ROOT, uploaded_file.name)
    with open(file_path, 'wb+') as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)
    return file_path

# Home view
def home(request):
    return render(request, 'home.html')

# Merge PDFs view
def merge_pdfs_view(request):
    if request.method == "POST":
        files = request.FILES.getlist('files')
        merger = PdfMerger()

        for file in files:
            file_path = save_uploaded_file(file)
            merger.append(file_path)

        output_path = os.path.join(settings.MEDIA_ROOT, 'merged.pdf')
        merger.write(output_path)
        merger.close()

        # Pass the file path to the template for download
        context = {
            'file_url': f"{settings.MEDIA_URL}merged.pdf",
            'operation': 'Merge PDFs'
        }
        return render(request, 'result.html', context)

    return render(request, 'merge.html')

# Split PDFs view
def split_pdfs_view(request):
    if request.method == "POST":
        uploaded_file = request.FILES['pdf']
        pages = request.POST['pages']
        file_path = save_uploaded_file(uploaded_file)
        page_numbers = [int(p) - 1 for p in pages.split(',')]

        reader = PdfReader(file_path)
        writer = PdfWriter()

        for page_num in page_numbers:
            writer.add_page(reader.pages[page_num])

        output_path = os.path.join(settings.MEDIA_ROOT, 'split.pdf')
        with open(output_path, 'wb') as output_pdf:
            writer.write(output_pdf)

        return FileResponse(open(output_path, 'rb'), as_attachment=True, filename='split.pdf')

    return render(request, 'split.html')

# Compress PDFs view
def compress_pdfs_view(request):
    if request.method == "POST":
        uploaded_file = request.FILES['pdf']
        file_path = save_uploaded_file(uploaded_file)

        # Dummy compression logic: Re-saving the file to simulate compression
        output_path = os.path.join(settings.MEDIA_ROOT, 'compressed.pdf')
        reader = PdfReader(file_path)
        writer = PdfWriter()

        for page in reader.pages:
            writer.add_page(page)

        with open(output_path, 'wb') as compressed_pdf:
            writer.write(compressed_pdf)

        return FileResponse(open(output_path, 'rb'), as_attachment=True, filename='compressed.pdf')

    return render(request, 'compress.html')

# Convert to PDF view
def convert_to_pdf_view(request):
    if request.method == "POST":
        uploaded_file = request.FILES['file']
        file_extension = os.path.splitext(uploaded_file.name)[1].lower()
        file_path = save_uploaded_file(uploaded_file)

        output_path = os.path.join(settings.MEDIA_ROOT, 'converted.pdf')

        if file_extension in ['.jpg', '.jpeg', '.png']:
            image = Image.open(file_path)
            pdf_path = output_path
            image.save(pdf_path, 'PDF', resolution=100.0)
        else:
            # Example placeholder for unsupported file formats
            return HttpResponse("Unsupported file format", status=400)

        return FileResponse(open(output_path, 'rb'), as_attachment=True, filename='converted.pdf')

    return render(request, 'convert.html')
