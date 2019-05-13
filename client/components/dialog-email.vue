<template>
  <v-layout row justify-center>
    <v-dialog v-model="dialog" persistent max-width="600px">
      <template v-slot:activator="{ on }">
        <b-btn
          id="change_email"
          v-b-popover.hover.bottom="'Click me to edit your email'"
          title="Edit Email"
          v-on="on"
        >Email : {{newemail}}</b-btn>
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
          <v-card-title class="title font-weight-regular">Change Email</v-card-title>
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
            id="old_email"
            v-model="oldemail"
            box
            color="deep-purple"
            label="Old Email address"
            type="email"
          ></v-text-field>
          <v-text-field
            id="new_email"
            v-model="newemail"
            box
            color="deep-purple"
            label="New Email address"
            type="email"
          ></v-text-field>
        </v-form>
        <v-divider></v-divider>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            id="submit"
            @click="submit"
            :disabled="!form"
            class="white--text"
            color="deep-purple accent-4"
            depressed
          >Submit</v-btn>
          <v-btn flat @click="$refs.form.reset()">Clear</v-btn>
          <v-btn color="blue darken-1" flat @click="dialog = false">Close</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-layout>
</template>
<script>
export default {
  props: ["oldemail", "newemail"],
  data: () => ({
    dialog: false,
    form: false,
    rules: {
      email: v => (v || "").match(/@/) || "Please enter a valid email",
      required: v => !!v || "This field is required"
    }
  }),
  methods: {
    async submit() {
      await this.$axios
        .post("api/edit_email", {
          old: this.oldemail,
          new: this.newemail
        })
        .then(e => {
          this.dialog = !this.dialog;
        })
        .catch(e => {
          console.log(e);
        });
    }
  }
};
</script>
