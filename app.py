
import base64, math, os
import pandas as pd

from io import BytesIO
from flask import Flask, render_template, request, flash, redirect
from matplotlib.figure import Figure


app = Flask(__name__)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

# Expected percentages for first digits 1-9 according to Benford's Law
EXPECTED_PERCENTS = [0.000001, 30.1, 17.6, 12.5, 9.7, 7.9, 6.7, 5.8, 5.1, 4.6]

# Critical value for P-value of 0.05 with 8 degrees of freedom is 15.51
CHI_SQUARE_CRITICAL_VALUE = 15.51



def chi_square_test(observed_count, expected_count):
    """Return boolean and stat value for Pearson's chi-square test on observed vs expected digit counts."""
    chi_square_stat = 0
    for observed, expected in zip(observed_count, expected_count):
        chi_square = math.pow(observed - expected, 2)
        chi_square_stat += chi_square / expected
    return chi_square_stat < CHI_SQUARE_CRITICAL_VALUE, round(chi_square_stat)


def get_observed_count_dist(first_digits):
    """Return digit count distribution and digit percent occurrence distribution for observed first_digits list."""
    observed_count_dist = []
    for i in range(0, 10):
        count = first_digits.count(i)
        observed_count_dist.append(count)
        observed_percent_dist = [(i / len(first_digits)) * 100 for i in observed_count_dist]
    return observed_count_dist, observed_percent_dist


def get_expected_count_dist(len_first_digits):
    """Return expected digit count distribution that obeys Benford's Law and has same number of total first digits as
       the observed count."""
    return [round(p * len_first_digits / 100) for p in EXPECTED_PERCENTS]


@app.route('/create', methods=['GET', 'POST'])
def create():
    return render_template('create.html')


@app.route('/handle_data', methods=['GET', 'POST'])
def handle_data():
    file = request.files['file']
    # If the user does not select a file, the browser submits an empty file without a filename.
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    column_name = request.form['column_name']
    df = pd.read_csv(file)
    col_of_interest = df[column_name]
    first_digits = [int(i) for i in list(col_of_interest.astype(str).str[0])]
    observed_count, observed_percentages = get_observed_count_dist(first_digits)
    expected_count = get_expected_count_dist(len(first_digits))
    expected_count[0] = 0.000001

    chi_square_bool, chi_square_stat = chi_square_test(observed_count, expected_count)

    if chi_square_bool:
        val_answer = "YES"
        explanation = "The Chi-Square statistic is lower than the critical value."
    else:
        val_answer = "NO"
        explanation = "The Chi-Square statistic is higher than the critical value."

    fig = Figure()
    ax = fig.subplots()
    ax.set_xticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    ax.set_xlabel('First Digit')
    ax.set_ylabel('First Digit Count')
    ax.set_title('Observed vs Expected Number of First Digits in ' + column_name)
    ax.plot(observed_count)
    ax.plot(expected_count)
    ax.legend(["Observed Count Distribution", "Expected Count Distribution"], loc="lower right")
    # Save to temporary buffer
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output
    plotdata = base64.b64encode(buf.getbuffer()).decode("ascii")

    return "<h2>Can we validate Benford's Law based on the '{}' column in the input file?</h2>" \
           "<h1><b>{}</b></h1><h3>{}</h3><br>" \
           "<img src='data:image/png;base64,{}'/>" \
           "<p>Observed digit count distribution: {}</p>" \
           "<p>Expected digit count distribution: {}</p>".format(column_name, val_answer, explanation, plotdata,
                                                                 observed_count, expected_count)
