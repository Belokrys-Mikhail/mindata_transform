# mindata_transform

This script takes .txt file with raw data of FEI Quanta-600 mineral analysis which includes:
  1. name of sample (named like 'sample ...');
  2. name of spectrum (named like ['sp 01', 'sp 02', ..., 'sp 12']);
  3. chemical composition (both elemental and oxide forms).

... and create a pivot table like:
  Indexes:
    level 0 - sample name;
    level 1 - spectrum name.
  Columns:
    all existing chemical compounds in the sample;
    total summ of spectrum compounds (if all is correct it should be like 100.0 +/- 0.01).
