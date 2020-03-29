<template>
  <q-page class="flex flex-center">
    <div>
      <div class="row no-wrap q-mb-md q-mt-sm">
        <div class="gibe-border full-width">Search</div>
        <q-btn class="bg-green-6 text-white" label="Browse Visitors"
          :class="{ hidden: !showVisitors }"
          v-on:click=" showVisitors = !showVisitors " />
        <q-btn class="bg-green-6 text-white" label="Browse Personnel"
          :class="{ hidden: showVisitors }"
          v-on:click=" showVisitors = !showVisitors " />
      </div>
      <person-card id="personnel" :personnel="personnel"
        :class="{ hidden: !showVisitors }" />
      <person-card id="visitors" :personnel="visitors"
        :class="{ hidden: showVisitors }" />
    </div>
  </q-page>
</template>

<style>
</style>

<script>
import axios from 'axios';
import PersonCard from './components/PersonCard';

export default {
  name: 'Personnel',
  data() {
    return {
      showVisitors: true,
      personnel: [],
      visitors: [],
    };
  },

  mounted() {
    axios.get('/personnel', {
      params: {
        visitors: false,
      },
    })
      .then((res) => {
        const personnel = res.data;

        this.personnel = personnel.map(person => (
          { ...person, expanded: false }
        ));
      })
      .catch((err) => {
        console.log(err);
      });

    axios.get('/personnel', {
      params: {
        visitors: true,
      },
    })
      .then((res) => {
        const visitors = res.data;

        this.visitors = visitors.map(person => (
          { ...person, expanded: false }
        ));
      })
      .catch((err) => {
        console.log(err);
      });
  },

  components: {
    PersonCard,
  },
};
</script>
