<template>
  <div>
    <b-alert show variant="warning">This is a secure page!</b-alert>
    <b-row>
      <b-col md="8">
        <b-card no-body class="overflow-hidden" style="max-width: 700px;">
          <b-row no-gutters>
            <b-col md="6">
              <img :src="src" alt>
            </b-col>
            <b-col md="6">
              <b-card-body title="Profile">
                <b-card-text>
                  <h4>Hi:{{name}} {{last}}</h4>
                </b-card-text>
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
                  <v-chip color="blue" text-color="white">
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
                  <v-chip color="blue" text-color="white">
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
  methods: {
    getProfilePic() {
      this.$axios
        .get("api/uploader", {
          name: this.$auth.user.image_file
        })
        .then((req, res) => {
          var myBuffer = yourFunctionReturnsBuffer();
          res.writeHead(200, {
            "Content-Type": "image/jpeg",
            "Content-Length": myBuffer.length
          });
          res.end(myBuffer);
        });
    }
  },
  computed: {
    state() {
      return JSON.stringify(this.$auth.$state, undefined, 2);
    }
  },
  created() {
    let config = {
      // example url
      url: "api/uploader",
      method: "GET",
      responseType: "arraybuffer"
    };
    this.$axios(config, { name: this.$auth.user.image_file }).then(response => {
      var bytes = new Uint8Array(response.data);
      var binary = bytes.reduce(
        (data, b) => (data += String.fromCharCode(b)),
        ""
      );
      this.src = "data:image/jpeg;base64," + btoa(binary);
    });
    this.$auth.fetchUser();
    this.username = this.$auth.user.user;
    this.name = this.$auth.user.name;
    this.last = this.$auth.user.last;
    this.email = this.$auth.user.email;
    this.admin = this.$auth.user.admin;
    this.premium = this.$auth.user.premium;
    this.imgUrl = this.getProfilePic();
  }
};
</script>
