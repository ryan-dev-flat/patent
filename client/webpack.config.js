const { override, addBabelPreset, addBabelPlugin } = require('customize-cra');

module.exports = override(
  addBabelPreset('@babel/preset-env'),
  addBabelPlugin('@babel/plugin-proposal-class-properties'),
  config => {
    config.module.rules.push({
      test: /\.js$/,
      exclude: /node_modules/,
      use: {
       
        options: {
          presets: ['@babel/preset-env'],
          plugins: ['@babel/plugin-proposal-class-properties']
        }
      }
    });
    return config;
  }
);
