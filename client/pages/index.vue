<template>
  <div>
    <v-carousel>
      <v-carousel-item
        v-for="(item,i) in items"
        :key="i"
        :src="item.src"
        reverse-transition="fade"
        transition="fade"
      >
        <div class="text-xs-center">
          <h1 class="blue--text">{{item.text}}</h1>
        </div>
      </v-carousel-item>
    </v-carousel>
    <b-jumbotron v-if="!$auth.$state.loggedIn" class="text-center">
      <h3>Why working so hard? try the new tool to create your developments forms</h3>
      <b-btn variant="success" to="/register">Click here to Register!</b-btn>
    </b-jumbotron>
    <br>
    <br>
    <div role="tablist">
      <b-card no-body class="mb-1">
        <b-card-header header-tag="header" class="p-1" role="tab">
          <b-button block href="#" v-b-toggle.accordion-1 variant="info">What can you do here?</b-button>
        </b-card-header>
        <b-collapse id="accordion-1" visible accordion="my-accordion" role="tabpanel">
          <b-card-body>
            <b-card-text>
              you can
              <code>create</code> a
              <code>specification form</code>
              for your new project
            </b-card-text>
            <b-card-text>{{ text }}</b-card-text>
          </b-card-body>
        </b-collapse>
      </b-card>
    </div>
  </div>
</template>

<script>
export default {
  auth: false,
  data() {
    return {
      items: [
        {
          src: "https://media.giphy.com/media/3oFzlVgIEJ3UIEL7k4/giphy.gif",
          text:
            "are you tired of filling a lot of papers for absolutely nothing "
        },
        {
          src: "https://media.giphy.com/media/jLK74MUW07RaU/giphy.gif",
          text: "are you tired of typing the same text over and over again "
        },
        {
          src:
            "https://media.giphy.com/media/ktcUyw6mBlMVa/giphy-downsized.gif",
          text: "are you tired of wanting to throw your f**** computer "
        },
        {
          src: "https://media.giphy.com/media/k10R0bgUhNMtO/giphy.gif",
          text: "throw it away and register to this site"
        }
      ],
      text: `
            you can also search for your idea in the patent database before you start the project :)
        `
    };
  }
};
</script>
<style slot-scope lang="stylus">
#example-custom-transition {
  .fade {
    &-enter-active, &-leave-active, &-leave-to {
      transition: 0.3s ease-out;
      position: absolute;
      top: 0;
      left: 0;
    }

    &-enter, &-leave, &-leave-to {
      opacity: 0;
    }
  }
}

h1 {
  color: white;
  text-shadow: 1px 1px 2px black, 0 0 25px blue, 0 0 5px darkblue;
}
</style>
