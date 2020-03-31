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
      <person-card id="personnel"
        :personnel="personnel"
        :types="types"
        :genders="genders"
        :class="{ hidden: !showVisitors }" />
      <person-card id="visitors"
        :personnel="visitors"
        :types="types"
        :genders="genders"
        :class="{ hidden: showVisitors }" />
    </div>
  </q-page>
</template>

<style>
</style>

<script>
import axios from 'axios';
import PersonCard from './components/PersonCard';
import { ParseDate } from '../../utils/StringUtils';

export default {
  name: 'Personnel',
  data() {
    return {
      showVisitors: true,
      personnel: [],
      visitors: [],
      types: {},
      genders: {},
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

        this.personnel = personnel.map((person) => {
          const parsedBirthday = ParseDate(person.birthday);
          person.birthday = parsedBirthday;
          const parsedVisitors = { ...person, expanded: false, editMode: false };

          return parsedVisitors;
        });
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

        this.visitors = visitors.map((person) => {
          const parsedBirthday = ParseDate(person.birthday);
          person.birthday = parsedBirthday;
          const parsedVisitors = { ...person, expanded: false, editMode: false };

          return parsedVisitors;
        });
      })
      .catch((err) => {
        console.log(err);
      });

    axios.get('/persontypes')
      .then((res) => {
        this.types = res.data;
      })
      .catch((err) => {
        console.log(err);
      });

    axios.get('/genders')
      .then((res) => {
        this.genders = res.data;
      })
      .catch((err) => {
        console.log(err);
      });
  },

  methods: {
    ParseDate,
  },

  components: {
    PersonCard,
  },
};
</script>
