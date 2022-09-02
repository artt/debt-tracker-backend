const express = require('express')
const app = express()
const cors = require('cors')
const port = 3003

app.use(cors())

app.get('/', (req, res) => {
  res.send('Hello World!')
})

app.get('/data/:facet/:value', (req, res) => {
  const dataFile = require(`./json/table-71-${req.params.facet}-${req.params.value}.json`)
  res.json(dataFile)
})

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`)
})