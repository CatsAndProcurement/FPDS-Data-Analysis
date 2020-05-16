# FPDS-Data-Analysis

Using Python and Pandas to download and analyze contract obligation data from the US government's Federal Procurement Data System (FPDS)

Created on Tue Apr 14 18:44:49 2020

@author: CatsAndProcurement

The purpose of the script is to download a user-defined dataset from the Federal Procurement Data System (FPDS) and aggregate and display the data using Pandas. Documentation is intended to guide a new Python/Pandas user through the process of writing similar scripts in a clear, simple, step-by-step way.

FPDS is a publicly accessible US government data system for prime contract award information.
Sample FPDS web API call (call parameters listed as individual lines):
https://www.fpds.gov/ezsearch/fpdsportal?s=FPDS
&indexName=awardfull
&templateName=CSV
&q=++CONTRACT_FISCAL_YEAR%3A%222019%22+DEPARTMENT_ID%3A%226900%22+PRODUCT_OR_SERVICE_CODE%3A%22D3*%22

The above sample call pulls data for Contract Fiscal Year 2019, Department ID #6900 (the Department of Transportation), and Product Service Code (PSC) D3 (IT services). These parameter values can be edited (and other parameters added) as needed by data analysts to meet customized needs.
