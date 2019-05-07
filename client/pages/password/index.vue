<template>
  <v-card
    class="mx-auto"
    style="max-width: 500px;"
  >
    <v-system-bar
      color="deep-purple darken-4"
      dark
    >
      <v-spacer></v-spacer>
      <v-icon small>mdi-square</v-icon>
      <v-icon
        class="ml-1"
        small
      >mdi-circle</v-icon>
      <v-icon
        class="ml-1"
        small
      >mdi-triangle</v-icon>
    </v-system-bar>
    <v-toolbar
      color="deep-purple accent-4"
      cards
      dark
      flat
    >
      <v-btn icon>
        <v-icon>mdi-arrow-left</v-icon>
      </v-btn>
      <v-card-title class="title font-weight-regular">Reset Password</v-card-title>
      <v-spacer></v-spacer>
      <v-btn icon>
        <v-icon>mdi-magnify</v-icon>
      </v-btn>
      <v-btn icon>
        <v-icon>mdi-dots-vertical</v-icon>
      </v-btn>
    </v-toolbar>
    <v-form
      ref="form"
      v-model="form"
      class="pa-3 pt-4"
    >
      <v-text-field
        id="old_pass"
        v-model="oldpassword"
        :rules="[rules.password, rules.length(4)]"
        box
        color="deep-purple"
        counter="4"
        label="Old Password"
        style="min-height: 96px"
        type="password"
      ></v-text-field>
      <v-text-field
        id="new_pass"
        v-model="newpassword"
        :rules="[rules.password, rules.length(4)]"
        box
        color="deep-purple"
        counter="4"
        label="New Password"
        style="min-height: 96px"
        type="password"
      ></v-text-field>
      <v-text-field
        id="email"
        v-model="email"
        :rules="[rules.email]"
        box
        color="deep-purple"
        label="Email address"
        type="email"
      ></v-text-field>
    </v-form>
    <v-divider></v-divider>
    <v-card-actions>
      <v-btn
        flat
        @click="$refs.form.reset()"
      >
        Clear
      </v-btn>
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
    </v-card-actions>
    <v-dialog
      v-model="dialog"
      absolute
      max-width="400"
      persistent
    >
    </v-dialog>
  </v-card>
</template>

<script>
  export default {
    data: () => ({
      old:"",
      new:"",
      email:"",
      rules: {
        email: v => (v || '').match(/@/) || 'Please enter a valid email',
        length: len => v => (v || '').length >= len || `Invalid character length, required ${len}`,
        password: v => 4,
        required: v => !!v || 'This field is required'
      }
    }),
    methods:{
      async submit(){
        await this.$axios.post("api/reset",{
          old:this.oldpassword,
          new:this.newpassword,
          email:this.email
        })
        .then(res=>{})
        .catch(e=>{
          console.log(e);
        });        
      }
    }
  }
</script>