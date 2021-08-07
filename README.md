# Benfords_Law
This app is intended to validate a user-provided ‘observed’ data against the phenomenon known as Benford’s Law.  Benford’s Law is defined as the phenomenon of leading digits in naturally occurring numbers having the following frequency of occurrences:  
 0 = 0% frequency of occurrence
 1 = 30.1% frequency of occurrence
 2 = 17.6% frequency of occurrence
 3 = 12.5% frequency of occurrence
 4 = 9.7% frequency of occurrence
 5 = 7.9% frequency of occurrence
 6 = 6.7% frequency of occurrence
 7 = 5.8% frequency of occurrence
 8 = 5.1% frequency of occurrence
 9 = 4.6% frequency of occurrence

The data validation step is performed by applying a Chi-Square test to the observed data from the input file and an ‘expected’ data set that is known to adhere to Benford’s Law.  The null hypothesis being tested is that the observed and expected data are related, meaning there is no independence between them. Failing to reject the null hypothesis results in the observed data from the input file being validated as adhering to Benford’s Law.  Comma separated (.csv) files are supported for loading by the app. The app's main form includes a 'Column Name' field, defaulting to ‘7_2009’, which can be used to manually identify the column to be analyzed in an input file.  This application was tested by submitting its form multiple times and observing the results.  

Assumptions made while developing the app include but are not limited to:
- All rows in the ‘7_2009’ and similar columns will contain a single integer value.
- The leading digit of column integer values may be ‘0’ but this will occur with an effectively zero percent frequency, represented by a percentage value of 0.00001 in the code base.  This assumption is based on the presence of two ‘0’ values in the ‘7_2009’ column of the provided data file.  
- A standard significance factor (alpha) of 0.05 is sufficient for the Chi-Square test.
- The randomly generated dataset will always be of sufficient quantity and distribution to validate Benford’s Law and therefore can always be used with the user-loaded dataset for performing the Chi-Square test.  
