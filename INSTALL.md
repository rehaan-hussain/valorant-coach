# Manual Installation Guide

If you encounter dependency conflicts during automatic setup, follow this manual installation guide.

## Step 1: Create Virtual Environment (Recommended)

```bash
# Create a new virtual environment
python -m venv valorant-coach-env

# Activate the environment
# Windows:
valorant-coach-env\Scripts\activate
# macOS/Linux:
source valorant-coach-env/bin/activate
```

## Step 2: Install Core Dependencies

Install the essential packages one by one:

```bash
pip install opencv-python>=4.8.0
pip install numpy>=1.21.0
pip install streamlit>=1.25.0
pip install mss>=9.0.0
pip install pillow>=9.0.0
pip install pandas>=1.5.0
pip install matplotlib>=3.5.0
pip install plotly>=5.0.0
```

## Step 3: Install Optional Dependencies

These are for advanced features and can be installed separately:

```bash
# For advanced AI features (optional)
pip install tensorflow>=2.13.0
pip install torch>=2.0.0
pip install torchvision>=0.15.0

# For additional computer vision
pip install ultralytics>=8.0.0
pip install easyocr>=1.7.0

# For additional utilities
pip install pynput>=1.7.0
pip install pygame>=2.5.0
pip install python-dotenv>=1.0.0
pip install requests>=2.31.0
```

## Step 4: Test Installation

```bash
python test_installation.py
```

## Step 5: Run the Application

```bash
# Run demo (no Valorant required)
python demo.py

# Run main application
python main.py
```

## Troubleshooting

### Common Issues

1. **Pillow Version Conflicts**
   ```bash
   pip uninstall pillow
   pip install pillow>=9.0.0
   ```

2. **OpenCV Issues**
   ```bash
   pip uninstall opencv-python
   pip install opencv-python-headless
   ```

3. **Streamlit Issues**
   ```bash
   pip install streamlit --upgrade
   ```

4. **Permission Issues (Windows)**
   - Run Command Prompt as Administrator
   - Or use: `pip install --user package_name`

### Alternative: Minimal Installation

If you only want the basic features, install just these:

```bash
pip install opencv-python
pip install numpy
pip install streamlit
pip install mss
pip install pillow
pip install pandas
pip install matplotlib
```

### Using Conda (Alternative)

If you prefer conda:

```bash
# Create conda environment
conda create -n valorant-coach python=3.10
conda activate valorant-coach

# Install packages
conda install -c conda-forge opencv numpy streamlit pillow pandas matplotlib
pip install mss plotly
```

## Verification

After installation, run:

```bash
python test_installation.py
```

You should see:
```
🎮 Valorant AI Coach - Installation Test
==================================================
🧪 Testing dependencies...
✅ opencv-python available
✅ numpy available
✅ streamlit available
✅ mss available
✅ pillow available

🧪 Testing imports...
✅ Capture modules imported successfully
✅ Analysis modules imported successfully
✅ Coaching modules imported successfully
✅ Utils modules imported successfully

🧪 Testing basic functionality...
✅ Frame processor initialized
✅ Game analyzer initialized
✅ Coach initialized
✅ Skill assessor initialized

==================================================
📊 Test Results:
Dependencies: ✅ PASS
Imports: ✅ PASS
Functionality: ✅ PASS

🎉 All tests passed! Valorant AI Coach is ready to use.
```

## Next Steps

Once installation is complete:

1. **Run the demo**: `python demo.py`
2. **Start the app**: `python main.py`
3. **Open browser**: Navigate to `http://localhost:8501`

## Support

If you still encounter issues:

1. Check your Python version (3.8+ required)
2. Ensure you're using a clean virtual environment
3. Try installing packages individually
4. Check the error messages for specific conflicts
5. Consider using conda instead of pip