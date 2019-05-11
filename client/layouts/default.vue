<template>
  <v-app>
    <Navdrow/>
    <div class="container">
      <nuxt/>
      <div class="fixed-bottom">
        User status:
        <b-badge>{{ $auth.$state.loggedIn ? $auth.$state.user.user : 'Guest' }}</b-badge>
      </div>
    </div>
  </v-app>
</template>

<script>
import Navdrow from "~/components/Navdrow";

export default {
  components: {
    Navdrow
  }
};
</script>
