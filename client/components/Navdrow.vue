<template>
  <div>
    <v-navigation-drawer temporary absolute v-model="sideNav">
      <v-list v-if="isAuthenticated">
        <v-list-tile v-for="item in menuItems" :key="item.title" :to="item.link">
          <v-list-tile-action>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-tile-action>
          <v-list-tile-content>{{ item.title }}</v-list-tile-content>
        </v-list-tile>
      </v-list>
    </v-navigation-drawer>

    <v-toolbar dark class="primary">
      <v-toolbar-side-icon @click.stop="sideNav = !sideNav"></v-toolbar-side-icon>
      <v-toolbar-title>
        <nuxt-link to="/" tag="span" style="cursor: pointer">Development Forms</nuxt-link>
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-toolbar-items>
        <template v-if="isAuthenticated">
          <b-btn variant="danger" class="navbar-item" @click="logout">Logout</b-btn>
        </template>
        <template v-else>
          <b-btn variant="success" class="navbar-item" @click="$router.push('/register')">Register</b-btn>
          <b-btn variant="info" class="navbar-item" @click="$router.push('/login')">Login</b-btn>
        </template>
      </v-toolbar-items>
    </v-toolbar>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
export default {
  data() {
    return {
      sideNav: false,
      menuItems: [
        { icon: "room", title: "create", link: "/create" },
        { icon: "fingerprint", title: "Profile", link: "/secure" }
      ]
    };
  },
  methods: {
    async logout() {
      await this.$auth.logout();
    }
  },
  computed: {
    ...mapGetters(["isAuthenticated", "loggedInUser"])
  }
};
</script>
