# SkyRefrax

A PyQt5 application to calculate the refraction delta based on wavelength, zenith angle, pressure, temperature, and water vapor content.

## Features
- Input multiple wavelengths and zenith angles.
- Compute refraction delta for given atmospheric conditions.
- Display results in a table format.
- Export table as a PNG or PDF.

## Requirements
- Python 3.8+
- PyQt5
- Matplotlib

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Icorebleidd/SkyRefrax.git
   cd SkyRefrax
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Run the application with:
```bash
python SkyRefrax.py
```

## Inputs
- **Wavelengths (Å):** Comma-separated values (e.g., `4000, 5000, 6000`).
- **Zenith Angles:** Format `deg min sec` (e.g., `45 30 0, 60 15 30`).
- **Pressure (mmHg)**
- **Temperature (°C)**
- **Water Vapor (mmHg)**

## Output
- A table displaying the computed refraction delta values.
- Column headers: Secant of zenith angles.
- Row headers: Wavelengths in Å.

## Exporting Data
You can save the table as a PNG or PDF file via the "Export Table" button.

## License
This project is licensed under the MIT License.

## Author
Leonardo Tozzo - [GitHub Profile](https://github.com/Icorebleidd)
