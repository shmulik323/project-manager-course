<template>
  <div>
    <v-stepper v-model="e6" vertical>
      <v-stepper-step :complete="e6 > 1" step="1">
        Select an app
        <small>
          <v-expansion-panel>
            <v-expansion-panel-content>
              <template v-slot:header>
                <div>need help?</div>
              </template>
              <v-card>
                <v-card-text>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</v-card-text>
              </v-card>
            </v-expansion-panel-content>
          </v-expansion-panel>
        </small>
      </v-stepper-step>

      <v-stepper-content step="1">
        <v-card color="grey lighten-1" class="mb-5" height="200px">
          <v-flex height="200px">
            <v-textarea
              solo
              name="input-7-4"
              label="Solo textarea"
              value="The Woodman set to work at once, and so sharp was his axe that the tree was soon chopped nearly through."
            ></v-textarea>
          </v-flex>
        </v-card>
        <v-btn color="primary" @click="e6 = 2">Continue</v-btn>
        <v-btn flat @click="$router.go('-1')">back</v-btn>
      </v-stepper-content>

      <v-stepper-step :complete="e6 > 2" step="2">Configure analytics for this app</v-stepper-step>

      <v-stepper-content step="2">
        <v-card color="grey lighten-1" class="mb-5" height="200px">
          <v-flex height="200px">
            <v-textarea
              solo
              name="input-7-4"
              label="Solo textarea"
              value="The Woodman set to work at once, and so sharp was his axe that the tree was soon chopped nearly through."
            ></v-textarea>
          </v-flex>
        </v-card>
        <v-btn color="primary" @click="e6 = 3">Continue</v-btn>
        <v-btn flat @click="e6 -=1">back</v-btn>
      </v-stepper-content>

      <v-stepper-step :complete="e6 > 3" step="3">Select an ad format and name ad unit</v-stepper-step>

      <v-stepper-content step="3">
        <v-card color="grey lighten-1" class="mb-5" height="200px">
          <v-flex height="200px">
            <v-textarea
              solo
              name="input-7-4"
              label="Solo textarea"
              value="The Woodman set to work at once, and so sharp was his axe that the tree was soon chopped nearly through."
            ></v-textarea>
          </v-flex>
        </v-card>
        <v-btn color="primary" @click="e6 = 4">Continue</v-btn>
        <v-btn flat @click="e6 -=1">back</v-btn>
      </v-stepper-content>

      <v-stepper-step step="4">View setup instructions</v-stepper-step>
      <v-stepper-content step="4">
        <v-card color="grey lighten-1" class="mb-5" height="200px">
          <v-flex height="200px">
            <v-textarea
              solo
              name="input-7-4"
              label="Solo textarea"
              value="The Woodman set to work at once, and so sharp was his axe that the tree was soon chopped nearly through."
            ></v-textarea>
          </v-flex>
        </v-card>
        <v-btn color="primary" @click="e6 = 1">Continue</v-btn>
        <v-btn flat @click="e6 -=1">back</v-btn>
      </v-stepper-content>
    </v-stepper>
    <v-btn>Submit</v-btn>
  </div>
</template>

<script>
export default {
  data() {
    return {
      e6: 1
    };
  }
};
</script>
