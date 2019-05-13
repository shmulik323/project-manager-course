<template>
  <v-layout row justify-center>
    <v-dialog v-model="dialog" persistent max-width="600px">
      <template v-slot:activator="{ on }">
        <b-btn
          id="change_profile"
          v-b-popover.hover.bottom="'Click me to edit your full name'"
          title="Edit Full Name"
          v-on="on"
        >Welcome Back : {{name}} {{last}}</b-btn>
      </template>
      <v-card class="mx-auto" style="max-width: 500px;">
        <v-system-bar color="deep-purple darken-4" dark>
          <v-spacer></v-spacer>
          <v-icon small>mdi-square</v-icon>
          <v-icon class="ml-1" small>mdi-circle</v-icon>
          <v-icon class="ml-1" small>mdi-triangle</v-icon>
        </v-system-bar>
        <v-toolbar color="deep-purple accent-4" cards dark flat>
          <v-btn icon>
            <v-icon>mdi-arrow-left</v-icon>
          </v-btn>
          <v-card-title class="title font-weight-regular">Change First-name and Last-name</v-card-title>
          <v-spacer></v-spacer>
          <v-btn icon>
            <v-icon>mdi-magnify</v-icon>
          </v-btn>
          <v-btn icon>
            <v-icon>mdi-dots-vertical</v-icon>
          </v-btn>
        </v-toolbar>
        <v-form ref="form" v-model="form" class="pa-3 pt-4">
          <v-text-field
            id="first"
            v-model="name"
            :rules="[rules.required]"
            box
            color="deep-purple"
            label="First Name"
            type="name"
          ></v-text-field>
          <v-text-field
            id="last"
            v-model="last"
            :rules="[rules.required]"
            box
            color="deep-purple"
            label="Last Name"
            type="name"
          ></v-text-field>
        </v-form>
        <v-divider></v-divider>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            id="submit"
            @click="submit"
            :disabled="!form"
            :loading="isLoading"
            class="white--text"
            color="deep-purple accent-4"
            depressed
          >Submit</v-btn>
          <v-btn flat @click="$refs.form.reset()">Clear</v-btn>
          <v-btn color="blue darken-1" flat @click="dialog = false">Close</v-btn>
        </v-card-actions>
        <v-dialog v-model="dialog" absolute max-width="400" persistent></v-dialog>
      </v-card>
    </v-dialog>
  </v-layout>
</template>
<script>
export default {
  props: ["name", "last"],
  data: () => ({
    dialog: false,
    agreement: false,
    name: "",
    last: "",
    dialog: false,
    email: null,
    form: false,
    isLoading: false,
    password: null,
    rules: {
      required: v => !!v || "This field is required"
    }
  }),
  methods: {
    async submit() {
      await this.$axios
        .post("api/edit_user", {
          name: this.name,
          last: this.last,
          email: this.$auth.user.email
        })
        .then(res => {})
        .then(e => {
          return this.$router.push("/profile");
        })
        .catch(e => {
          console.log(e);
        });
    }
  }
};
</script>
