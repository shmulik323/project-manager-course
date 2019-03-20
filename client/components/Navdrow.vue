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
        <router-link to="/" tag="span" style="cursor: pointer">Development Forms</router-link>
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-toolbar-items>
        <template v-if="isAuthenticated">
          <a class="navbar-item" @click="logout">Logout</a>
        </template>
        <template v-else>
          <router-link class="navbar-item" to="/register">Register</router-link>
          <router-link class="navbar-item" to="/login">Log In</router-link>
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
        { icon: "person", title: "Profile", link: "/profile" }
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
