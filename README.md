# 🧶 Knitting Pattern Tool

A simple and user-friendly web application that helps you create detailed knitting patterns from photos. Perfect for elderly users and those with limited computer experience!

## Features

- **Photo Upload**: Easy drag-and-drop or click to upload photos of knitted items
- **Pattern Analysis**: Automatically analyzes the image to detect colors, complexity, and pattern type
- **Detailed Instructions**: Generates step-by-step knitting instructions including:
  - Number of stitches and rows needed
  - Color information
  - Materials list
  - Stitch types
  - Complete instructions from cast-on to bind-off
- **Large, Clear Interface**: Designed with large fonts and buttons for easy readability
- **Print-Friendly**: Print your pattern directly from the browser

## Installation

### Requirements

- Python 3.8 or higher
- pip (Python package installer)

### Setup Instructions

1. **Clone or download this repository**

2. **Open a terminal/command prompt and navigate to the project folder**

3. **Install required packages**:
   ```bash
   pip install -r requirements.txt
   ```

   Note: If you encounter issues with OpenCV on some systems, you might need to install additional dependencies. On Linux:
   ```bash
   sudo apt-get install python3-opencv
   ```

4. **Run the application**:
   ```bash
   python app.py
   ```

5. **Open your web browser and go to**:
   ```
   http://localhost:5000
   ```

## How to Use

1. **Start the Application**: Run `python app.py` in your terminal

2. **Open the Web Page**: Go to http://localhost:5000 in your web browser

3. **Upload a Photo**: 
   - Click on "Choose File" button
   - Select a photo of a knitted sweater, scarf, or other item
   - The photo can be in PNG, JPG, JPEG, GIF, or BMP format

4. **Create Pattern**: 
   - Click the large "Create My Pattern" button
   - Wait a few seconds while the tool analyzes your photo

5. **View Your Pattern**: 
   - The pattern will appear with all the details you need
   - Including colors, materials, and step-by-step instructions

6. **Print Your Pattern**: 
   - Click the "Print Pattern" button to print your instructions
   - Or save it as a PDF using your browser's print dialog

7. **Create Another Pattern**: 
   - Click "Create Another Pattern" to start over with a new photo

## Tips for Best Results

- Use clear, well-lit photos of knitted items
- Close-up photos work better than distant shots
- Photos with good contrast between colors produce better color analysis
- The tool works best with photos showing the full pattern

## Technical Details

The tool uses:
- **Flask**: Web framework for the application
- **OpenCV**: Image processing for pattern analysis
- **Pillow**: Image handling
- **NumPy**: Numerical computations for color analysis

## Troubleshooting

**Problem**: The application won't start
- **Solution**: Make sure you have installed all requirements using `pip install -r requirements.txt`

**Problem**: Error uploading photo
- **Solution**: Check that your photo is under 16MB and in a supported format (PNG, JPG, JPEG, GIF, BMP)

**Problem**: Pattern doesn't look accurate
- **Solution**: Try a different photo with better lighting or a clearer view of the pattern

## For Developers

### Project Structure
```
KnittingPatternTool/
├── app.py                 # Main Flask application
├── templates/
│   └── index.html        # Web interface
├── uploads/              # Uploaded photos (temporary)
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

### Extending the Tool

The pattern analysis in `app.py` can be enhanced by:
- Improving color detection algorithms
- Adding more stitch pattern recognition
- Implementing machine learning for better pattern classification
- Adding user preferences for gauge and yarn weight

## License

This project is open source and available for anyone to use and modify.

## Support

If you need help or have questions, please open an issue on the project repository.
