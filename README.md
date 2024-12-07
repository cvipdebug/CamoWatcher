### **CamoWatcher - Real-Time Camo Unlock Detection**

**CamoWatcher** is a Python-based tool designed to monitor a selected screen region for Call of Duty camo unlock notifications. Leveraging OCR technology, it detects and extracts the camo name from real-time game footage, ensuring you never miss a milestone.

---

### **Features**
- 🎯 **Accurate Text Recognition**: Uses [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) to detect camo unlock messages from the game screen.  
- 📡 **Real-Time Monitoring**: Continuously scans the selected region for new notifications.  
- 🔄 **Duplicate Detection Prevention**: Ensures the same camo is not reported multiple times in quick succession.  
- 🖼️ **Custom Region Selection**: Interactively select the area of the screen you want to monitor.  
- 🖥️ **Live Preview (Optional)**: Displays the monitored region in a preview window.  
- ⚡ **Lightweight & Efficient**: Designed to run seamlessly in the background without affecting game performance.  

---

### **How It Works**
1. Select the screen region to monitor via a simple click-and-drag interface.  
2. CamoWatcher scans the selected area in real-time, processing text with OCR.  
3. When a camo unlock message is detected, it prints the camo name in this format:  
   ```
   [CamoWatcher] Camo Unlocked: {CAMO_NAME}
   ```
4. The tool prevents duplicate notifications by tracking the last detected camo name.

---

### **Requirements**
- **Python 3.7+**  
- **Tesseract OCR** installed and accessible in your system's PATH.  
- Dependencies: `opencv-python`, `numpy`, `mss`, `pytesseract`  

Install required packages with:  
```bash
pip install -r requirements.txt
```

---

### **Getting Started**
1. Clone the repository:  
   ```bash
   git clone https://github.com/yourusername/camowatcher.git
   ```
2. Install dependencies:  
   ```bash
   pip install -r requirements.txt
   ```
3. Run the script:  
   ```bash
   python camowatcher.py
   ```

---

### **Usage**
- **Interactive Region Selection**: Use your mouse to drag and select the area of interest on your screen.  
- **Live Monitoring**: Choose whether to enable a live preview window after region selection.  
- **Stop Monitoring**: Press `q` to exit the tool safely.  

---

### **Contribute**
Pull requests are welcome! If you find a bug or have suggestions for new features, feel free to open an issue.  

---
