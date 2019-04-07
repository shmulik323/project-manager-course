<template>
  <section class="section">
    <v-layout>
      <v-flex xs12 sm6 offset-sm3>
        <v-card>
          <div class="columns">
            <div class="column is-4 is-offset-4">
              <h2 class="title has-text-centered">Register!</h2>

              <Notification :message="error" v-if="error"/>

              <form method="post" @submit.prevent="register">
                <div class="field">
                  <label class="label">profile pic</label>
                  <div class="control">
                    <picture-input
                      ref="pictureInput"
                      width="200"
                      height="200"
                      margin="8"
                      accept="image/jpeg, image/png"
                      size="10"
                      :removable="true"
                      :customStrings="{
        upload: '<h1>Bummer!</h1>',
        drag: 'Drag a image'
      }"
                    ></picture-input>
                  </div>
                </div>
                <div class="field">
                  <label class="label">First-name</label>
                  <div class="control">
                    <input type="fname" class="input" name="firstname" v-model="name" required>
                  </div>
                </div>

                <div class="field">
                  <label class="label">Last name</label>
                  <div class="control">
                    <input type="lastname" class="input" name="last" v-model="last" required>
                  </div>
                </div>
                <div class="field">
                  <label class="label">Username</label>
                  <div class="control">
                    <input type="text" class="input" name="username" v-model="username" required>
                  </div>
                </div>
                <div class="field">
                  <label class="label">Email</label>
                  <div class="control">
                    <input type="email" class="input" name="email" v-model="email" required>
                  </div>
                </div>
                <div class="field">
                  <label class="label">Password</label>
                  <div class="control">
                    <input
                      type="password"
                      class="input"
                      name="password"
                      v-model="password"
                      required
                    >
                  </div>
                </div>
                <div class="control">
                  <button type="submit" class="button is-dark is-fullwidth">Register</button>
                </div>
              </form>

              <div class="has-text-centered" style="margin-top: 20px">
                Already got an account?
                <nuxt-link to="/login">Login</nuxt-link>
              </div>
            </div>
          </div>
        </v-card>
      </v-flex>
    </v-layout>
  </section>
</template>

<script>
import Notification from "~/components/Notification";
import PictureInput from "vue-picture-input";

export default {
  middleware: "guest",
  components: {
    Notification,
    PictureInput
  },

  data() {
    return {
      username: "",
      name: "",
      last: "",
      email: "",
      password: "",
      error: null,
      selectedFile: null,
      file_name: null
    };
  },

  methods: {
    sendUploadToBackend(name, data) {
      const path = "http://localhost:5000/api/uploader";
      this.$axios.post(path, { name: name, data: data });
      console.log("tried code in sendUploadToBackend");
    },
    onChange(image) {
      console.log("New picture selected!");
      if (this.$refs.pictureInput.image) {
        this.file_name = this.$refs.pictureInput.file.name;
        console.log("Picture is loaded.");
        this.sendUploadToBackend(
          this.$refs.pictureInput.file.name,
          this.$refs.pictureInput.image
        );
      } else {
        console.log("FileReader API not supported: use the <form>, Luke!");
      }
    },
    async register() {
      this.onChange();
      try {
        await this.$axios.post("api/register", {
          name: this.name,
          last: this.last,
          username: this.username,
          email: this.email,
          password: this.password,
          image_file: this.file_name
        });

        await this.$auth.loginWith("local", {
          data: {
            email: this.email,
            password: this.password
          }
        });

        this.$router.push("/");
      } catch (e) {
        this.error = e.response.data.message;
      }
    }
  }
};
</script>
