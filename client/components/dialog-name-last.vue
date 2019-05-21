<template>
  <v-layout row justify-center>
    <b-toast id="my-toast" :variant="varient" solid>
      <div slot="toast-title" class="d-flex flex-grow-1 align-items-baseline">
        <strong class="mr-auto">Massege!</strong>
      </div>
      {{massege}}
    </b-toast>
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
            id="edit_names"
            @click="submit"
            :disabled="!form"
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
    form: false,
    email: null,
    form: false,
    isLoading: false,
    password: null,
    massege: "",
    varient: "",
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

        .then(e => {
          this.dialog = !this.dialog;
          this.varient = "success";
          this.massege = "The new name is:" + this.name + " " + this.last;
          this.$bvToast.show("my-toast");
        })
        .catch(e => {
          this.massege = e;
          this.dialog = !this.dialog;
          this.varient = "warning";

          this.$bvToast.show("my-toast");
        });
    }
  }
};
</script>
