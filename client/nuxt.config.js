const pkg = require('./package')

const webpack = require("webpack")
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
        content: "width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no, minimal-ui"
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
        href: 'https://fonts.googleapis.com/css?family=Roboto:100,300,400,500,700,900|Material+Icons'
      },
      {
        rel: 'stylesheet',
        href: 'https://cdnjs.cloudflare.com/ajax/libs/bulma/0.7.1/css/bulma.min.css'
      },

    ]
  },

  /*
   ** Customize the progress-bar color
   */
  loading: {
    color: '#0077ff',
    height: '5px'

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
      src: '@/plugins/vue-picture-input.js',
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
    vendor: ['jsPDF'],
    transpile: ['vuetify/lib'],
    plugins: [new VuetifyLoaderPlugin(), new webpack.ProvidePlugin({
      'window.Quill': 'quill/dist/quill.js',
      'Quill': 'quill/dist/quill.js'
    })],

    loaders: {
      stylus: {
        import: ["~assets/style/variables.styl"]
      }
    },


    /*
     ** You can extend webpack config here
     */

    extend(config, ctx) {
      config.node = {
        fs: 'empty'
      }
    }
  }
}
