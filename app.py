from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import os
import csv
import time
import pandas as pd
import io


app = Flask(__name__)


def update():
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')
    browser = webdriver.Chrome(f"{os.getcwd()}/chromedriver", options=options)
    link = "http://www.koeri.boun.edu.tr/scripts/lst8.asp"
    browser.get(link)
    raw_text = browser.find_elements(by=By.TAG_NAME, value="pre")[0].text
    browser.close()
    data_buffer = io.StringIO(raw_text)
    widths = [(0, 10), (11, 19), (21, 28), (31, 38), (43, 49), (59, 63), (71, 120)]
    df = pd.read_fwf(data_buffer, colspecs=widths, skiprows=[i for i in range(6)], header=None)
    df.columns = ["date", "time", "latitude", "longitude", "depth", "magnitude", "location"]
    return df


@app.route('/')
def index():
    df = update()
    return render_template("index.html",
                           dates=df["date"].tolist(),
                           times=df["time"].tolist(),
                           latitudes=df["latitude"].tolist(),
                           longitudes=df["longitude"].tolist(),
                           depths=df["depth"].tolist(),
                           magnitudes=df["magnitude"].tolist(),
                           locations=df["location"].tolist(),
                           table=df.to_html(classes='table table-striped table-bordered table-hover table-sm',
                                            index=False))


if __name__ == '__main__':
    app.run()
