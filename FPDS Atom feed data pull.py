# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 18:44:49 2020

@author: CatsAndProcurement

The purpose of the script is to
download a user-defined dataset from the 
Federal Procurement Data System (FPDS)
and aggregate and display the data using Pandas.

FPDS is a publicly accessible US government data system 
for prime contract award information.
Sample FPDS web API call:
https://www.fpds.gov/ezsearch/fpdsportal?s=FPDS&indexName=awardfull&templateName=CSV&q=++CONTRACT_FISCAL_YEAR%3A%222019%22+DEPARTMENT_ID%3A%224700%22+PRODUCT_OR_SERVICE_CODE%3A%22D3*%22

"""

# Pandas lets us do fancy calculations:
import pandas as pd
# We'll use this to write a paragraph later:
writePara = ""

# The following are parameters we'll use for the FPDS API call
# '4700' is the API call code for the General Services Administration (GSA):
callDept = "4700"
# 2019 is the fiscal year that we'll pull data for:
callFY = "2019"
# Product and Service Codes (PSCs) tell us what the government is buying:
askPSC = input("Hi! This Python script provides info on General Services"+
               "Administration (GSA) contracting!"+"\n"+
               "Please enter a 2-digit Product Service Code (PSC)."+"\n"+
               "Suggestions include 'D3' for IT services,"+
               "'S2' for Housekeeping services,"+
               "see here for others:"+"\n"+
               "https://www.acquisition.gov/PSC_Manual"+"\n")
# FPDS uses asterisks as wildcards, so the following lets us pull all PSC data:
callPSC = askPSC + "*"

# The following assembles our API call as a string:
callURL = ("https://www.fpds.gov/ezsearch/fpdsportal?s=FPDS&indexName=awardfull&templateName=CSV&q=++"+
           "CONTRACT_FISCAL_YEAR%3A%22"+callFY+
           "%22+DEPARTMENT_ID%3A%22"+callDept+
           "%22+PRODUCT_OR_SERVICE_CODE%3A%22"+callPSC+
           "%22")
# The following lets the user know the program is pulling their data:
print("\n"+
      "Now accessing:"+"\n"+
      callURL+
      "\n")
# The following extracts the data from the FPDS web site as a CSV file:
dfFPDS = pd.read_csv(callURL,encoding="latin-1")

# A contract 'obligation' is the point at which a US govt contracting officer 
# agrees that the USA will pay money on a contract
# The following cleans up potentially error-causing contract obligation data:
dfFPDS["Action Obligation ($)"] = dfFPDS["Action Obligation ($)"].str.replace("$","")
dfFPDS["Action Obligation ($)"] = dfFPDS["Action Obligation ($)"].str.replace(",","")
dfFPDS["Action Obligation ($)"] = dfFPDS["Action Obligation ($)"].astype(float)
# The following modifies PSC data to make it more readable:
dfFPDS["PSC Description"] = dfFPDS["PSC Description"].str.lower()
# The following creates a new variable with both PSC and a description of
# what that PSC means:
dfFPDS["Code and Description"] = (dfFPDS["PSC"].apply(str)+" ("+dfFPDS["PSC Description"]+")")
# The following deletes hyphens and capitalizes the phrases 'IT' & 'R&D' if needed:
dfFPDS["Code and Description"] = dfFPDS["Code and Description"].str.replace("- "," ")
dfFPDS["Code and Description"] = dfFPDS["Code and Description"].str.replace("it ","IT ")
dfFPDS["Code and Description"] = dfFPDS["Code and Description"].str.replace("r&d ","R&D ")

# The following uses Pandas to create a pivot table and add up the obligations
# based on our new 'Code and Description' variable:
dfPivot = dfFPDS.pivot_table(index=["Code and Description"],
                             values=["Action Obligation ($)"],
                             aggfunc=sum,
                             fill_value=0,
                             margins="true")
# The following sorts the data high to low:
dfPivot = dfPivot.reindex(dfPivot["Action Obligation ($)"].sort_values(ascending=False).index).reset_index()

# The following adds an introduction sentence to our paragraph:
writePara=(writePara+
           "The following data represents real-time information on US General Services "+
           "Administration (GSA) contract obligations for fiscal year "+callFY+
           " in Product Service Code (PSC) category "+askPSC+". ")

# The following figures out how many times we ought to loop through the pivot
# table to write sentences:
numPSCs = len(dfPivot.index)-1
iCounter = min(numPSCs-1,5)

# The following reads the top few aggregated values in the pivot table,
# also finds their PSC code/descriptions, puts them in sentences, and
# puts the sentences in a paragraph:
for i in range(1,iCounter):
    writeSent=("GSA obligated "+
               "${:,.0f}".format(round(dfPivot.iloc[i,1]))+
               " on contracts coded under PSC "+
               dfPivot.iloc[i,0]+".")
    writePara=writePara+writeSent
    i=i+1

# The following adds a final sentence to the paragraph, letting the user know 
# how much the agency obligated in total for all PSCs in the dataset:
writeSent = ("In total, GSA obligated "+
             "${:,.0f}".format(round(dfPivot.iloc[0,1]))+
             " on contracts listed under PSC category "+askPSC+".")
# The following adds that last sentence to the paragraph:
writePara=writePara+writeSent
# The following prints the paragraph:
print(writePara)

# Now we'll create a basic chart in Pandas
# The following deletes the first row of the dataframe (the sum total):
dfPivot=dfPivot.drop(dfPivot.index[0])
# And the following displays the entire pivot table, minus that first row
# we deleted, as a bar graph:
dfPivot.plot.bar(x="Code and Description",
                 y="Action Obligation ($)",
                 title=("GSA contract obligations in PSC category "+askPSC+" for fiscal year "+callFY),
                 figsize=(10,6))


