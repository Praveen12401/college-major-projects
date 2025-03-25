from django.shortcuts import render

from django.http import HttpResponse

from .forms import ImageUploadForm
from PIL import Image
import os
import io

# Create your views here.
def image_tool(request):
    return render(request, "index.html")

def converter(request):
    return render(request, "converter.html")

def convertAll(request):
    return render(request, "convertAll.html")

def image_to_pdf(request):
    return render(request, "image_to_pdf.html")




def image_compress(image, target_size_kb):
    """Compresses an image to the target size in KB, supporting PNG and JPEG."""
    target_size_bytes = target_size_kb * 1024
    img = Image.open(image)
    img_format = img.format  # Preserve original format (e.g., PNG, JPEG)

    output_io = io.BytesIO()

    # Handle JPEG compression
    if img_format in ["JPEG", "JPG"]:
        quality = 95
        while True:
            output_io.seek(0)
            img.save(output_io, format="JPEG", quality=quality, optimize=True)
            size = output_io.tell()
            if size <= target_size_bytes or quality <= 10:
                break
            quality -= 5

    # Handle PNG compression
    elif img_format == "PNG":
        img = img.convert("RGBA")  # Ensure RGBA format for PNG
        while True:
            output_io.seek(0)
            img.save(output_io, format="PNG", optimize=True)
            size = output_io.tell()
            if size <= target_size_bytes:
                break
            # Resize as a fallback for PNG compression
            width, height = img.size
            img = img.resize((int(width * 0.9), int(height * 0.9)))

    else:
        raise ValueError("Unsupported image format. Only JPEG and PNG are supported.")

    output_io.seek(0)
    return output_io, img_format.lower()

def upload_image(request):
    if request.method == "POST":
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data["image"]
            target_size = form.cleaned_data["target_size"]
            

            try:
                compressed_image, img_format = image_compress(image, target_size)
            except ValueError as e:
                return HttpResponse(str(e), status=400)

            # Extract the original file name without extension
            original_name, ext = os.path.splitext(image.name)
            compressed_name = f"{original_name}_compressed{ext}"

            response = HttpResponse(compressed_image, content_type=f"image/{img_format}")
            response["Content-Disposition"] = f"attachment; filename={compressed_name}"
             
            return response
    else:
        form = ImageUploadForm()

    return render(request, "image_compress.html", {"form": form})