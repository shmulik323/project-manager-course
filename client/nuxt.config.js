const pkg = require('./package')

const CKEditorWebpackPlugin = require("@ckeditor/ckeditor5-dev-webpack-plugin")
const CKEditorStyles = require("@ckeditor/ckeditor5-dev-utils").styles
const VuetifyLoaderPlugin = require('vuetify-loader/lib/plugin')

module.exports = {
  mode: 'universal',

  /*
   ** Headers of the page
   */
  head: {
    title: pkg.name,

    meta: [{
        charset: 'utf-8'
      },
      {
        name: 'viewport',
        content: 'width=device-width, initial-scale=1'
      },
      {
        hid: 'description',
        name: 'description',
        content: pkg.description
      }
    ],

    link: [{
        rel: 'icon',
        type: 'image/x-icon',
        href: '/favicon.ico'
      },
      {
        rel: 'stylesheet',
        href: 'https://fonts.googleapis.com/css?family=Roboto:300,400,500,700,900|Material+Icons'
      }, {
        rel: 'stylesheet',
        href: 'https://cdnjs.cloudflare.com/ajax/libs/bulma/0.7.1/css/bulma.min.css'
      }
    ]
  },

  /*
   ** Customize the progress-bar color
   */
  loading: {
    color: '#fff'
  },

  /*
   ** Global CSS
   */
  css: [
    'quill/dist/quill.snow.css',
    'quill/dist/quill.bubble.css',
    'quill/dist/quill.core.css',
    '~/assets/style/app.styl'
  ],

  /*
   ** Plugins to load before mounting the App
   */
  plugins: [
    '@/plugins/vuetify',
    {
      src: '@/plugins/quill.js',
      ssr: false
    },
    {
      src: '@/plugins/ckeditor.js',
      ssr: false
    }


  ],
  router: {
    middleware: ['auth']
  },
  /*
   ** Nuxt.js modules
   */
  modules: [
    '@nuxtjs/vendor',
    '@nuxtjs/axios',
    '@nuxtjs/auth',
    '@nuxtjs/proxy',
    'bootstrap-vue/nuxt'
  ],
  axios: {
    baseURL: 'http://127.0.0.1:5000',
    proxy: true
  },
  proxy: {
    '/api': 'http://127.0.0.1:5000',
  },
  auth: {
    redirect: {
      callback: '/callback'
    },
    strategies: {
      local: {
        endpoints: {
          login: {
            method: 'post',
            dataType: 'json',
            propertyName: 'token'
          }
        }
      },
      auth0: {
        domain: 'nuxt-auth.auth0.com',
        client_id: 'q8lDHfBLJ-Fsziu7bf351OcYQAIe3UJv'
      },
      facebook: {
        client_id: '1671464192946675',
        userinfo_endpoint: 'https://graph.facebook.com/v2.12/me?fields=about,name,picture{url},email,birthday',
        scope: ['public_profile', 'email', 'user_birthday']
      },
      google: {
        client_id: '956748748298-kr2t08kdbjq3ke18m3vkl6k843mra1cg.apps.googleusercontent.com'
      },

      twitter: {
        client_id: 'FAJNuxjMTicff6ciDKLiZ4t0D'
      },
    }
  },
  vendor: ['ckeditor'],
  /*
   ** Build configuration
   */
  build: {
    vendor: ['jsPDF', 'ckeditor'],
    transpile: ['vuetify/lib'],
    plugins: [new VuetifyLoaderPlugin(), new CKEditorWebpackPlugin({
      language: "en"
    })],
    postcss: CKEditorStyles.getPostCssConfig({
      themeImporter: {
        themePath: require.resolve("@ckeditor/ckeditor5-theme-lark")
      },
      minify: true
    }),
    loaders: {
      stylus: {
        import: ["~assets/style/variables.styl"]
      }
    },


    /*
     ** You can extend webpack config here
     */

    extend(config, ctx) {
      const filesRuleIndex = config.module.rules.findIndex(item => {
        return `${item.test}` == "/\\.(png|jpe?g|gif|svg|webp)$/"
      })
      if (filesRuleIndex !== -1) {
        config.module.rules[filesRuleIndex].test = /\.(png|jpe?g|gif|webp)$/
        const svgRule = config.module.rules[filesRuleIndex]
        svgRule.test = /\.svg/
        svgRule.exclude = svgRule.exclude || []
        svgRule.exclude.push(__dirname + "/node_modules/@ckeditor")
        config.module.rules.push(svgRule)
      }
      // Vue CLI would normally use its own loader to load .svg files. The icons used by
      // CKEditor should be loaded using raw-loader instead.
      config.module.rules.push({
        test: /ckeditor5-[^/\\]+[/\\]theme[/\\]icons[/\\][^/\\]+\.svg$/,
        use: ["raw-loader"]
      }), config.node = {
        fs: 'empty'
      }
    }
  }
}
