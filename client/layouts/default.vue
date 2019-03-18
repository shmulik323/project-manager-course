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
