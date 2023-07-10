const path = require('path');
const Dotenv = require('dotenv-webpack');

module.exports = {
  entry: {
    mainPanel: './applications/web/typescript/mainPanel/main.ts',
    removeVirtualMachine: './applications/web/typescript/removeVirtualMachine/main.ts',
  },
  output: {
      filename: '[name]/bundle.js',
      path: path.resolve(__dirname, './applications/web/static/js'),
      libraryTarget: 'umd',
  },
  module: {
    rules: [
      {
        test: /\.ts$/,
        use: [
            {
              loader: 'babel-loader',
              options: {
                presets: [
                    '@babel/preset-env',
                    '@babel/preset-typescript',
                ],
              },
            },
            'ts-loader',
        ],
        exclude: /node_modules/,
      },
    ],
  },
  plugins: [
    new Dotenv(),
  ],
  resolve: {
    extensions: ['.ts', '.js'],
  },
};