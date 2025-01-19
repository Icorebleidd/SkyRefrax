import math
import matplotlib.pyplot as plt

def calcola_n_lambda(lambda_angstrom, pressione, temperatura, vapore_acqueo):
    # Constants for the formula
    K1 = 64.328
    K2 = 29498.1
    K3 = 255.4

    # Calculate the first term
    primo_termine = K1 + (K2 / (146 - (1 / lambda_angstrom) ** 2)) + (K3 / (41 - (1 / lambda_angstrom) ** 2))

    # Calculate with pressure and temperature
    secondo_termine = primo_termine * (pressione * (1 + (1.049 - 0.0157 * temperatura) * 1e-6 * pressione) / (720.883 * (1 + 0.003661 * temperatura)))

    # Calculate the third term
    terzo_termine = secondo_termine - (0.0624 - (0.000680 / lambda_angstrom) / (1 + 0.003661 * temperatura)) * vapore_acqueo

    # Calculate the fourth term
    quarto_termine = terzo_termine / (1e+6) + 1

    return quarto_termine

def calcola_delta_r(n_lambda, n_5000, angolo_rad):
    r_lambda = 206265 * (n_lambda - n_5000) * math.tan(float(angolo_rad))
    return r_lambda

def main():
    print("Enter values separated by commas: ")
    # Input for wavelengths
    lambda_angstrom_list = list(map(float, input("Wavelength in Angstroms: ").split(',')))

    # Convert wavelengths to micrometers
    micr_lambda_angstrom = [lungond * 1e-4 for lungond in lambda_angstrom_list]

    # Input for zenith angles
    angoli_gradi_lst = input("Zenith angles in degrees: ")
    angoli = angoli_gradi_lst.split(',')

    # Convert angles to radians and calculate the secant
    angoli_resolved = []
    secanti = []
    for ang_non_res in angoli:
        grado = ang_non_res.index('°')
        minuto = ang_non_res.index('\'')
        act_grado = float(ang_non_res[0:grado])
        act_minuto = float(ang_non_res[grado+1:minuto])
        act_secondo = float(ang_non_res[minuto+1:-1])
        angolo_gradi = act_grado + act_minuto / 60 + act_secondo / 3600
        angolo_radianti = math.radians(angolo_gradi)
        angoli_resolved.append(angolo_radianti)
        secanti.append(1 / math.cos(angolo_radianti))  # Calculate the secant

    # Other parameters
    pressione = float(input("Enter the pressure in mmHg: "))
    temperatura = float(input("Enter the temperature in °C: "))
    vapore_acqueo = float(input("Enter the water vapor pressure in mmHg: "))

    # Assume R(5000)
    r_5000 = calcola_n_lambda(5000 * 1e-4, pressione, temperatura, vapore_acqueo)

    # Calculate n_lambda for each wavelength
    nLambda = [calcola_n_lambda(lungondconv, pressione, temperatura, vapore_acqueo) for lungondconv in micr_lambda_angstrom]

    # Calculate the rDelta values for each combination
    rDelta_matrix = []
    for lambdas in nLambda:
        rDelta_row = []
        for angolo in angoli_resolved:
            rDelta = calcola_delta_r(lambdas, r_5000, angolo)
            rDelta_row.append(rDelta)
        rDelta_matrix.append(rDelta_row)

    # Create the table
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.axis('tight')
    ax.axis('off')

    # Labels for rows and columns
    col_labels = [f"Sec({round(sec, 2)})" for sec in secanti]
    row_labels = [f"{round(wavelength, 2)} Å" for wavelength in lambda_angstrom_list]

    # Insert the matrix into the table
    table_data = [[round(value, 2) for value in row] for row in rDelta_matrix]
    table = ax.table(cellText=table_data, colLabels=col_labels, rowLabels=row_labels, loc='center', cellLoc='center')

    # Improve the table's style
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.auto_set_column_width(col=list(range(len(secanti))))

    # Title
    ax.set_title("Tabella dei valori di rDelta", fontsize=14, pad=20)

    # Show the plot
    plt.show()

if __name__ == "__main__":
    main()
