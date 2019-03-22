<template>
  <v-app>
    <Navdrow/>
    <div class="container">
      <nuxt/>
      <Footer/>
    </div>
  </v-app>
</template>

<script>
import Navbar from "~/components/Navbar";
import Navdrow from "~/components/Navdrow";
import Footer from "~/components/Footer";

export default {
  components: {
    Navbar,
    Navdrow,
    Footer
  }
};
</script>
