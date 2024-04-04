const path = require('path');
const Dotenv = require('dotenv-webpack');

module.exports = {
  mode: 'production', // O 'development' accorde the case
  entry: {
    mainPanel: './applications/web/typescript/mainPanel/main.ts',
    deleteVirtualMachine: './applications/web/typescript/deleteVirtualMachine/main.ts',
    resourceMonitor: './applications/web/typescript/resourceMonitor/main.ts',
    createVMInteractionButton: './applications/web/typescript/createNewVirtualMachine/main.ts',
    setupVirtualMachine: './applications/web/typescript/setupVirtualMachine/main.ts'
  },
  watch: true,
  watchOptions: {
    ignored: /node_modules/,
  },
  output: {
    filename: '[name]/bundle.js',
    path: path.resolve(__dirname, './applications/web/qubik_static_files/js'),
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
  optimization: {
    minimize: true, // Optimization for production code.
    splitChunks: {
      cacheGroups: {
        commons: {
          name: 'commons',
          chunks: 'all',
          minChunks: 2,
        },
      },
    },
  },
  plugins: [
    new Dotenv({
      path: `.env.${process.env.NODE_ENV}`,
    }),
  ],
  resolve: {
    extensions: ['.ts', '.js'],
  },
};
