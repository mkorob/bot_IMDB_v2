# Advanced Techniques in Artificial Intelligence Conversational Agent


This project contains an intelligent conversational agent built as an assingment for the Advanced Topics in Artificial Intelligence course at the University of Zurich.
It is able to answer three types of queries:
* factual questions about properties of movies that are available on Wikidata (e.g. director of Inception)
* movie recommendations based on one or several movies provided by the user.
* image retrieval of one or more actors (if photos of them together exist) from the IMDb database.


## How It Works

1. Size Limit contains a CLI tool, 3 plugins (`file`, `webpack`, `time`)
   and 3 plugin presets for popular use cases (`app`, `big-lib`, `small-lib`).
   A CLI tool finds plugins in `package.json` and loads the config.
2. If you use the `webpack` plugin, Size Limit will bundle your JS files into
   a single file. It is important to track dependencies and�webpack polyfills.
   It is also useful for small libraries with many small files and without
   a bundler.
3. The `webpack` plugin creates an empty webpack project, adds your library
   and looks for the bundle size difference.
4. The `time` plugin compares the current machine performance with that of
   a low-priced Android devices to calculate the CPU throttling rate.
5. Then the `time` plugin runs headless Chrome (or desktop Chrome if it's
   available) to�track the time a browser takes to�compile and execute your JS.
   Note that these measurements depend on available resources and might
   be unstable. [See here](https://github.com/mbalabash/estimo/issues/5)
   for more details.
   
 ### Classifier Model
 The model used to classify user-typed input into one of the types of question was a customly fine-tuned BERT transformer model by me using a small training dataset of 50 rows.
 
 ```from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
	tokenizerClass = AutoTokenizer.from_pretrained("mkorob/class-sent")
	modelClass = AutoModelForSequenceClassification.from_pretrained("mkorob/class-sent")
	classSent = pipeline("text-classification", model=modelClass, tokenizer=tokenizerClass)
    ```
 The model has 5 classes: 0 - complicated question (requiring more than one query), 1 - recommendation question, 2 - media question, 3- factual question, 4 - random question (not regarding movies or actors), and was trained on a small 

## Operation Instructions

Suitable for applications that have their own bundler and send the JS bundle
directly to a client (without publishing it to npm). Think of a user-facing app
or website, like an email client, a CRM, a landing page or a blog with
interactive elements, using React/Vue/Svelte lib or vanilla JS.

<details><summary><b>Show instructions</b></summary>

1. Install the preset:

    ```sh
    $ npm install --save-dev size-limit @size-limit/file
    ```

2. Add the `size-limit` section and the `size` script to your `package.json`:

    ```diff
    + "size-limit": [
    +   {
    +     "path": "dist/app-*.js"
    +   }
    + ],
      "scripts": {
        "build": "webpack ./webpack.config.js",
    +   "size": "npm run build && size-limit",
        "test": "jest && eslint ."
      }
    ```

3. Here's how you can get the size for your current project:

    ```sh
    $ npm run size

      Package size: 30.08 kB with all dependencies, minified and gzipped
    ```

4. Now, let's set the limit. Add 25% to the current total size and use that as
   the limit in your `package.json`:

    ```diff
      "size-limit": [
        {
    +     "limit": "35 kB",
          "path": "dist/app-*.js"
        }
      ],
    ```

5. Add the `size` script to your test suite:

    ```diff
      "scripts": {
        "build": "webpack ./webpack.config.js",
        "size": "npm run build && size-limit",
    -   "test": "jest && eslint ."
    +   "test": "jest && eslint . && npm run size"
      }
    ```

6. If you don't have a continuous integration service running, don't forget
   to add one -�start with [Travis CI].

</details>


### JS Application and Time-based Limit

File size limit (in kB) is not the best way to describe your JS application
cost for developers. Developers will compare the size of the JS bundle
with the size of images. But browsers need much more time to parse 100 kB
of JS than 100 kB of an image since JS compilers are very complex.

This is why Size Limit support time-based limit. It runs headless Chrome
to track the time a browser takes to compile and execute your JS.

<details><summary><b>Show instructions</b></summary>

1. Install the preset:

    ```sh
    $ npm install --save-dev size-limit @size-limit/preset-app
    ```

2. Add the `size-limit` section and the `size` script to your `package.json`:

    ```diff
    + "size-limit": [
    +   {
    +     "path": "dist/app-*.js"
    +   }
    + ],
      "scripts": {
        "build": "webpack ./webpack.config.js",
    +   "size": "npm run build && size-limit",
        "test": "jest && eslint ."
      }
    ```

3. Here's how you can get the size for your current project:

    ```sh
    $ npm run size

      Package size: 30.08 kB with all dependencies, minified and gzipped
      Loading time: 602 ms   on slow 3G
      Running time: 214 ms   on Snapdragon 410
      Total time:   815 ms
    ```

4. Now, let's set the limit. Add 25% to the current total time and use that as
   the limit in your `package.json`:

    ```diff
      "size-limit": [
        {
    +     "limit": "1 s",
          "path": "dist/app-*.js"
        }
      ],
    ```

5. Add the `size` script to your test suite:

    ```diff
      "scripts": {
        "build": "webpack ./webpack.config.js",
        "size": "npm run build && size-limit",
    -   "test": "jest && eslint ."
    +   "test": "jest && eslint . && npm run size"
      }
    ```

6. If you don't have a continuous integration service running, don't forget
   to add one -�start with [Travis CI].

</details>


### Big Libraries

JS libraries > 10 kB in size.

This preset includes headless Chrome, and will measure your lib's execution
time. You likely don't need this overhead for a small 2 kB lib, but for larger
ones the execution time is a more accurate and understandable metric that
the size in bytes. Libraries like [React] are good examples for this preset.

<details><summary><b>Show instructions</b></summary>

1. Install preset:

    ```sh
    $ npm install --save-dev size-limit @size-limit/preset-big-lib
    ```

2. Add the `size-limit` section and the `size` script to your `package.json`:

    ```diff
    + "size-limit": [
    +   {
    +     "path": "dist/react.production-*.js"
    +   }
    + ],
      "scripts": {
        "build": "webpack ./scripts/rollup/build.js",
    +   "size": "npm run build && size-limit",
        "test": "jest && eslint ."
      }
    ```

3. If you use ES modules you can test the size after tree-shaking with `import`
   option:

    ```diff
      "size-limit": [
        {
          "path": "dist/react.production-*.js",
    +     "import": "{ createComponent }"
        }
      ],
    ```

4. Here's how you can get the size for your current project:

    ```sh
    $ npm run size

      Package size: 30.08 kB with all dependencies, minified and gzipped
      Loading time: 602 ms   on slow 3G
      Running time: 214 ms   on Snapdragon 410
      Total time:   815 ms
    ```

5. Now, let's set the limit. Add 25% to the current total time and use that
   as the limit in your `package.json`:

    ```diff
      "size-limit": [
        {
    +     "limit": "1 s",
          "path": "dist/react.production-*.js"
        }
      ],
    ```

6. Add a `size` script to your test suite:

    ```diff
      "scripts": {
        "build": "rollup ./scripts/rollup/build.js",
        "size": "npm run build && size-limit",
    -   "test": "jest && eslint ."
    +   "test": "jest && eslint . && npm run size"
      }
    ```

7. If you don't have a continuous integration service running, don't forget
   to add one -�start with [Travis CI].
8. Add the library size to docs, it will help users to choose your project:

    ```diff
      # Project Name

      Short project description

      * **Fast.** 10% faster than competitor.
    + * **Small.** 15 kB (minified and gzipped).
    +   [Size Limit](https://github.com/ai/size-limit) controls the size.
    ```

</details>


### Small Libraries

JS libraries < 10 kB in size.

This preset will only measure the size, without the execution time, so it's
suitable for small libraries. If your library is larger, you likely want
the Big Libraries preset above. [Nano�ID]�or�[Storeon]�are�good�examples
for this preset.

<details><summary><b>Show instructions</b></summary>

1. First, install `size-limit`:

    ```sh
    $ npm install --save-dev size-limit @size-limit/preset-small-lib
    ```

2. Add the `size-limit` section and the `size` script to your `package.json`:

    ```diff
    + "size-limit": [
    +   {
    +     "path": "index.js"
    +   }
    + ],
      "scripts": {
    +   "size": "size-limit",
        "test": "jest && eslint ."
      }
    ```

3. Here's how you can get the size for your current project:

    ```sh
    $ npm run size

      Package size: 177 B with all dependencies, minified and gzipped
    ```

4. If your project size starts to look bloated, run `--why` for analysis:

    ```sh
    $ npm run size -- --why
    ```

    > We use [Statoscope](https://github.com/statoscope/statoscope) as bundle analyzer.

6. Now, let's set the limit. Determine the current size of your library,
   add just a little bit (a kilobyte, maybe) and�use�that�as�the�limit
   in your `package.json`:

    ```diff
     "size-limit": [
        {
    +     "limit": "9 kB",
          "path": "index.js"
        }
     ],
    ```

7. Add the `size` script to your test suite:

    ```diff
      "scripts": {
        "size": "size-limit",
    -   "test": "jest && eslint ."
    +   "test": "jest && eslint . && npm run size"
      }
    ```

8. If you don't have a continuous integration service running, don't forget
   to add one -�start with [Travis CI].
9. Add the library size to docs, it will help users to choose your project:

    ```diff
      # Project Name

      Short project description

      * **Fast.** 10% faster than competitor.
    + * **Small.** 500 bytes (minified and gzipped). No�dependencies.
    +   [Size Limit](https://github.com/ai/size-limit) controls the size.
    ```

</details>

[Travis CI]: https://github.com/dwyl/learn-travis
[Storeon]: https://github.com/ai/storeon/
[Nano�ID]: https://github.com/ai/nanoid/
[React]: https://github.com/facebook/react/


## Reports

Size Limit has a [GitHub action] that comments and rejects pull requests based
on Size Limit output.

1. Install and configure Size Limit as shown above.
2. Add the following action inside `.github/workflows/size-limit.yml`

```yaml
name: "size"
on:
  pull_request:
    branches:
      - master
jobs:
  size:
    runs-on: ubuntu-latest
    env:
      CI_JOB_NUMBER: 1
    steps:
      - uses: actions/checkout@v1
      - uses: andresz1/size-limit-action@v1
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
```


## Config

### Plugins and Presets

Plugins or plugin presets will be loaded automatically from `package.json`.
For example, if you want to use `@size-limit/webpack`, you can just use
`npm install --save-dev @size-limit/webpack`, or you can use our preset
`@size-limit/preset-big-lib`.

Plugins:

* `@size-limit/file` checks the size of files with Gzip, Brotli
  or without compression.
* `@size-limit/webpack` adds your library to empty webpack project
  and prepares bundle file for `file` plugin.
* `@size-limit/webpack-why` adds reports for `webpack` plugin
  about your library is of this size to show the cost of all your
  dependencies.
* `@size-limit/webpack-css` adds css support for `webpack` plugin.
* `@size-limit/esbuild` is like `webpack` plugin, but uses `esbuild`
  to be faster and use less space in `node_modules`.
* `@size-limit/time` uses headless Chrome to track time to execute JS.
* `@size-limit/dual-publish` compiles files to ES modules with [`dual-publish`]
  to check size after tree-shaking.

Plugin presets:

* `@size-limit/preset-app` contains `file` and `time` plugins.
* `@size-limit/preset-big-lib` contains `webpack`, `file`, and `time` plugins.
* `@size-limit/preset-small-lib` contains `esbuild` and `file` plugins.

[`dual-publish`]: https://github.com/ai/dual-publish


#### Third-Party Plugins

Third-party plugins and presets named start with `size-limit-` are also supported.
For example:

* [`size-limit-node-esbuild`](https://github.com/un-ts/size-limit/tree/main/packages/node-esbuild)
  is like `@size-limit/esbuild` but for Node libraries.
* [`size-limit-preset-node-lib`](https://github.com/un-ts/size-limit/tree/main/packages/preset-node-lib)
  is like `@size-limit/preset-small-lib` but for Node libraries which contains
  above `node-esbuild` and core `file` plugins.


### Limits Config

Size Limits supports three ways to define limits config.

1. `size-limit` section in `package.json`:

   ```json
     "size-limit": [
       {
         "path": "index.js",
         "import": "{ createStore }",
         "limit": "500 ms"
       }
     ]
   ```

2. or a separate `.size-limit.json` config file:

   ```js
   [
     {
       "path": "index.js",
       "import": "{ createStore }",
       "limit": "500 ms"
     }
   ]
   ```

3. or a more flexible `.size-limit.js` or `.size-limit.cjs` config file:

   ```js
   module.exports = [
     {
       path: "index.js",
       import: "{ createStore }",
       limit: "500 ms"
     }
   ]
   ```

Each section in the config can have these options:

* **path**: relative paths to files. The only mandatory option.
  It could be a path `"index.js"`, a [pattern] `"dist/app-*.js"`
  or�an�array `["index.js", "dist/app-*.js", "!dist/app-exclude.js"]`.
* **import**: partial import to test tree-shaking. It could be `"{ lib }"`
  to test `import { lib } from 'lib'`, `*` to test all exports,
  or `{ "a.js": "{ a }", "b.js": "{ b }" }` to test multiple files.
* **limit**: size or time limit for files from the `path` option. It should be
  a string with a number and unit, separated by a space.
  Format: `100 B`, `10 kB`, `500 ms`, `1 s`.
* **name**: the name of the current section. It will only be useful
  if you have multiple sections.
* **entry**: when using a custom webpack config, a webpack entry could be given.
  It could be a string or an array of strings.
  By default, the total size of all entry points will be checked.
* **webpack**: with `false` it will disable webpack.
* **running**: with `false` it will disable calculating running time.
* **gzip**: with `false` it will disable gzip compression.
* **brotli**: with `true` it will use brotli compression and disable
  gzip compression.
* **config**: a path to a custom webpack config.
* **ignore**: an array of files and dependencies to exclude from
  the project size calculation.
* **modifyWebpackConfig**: (.size-limit.js only) function that can be used
  to do last-minute changes to the webpack config, like adding a plugin.
* **compareWith**: path to `stats.json` from another build to compare
  (when `--why` is using).
* **uiReports**: custom UI reports list (see [Statoscope docs]).

If you use Size Limit to track the size of CSS files, make sure to set
`webpack: false`. Otherwise, you will get wrong numbers, because webpack
inserts `style-loader` runtime (�2 kB) into the bundle.

[Statoscope docs]: https://github.com/statoscope/statoscope/tree/master/packages/webpack-plugin#optionsreports-report
[pattern]: https://github.com/sindresorhus/globby#globbing-patterns


## JS API

```js
const sizeLimit = require('size-limit')
const filePlugin = require('@size-limit/file')
const webpackPlugin = require('@size-limit/webpack')

sizeLimit([filePlugin, webpackPlugin], [filePath]).then(result => {
  result //=> { size: 12480 }
})
```