<template>
  <div v-if="personnel.length > 0">

    <q-card
      flat
      class="person-card text-grey-10 q-mb-xs"
      v-for="person in personnel" :key="person.id"
    >
      <div class="row items-center no-wrap bg-green-3">

        <q-avatar size="80px" class="q-ma-xs">
          <img :src="person.image">
        </q-avatar>

        <div class="column fit q-ml-sm">

          <div class="row justify-between text-weight-bold">
            <div>{{ ParseName(
              person.first_name,
              person.middle_name,
              person.last_name
            ) }}</div>
            <div>
              {{ CapitalizeFirstLetter(person.person_type.type_name) }}
            </div>
          </div>

          <div class="text-caption text-justify q-mt-xs">
            Occupation: {{ person.occupation }}
          </div>

        </div>

        <q-card-actions
          class="side-button self-stretch no-padding q-ml-xs"
        >
          <q-btn
            class="self-stretch bg-green-6 text-white"
            unelevated
            :icon="person.expanded ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
            @click="person.expanded = !person.expanded" >
            <q-tooltip>Details</q-tooltip>
          </q-btn>
        </q-card-actions>

      </div>

      <q-slide-transition>

        <div v-show="person.expanded">

          <q-separator />

          <div class="row no-wrap text-body2 bg-green-1">
            <q-card-section class="fit q-mt-xs">
              <div>Institution: {{ person.institution }}</div>

              <div class="row no-wrap q-mt-sm">
                <div class="column full-width justify-between">
                  <div>Birthday: {{ person.birthday }}</div>
                  <div class="q-mt-sm">
                    Gender: {{ CapitalizeFirstLetter(
                      person.person_gender.gender_name
                    ) }}
                  </div>
                </div>

                <div class="column full-width justify-between">
                  <div>Phone: {{ person.phone }}</div>
                  <div class="q-mt-sm">Email: {{ person.email }}</div>
                </div>
              </div>

            </q-card-section>

            <div class="column no-wrap no-padding q-ml-xs">
              <q-btn
                class="side-button full-height"
                color="green-6"
                flat
                unelevated
                :icon="person.editMode ? 'cancel' : 'edit'"
                @click="person.editMode = !person.editMode"
              >
                <q-tooltip>Edit</q-tooltip>
              </q-btn>

              <q-btn
                class="side-button full-height"
                flat
                unelevated
                color="green-6"
                icon="open_in_browser"
                @click="logDate(person.birthday)"
              >
                <q-tooltip>Full view</q-tooltip>
              </q-btn>

            </div>
          </div>

          <q-slide-transition v-show="person.editMode">
            <PersonEdit
              class="q-mb-md q-mt-sm"
              :person="person"
              :types="types"
              :genders="genders"
            />
          </q-slide-transition>

        </div>
      </q-slide-transition>
    </q-card>

  </div>

  <div v-else class="person-card row items-center no-wrap bg-green-3"
    style="height: 90px;" >
    <div class="full-width flex justify-center">
      <q-spinner-oval
        color="green-8"
        size="3em"
      />
    </div>
    <q-btn
      class="side-button self-stretch bg-green-6 text-white"
      unelevated
      disabled
      icon="keyboard_arrow_down"
     >
    </q-btn>
  </div>
</template>

<script>
import PersonEdit from './PersonEdit';
import {
  ParseName,
  CapitalizeFirstLetter,
  DateToUnix,
} from '../../../utils/StringUtils';

export default {
  name: 'PersonCard',

  props: {
    personnel: Array,
    types: Object,
    genders: Object,
  },

  methods: {
    ParseName,
    DateToUnix,
    CapitalizeFirstLetter,
    logDate(date) {
      // console.log('person.birthday is:');
      // console.log(date);
      // console.log('Calling DateToUnix...');
      // const unparsed = DateToUnix(date);
      DateToUnix(date);
      // console.log('dates above');
    },
  },

  components: {
    PersonEdit,
  },
};
</script>

<style lang="stylus" scoped>
  img
    max-width 100%
    max-height 100%
    border-radius 50%

  .side-button
    width: 40px

  .person-card
    width: 90vw

    @media (min-width: 900px)
      width: 70vw

    @media (min-width: 1200px)
      width: 60vw

    @media (min-width: 1400px)
      width: 50vw
</style>
