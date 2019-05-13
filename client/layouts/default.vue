<template>
  <v-app>
    <Navdrow/>
    <div class="container">
      <v-container fluid>
        <v-fade-transition mode="out-in">
          <nuxt/>
        </v-fade-transition>
      </v-container>
      <div class="fixed-bottom">
        User status:
        <b-badge>{{ $auth.$state.loggedIn ? $auth.$state.user.user : 'Guest' }}</b-badge>
        <b-badge v-if="$auth.user.admin" variant="success">Admin</b-badge>
        <b-badge v-if="$auth.user.premium" variant="warning">Premium</b-badge>
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
