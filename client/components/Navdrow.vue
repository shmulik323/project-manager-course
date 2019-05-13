<template>
  <div>
    <v-navigation-drawer temporary absolute v-model="sideNav">
      <v-list v-if="isAuthenticated">
        <v-list-tile v-for="item in menuItems" :key="item.title" :to="item.link">
          <v-list-tile-action>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-tile-action>
          <v-list-tile-content>
            <h5>{{ item.title }}</h5>
          </v-list-tile-content>
        </v-list-tile>
      </v-list>
    </v-navigation-drawer>

    <v-toolbar dark class="primary lighten-2">
      <v-toolbar-side-icon @click.stop="sideNav = !sideNav"></v-toolbar-side-icon>
      <v-toolbar-title>
        <nuxt-link to="/" tag="span" style="cursor: pointer">Development Forms</nuxt-link>
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-toolbar-items>
        <template v-if="isAuthenticated">
          <b-btn
            variant="success"
            id="success"
            @click="$router.push('/profile')"
          >Hi {{$auth.user.name}}!</b-btn>
          <b-btn
            variant="danger"
            id="logout"
            v-b-modal.modal-prevent-closing
            class="navbar-item"
          >Logout</b-btn>
          <b-btn
            v-if="$auth.user.admin"
            variant="primary"
            id="admin"
            href="http://127.0.0.1:5000/admin"
            class="navbar"
          >Admin</b-btn>
        </template>
        <template v-else>
          <b-btn
            variant="success"
            id="register"
            class="navbar-item"
            @click="$router.push('/register')"
          >Register</b-btn>
          <b-btn
            variant="info"
            id="login_link"
            class="navbar-item"
            @click="$router.push('/login')"
          >Login</b-btn>
        </template>
      </v-toolbar-items>
    </v-toolbar>
    <b-modal id="modal-prevent-closing" ref="modal" title="are you sure?" @ok="logout">
      <h1>you will be logged out!</h1>
    </b-modal>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
export default {
  data() {
    return {
      sideNav: false,
      menuItems: [
        { icon: "create", title: "Create form", link: "/create" },
        { icon: "fingerprint", title: "Profile", link: "/profile" },
        { icon: "email", title: "Contact", link: "/contact" },
        { icon: "email", title: "Contact Manager", link: "/contact_manager" },
        { icon: "search", title: "Patent search", link: "/search" }
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
