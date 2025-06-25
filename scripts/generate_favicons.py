from PIL import Image, ImageDraw
import os

def create_favicon():
    # Create directories if they don't exist
    img_dir = os.path.join('static', 'img')
    os.makedirs(img_dir, exist_ok=True)
    
    # Create base icon (32x32 pixels)
    icon = Image.new('RGB', (32, 32), color='#0284c7')  # Tailwind blue-600
    draw = ImageDraw.Draw(icon)
    
    # Add a simple 'P' letter
    draw.text((8, 4), 'P', fill='white', size=24)
    
    # Save favicon.ico
    icon.save(os.path.join('static', 'favicon.ico'))
    
    # Create other sizes
    sizes = {
        'favicon-16x16.png': (16, 16),
        'favicon-32x32.png': (32, 32),
        'apple-touch-icon.png': (180, 180)
    }
    
    for filename, size in sizes.items():
        resized = icon.resize(size, Image.Resampling.LANCZOS)
        resized.save(os.path.join(img_dir, filename))
        print(f"Generated {filename}")

if __name__ == '__main__':
    create_favicon()