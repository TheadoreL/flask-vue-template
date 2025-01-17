const path = require('path');
const { VueLoaderPlugin } = require('vue-loader');
const webpack = require('webpack');
const fs = require('fs');
const ini = require('ini');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');  // 引入插件
const { WebpackManifestPlugin } = require('webpack-manifest-plugin');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');

const AutoImport = require('unplugin-auto-import/webpack').default;;
const Components = require('unplugin-vue-components/webpack').default;;
const { ElementPlusResolver } = require('unplugin-vue-components/resolvers')

// 读取 config.ini 文件
const config = ini.parse(fs.readFileSync(path.resolve(__dirname, 'config.ini'), 'utf-8'));

// 获取 environment 变量
const environment = config.environment || 'development'; // 默认为 development

module.exports = {
  entry: './front/app.ts',
  output: {
    path: path.resolve(__dirname, 'public'),  // 输出到 Flask 的静态目录
    filename: 'js/[name].[contenthash].js',
    chunkFilename: 'js/[name].[contenthash].js',
  },
  optimization: {
    splitChunks: {
      chunks: 'all',
      cacheGroups: {
        vendor: {
          test: /[\\/]node_modules[\\/]/,
          name: 'vendor',
          chunks: 'all',
          enforce: true,
        },
        common: {
          test: /[\\/]src[\\/]/,
          name: 'common',
          chunks: 'all',
          minChunks: 2,
        },
        // 进一步拆分某些大型模块
        largeModule: {
          test: /[\\/]src[\\/]largeModule[\\/]/,
          name: 'largeModule',
          chunks: 'all',
        },
      },
    },
  },
  module: {
    rules: [
      {
        test: /\.vue$/,
        loader: 'vue-loader',
      },
      {
        test: /\.ts$/,
        loader: 'ts-loader',
        exclude: /node_modules/,
        options: {
          appendTsSuffixTo: [/\.vue$/], // 使得 .vue 文件能够被 ts-loader 处理
        },
      },
      {
        test: /\.js$/,
        loader: 'babel-loader',
        exclude: /node_modules/,
      },
      {
        test: /\.css$/,
        use: [
          MiniCssExtractPlugin.loader,
          'css-loader',
          {
            loader: 'postcss-loader',
            options: {
              postcssOptions: {
                plugins: [
                  require('autoprefixer'),
                ],
              },
            },
          },
        ],
      },
      {
        test: /\.scss$/,
        use: [
          MiniCssExtractPlugin.loader,
          'css-loader',
          'sass-loader',
        ],
      },
    ],
  },
  resolve: {
    alias: {
      vue$: 'vue/dist/vue.esm-bundler.js', // 使用 Vue 3 的完整版
    },
    extensions: ['.ts', '.js', '.vue', '.json'],  // 增加 .ts 文件解析支持
  },
  plugins: [
    new CleanWebpackPlugin({
      cleanOnceBeforeBuildPatterns: [
          '**/*',
         '!favicon.ico' // 排除特定文件
        ],
      cleanStaleWebpackAssets: true, // 清理旧文件
      protectWebpackAssets: false, // 禁止删除 Webpack 生成的文件
    }),
    new VueLoaderPlugin(),
    new MiniCssExtractPlugin({
      filename: 'css/[name].[contenthash].css',
    }),
    new webpack.DefinePlugin({
      'process.env': JSON.stringify({
        NODE_ENV: environment,  // 使用从 config.ini 中读取的环境变量
      }),
    }),
    new WebpackManifestPlugin({
      fileName: 'manifest.json',  // 生成的 manifest 文件
      publicPath: '',  // 设置公共路径
    }),

    AutoImport({
      resolvers: [ElementPlusResolver()],
      dts: 'public/auto-imports.d.ts',  // 自动生成类型声明文件
    }),

    Components({
      resolvers: [ElementPlusResolver()],
      dts: 'public/components.d.ts',  // 自动生成组件类型声明文件
    }),
  ],
};
