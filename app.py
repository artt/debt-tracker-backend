from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import os
from waitress import serve

app = Flask(__name__)
logger = app.logger
logger.setLevel(20)
cors = CORS(app)

@app.route("/")
def hello_world():
  return "Hi!"

@app.route("/data/nd", methods=["POST"])
def data_nd():
  # will replace this with data from request body
  req = request.get_json()
  facet = req['facet']

  filter_list = list(req['filters'].keys())
  for i, f in enumerate(filter_list):
    print('-------------')
    print('filter', f, req['filters'][f])
    # special treatment for filter_product and filter_fi
    adjusted_f = 'filter_' + f if f in ['product', 'fi'] else f
    if (i == 0):
      mask = (df[adjusted_f].isin(req['filters'][f]))
    else:
      mask = (mask) & (df[adjusted_f].isin(req['filters'][f]))
  tmp = df[mask][['period', facet, 'count']].groupby(['period', facet]).sum()

  new_index = pd.MultiIndex.from_product([tmp.index.unique(level=0), tmp.index.unique(level=1)])
  tmp = tmp.reindex(new_index) \
    .fillna(0)
  periods = tmp.index.get_level_values(0).drop_duplicates()
  tmp = tmp.sort_values([facet, 'period']) \
    .groupby(facet).agg(count=('count', pd.Series.to_list))
  return({
    "facet": facet,
    "first_period": str(periods[0]),
    "data": tmp['count'].to_dict(),
  })

if __name__ == '__main__':
  df = pd.read_pickle('processed/table-83-borrowers.pickle')
  logger.info('Starting app...')
  if os.getenv('FLASK_ENV') == 'development':
    app.run(host='0.0.0.0', debug=True, port=int(os.environ.get('PORT', '1443')))
  else:
    serve(app, host='0.0.0.0', port=int(os.environ.get('PORT', '1443')))