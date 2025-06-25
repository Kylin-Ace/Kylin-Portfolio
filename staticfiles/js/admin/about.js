document.addEventListener('DOMContentLoaded', function() {
    // Add image preview functionality
    const imageInput = document.querySelector('input[type="file"]');
    if (imageInput) {
        imageInput.addEventListener('change', function() {
            const file = this.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    const preview = document.createElement('img');
                    preview.src = e.target.result;
                    preview.style.maxWidth = '300px';
                    preview.style.marginTop = '10px';
                    
                    const container = imageInput.parentElement;
                    const oldPreview = container.querySelector('img');
                    if (oldPreview) {
                        container.removeChild(oldPreview);
                    }
                    container.appendChild(preview);
                };
                reader.readAsDataURL(file);
            }
        });
    }
});