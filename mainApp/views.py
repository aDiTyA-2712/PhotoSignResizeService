from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from PIL import Image
from .models import ImageUp
from .serializers import ImageSerializer
import os
from .forms import ImageUpForm
from django.shortcuts import redirect,render
from django.conf import settings
from django.core.exceptions import ValidationError


def resize_image_to_mm(img, width_mm, height_mm):
    # Get the DPI from the image (assume 300 DPI for printing quality)
    dpi = img.info.get('dpi', (300, 300))[0]  # Use horizontal DPI for both width and height

    # Convert mm to pixels
    width_px = int((width_mm / 25.4) * dpi)
    height_px = int((height_mm / 25.4) * dpi)

    # Resize image
    return img.resize((width_px, height_px))

class ImageViewSet(viewsets.ModelViewSet):
    queryset=ImageUp.objects.all()
    serializer_class=ImageSerializer

    @action(detail=True,methods=['post'])
    def resize(self,request,pk=None):
        img_upload=self.get_object()

        try:
            # Validate dimensions before resizing
            validate_dimensions(img_upload.desired_width, img_upload.desired_height, "mm", "Image")

            # Open the main image
            img = Image.open(img_upload.img.path)

            # Resize the image using the input dimensions in mm
            resized_img = resize_image_to_mm(img, img_upload.desired_width, img_upload.desired_height)

            # Save resized image
            resized_img_path = os.path.join(settings.MEDIA_ROOT, 'uploads', f'resized_{img_upload.img.name}')
            resized_img.save(resized_img_path)

            # Update the database record
            img_upload.is_resized = True
            img_upload.save()

            return Response({'status': 'image resized', 'resized_img_url': resized_img_path})

        except ValidationError as e:
            return Response({'error': str(e)}, status=400)
        
def upload_images(request):
    if request.method == 'POST':
        form = ImageUpForm(request.POST, request.FILES)
        if form.is_valid():
            profile_pic = form.cleaned_data['profile_pic']
            sign_pic = form.cleaned_data['sign_pic']

            profile_width = float(form.cleaned_data['profile_width'])
            profile_height = float(form.cleaned_data['profile_height'])

            sign_width = float(form.cleaned_data['sign_width'])
            sign_height = float(form.cleaned_data['sign_height'])

            try:
                # Validate dimensions for profile photo
                validate_dimensions(profile_width, profile_height, "mm", "Profile Photo")

                # Validate dimensions for signature
                validate_dimensions(sign_width, sign_height, "mm", "Signature")

                # Save profile photo and signature as ImageUp records
                profile_image = ImageUp.objects.create(
                    img=profile_pic,
                    desired_width=profile_width,
                    desired_height=profile_height
                )

                sign_image = ImageUp.objects.create(
                    img=sign_pic,
                    desired_width=sign_width,
                    desired_height=sign_height
                )

                # Trigger resizing
                profile_image.resize()
                sign_image.resize()

                return redirect('upload_success')

            except ValidationError as e:
                # Return validation error message to the form
                return render(request, 'upload_images.html', {'form': form, 'error_message': str(e)})

    else:
        form = ImageUpForm()

    return render(request, 'upload_images.html', {'form': form})


def upload_success(request):
    latest_images=ImageUp.objects.order_by('-upload_date')[:2]
    return render(request, 'upload_success.html',{
        'images': latest_images,
        'resized_img_url':lambda image: f"/uploads/resized_{image.img.name}" if image.is_resized else None
        })            

def validate_dimensions(width, height, unit, file_type):
    if unit == "mm" and (width < 51 or height < 51):
        raise ValidationError(f"{file_type} dimensions must be at least 51mm x 51mm.")
    elif unit == "inches" and (width < 2 or height < 2):
        raise ValidationError(f"{file_type} dimensions must be at least 2 inches x 2 inches.")
