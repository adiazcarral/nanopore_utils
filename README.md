### Nanopore Utils  

**Nanopore Utils** is a Python-based toolkit for processing and analyzing nanopore sequencing data. This repository includes scripts for feature extraction, normalization, and preprocessing, designed to streamline workflows and facilitate downstream applications such as machine learning or statistical analysis.  

---

#### Features  
- **Feature Extraction**:  
  Extract the following features from nanopore translocation signals:  
  - **Coordinates**: Starting positions of events.  
  - **Dwell Time**: Duration of events.  
  - **Mean**: Average signal value for each event.  
  - **Height**: Difference between the maximum and minimum signal within each event.  
  - **Number of Levels**: Count of discrete levels in an event.  

- **Normalization**:  
  Scale extracted features to a defined range (e.g., `[0, 255]`) for consistency.  

- **File Handling**:  
  - Input: `.mat` (MATLAB) and `.csv` formats.  
  - Output: Processed features saved in `.csv` or `.mat` formats.  

---

#### Installation  
1. Clone the repository:  
   ```bash
   git clone https://github.com/your-username/nanopore-utils.git
   cd nanopore-utils
   ```  
2. Install the required Python dependencies:  
   ```bash
   pip install -r requirements.txt
   ```  

---

#### Usage  
1. Place your input files (`.mat` or `.csv`) in the working directory.  
2. Modify the `input_file` and `output_file` variables in the `main` function of the script you want to use.  
3. Run the script:  
   ```bash
   python nanopore_feature_extraction.py
   ```  
4. Extracted features will be saved to the specified output file.  

---

#### Example  
To process a file named `A1.mat` and save features to `output_features.csv`:  
```python
# In nanopore_feature_extraction.py
input_file = "A1.mat"
output_file = "output_features.csv"
```  
Run the script:  
```bash
python nanopore_feature_extraction.py
```  

---

#### Contributing  
Contributions are welcome! If you have suggestions, bug reports, or new features to add, feel free to:  
- Fork the repository.  
- Create a new branch.  
- Submit a pull request.  

---

#### License  
This repository is licensed under the MIT License.  

---

#### Contact  
For any questions or issues, please reach out via GitHub or email.  

