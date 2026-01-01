from flask import Flask, render_template, request, jsonify
import os
from werkzeug.utils import secure_filename
import cv2
import numpy as np
from PIL import Image
from scipy.cluster.vq import kmeans, vq

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}

# Create uploads directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def analyze_knitting_pattern(image_path):
    """
    Analyze an image and generate knitting pattern instructions.
    This function processes the image to extract color information and 
    estimate pattern complexity.
    """
    # Load image
    img = cv2.imread(image_path)
    if img is None:
        return None
    
    # Get image dimensions
    height, width = img.shape[:2]
    
    # Convert to RGB for better color analysis
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Resize for analysis (to make processing faster)
    max_dimension = 400
    if max(height, width) > max_dimension:
        scale = max_dimension / max(height, width)
        new_width = int(width * scale)
        new_height = int(height * scale)
        img_rgb = cv2.resize(img_rgb, (new_width, new_height))
    
    # Detect dominant colors
    pixels = img_rgb.reshape(-1, 3)
    
    # Use k-means to find dominant colors
    n_colors = min(5, len(np.unique(pixels, axis=0)))  # Max 5 colors
    
    # Convert to float for kmeans
    pixels_float = np.float32(pixels)
    
    try:
        centroids, _ = kmeans(pixels_float, n_colors)
        centroids = np.uint8(centroids)
    except (ValueError, RuntimeError) as e:
        # Fallback if kmeans fails (e.g., not enough unique colors)
        unique_colors = np.unique(pixels, axis=0)[:n_colors]
        centroids = unique_colors
    
    # Calculate complexity based on color variations
    gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    complexity = np.sum(edges) / (edges.shape[0] * edges.shape[1]) * 100
    
    # Estimate pattern dimensions
    # Assume standard gauge: 5.5 stitches per inch, 7.5 rows per inch
    stitches_per_inch = 5.5
    rows_per_inch = 7.5
    
    # Estimate based on a medium sweater size
    estimated_width_inches = 20  # Average sweater width
    estimated_height_inches = 24  # Average sweater height
    
    estimated_stitches = int(estimated_width_inches * stitches_per_inch)
    estimated_rows = int(estimated_height_inches * rows_per_inch)
    
    # Determine stitch types based on complexity
    if complexity < 5:
        stitch_type = "Stockinette stitch (knit on right side, purl on wrong side)"
        difficulty = "Beginner"
    elif complexity < 15:
        stitch_type = "Ribbing pattern (K2, P2) or simple texture"
        difficulty = "Easy"
    elif complexity < 30:
        stitch_type = "Cable patterns or colorwork"
        difficulty = "Intermediate"
    else:
        stitch_type = "Complex patterns with multiple cable crosses or intricate colorwork"
        difficulty = "Advanced"
    
    # Generate color descriptions
    color_descriptions = []
    for i, color in enumerate(centroids):
        color_name = get_color_name(color)
        color_descriptions.append(f"Color {i+1}: {color_name} (RGB: {color[0]}, {color[1]}, {color[2]})")
    
    # Create pattern instructions
    pattern = {
        'title': 'Custom Knitting Pattern',
        'difficulty': difficulty,
        'estimated_stitches': estimated_stitches,
        'estimated_rows': estimated_rows,
        'colors': color_descriptions,
        'primary_stitch': stitch_type,
        'gauge': f"{stitches_per_inch} stitches x {rows_per_inch} rows = 1 inch in stockinette stitch",
        'materials': generate_materials(centroids, estimated_stitches, estimated_rows),
        'instructions': generate_instructions(estimated_stitches, estimated_rows, stitch_type, len(centroids))
    }
    
    return pattern

def get_color_name(rgb):
    """Convert RGB to approximate color name"""
    r, g, b = rgb
    
    # Simple color naming based on dominant channel
    if r > 200 and g > 200 and b > 200:
        return "White/Cream"
    elif r < 50 and g < 50 and b < 50:
        return "Black/Charcoal"
    elif r > max(g, b) + 30:
        if r > 200:
            return "Bright Red"
        return "Red/Burgundy"
    elif g > max(r, b) + 30:
        if g > 200:
            return "Bright Green"
        return "Green/Forest"
    elif b > max(r, g) + 30:
        if b > 200:
            return "Bright Blue"
        return "Blue/Navy"
    elif r > 150 and g > 150 and b < 100:
        return "Yellow/Gold"
    elif r > 150 and g < 100 and b > 150:
        return "Purple/Violet"
    elif r > 100 and g > 100 and b > 100:
        return "Gray"
    elif r > 150 and g > 100 and b < 100:
        return "Orange/Rust"
    elif r > 100 and g > 80 and b > 120:
        return "Mauve/Lavender"
    else:
        return "Mixed Color"

def generate_materials(colors, stitches, rows):
    """Generate materials list based on pattern"""
    # Estimate yarn needed (very rough approximation)
    # Average: 1 yard per stitch for medium weight yarn
    yards_needed = int(stitches * rows / 6)  # Rough estimate
    
    materials = [
        f"Approximately {yards_needed} yards of medium weight (worsted) yarn",
        f"Number of colors needed: {len(colors)}",
        "US Size 7 (4.5mm) knitting needles (or size needed to obtain gauge)",
        "Tapestry needle for weaving in ends",
        "Stitch markers (optional but helpful)",
        "Measuring tape"
    ]
    
    return materials

def generate_instructions(stitches, rows, stitch_type, num_colors):
    """Generate step-by-step knitting instructions"""
    instructions = []
    
    # Cast on
    instructions.append({
        'step': 1,
        'title': 'Cast On',
        'description': f"Cast on {stitches} stitches using the long-tail cast-on method."
    })
    
    # Setup rows
    instructions.append({
        'step': 2,
        'title': 'Setup Row',
        'description': "Knit 1 row to establish your working yarn."
    })
    
    # Main body
    if "Stockinette" in stitch_type:
        instructions.append({
            'step': 3,
            'title': 'Main Body Pattern',
            'description': f"Work in stockinette stitch for approximately {rows} rows:\n- Row 1 (Right Side): Knit all stitches\n- Row 2 (Wrong Side): Purl all stitches\nRepeat these 2 rows until piece measures desired length."
        })
    elif "Ribbing" in stitch_type:
        instructions.append({
            'step': 3,
            'title': 'Main Body Pattern',
            'description': f"Work in K2, P2 ribbing for approximately {rows} rows:\n- All Rows: *K2, P2*, repeat from * to end\nRepeat until piece measures desired length."
        })
    elif "Cable" in stitch_type:
        instructions.append({
            'step': 3,
            'title': 'Main Body Pattern',
            'description': f"Work cable pattern for approximately {rows} rows. Place cable crosses every 6-8 rows. Consult a cable pattern chart for specific cable arrangement."
        })
    else:
        instructions.append({
            'step': 3,
            'title': 'Main Body Pattern',
            'description': f"Work your chosen stitch pattern for approximately {rows} rows, changing colors as needed to match the design."
        })
    
    # Color changes if multiple colors
    if num_colors > 1:
        instructions.append({
            'step': 4,
            'title': 'Color Changes',
            'description': f"This pattern uses {num_colors} colors. When changing colors, twist the yarns together at the back of work to prevent holes. Carry unused color loosely across the back."
        })
    
    # Finishing
    instructions.append({
        'step': 5 if num_colors > 1 else 4,
        'title': 'Bind Off',
        'description': "When piece reaches desired length, bind off all stitches loosely in pattern."
    })
    
    instructions.append({
        'step': 6 if num_colors > 1 else 5,
        'title': 'Finishing',
        'description': "Weave in all ends using tapestry needle. Block piece to measurements if desired. Seam pieces together if making a garment."
    })
    
    return instructions

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and pattern generation"""
    # Check if file is present
    if 'photo' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['photo']
    
    # Check if file is selected
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Check if file is allowed
    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not allowed. Please upload an image file (PNG, JPG, JPEG, GIF, or BMP)'}), 400
    
    # Save file
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    
    # Analyze pattern
    try:
        pattern = analyze_knitting_pattern(filepath)
        if pattern is None:
            return jsonify({'error': 'Could not process image. Please try another photo.'}), 400
        
        return jsonify({'success': True, 'pattern': pattern})
    except Exception as e:
        return jsonify({'error': f'Error processing image: {str(e)}'}), 500

if __name__ == '__main__':
    # Get debug mode from environment variable, default to True for development
    debug_mode = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    # Get host from environment variable, default to 0.0.0.0 for development
    host = os.environ.get('FLASK_HOST', '0.0.0.0')
    # Get port from environment variable, default to 5000
    port = int(os.environ.get('FLASK_PORT', 5000))
    
    app.run(debug=debug_mode, host=host, port=port)
