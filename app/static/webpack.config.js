const resolve = require("path").resolve;

module.exports = {
  // When debugging, allow error to be found in source code
  devtool: "eval-source-map",
  // entry file to figure out dependencies from
  entry: __dirname + "/js/index.jsx",
  // where webpack will dump built assets
  output: {
    // local path on disk
    path: resolve("../public"),
    filename: "bundle.js",
    // path in browser e.g. /server/public
    publicPath: resolve("../public")
  },
  resolve: {
    extensions: [".js", ".jsx", ".css"]
  },

  // TODO: move to .babelrc in static/
  module: {
    rules: [
      {
        // Babel loaded for JSX -> JS
        test: /\.jsx?/,
        loader: "babel-loader",
        exclude: /node_modules/,
        query: {
          presets: ["@babel/preset-env", "@babel/preset-react"]
        }
      },
      {
        // handle css stylesheets
        test: /\.csv$/,
        loader: "style-loader!css-loader?modules"
      }
    ]
  }
};
