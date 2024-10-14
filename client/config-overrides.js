const { override, addBabelPreset, addBabelPlugin } = require('customize-cra');

module.exports = override(
  addBabelPreset('@babel/preset-env'),
  addBabelPlugin('@babel/plugin-proposal-class-properties')
);

