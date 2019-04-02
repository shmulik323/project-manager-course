<template>
  <div>
    <b-alert show variant="warning">This is a secure page!</b-alert>
    <b-row>
      <b-col md="8">
        <b-card no-body class="overflow-hidden" style="max-width: 540px;">
          <b-row no-gutters>
            <b-col md="6">
              <b-card-img src="https://picsum.photos/400/400/?image=20" class="rounded-0"></b-card-img>
            </b-col>
            <b-col md="6">
              <b-card-body title="Profile">
                <b-card-text>
                  <v-chip color="indigo" text-color="white">
                    <v-avatar>
                      <v-icon>account_circle</v-icon>
                    </v-avatar>
                    <h4>username:</h4>
                    {{ username }}
                  </v-chip>
                </b-card-text>
                <b-card-text>
                  <v-chip color="indigo" text-color="white">
                    <v-avatar>
                      <v-icon>account_circle</v-icon>
                    </v-avatar>
                    <h4>email:</h4>
                    {{ email }}
                  </v-chip>
                </b-card-text>
                <b-card-text v-if="admin">
                  <v-chip color="indigo" text-color="white">
                    <v-avatar>
                      <v-icon>account_circle</v-icon>
                    </v-avatar>
                    <h4>admin:</h4>
                    {{ admin }}
                  </v-chip>
                </b-card-text>
                <b-card-text v-if="premium">
                  <v-chip color="indigo" text-color="white">
                    <v-avatar>
                      <v-icon>account_circle</v-icon>
                    </v-avatar>
                    <h4>premium:</h4>
                    {{ premium }}
                  </v-chip>
                </b-card-text>
              </b-card-body>
            </b-col>
          </b-row>
        </b-card>
      </b-col>
    </b-row>
    <hr>
    <b-btn-group>
      <b-button @click="$auth.fetchUser()">Fetch User</b-button>
      <b-button @click="$auth.logout()">Logout</b-button>
    </b-btn-group>
  </div>
</template>

<script>
export default {
  middleware: ["auth"],
  data() {
    return {
      username: null,
      email: null,
      admin: null,
      premium: null
    };
  },
  computed: {
    state() {
      return JSON.stringify(this.$auth.$state, undefined, 2);
    }
  },
  created() {
    this.$auth.fetchUser();
    this.username = this.$auth.user.user;
    this.email = this.$auth.user.email;
    this.admin = this.$auth.user.admin;
    this.premium = this.$auth.user.premium;
  }
};
</script>
