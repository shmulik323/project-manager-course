<template>
  <v-layout row justify-center>
    <v-dialog v-model="dialog" persistent max-width="600px">
      <template v-slot:activator="{ on }">
        <b-btn
          id="change_username"
          v-b-popover.hover.bottom="'Click me to edit your user name'"
          title="Edit User Name"
          v-on="on"
        >User-Name : {{olduser}}</b-btn>
      </template>
      <v-card class="mx-auto" style="max-width: 500px;">
        <v-system-bar>
          <v-spacer></v-spacer>
          <v-icon small>mdi-square</v-icon>
          <v-icon class="ml-1" small>mdi-circle</v-icon>
          <v-icon class="ml-1" small>mdi-triangle</v-icon>
        </v-system-bar>
        <v-toolbar cards flat>
          <v-btn icon>
            <v-icon>mdi-arrow-left</v-icon>
          </v-btn>
          <v-card-title class="title font-weight-regular">Change Username</v-card-title>
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
            id="email"
            v-model="email"
            :rules="[rules.email]"
            box
            color="deep-purple"
            label="Email address"
            type="email"
          ></v-text-field>
          <v-text-field
            id="old_user"
            v-model="olduser"
            :rules="[rules.required]"
            box
            color="deep-purple"
            label="Old User Name"
            type="user"
          ></v-text-field>
          <v-text-field
            id="new_user"
            v-model="newuser"
            :rules="[rules.required]"
            box
            color="deep-purple"
            label="New User Name"
            type="user"
          ></v-text-field>
        </v-form>
        <v-divider></v-divider>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            id="edit_info"
            @click="submit"
            :disabled="!form"
            class="white--text"
            color="blue accent-4"
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
  props: ["newuser", "olduser"],
  data: () => ({
    dialog: false,
    form: false,
    agreement: false,
    email: "",
    rules: {
      email: v => (v || "").match(/@/) || "Please enter a valid email",
      length: len => v =>
        (v || "").length >= len || `Invalid character length, required ${len}`,
      required: v => !!v || "This field is required"
    }
  }),
  methods: {
    async submit() {
      await this.$axios
        .post("api/change_username", {
          email: this.email,
          old: this.olduser,
          new: this.newuser
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
