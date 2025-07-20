const spec = {
  "$schema": "https://vega.github.io/schema/vega-lite/v4.17.0.json",
  "config": { "view": { "continuousWidth": 400, "continuousHeight": 300 } },
  "title": "Probability of each emotion over time",
  "width": 1000,
  "height": 400,
  "data": { "name": "emotionData" },
  "datasets": {
    "emotionData": [
      { "Time": 0, "Angry": 0.34, "Disgust": 0.0002, "Fear": 0.0548, "Happy": 0.089, "Sad": 0.0471, "Surprise": 0.0364, "Neutral": 0.4315 },
      { "Time": 1, "Angry": 0.0408, "Disgust": 0.00009, "Fear": 0.0146, "Happy": 0.0153, "Sad": 0.0538, "Surprise": 0.0039, "Neutral": 0.8713 },
      // ... continue with more records
    ]
  },
  "layer": [
    {
      "mark": { "type": "line", "color": "orange", "strokeWidth": 2 },
      "encoding": {
        "x": { "field": "Time", "type": "quantitative" },
        "y": { "field": "Angry", "type": "quantitative" },
        "tooltip": [{ "field": "Angry", "type": "quantitative" }]
      }
    },
    {
      "mark": { "type": "line", "color": "red", "strokeWidth": 2 },
      "encoding": {
        "x": { "field": "Time", "type": "quantitative" },
        "y": { "field": "Disgust", "type": "quantitative" },
        "tooltip": [{ "field": "Disgust", "type": "quantitative" }]
      }
    },
    {
      "mark": { "type": "line", "color": "green", "strokeWidth": 2 },
      "encoding": {
        "x": { "field": "Time", "type": "quantitative" },
        "y": { "field": "Fear", "type": "quantitative" },
        "tooltip": [{ "field": "Fear", "type": "quantitative" }]
      }
    },
    {
      "mark": { "type": "line", "color": "blue", "strokeWidth": 2 },
      "encoding": {
        "x": { "field": "Time", "type": "quantitative" },
        "y": { "field": "Happy", "type": "quantitative" },
        "tooltip": [{ "field": "Happy", "type": "quantitative" }]
      }
    },
    {
      "mark": { "type": "line", "color": "black", "strokeWidth": 2 },
      "encoding": {
        "x": { "field": "Time", "type": "quantitative" },
        "y": { "field": "Sad", "type": "quantitative" },
        "tooltip": [{ "field": "Sad", "type": "quantitative" }]
      }
    },
    {
      "mark": { "type": "line", "color": "pink", "strokeWidth": 2 },
      "encoding": {
        "x": { "field": "Time", "type": "quantitative" },
        "y": { "field": "Surprise", "type": "quantitative" },
        "tooltip": [{ "field": "Surprise", "type": "quantitative" }]
      }
    },
    {
      "mark": { "type": "line", "color": "brown", "strokeWidth": 2 },
      "encoding": {
        "x": { "field": "Time", "type": "quantitative" },
        "y": { "field": "Neutral", "type": "quantitative" },
        "tooltip": [{ "field": "Neutral", "type": "quantitative" }]
      }
    }
  ]
};

vegaEmbed('#vis', spec);
