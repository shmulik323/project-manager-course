<template>
  <v-card>
    <v-data-table next-icon :headers="headers" :items="pData.docs" :search="search">
      <template v-slot:items="props">
        <td>{{ props.item.title }}</td>
        <td id="type" class="text-xs-right">{{ props.item.applicationType }}</td>
        <td class="text-xs-right">{{ props.item.publicationDate }}</td>
        <td id="date" class="text-xs-right">{{ props.item.documentDate }}</td>
        <td class="text-xs-right">{{ props.item.applicant }}</td>
        <td class="text-xs-right">{{ props.item.inventor }}</td>
        <td class="text-xs-right">{{props.item.archiveUrl}}</td>
      </template>
      <template v-slot:no-results>
        <v-alert
          :value="true"
          color="error"
          icon="warning"
        >Your search for "{{ params.id }}" found no results.</v-alert>
      </template>
    </v-data-table>
    <v-btn to="/search">Back</v-btn>
  </v-card>
</template>
<script>
import axios from "axios";
export default {
  data() {
    return {
      search: "",

      headers: [
        {
          text: "Patent Name",
          align: "left",
          sortable: true,
          value: "title"
        },
        { text: "applicationType", value: "applicationType" },
        { text: "publicationDate", value: "publicationDate" },
        { text: "documentDate", value: "documentDate" },
        { text: "applicant", value: "applicant" },
        { text: "inventor", value: "inventor" },
        { text: "archiveUrl", value: "archiveUrl" }
      ]
    };
  },
  asyncData({ params }) {
    return axios
      .get(
        `https://developer.uspto.gov/ibd-api/v1/patent/application?searchText=${
          params.id
        }`
      )
      .then(response => {
        return { pData: response.data.response };
      });
  }
};
</script>
