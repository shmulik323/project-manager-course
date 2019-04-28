<template>
  <b-card title="Contact" sub-title="contact the site managers">
    <b-jumbotron bg-variant="denger" text-variant="white" border-variant="dark">
      <form>
        <v-text-field
          id="subject"
          v-model="subject"
          v-validate="'required'"
          :error-messages="errors.collect('subject')"
          label="subject"
          data-vv-name="subject"
          required
        ></v-text-field>
        <v-select
          id="select_manager"
          v-model="select"
          v-validate="'required'"
          :items="managers"
          :error-messages="errors.collect('select')"
          label="Select Manager"
          data-vv-name="select"
          required
        ></v-select>
        <v-textarea
          id="message"
          name="massege"
          v-validate="'required'"
          :error-messages="errors.collect('massege')"
          label="Massege"
          v-model="text"
          hint="here you can send a message to the developers of this site."
        ></v-textarea>
        <v-btn id="submit" @click="submit">submit</v-btn>

        <v-btn @click="clear">clear</v-btn>
      </form>
    </b-jumbotron>
  </b-card>
</template>

//<script>
// export default {
//   data () {
//     return{
//       title: 'The Managers',
//       managers:[
//    
//         {name:'Shmuel',speciality:'Admin',email:'shmuemo1@ac.sce.ac.il',show:false},
//       
//         {name:'Mishel',speciality:'Admin',email:'misheel@ac.sce.ac.il',show:false}
//       ]
//     }
//   },
// }
//
//</script>
<script>
import Vue from "vue";
import VeeValidate from "vee-validate";

Vue.use(VeeValidate);

export default {
  $_veeValidate: {
    validator: "new"
  },

  data: () => ({
    name: "",
    subject: "",
    text: "",
    user: null,
    select: null,
    managers: [
      "shmulik323@gmail.com",
      "misheel@ac.sce.ac.il"
    ],
    dictionary: {
      attributes: {
        email: "E-mail Address"
        // custom attributes
      },
      custom: {
        name: {
          required: () => "Name can not be empty",
          max: "The name field may not be greater than 20 characters"
          // custom messages
        },
        select: {
          required: "Select field is required"
        }
      }
    }
  }),

  mounted() {
    this.$validator.localize("en", this.dictionary);
  },

  methods: {
    submit() {
      this.$validator.validateAll();
      this.$axios.post("/api/Sent", {
        name: this.subject,
        dev: this.select,
        message: "message from:" + this.$auth.user.email + "\n" + this.text
      });
    },
    clear() {
      this.name = "";
      this.email = "";
      this.select = null;
      this.checkbox = null;
      this.text = null;
      this.$validator.reset();
    }
  }
};
</script>
<style scoped>
#programmers {
  width: 100%;
  max-width: 1200px;
  margin: 40px auto;
  padding: 0 20px;
  box-sizing: border-box;
}
ul {
  display: flex;
  flex-wrap: wrap;
  list-style-type: none;
  padding: 0;
}
li {
  flex-grow: 1;
  flex-basis: 300px;
  text-align: center;
  padding: 100px;
  border: 1px solid #222;
  margin: 10px;
}
header {
  background: lightgreen;
  padding: 10px;
}
h1 {
  color: #222;
  text-align: center;
}
</style>
