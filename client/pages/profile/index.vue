
<template>
  <section class="section">
    <v-layout>
      <v-flex xs12 sm6 offset-sm3>
        <v-card>
          <h2 class="title">My Profile</h2>
          <div class="content">
            <p>
              <strong>Username:</strong>
              {{ $auth.$state.user }}
            </p>
          </div>
        </v-card>
      </v-flex>
    </v-layout>
  </section>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  middleware: "auth",
  computed: {
    ...mapGetters(["loggedInUser"])
  }
};
</script>
