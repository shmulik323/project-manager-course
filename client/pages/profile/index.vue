<template>
  <div>
    <b-row>
      <b-col md="8">
        <b-card no-body class="overflow-hidden" style="max-width: 700px;">
          <b-row no-gutters>
            <b-col
              md="6"
              v-b-popover.hover.bottom="'Click me to edit profile pic'"
              title="profile pic"
            >
              <b-btn id="change_picture" variant="outline-primary" to="/picture">
                <img :src="src" alt>
              </b-btn>
            </b-col>
            <b-col md="6">
              <b-card-body title="Profile">
                <b-card-text>
                  <DialogNameLast :name="name" :last="last"/>
                </b-card-text>
                <b-card-text>
                  <DialogUsername :olduser="username"/>
                </b-card-text>
                <b-card-text>
                  <DialogEmail :oldemail="email"/>
                </b-card-text>
                <b-badge v-if="admin" variant="success">Admin</b-badge>
                <b-badge v-if="premium" variant="warning">Premium</b-badge>
              </b-card-body>
            </b-col>
          </b-row>
        </b-card>
      </b-col>
    </b-row>
    <hr>
    <b-btn-group>
      <b-btn v-b-popover.hover="'click me to logout!'" title="Logout" @click="$auth.logout()">Logout</b-btn>

      <nuxt-link id="reset_password" class="button" to="/password">Reset Password</nuxt-link>
      <nuxt-link v-if="premium" id="cancel_premium" class="button" to="/cancel">Cancel Premium</nuxt-link>
    </b-btn-group>
  </div>
</template>

<script>
import DialogNameLast from "~/components/dialog-name-last";
import DialogUsername from "~/components/dialog-username";
import DialogEmail from "~/components/dialog-email";

export default {
  components: {
    DialogNameLast,
    DialogUsername,
    DialogEmail
  },

  data() {
    return {
      name: null,
      last: null,
      username: null,
      email: null,
      admin: null,
      premium: null,
      src:
        "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"
    };
  },
  methods: {},
  computed: {
    state() {
      return JSON.stringify(this.$auth.$state, undefined, 2);
    }
  },
  async created() {
    let config = {
      // example url
      url: "api/uploader",
      method: "GET",
      responseType: "arraybuffer"
    };

    await this.$axios(config, { name: this.$auth.user.image_file }).then(
      response => {
        var bytes = new Uint8Array(response.data);
        var btoa = require("btoa");
        var binary = bytes.reduce(
          (data, b) => (data += String.fromCharCode(b)),
          ""
        );
        this.src = "data:image/jpeg;base64," + btoa(binary);
      }
    );
    this.$auth.fetchUser();
    this.username = this.$auth.user.user;
    this.name = this.$auth.user.name;
    this.last = this.$auth.user.last;
    this.email = this.$auth.user.email;
    this.admin = this.$auth.user.admin;
    this.premium = this.$auth.user.premium;
  },
  mounted() {}
};
</script>
