from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import os

app = Flask(__name__)
cors = CORS(app)

@app.route("/")
def hello_world():
  return "Hello!"

@app.route("/data/nd", methods=["POST"])
def data_nd():
  # will replace this with data from request body
  facet = 'age'
  filter_product = 0
  filter_fi = 0
  tmp = df[(df['filter_product'] == filter_product) & (df['filter_fi'] == filter_fi)] \
    [['period', facet, 'count']].groupby(['period', facet]).sum()
  new_index = pd.MultiIndex.from_product([tmp.index.unique(level=0), tmp.index.unique(level=1)])
  tmp = tmp.reindex(new_index) \
    .fillna(0) \
    .sort_values([facet, 'period']) \
    .groupby(facet).agg(count=('count', pd.Series.to_list))
  return tmp['count'].to_dict()

if __name__ == '__main__':
  df = pd.read_csv('processed/table-83-borrowers.csv')
  app.run(host='0.0.0.0', debug=True, port=int(os.environ.get('PORT', '1443')))