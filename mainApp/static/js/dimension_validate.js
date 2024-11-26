function updateImagePlaceholder() {
    const unit = document.getElementById('dimension_unit_image').value;
    const widthField = document.getElementById('profile_width');
    const heightField = document.getElementById('profile_height');

    if (unit === 'mm') {
        widthField.placeholder = 'Enter width greater than 51 mm';
        heightField.placeholder = 'Enter height greater than 51 mm';
    } else if (unit === 'inches') {
        widthField.placeholder = 'Enter width greater than 2 inches';
        heightField.placeholder = 'Enter height greater than 2 inches';
    }
}

function updateSignaturePlaceholder() {
    const unit = document.getElementById('dimension_unit_signature').value;
    const widthField = document.getElementById('signature_width');
    const heightField = document.getElementById('signature_height');

    if (unit === 'mm') {
        widthField.placeholder = 'Enter width greater than 51 mm';
        heightField.placeholder = 'Enter height greater than 51 mm';
    } else if (unit === 'inches') {
        widthField.placeholder = 'Enter width greater than 2 inches';
        heightField.placeholder = 'Enter height greater than 2 inches';
    }
}
