<<<<<<< HEAD
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
=======
<template>
  <v-app>
    <Navdrow/>
    <div class="container">
      <nuxt/>
    </div>
  </v-app>
</template>

<script>
import Navbar from "~/components/Navbar";
import Navdrow from "~/components/Navdrow";

export default {
  components: {
    Navbar,
    Navdrow
  }
};
</script>
>>>>>>> 8d674cb22c805223e9046c5b6b65d5c892190353
